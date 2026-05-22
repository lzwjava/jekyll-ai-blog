---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU空闲：最大化VRAM用于机器学习
translated: true
type: note
---

GPU 基本上处于空闲状态。以下是快照：

```
RTX 4070  |  VRAM: 168 MiB / 12,282 MiB (1.4%)
GPU Util: 0%  |  Memory Util: 0%  |  Temp: 43°C  |  Power: 10W / 215W
System RAM: 5.0 GiB used / 62 GiB total
```

只有 Xorg（105 MiB）和 gnome-shell（11 MiB）在 GPU 上。12 GB 的 VRAM 是你在机器学习上的主要瓶颈。以下是如何充分利用它的方法：

---

## 1. QLoRA — 微调的默认选择

在 12 GB 下，你无法对 7B+ 模型进行全量微调。QLoRA（4-bit 基座 + LoRA 适配器）可以解决这个问题：

```python
from transformers import BitsAndBytesConfig
from peft import LoraConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

lora_config = LoraConfig(
    r=16,           # rank — 8-64，16 是一个好的默认值
    lora_alpha=32,  # scaling — 通常是 rank 的 2 倍
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
)
```

这将一个 7B 模型占用约 4-5 GB VRAM，为梯度和激活值留出了空间。

## 2. Flash Attention 2 — 免费 VRAM

在零精度损失的情况下节省 30-50% 的注意力内存：

```bash
pip install flash-attn --no-build-isolation
```

```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B",
    attn_implementation="flash_attention_2",
    torch_dtype=torch.bfloat16,
)
```

## 3. 梯度检查点 — 用计算换内存

在反向传播时重新计算激活值，而不是存储它们：

```python
model.gradient_checkpointing_enable()
# 使用 Unsloth：
model.gradient_checkpointing_enable({"use_reentrant": False})
```

节省约 40-60% 的激活内存，吞吐量损失 15-20%。

## 4. Unsloth — 2 倍速度，50% 更少 VRAM

用 Unsloth 替换 `transformers` + `peft` 以获得免费优势：

```bash
pip install unsloth
```

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(model, lora_config)
```

Unsloth 手写的 Triton 内核显著降低了 VRAM 使用。对于一个 7B QLoRA 模型，你可以在 12 GB 上使用 4096 的序列长度进行训练。

## 5. 微批次 + 梯度累积

在 12 GB 下，batch_size=1 通常是极限。模拟更大的批次：

```python
training_args = TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,  # 有效批次 = 16
    # ...
)
```

## 6. 优化器选择 — 8-bit Adam

```python
# paged_adamw_8bit 相比常规 AdamW 节省约 1-2 GB
training_args = TrainingArguments(
    optim="paged_adamw_8bit",
    # ...
)
```

## 7. 当 12 GB 不够时 — CPU 卸载

你的 62 GB 系统内存是一个巨大的缓冲。对于更大模型的推理：

```bash
# llama.cpp 使用 GPU 卸载层
./llama-cli -m model.gguf -ngl 33  # 将 33 层卸载到 GPU，其余在 CPU
```

对于训练，DeepSpeed ZeRO-3 可以将优化器状态卸载到 CPU，让你训练原本需要 24+ GB 的模型。

## 8. 从头开始训练 — nanoGPT 规模

在 12 GB 下，你可以从零训练一个约 100M 参数的 GPT-2（你之前做过的那种）。在这个规模下：

```python
# 12 GB 的关键杠杆
batch_size = 64          # 尽量推高到合适值
block_size = 1024        # 上下文长度
gradient_accumulation_steps = 4
dtype = torch.bfloat16   # 相比 fp32 节省 50% 内存
compile = True            # torch.compile() 带来约 20% 加速
```

---

**快速检查——你现在想训练或运行什么？** 知道模型大小和任务，我可以给你精确的配置值而不是范围。