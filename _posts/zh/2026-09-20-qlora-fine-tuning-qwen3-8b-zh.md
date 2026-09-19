---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QLoRA微调Qwen3-8B
translated: true
type: note
---

**问题：** 如何在约100MB的企业私有文本数据上微调Qwen3-8B？

**回答：**

以下是微调Qwen3-8B（80亿参数）在私有企业数据上的实用端到端指南。

---

## 1. 环境设置

```bash
# 推荐：Python 3.10+，CUDA 12.1+
pip install transformers==4.51.0 peft trl datasets accelerate bitsandbytes
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

**硬件要求：**

| 方法 | 最低显存 | 推荐 |
| -------- | ---------- | ------------- |
| 全量微调 | 80GB (A100) | 4× A100 |
| LoRA (4比特 QLoRA) | **16–24GB** | 1× A100/H100 |
| LoRA (8比特) | 32GB | 2× A100 |

> 对于100MB的文本，**QLoRA（4比特LoRA）** 是最实用的企业级方法 — 所需GPU少，迭代快。

---

## 2. 准备数据（约100MB文本）

您的原始文本需要转换为指令微调或继续预训练的格式。

**选项A — 继续预训练（原始文本，无标签）**

```python
# data/train.jsonl
{"text": "您的企业文档内容..."}
{"text": "另一篇文档或段落..."}
```

**选项B — 指令微调（问答对，企业推荐）**

```python
# data/train.jsonl
{"instruction": "我们的退款政策是什么？", "input": "", "output": "我们的退款政策规定..."}
{"instruction": "总结此合同条款", "input": "...", "output": "..."}
```

**将原始.txt文件转换为JSONL格式：**

```python
import json, glob

records = []
for path in glob.glob("data/raw/*.txt"):
    with open(path) as f:
        text = f.read()
    # 切分为约512个token的片段
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    for chunk in chunks:
        records.append({"text": chunk})

with open("data/train.jsonl", "w") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
```

---

## 3. QLoRA微调脚本（推荐）

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import torch

MODEL_ID = "Qwen/Qwen3-8B"  # 或 "Qwen/Qwen3-8B-Instruct"

# 1. 4比特量化配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# 2. 加载模型 + 分词器
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# 3. LoRA配置 — 针对Qwen3注意力层
lora_config = LoraConfig(
    r=16,                    # 秩：8-64，越高表示容量越大
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# → 可训练参数：约2000万 / 80亿 = 约0.25%

# 4. 加载数据集
dataset = load_dataset("json", data_files={"train": "data/train.jsonl"})

# 5. 训练配置
sft_config = SFTConfig(
    output_dir="./qwen3-8b-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,   # 有效批次大小 = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    bf16=True,
    logging_steps=10,
    save_steps=100,
    max_seq_length=2048,
    dataset_text_field="text",       # 或对聊天格式使用"instruction"/"output"
)

# 6. 训练
trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
)
trainer.train()

# 7. 仅保存LoRA适配器（约100MB）
model.save_pretrained("./qwen3-8b-lora-adapter")
tokenizer.save_pretrained("./qwen3-8b-lora-adapter")
```

---

## 4. 使用LLaMA-Factory（界面化替代方案，更简单）

如果您喜欢无需代码的方法：

```bash
git clone https://github.com/hiyouga/LLaMA-Factory
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# 启动Web界面
llamafactory-cli webui
```

然后在界面中：选择 **Qwen3-8B** → 上传您的JSONL文件 → 选择 **LoRA** → 点击训练。

---

## 5. 使用微调后的适配器进行推理

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B", device_map="auto")
model = PeftModel.from_pretrained(base, "./qwen3-8b-lora-adapter")
tokenizer = AutoTokenizer.from_pretrained("./qwen3-8b-lora-adapter")

inputs = tokenizer("我们的企业退款政策是什么？", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## 6. 100MB数据的关键超参数

| 参数 | 建议值 | 原因 |
| ----------- | ---------------- | -------- |
| `r` (LoRA秩) | 16–32 | 平衡容量与过拟合 |
| `lora_alpha` | 2× 秩 | 标准缩放 |
| `epochs` | 2–5 | 100MB较小；避免过拟合 |
| `learning_rate` | 1e-4 – 3e-4 | QLoRA最佳范围 |
| `max_seq_length` | 1024–2048 | 与您的文档长度匹配 |
| `batch_size`（有效） | 16–32 | 通过梯度累积实现 |

---

## 7. 隐私/企业安全注意事项

- 完全在**本地（on-premise）**运行 — 数据不会离开您的环境
- 使用**Hugging Face离线模式**：`TRANSFORMERS_OFFLINE=1`
- 将适配器存储在您的内部模型注册中心（MLflow、Weights & Biases本地版）
- 训练前考虑**数据去重**，避免记忆敏感记录

---

**参考资料：**

- [Qwen3 on Hugging Face](https://huggingface.co/Qwen/Qwen3-8B)
- [LLaMA-Factory (最简单的微调界面)](https://github.com/hiyouga/LLaMA-Factory)
- [TRL SFTTrainer文档](https://huggingface.co/docs/trl/sft_trainer)
- [QLoRA论文 (Dettmers等)](https://arxiv.org/abs/2305.14314)
- [PEFT库文档](https://huggingface.co/docs/peft)
