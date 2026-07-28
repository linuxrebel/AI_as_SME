# SML/SLM Technical Implementation Guide
## Practical Deployment, Fine-tuning, and Optimization

---

## Quick Start: Running Your First SLM Locally

### Option 1: Ollama (Simplest)

```bash
# Install Ollama
# macOS/Linux/Windows from https://ollama.ai

# Pull and run a small model
ollama pull mistral:7b
ollama run mistral:7b

# Or with Phi-3 Mini (3.8B)
ollama pull phi3:mini
ollama run phi3:mini

# API endpoint (default)
# curl http://localhost:11434/api/generate
```

### Option 2: LM Studio (GUI-based)

1. Download from https://lmstudio.ai/
2. Browse model library (filtered by size)
3. Download model with one click
4. Chat interface or API access
5. Integrated performance metrics

### Option 3: Hugging Face Transformers (Python)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/phi-2"  # or "meta-llama/Llama-3.2-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)

inputs = tokenizer("Hello, my name is", return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
print(tokenizer.decode(outputs[0]))
```

---

## Model Selection Guide

### By Use Case

**Fastest Inference (CPU-friendly)**
- TinyLlama (1.1B)
- Qwen 0.5B
- Phi-3 Mini (3.8B, optimized)

**Best Accuracy/Speed Balance**
- Mistral 7B
- Llama 3.2 3B
- Qwen 3.5 3B
- Phi-3 14B (if hardware allows)

**Specialized Domain Tasks**
- Search HuggingFace for domain-specific fine-tuned versions
- Medical: ClimateBERT, MedLAMA
- Finance: FinBERT, BloombergGPT
- Code: Phi-3 Code variants

**Multilingual**
- Qwen 3.5 (200+ languages)
- Mistral 7B (good coverage)
- mT5 (many languages, small)

### Hardware Requirements

| Model | Parameters | Memory | Notes |
|-------|-----------|--------|-------|
| TinyLlama | 1.1B | ~2GB RAM | CPU capable |
| Phi-3 Mini | 3.8B | ~8GB RAM | Optimized |
| Qwen 0.5-3B | 0.5-3B | ~2-8GB | Various sizes |
| Mistral 7B | 7B | ~16GB | Standard GPU |
| Llama 3.2 1B-3B | 1-3B | ~4-8GB | Flexible |

---

## Fine-tuning for Your Domain

### 1. Prepare Your Data

```python
# Format: JSONL (one JSON per line)
# {"text": "Your training text here..."}

# Example structure
{
  "text": "Patient presented with symptoms... diagnosis was..."
}

# Create train/validation splits (80/20)
# Aim for 1000-10000 examples for good fine-tuning
```

### 2. Simple Fine-tuning with LoRA (Parameter-Efficient)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
import torch
from transformers import TrainingArguments, Trainer

# Load model in 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-3-mini",
    quantization_config=bnb_config,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini")

# Configure LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "v_proj"]
)

model = get_peft_model(model, lora_config)

# Load your data
dataset = load_dataset("json", data_files="training_data.jsonl")

# Training arguments
training_args = TrainingArguments(
    output_dir="./models/phi3-domain-tuned",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    learning_rate=2e-4,
    warmup_steps=100,
    save_strategy="epoch",
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
)

trainer.train()
```

### 3. Knowledge Distillation (Using Larger Teacher)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch.nn.functional as F

# Teacher model (larger, more capable)
teacher_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b")

# Student model (small SLM)
student_model = AutoModelForCausalLM.from_pretrained("microsoft/phi-3-mini")

# During training, minimize:
# (1-alpha) * CE_loss(student_output, labels)
# + alpha * KL_divergence(student_logits, teacher_logits)

def distillation_loss(student_logits, teacher_logits, labels, temperature=3.0):
    ce_loss = F.cross_entropy(student_logits, labels)
    kl_loss = F.kl_div(
        F.log_softmax(student_logits / temperature, dim=-1),
        F.softmax(teacher_logits / temperature, dim=-1),
        reduction='batchmean'
    )
    return 0.3 * ce_loss + 0.7 * kl_loss
```

---

## Model Quantization & Optimization

### 1. 4-bit Quantization (Recommended)

```python
from transformers import BitsAndBytesConfig, AutoModelForCausalLM

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1b",
    quantization_config=bnb_config,
    device_map="auto"
)
# Reduces model size 4x with minimal accuracy loss
```

### 2. ONNX Export (Cross-platform)

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.onnx import export

model_name = "microsoft/phi-3-mini"
export(
    preprocessor=AutoTokenizer.from_pretrained(model_name),
    model=AutoModelForCausalLM.from_pretrained(model_name),
    config=OnnxConfig.from_model_config(
        AutoConfig.from_pretrained(model_name)
    ),
    opset=14,
    output="./models/phi3-onnx"
)

# Use with ONNX Runtime for inference
import onnxruntime
session = onnxruntime.InferenceSession("./models/phi3-onnx/model.onnx")
```

### 3. Weight Pruning

```python
from torch.nn.utils.prune import global_unstructured, l1_unstructured
import torch.nn.utils.prune as prune

# Prune 30% of weights globally
parameters_to_prune = (
    (model.transformer.h[0], "weight"),
    (model.transformer.h[1], "weight"),
    # ... more layers
)

global_unstructured(
    parameters_to_prune,
    pruning_method=l1_unstructured,
    amount=0.3,
)

# Permanent removal of pruning reparameterization
for module, name in parameters_to_prune:
    prune.remove(module, name)
```

---

## Deployment Options

### 1. Local Python API

```python
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

# Load model once at startup
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-3-mini")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

class QueryRequest(BaseModel):
    text: str
    max_length: int = 100

@app.post("/generate")
async def generate(request: QueryRequest):
    output = pipe(request.text, max_length=request.max_length)
    return {"output": output[0]["generated_text"]}

# Run: uvicorn app:app --host 0.0.0.0 --port 8000
```

### 2. Docker Containerization

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install torch transformers fastapi uvicorn

COPY app.py .
COPY models/ ./models/

ENV TRANSFORMERS_OFFLINE=1
ENV HF_HOME=/app/models

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Mobile Deployment (TensorFlow Lite)

```python
# Convert to TFLite for Android/iOS
from transformers import TFAutoModelForCausalLM
import tensorflow as tf

model = TFAutoModelForCausalLM.from_pretrained("microsoft/phi-3-mini")
concrete_func = tf.function(lambda x: model(x))

# Convert
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)
```

### 4. Edge Device (Jetson Nano / Raspberry Pi)

```bash
# On Jetson Nano
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu118

# Or use optimized builds
pip install tensorrt tensorrt_llm

# Run optimized inference
from tensorrt_llm import LLM
llm = LLM("models/phi3-mini")
output = llm.generate("Hello, ")
```

---

## Performance Monitoring

### Inference Benchmarking

```python
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-3-mini")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini")

# Warm up
for _ in range(3):
    inputs = tokenizer("Hello", return_tensors="pt")
    model.generate(**inputs, max_length=50)

# Benchmark
times = []
for _ in range(100):
    start = time.time()
    inputs = tokenizer("Hello", return_tensors="pt")
    with torch.no_grad():
        model.generate(**inputs, max_length=50)
    times.append(time.time() - start)

print(f"Average latency: {sum(times)/len(times):.3f}s")
print(f"Throughput: {1/sum(times)/len(times):.1f} req/s")
print(f"Memory: {torch.cuda.memory_allocated()/1e9:.1f}GB")
```

### Token/Sec Measurement

```python
import time

start_time = time.time()
total_tokens = 0

inputs = tokenizer("Tell me about AI", return_tensors="pt")
output = model.generate(**inputs, max_length=200, output_scores=True)

elapsed = time.time() - start_time
tokens_generated = output.shape[1] - inputs.shape[1]
tokens_per_sec = tokens_generated / elapsed

print(f"Tokens/sec: {tokens_per_sec:.1f}")
```

---

## Common Pitfalls & Solutions

### Problem: Model Too Slow
**Solutions**:
- Use smaller model (1B instead of 7B)
- Enable quantization (4-bit or 8-bit)
- Batch requests together
- Use model caching
- Add GPU acceleration

### Problem: OOM (Out of Memory)
**Solutions**:
- Reduce batch size
- Use quantization (BitsAndBytes 4-bit)
- Enable gradient checkpointing
- Use smaller model variant
- Add swap space (last resort)

### Problem: Poor Domain Performance
**Solutions**:
- Fine-tune on domain data (not just zero-shot)
- Use knowledge distillation from larger model
- Increase training data quality/quantity
- Use prompt engineering/few-shot examples
- Consider larger base model

### Problem: Token Limit Exceeded
**Solutions**:
- Use models with longer context (Qwen 262K, Llama 4K)
- Implement sliding window approach
- Chunking + summarization pipeline
- Use retrieval-augmented generation (RAG)

---

## Evaluation & Testing

### Domain Accuracy Evaluation

```python
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Generate predictions on test set
predictions = []
ground_truth = []

for example in test_dataset:
    inputs = tokenizer(example["prompt"], return_tensors="pt")
    output = model.generate(**inputs, max_length=50)
    pred_text = tokenizer.decode(output[0])
    predictions.append(pred_text)
    ground_truth.append(example["expected_output"])

# Exact match accuracy
exact_match = sum(p == g for p, g in zip(predictions, ground_truth)) / len(test_dataset)
print(f"Exact match: {exact_match:.1%}")

# Or use BLEU/ROUGE for text generation
from rouge_score import rouge_scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
```

---

## Security Considerations

### Prompt Injection Prevention

```python
# Validate input length
max_input_length = 1000

def generate_safe(prompt: str) -> str:
    if len(prompt) > max_input_length:
        raise ValueError("Input too long")
    
    # Remove potentially dangerous tokens
    dangerous_patterns = ["DROP", "DELETE", "exec("]
    for pattern in dangerous_patterns:
        if pattern in prompt.upper():
            raise ValueError("Suspicious input detected")
    
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_length=100)
    return tokenizer.decode(output[0])
```

### Data Privacy in Fine-tuning

```python
# Ensure training data is properly handled
# 1. Use encryption for data at rest
# 2. Use HTTPS for data in transit
# 3. Implement access controls
# 4. Remove PII before training
# 5. Use differential privacy in training

from tensorflow_privacy.DPQuery.gaussian_query import GaussianAverageQuery

dp_query = GaussianAverageQuery(
    l2_norm_clip=1.0,
    stddev=0.5  # noise level
)
```

---

## Production Checklist

- [ ] Model selected and tested locally
- [ ] Fine-tuning complete on domain data (if needed)
- [ ] Performance benchmarked on target hardware
- [ ] Quantization applied and accuracy verified
- [ ] API endpoint implemented and tested
- [ ] Error handling implemented
- [ ] Logging and monitoring setup
- [ ] Security considerations addressed
- [ ] Containerized for deployment
- [ ] Documentation completed
- [ ] Fallback/degradation strategy defined
- [ ] Cost analysis completed
- [ ] Privacy compliance verified
- [ ] Load testing completed
- [ ] Rollback plan documented

---

## References for Implementation

- **Hugging Face Docs**: https://huggingface.co/docs/transformers
- **PyTorch Docs**: https://pytorch.org/docs
- **PEFT Library**: https://github.com/huggingface/peft
- **BitsAndBytes**: https://github.com/TimDettmers/bitsandbytes
- **ONNX Runtime**: https://onnxruntime.ai/docs
- **TensorFlow Lite**: https://www.tensorflow.org/lite/guide
