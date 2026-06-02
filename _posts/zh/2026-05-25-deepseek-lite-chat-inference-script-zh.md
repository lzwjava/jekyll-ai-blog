---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek 精简版聊天推理脚本
translated: true
type: note
---

```python
#!/usr/bin/env python3
"""
DeepSeek-V2-Lite-Chat 4-bit量化推理。
适合12GB显存（RTX 4070）。

用法：
    python run_lite.py                          # 交互式对话
    python run_lite.py -p "在此输入提示"    # 单次提示
"""

import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_PATH = "/mnt/data/models/DeepSeek-V2-Lite-Chat"


def load_model():
    """加载4-bit量化模型。"""
    print("正在加载tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

    print("正在以4-bit方式加载模型...")
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
    print(f"模型加载完成。GPU显存使用量：{mem_gb:.1f} GB")
    return model, tokenizer


def generate(model, tokenizer, prompt, max_new_tokens=512):
    """生成回复。"""
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
    """交互式对话循环。"""
    print("\nDeepSeek-V2-Lite-Chat (4-bit) — 交互模式")
    print("输入'quit'退出，输入'clear'重置历史记录。\n")

    while True:
        try:
            user_input = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            print("上下文已清除。\n")
            continue

        response = generate(model, tokenizer, user_input)
        print(f"\nDeepSeek：{response}\n")


def main():
    parser = argparse.ArgumentParser(description="DeepSeek-V2-Lite推理")
    parser.add_argument("-p", "--prompt", help="单次提示模式")
    parser.add_argument(
        "-n", "--max-tokens", type=int, default=512, help="最大新生成token数"
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
```
