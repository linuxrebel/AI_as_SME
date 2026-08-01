#!/usr/bin/env python3
"""LoRA fine-tune phi3 on Python QA pairs. Per docs/implementations.html Use Case 2A.

Run inside a venv with torch/transformers/peft/datasets/bitsandbytes installed
(see requirements.txt), e.g. `python3 -m venv venv && venv/bin/pip install -r requirements.txt`.

Training data: python_training_data.jsonl, one JSON object per line:
  {"messages": [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "A"}]}

Pass --smoke-test to run a single training step only, to verify the setup
actually completes a step before committing to a full multi-hour run.
"""
import argparse
import glob
import json
import os
import time

import torch
from datasets import Dataset
from peft import LoraConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, Trainer, TrainingArguments

MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
DATA_FILE = "python_training_data.jsonl"
OUTPUT_DIR = "./phi3-python"


def load_data(path, eos_token):
    with open(path) as f:
        rows = [json.loads(line) for line in f]
    texts = []
    for row in rows:
        msgs = row["messages"]
        user = next(m["content"] for m in msgs if m["role"] == "user")
        assistant = next(m["content"] for m in msgs if m["role"] == "assistant")
        texts.append(f"Request: {user}\n\nPython code:\n{assistant}{eos_token}")
    return Dataset.from_dict({"text": texts})


def find_latest_checkpoint(output_dir):
    checkpoints = glob.glob(os.path.join(output_dir, "checkpoint-*"))
    if not checkpoints:
        return None
    return max(checkpoints, key=lambda p: int(p.rsplit("-", 1)[-1]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true", help="Run a single training step only, print its wall-clock time, then exit.")
    parser.add_argument("--resume-adapter", metavar="DIR", help="Load an existing (finished) LoRA adapter from this dir and continue training it on new data, instead of starting fresh.")
    parser.add_argument("--data-file", default=DATA_FILE, help="Training data JSONL to use (default: %(default)s).")
    parser.add_argument("--resume-from-checkpoint", metavar="DIR", nargs="?", const="auto",
                         help="Resume an interrupted run from a mid-training checkpoint (optimizer/scheduler state included). "
                              "Pass a checkpoint-N dir, or omit the value to auto-pick the latest checkpoint under the output dir.")
    args = parser.parse_args()

    if args.resume_adapter and args.resume_from_checkpoint:
        raise SystemExit("--resume-adapter and --resume-from-checkpoint are mutually exclusive: "
                          "the former starts a new training stage on a finished adapter, "
                          "the latter continues an interrupted run's optimizer state.")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="cuda", quantization_config=bnb_config)
    model = prepare_model_for_kbit_training(model)

    if args.resume_adapter:
        model = PeftModel.from_pretrained(model, args.resume_adapter, is_trainable=True)
    else:
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["qkv_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
        )
        model = get_peft_model(model, lora_config)

    dataset = load_data(args.data_file, tokenizer.eos_token)

    def tokenize(batch):
        encoded = tokenizer(batch["text"], truncation=True, padding="max_length", max_length=512)
        encoded["labels"] = [
            [tok if mask else -100 for tok, mask in zip(ids, attn)]
            for ids, attn in zip(encoded["input_ids"], encoded["attention_mask"])
        ]
        return encoded

    tokenized = dataset.map(tokenize, batched=True)

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1 if args.smoke_test else 3,
        max_steps=1 if args.smoke_test else -1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=1,
        save_strategy="no" if args.smoke_test else "steps",
        save_steps=25,
        save_total_limit=3,
    )

    resume_path = None
    if args.resume_from_checkpoint:
        resume_path = (
            find_latest_checkpoint(OUTPUT_DIR)
            if args.resume_from_checkpoint == "auto"
            else args.resume_from_checkpoint
        )
        if not resume_path:
            raise SystemExit(f"--resume-from-checkpoint: no checkpoint-* found under {OUTPUT_DIR}")
        print(f"Resuming from checkpoint: {resume_path}")

    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized)
    start = time.monotonic()
    trainer.train(resume_from_checkpoint=resume_path)
    elapsed = time.monotonic() - start
    print(f"SMOKE_TEST_ELAPSED_SECONDS={elapsed:.1f}" if args.smoke_test else f"TRAIN_ELAPSED_SECONDS={elapsed:.1f}")
    if not args.smoke_test:
        model.save_pretrained(OUTPUT_DIR)


if __name__ == "__main__":
    main()
