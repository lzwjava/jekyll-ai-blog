---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070的基础强化学习模型
translated: true
type: note
---

**问题：** 对于在 RTX 4070 上进行的这个 RL 实验，你能给我推荐一个基础（非指令）模型吗？

**回答：**

可以 —— 对于 GRPO/RL 实验，你**始终需要基础模型**，而不是指令模型。原因如下以及该使用什么：

---

## 为什么 RL 要使用基础模型？

- **指令模型**已经过 RLHF 调优——你是在对抗已有的对齐，奖励黑客行为更难观察到
- **基础模型**是一张白纸——RL 奖励信号有完全的控制权，你可以清晰地看到策略学习过程
- 这正是 DeepSeek-R1 和 Qwen 思考模式的构建方式：**基础模型 → 直接 RL**（小型实验无需 SFT 预热）

---

## 适用于 RTX 4070（12 GB）的最佳基础模型

| 模型 | VRAM（4-bit） | 速度 | RL 适用性 |
|---|---|---|---|
| `Qwen/Qwen2.5-1.5B` | ~1.1 GB | 非常快 | ⭐⭐⭐ 快速迭代最佳选择 |
| `Qwen/Qwen2.5-3B` | ~2.0 GB | 快 | ⭐⭐⭐ 良好的平衡性 |
| `Qwen/Qwen2.5-7B` | ~4.5 GB | 适中 | ⭐⭐⭐ 效果最强 |
| `microsoft/Phi-4-mini` | ~2.5 GB | 快 | ⭐⭐ 推理基础好 |
| `google/gemma-3-1b-pt` | ~0.9 GB | 最快 | ⭐ 较弱但体积小 |

**推荐：** 首次实验使用 **`Qwen/Qwen2.5-1.5B`**，一旦你的奖励函数验证通过后，再扩展到 `Qwen/Qwen2.5-7B`。

---

## 使用基础模型的更新完整脚本

```python
# rl_grpo_base.py
# 使用 Qwen2.5-1.5B 基础模型在 RTX 4070 上进行 GRPO RL 实验
# 目标：仅通过 RL 从头开始教授思维链数学推理

import re
import random
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from trl import GRPOConfig, GRPOTrainer

# ── 配置 ────────────────────────────────────────────────────────────────────
MODEL_ID   = "Qwen/Qwen2.5-1.5B"   # 基础模型，非指令模型
OUTPUT_DIR = "./grpo_qwen1.5b_math"

# ── 1. 以 4-bit 加载模型 ────────────────────────────────────────────────────
bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,   # 额外节省约 0.4 GB
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"      # 对生成很重要

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb,
    device_map="cuda",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # 节省 VRAM，速度更快
)

# ── 2. LoRA 适配器——仅训练约 1% 的权重 ───────────────────────────────
lora_cfg = LoraConfig(
    r=16,                 # rank: 16 是不错的默认值
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()
# 预期输出：可训练参数：~8M || 总参数：1.54B || ~0.5%

# ── 3. 数据集——难度不同的算术题 ───────────────────────────────────────────
SYSTEM = (
    "你是一个数学求解器。在 思考... 回复 "
    "标签内逐步思考，然后在 回复 之后给出最终的数字答案。"
)

def make_problem():
    level = random.choice(["easy", "medium", "hard"])
    if level == "easy":
        a, b = random.randint(1, 20), random.randint(1, 20)
        expr = f"{a} + {b}"
    elif level == "medium":
        a, b, c = random.randint(1, 15), random.randint(1, 10), random.randint(1, 5)
        expr = f"{a} * {b} + {c}"
    else:
        a, b, c = random.randint(2, 12), random.randint(2, 8), random.randint(1, 10)
        expr = f"({a} + {b}) * {c}"
    answer = str(eval(expr))
    prompt = f"{SYSTEM}\n\n问题: {expr} = ?"
    return {"prompt": prompt, "answer": answer}

random.seed(42)
data = [make_problem() for _ in range(800)]
dataset = Dataset.from_list(data).train_test_split(test_size=0.1)

# ── 4. 奖励函数——多信号 ─────────────────────────────────────────────────────
def extract_answer(text: str) -> str | None:
    """提取 回复 标签后的最后一个数字。"""
    after_think = text.split(" 回复")[-1] if " 回复" in text else text
    nums = re.findall(r"-?\d+\.?\d*", after_think)
    return str(int(float(nums[-1]))) if nums else None

def reward_fn(completions, answer, **kwargs) -> list[float]:
    rewards = []
    for completion, gold in zip(completions, answer):
        # TRL 将补全作为字典列表或纯字符串传递
        text = completion[0]["content"] if isinstance(completion, list) else completion
        r = 0.0

        # 格式奖励：是否有 思考 块？
        has_think = " 思考" in text and " 回复" in text
        if has_think:
            r += 0.2
            # 非平凡推理奖励（标签内超过 20 个字符）
            think_content = re.findall(r" 思考(.*?) 回复", text, re.DOTALL)
            if think_content and len(think_content[0].strip()) > 20:
                r += 0.1

        # 正确性奖励
        pred = extract_answer(text)
        if pred is not None and pred == gold:
            r += 1.0           # 正确答案
        elif pred is not None:
            r -= 0.3           # 错误答案（惩罚，但不严厉）
        else:
            r -= 0.5           # 完全未提取到答案

        rewards.append(r)
    return rewards

# ── 5. 针对 12 GB 调优的 GRPO 配置 ───────────────────────────────────────────
grpo_args = GRPOConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,    # 有效批次 = 16
    learning_rate=5e-6,               # 为稳定基础模型使用较低的学习率
    warmup_ratio=0.05,
    num_generations=4,                # GRPO 组大小 G=4
    max_prompt_length=256,
    max_completion_length=400,
    temperature=1.0,                  # 早期为探索使用高温
    beta=0.02,                        # KL 惩罚——对于基础模型较低
    loss_type="grpo",
    optim="paged_adamw_8bit",
    bf16=True,
    fp16=False,
    gradient_checkpointing=True,      # 用计算换约 3 GB VRAM 节省
    logging_steps=10,
    eval_steps=50,
    save_steps=100,
    report_to="none",                 # 如需跟踪，设置为 "wandb"
    seed=42,
)

# ── 6. 训练 ──────────────────────────────────────────────────────────────────
trainer = GRPOTrainer(
    model=model,
    args=grpo_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    reward_funcs=reward_fn,
    processing_class=tokenizer,
)

print("=" * 60)
print(f"模型:     {MODEL_ID}")
print(f"任务:      通过 GRPO 进行数学推理")
print(f"训练大小: {len(dataset['train'])} | 评估: {len(dataset['test'])}")
print("=" * 60)

trainer.train()
trainer.save_model(f"{OUTPUT_DIR}/final")
tokenizer.save_pretrained(f"{OUTPUT_DIR}/final")
print("完成——LoRA 适配器已保存。")

# ── 7. 快速评估 ─────────────────────────────────────────────────────────────
def test_model(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

print("\n── 训练后测试 ──")
test_prompt = f"{SYSTEM}\n\n问题: (7 + 5) * 3 = ?"
print(test_model(test_prompt))
```

---

## 训练期间要观察的内容

```
步骤  10 | 奖励：0.12  ← 模型尚未很好推理
步骤  50 | 奖励：0.45  ← 开始使用 思考 标签
步骤 150 | 奖励：0.78  ← 答案大多正确
步骤 300 | 奖励：1.05  ← 形成稳定的推理链
```

奖励随步骤增加而上升，说明 RL 信号在起作用。如果早期陷入平台期，请降低 `beta`（减少 KL 惩罚）或提高 `temperature`。

---

## 一行命令安装

```bash
pip install torch transformers trl peft bitsandbytes datasets flash-attn --upgrade
```

如果 `flash-attn` 构建失败，只需从模型加载中移除 `attn_implementation="flash_attention_2"`——它是可选的，但可以节省约 1.5 GB VRAM。

**参考资料：**
- [HuggingFace 上的 Qwen2.5-1.5B 基础模型](https://huggingface.co/Qwen/Qwen2.5-1.5B)
- [TRL GRPOTrainer 文档](https://huggingface.co/docs/trl/grpo_trainer)
- [DeepSeek-R1 论文（GRPO 起源）](https://arxiv.org/abs/2501.12948)
- [PEFT LoRA 文档](https://huggingface.co/docs/peft/conceptual_guides/lora)