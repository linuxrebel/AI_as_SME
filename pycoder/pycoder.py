#!/usr/bin/env python3
"""Local Python code generator using Ollama (phi3), per docs/implementations.html Use Case 2A."""
import argparse
import json
import sys

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

SYSTEM_PROMPT = (
    "You are a Python coding assistant. Given a request, respond with "
    "correct, idiomatic Python code only. Use markdown code fences."
)


def generate(prompt: str, model: str = MODEL) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\nRequest: {prompt}\n\nPython code:"
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": full_prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]


def main():
    parser = argparse.ArgumentParser(description="Generate Python code from a prompt via local Ollama model.")
    parser.add_argument("prompt", nargs="*", help="What you want the code to do")
    parser.add_argument("--model", default=MODEL, help=f"Ollama model to use (default: {MODEL})")
    args = parser.parse_args()

    prompt = " ".join(args.prompt) if args.prompt else input("What should the code do? ")
    print(generate(prompt, args.model))


if __name__ == "__main__":
    main()
