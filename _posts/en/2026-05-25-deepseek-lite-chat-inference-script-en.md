---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek Lite Chat Inference Script
translated: false
type: note
---

#!/usr/bin/env python3
"""
DeepSeek-V2-Lite-Chat inference with 4-bit quantization.
Fits in 12GB VRAM (RTX 4070).

Usage:
    python run_lite.py                          # interactive chat
    python run_lite.py -p "Your prompt here"    # single prompt
"""

import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_PATH = "/mnt/data/models/DeepSeek-V2-Lite-Chat"


def load_model():
    """Load model with 4-bit quantization."""
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

    print("Loading model in 4-bit...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    )

    mem_gb = torch.cuda.memory_allocated() / 1024**3
    print(f"Model loaded. GPU memory used: {mem_gb:.1f} GB")
    return model, tokenizer


def generate(model, tokenizer, prompt, max_new_tokens=512):
    """Generate a response."""
    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
    )
    return response


def interactive(model, tokenizer):
    """Interactive chat loop."""
    print("\nDeepSeek-V2-Lite-Chat (4-bit) — Interactive Mode")
    print("Type 'quit' to exit, 'clear' to reset history.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            print("Context cleared.\n")
            continue

        response = generate(model, tokenizer, user_input)
        print(f"\nDeepSeek: {response}\n")


def main():
    parser = argparse.ArgumentParser(description="DeepSeek-V2-Lite inference")
    parser.add_argument("-p", "--prompt", help="Single prompt mode")
    parser.add_argument(
        "-n", "--max-tokens", type=int, default=512, help="Max new tokens"
    )
    args = parser.parse_args()

    model, tokenizer = load_model()

    if args.prompt:
        response = generate(model, tokenizer, args.prompt, args.max_tokens)
        print(response)
    else:
        interactive(model, tokenizer)


if __name__ == "__main__":
    main()