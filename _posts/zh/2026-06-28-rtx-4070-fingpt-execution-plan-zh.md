---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 FinGPT 执行计划
translated: true
type: note
---

问题：将“在你的 RTX 4070 上运行 FinGPT 风格实验”这一任务展开为一个具体、可执行的计划。

回答：

以下是展开后的完整执行计划——结构清晰，可复制粘贴并在 REPL 中迭代。

## 1. 在你的 RTX 4070 上运行 FinGPT 风格实验（最高优先级）

**为什么优先做这个：** 这是将你的三项资产——银行业领域知识、GPU 训练技能和 AI 原生工具——融合为一个可展示的作品集的唯一成果。一个在你自己的 4070 上训练、通过 SGLang 服务、附带评估指标的 QLoRA 金融情感适配器，对招聘经理（或你的家人）而言，比任何简历上的一行描述都更有说服力。

### 先做硬件现实检查

4070 有 **12 GB VRAM**。这意味着无法对 8B 模型进行全量微调（需要 ~60+ GB）。8B 模型上的 QLoRA（4-bit 基座 + LoRA 适配器）可以塞进去，但空间紧张——需要将 batch size 降到 1，并依赖梯度累积。如果遇到 OOM，则回退到 3B（Qwen2.5-3B / Llama-3.2-3B），后者训练舒适，迭代速度快 3–4 倍。对于首次端到端运行，**从 3B 开始验证流程，等流程跑通后再扩展到 8B。**

### 步骤 0 — 环境

```bash
ssh lzw@192.168.1.36
mkdir -p ~/fin-sft && cd ~/fin-sft
python -m venv .venv && source .venv/bin/activate
pip install -U "transformers>=4.44" "peft>=0.13" "trl>=0.11" \
    "bitsandbytes>=0.43" "datasets" "accelerate" "scikit-learn"
nvidia-smi   # 开始前确认 4070 空闲
```

### 步骤 1 — 构建指令数据集

不要克隆 FinGPT 的完整仓库——其管道中包含许多你不需要的遗留代码。有价值的部分是 *数据配方*。使用公开的 `financial_phrasebank` 数据集（约 4.8K 条带标签的标题，正面/负面/中性）作为基础，并将其重塑为指令格式。

```python
# make_dataset.py
from datasets import load_dataset
import json, random

ds = load_dataset("financial_phrasebank", "sentences_50agree", split="train")
label_map = {0: "negative", 1: "neutral", 2: "positive"}

INSTR = "Classify the sentiment of this financial news headline as positive, negative, or neutral."

rows = []
for ex in ds:
    rows.append({
        "messages": [
            {"role": "user", "content": f"{INSTR}\n\nHeadline: {ex['sentence']}"},
            {"role": "assistant", "content": label_map[ex["label"]]},
        ]
    })

random.seed(0)
random.shuffle(rows)
split = int(len(rows) * 0.9)
with open("train.jsonl", "w") as f:
    for r in rows[:split]: f.write(json.dumps(r) + "\n")
with open("eval.jsonl", "w") as f:
    for r in rows[split:]: f.write(json.dumps(r) + "\n")

print(f"train={split} eval={len(rows)-split}")
```

如果你想获得真正的领域优势：用你银行实际问题空间（财报、利率变动、信用事件）中提取的几百条标题进行扩充，并通过 LLM 调用为它们打标签——这就是你的 AI 原生数据集工程操作，使适配器成为你的专属，而不是教程的复现。

### 步骤 2 — QLoRA 训练脚本

```python
# train.py
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

MODEL = "Qwen/Qwen2.5-3B-Instruct"   # 流程跑通后升级到 8B

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(
    MODEL, quantization_config=bnb, device_map="auto",
    attn_implementation="sdpa",
)

peft_cfg = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
)

train_ds = load_dataset("json", data_files="train.jsonl", split="train")

cfg = SFTConfig(
    output_dir="out",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,   # 有效 batch 16
    num_train_epochs=3,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    bf16=True,
    gradient_checkpointing=True,
    logging_steps=10,
    save_strategy="epoch",
    max_seq_length=512,
    packing=False,
)

trainer = SFTTrainer(model=model, args=cfg,
                     train_dataset=train_ds, peft_config=peft_cfg)
trainer.train()
trainer.save_model("out/adapter")
```

```bash
python make_dataset.py
python train.py     # 3B/3 epoch 在 4070 上 ≈ 15–30 分钟
watch -n2 nvidia-smi   # 在另一个面板中确认没有 OOM
```

**OOM 调整手段（按顺序）：** 降低 `max_seq_length` 到 256 → 确认 `gradient_checkpointing=True` → 将 `r` 降到 8 → 如果从 8B 开始则回退到 3B。

### 步骤 3 — 评估（这才是使其成为作品集内容而非玩具的关键）

数字是可交付成果。对保留集计算准确率 + 每类 F1，并比较适配器与基座模型，以证明微调起到了作用。

```python
# eval.py
import json, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from sklearn.metrics import accuracy_score, classification_report

BASE = "Qwen/Qwen2.5-3B-Instruct"
tok = AutoTokenizer.from_pretrained(BASE)
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16, device_map="auto")
model = PeftModel.from_pretrained(model, "out/adapter").eval()

LABELS = ["positive","negative","neutral"]
def predict(text):
    msgs = [{"role":"user","content":text}]
    ids = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to(model.device)
    out = model.generate(ids, max_new_tokens=5, do_sample=False)
    resp = tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True).lower()
    return next((l for l in LABELS if l in resp), "neutral")

rows = [json.loads(l) for l in open("eval.jsonl")]
y_true = [r["messages"][1]["content"] for r in rows]
y_pred = [predict(r["messages"][0]["content"]) for r in rows]

print("acc:", accuracy_score(y_true, y_pred))
print(classification_report(y_true, y_pred, labels=LABELS))
```

### 步骤 4 — 通过现有 SGLang 设置提供服务

SGLang 直接支持 LoRA 适配器，因此测试时无需先合并：

```bash
python -m sglang.launch_server \
    --model-path Qwen/Qwen2.5-3B-Instruct \
    --lora-paths fin=out/adapter \
    --port 30000

curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"fin","messages":[{"role":"user",
       "content":"Classify: Bank reports record quarterly losses amid loan defaults"}]}'
```

对于部署（而非仅测试），使用 `model.merge_and_unload()` 将适配器合并到基座权重中，然后提供合并后的检查点——推理速度稍快，且无适配器切换开销。

### 步骤 5 — 撰写文档（30 分钟，收益永久）

在 lzwjava.github.io 上写一篇短文：数据集配方、你在 12 GB VRAM 上实际遇到的 OOM 调整、基座 vs 适配器 F1 对比表、SGLang 服务代码片段。这是按照你自己的剧本，为你做营销/建立可信度的公开作品。

### 今日实际时间线

- 0:00–0:30 环境 + 数据集
- 0:30–1:15 首次 3B 训练运行 + 观察 OOM
- 1:15–1:45 评估，获取数字
- 1:45–2:15 SGLang 服务 + 验证提示
- 2:15–3:00 （可选）如果 VRAM 允许则扩展到 8B，否则写文档

这是一个完整的闭环——训练 → 评估 → 服务 → 发布——在 3 小时内完成。

参考资料：

- [FinGPT (AI4Finance)](https://github.com/AI4Finance-Foundation/FinGPT)
- [financial_phrasebank 数据集](https://huggingface.co/datasets/financial_phrasebank)
- [TRL SFTTrainer 文档](https://huggingface.co/docs/trl/en/sft_trainer)
- [PEFT QLoRA 指南](https://huggingface.co/docs/peft/en/developer_guides/quantization)
- [SGLang LoRA 服务](https://docs.sglang.ai/backend/lora.html)