---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在1万条Jekyll笔记上进行微调
translated: true
type: note
---

**问题：** 我在 lzwjava.github.io 上存有约 1 万条笔记（Jekyll 仓库：github.com/lzwjava/jekyll-ai-blog）。我想基于这些笔记微调一个模型——该怎么做？

**回答：**

首先，坦诚地说：1 万条笔记约等于 **8–15M tokens**。这对于预训练来说太小了，但对于 SFT 数据集而言却非常合适——尤其是因为你的笔记-en 语料库已经天然是 Q&A 格式（标题 = 问题，正文 = 答案）。微调能教会模型你的**语气、格式和回答风格**，但无法可靠地记住每一条笔记的具体内容（对于记忆性任务，RAG 更优；以这个数据规模，权重只是一个有损压缩器）。这个项目的有趣之处在于：**"一个能像 lzwjava 的笔记一样回答的模型"**——而这正是 SFT 擅长做的事情。

## 第一步 —— 从 Jekyll 提取数据集

你的文章是带有 YAML 头部的 Markdown 文件。将其解析为 `{question, answer}` 对：

```python
# build_dataset.py
import json, re
from pathlib import Path
import frontmatter  # pip install python-frontmatter

POSTS = Path("jekyll-ai-blog/_posts")  # 或笔记所在位置
out = open("notes_sft.jsonl", "w")

LIQUID = re.compile(r"{[%{].*?[%}]}", re.DOTALL)

n = 0
for f in sorted(POSTS.rglob("*.md")):
    post = frontmatter.load(f)
    if post.get("lang", "en") != "en":      # 仅保留英文
        continue
    title = post.get("title", "").strip()
    body = LIQUID.sub("", post.content).strip()
    if not title or len(body) < 300:        # 过滤短内容
        continue
    out.write(json.dumps({
        "conversations": [
            {"role": "user", "content": title},
            {"role": "assistant", "content": body},
        ]
    }, ensure_ascii=False) + "\n")
    n += 1

print(f"{n} 条示例")
```

然后检查 token 数量并去重：

```bash
python -c "
import json, tiktoken
enc = tiktoken.get_encoding('cl100k_base')
tot = sum(len(enc.encode(json.loads(l)['conversations'][1]['content'])) for l in open('notes_sft.jsonl'))
print(f'{tot/1e6:.1f}M 条辅助 token')"
```

在训练前保留约 200 条示例作为评估集。同时要严格筛选——7000 条干净示例胜过 10000 条嘈杂的。丢弃纯链接堆叠、不含叙述的配置片段或重复答案的笔记。

## 第二步 —— 选择模型和机器

| 配置 | 模型 | 方法 | 原因 |
| --- | --- | --- | --- |
| RTX 4070 (12GB) | Qwen3-4B / Llama-3.1-8B | QLoRA 4-bit | 使用 Unsloth 可适配 12GB 显存；免费迭代 |
| MI300X ($2/小时) | Qwen3-32B 或 Llama-3.3-70B | LoRA 16-bit | 192GB HBM3 允许你在一块 GPU 上对 70B 模型做 LoRA |

Unsloth 现已正式支持 AMD——其 Triton 内核已与 ROCm 团队合作移植到 HIP/ROCm，并在真实的 MI300X 硬件上得到验证。在 MI300X 机器上安装：

```bash
python3 -m venv unsloth_env && source unsloth_env/bin/activate
pip install torch torchvision torchao xformers --index-url https://download.pytorch.org/whl/rocm6.4
pip install --no-deps unsloth unsloth-zoo
pip install "unsloth[amd] @ git+https://github.com/unslothai/unsloth"
```

（ROCm 系统需要预发布版本的 bitsandbytes——≤ 0.49.2 版本在 AMD GPU 上存在 4-bit 解码 NaN 错误；仅在你使用 4-bit 时需要注意；在 MI300X 上直接使用 16-bit LoRA。）

## 第三步 —— 训练

```python
# train.py — 同时适用于 4070 (CUDA) 和 MI300X (ROCm)
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-8B",          # 如需在 MI300X 上使用 70B
    max_seq_length=4096,
    load_in_4bit=True,            # 在 MI300X 上设为 False
)
model = FastLanguageModel.get_peft_model(
    model, r=32, lora_alpha=32,
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
)

ds = load_dataset("json", data_files="notes_sft.jsonl", split="train")
ds = ds.map(lambda x: {"text": tokenizer.apply_chat_template(
    x["conversations"], tokenize=False)})

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=ds,
    args=SFTConfig(
        per_device_train_batch_size=2,   # MI300X 上可设为 64+
        gradient_accumulation_steps=8,
        num_train_epochs=2,              # 数据量小——不要超过 3 轮
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        bf16=True, logging_steps=10,
        output_dir="lzw-notes-lora",
        packing=True,                    # 对短 Q&A 对至关重要
    ),
)
trainer.train()
model.save_pretrained_merged("lzw-notes-merged", tokenizer)
```

对于约 10M tokens，在 8B QLoRA 上跑 2 轮，4070 需要几小时；在 MI300X 上 batch size 达到 64+，时间远低于 1 小时——一次 $2 的实例会话就能完成多次实验。关注评估损失；由于数据量很小，**过拟合（记忆化表达、重复）在 2-3 轮后会迅速显现**。

## 第四步 —— 评估和服务

在 200 条保留标题上对基础模型进行风格评估：同时生成两个模型的输出，比较风格差异。然后导出供本地使用：

```bash
# 为 M2 Air 上的 llama.cpp / ollama 导出 GGUF 格式
model.save_pretrained_gguf("lzw-notes-gguf", tokenizer, quantization_method="q4_k_m")
# 或在 4070 机器上提供服务：
vllm serve ./lzw-notes-merged --max-model-len 4096
```

## 推荐路径

1. **本周内，4070**：构建数据集 → QLoRA Qwen3-4B → 观察"lzwjava 风格"是否出现。总成本：$0。
2. **管道跑通后，MI300X**：使用相同脚本，对 32B/70B 模型做 16-bit LoRA，batch size 64。这也是你后续 nanochat/DeepSeek 项目所需的核心技能——nanochat 的 SFT 阶段本质上是相同的循环，只是需要手工适配。
3. **进阶**：使用 LoRA 后的模型 + DPO 对（你编辑过的回答 vs 原始模型回答）——这是你希望学习的 RLHF/DPO 领域的自然下一步。

**参考资料：**

- [Unsloth — 在 AMD GPU (MI300X) 上微调 LLM](https://unsloth.ai/docs/new/fine-tuning-llms-on-amd-gpus-with-unsloth)
- [Unsloth AMD 安装指南](https://unsloth.ai/docs/get-started/install/amd)
- [AMD 博客 — 使用 Unsloth 在单个 MI300X 上微调 Llama-3.3-70B LoRA](https://www.amd.com/en/developer/resources/technical-articles/2025/10x-model-fine-tuning-using-synthetic-data-with-unsloth.html)
- [llm-tracker — AMD GPU 训练笔记 (torchtune vs axolotl vs unsloth)](https://llm-tracker.info/howto/AMD-GPUs)
