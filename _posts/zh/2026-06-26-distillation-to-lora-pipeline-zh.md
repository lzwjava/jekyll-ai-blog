---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LoRA蒸馏流程
translated: true
type: note
---

**问题：** 如何真正构建蒸馏→LoRA管道——前沿模型从我的SEC语料库生成指令数据，然后在数据上对一个小模型进行LoRA微调，并附带下游任务基准测试？

**回答：**

以下是完整的管道，以构建为先。四个阶段：**切分语料库→蒸馏指令→LoRA训练→对比零样本基线评估**。我将为每个阶段提供可运行的代码。优先针对你的4070（快速迭代），MI300X用于扩展。

核心设计思路：你不是在教模型*金融*（前沿模型已经懂金融）。你是在教它*你的任务格式*——把一个强大的通用模型转变为一个可靠、低成本、结构化输出的专用模型。这就是蒸馏：在狭窄任务上，大老师教小学生。

---

## 阶段0：架构

```
SEC .npy tokens  ──(反分词)──> 原始 10-K 文本段落
                                          │
                                          ▼
                          ┌─────────────────────────────┐
                          │ TEACHER (V4-Pro / Opus API)  │
                          │ 段落 → 指令对               │
                          └─────────────────────────────┘
                                          │  ~5k JSONL 对
                                          ▼
                          ┌─────────────────────────────┐
                          │ STUDENT (Qwen3-8B + LoRA)    │
                          │ 在对上训练，4070             │
                          └─────────────────────────────┘
                                          │
                                          ▼
                   评估: student-LoRA vs student-zero-shot vs teacher
                         在保留任务上（精确匹配 / F1）
```

你在选择器中选定了目标——我会编写阶段1以支持**提取**和**问答/摘要**，因为这些是实际选项；你只需切换一个标志。

---

## 阶段1：从 .npy shard 恢复文本

你使用GPT-2 BPE进行分词，所以反分词回干净的段落文本。不要将原始token ID喂给老师——喂可读的申报文档。

```python
# detok.py — 从分词后的shard恢复10-K文本段落
import numpy as np, tiktoken, re, json

enc = tiktoken.get_encoding("gpt2")
shard = np.load("/mnt/data/zz/datasets/sec-edgar-tok/val_000000.npy")  # 使用验证集避免后续训练泄露

text = enc.decode(shard[:5_000_000].tolist())  # 解码一个块；完整shard很大

# 10-K有自然段落标记——以此分割
SECTION_RE = re.compile(r"(Item\s+\d+[A-Z]?\.\s)", re.IGNORECASE)
parts = SECTION_RE.split(text)
# 将标记+正文重新拼接，保留长度800-6000字符的段落（适配老师上下文，且有一定意义）
sections = []
for i in range(1, len(parts)-1, 2):
    sec = (parts[i] + parts[i+1]).strip()
    if 800 <= len(sec) <= 6000:
        sections.append(sec)

print(f"{len(sections)} 个可用段落")
with open("sections.jsonl", "w") as f:
    for s in sections[:6000]:           # 上限——你只需要几千个
        f.write(json.dumps({"text": s}) + "\n")
```

为什么用验证集shard：你将保留其中一些用于评估，并且希望与学生后续可能看到的数据零重叠。如果要扩展，保留训练shard。

---

## 阶段2：蒸馏——老师生成指令对

这是核心。老师读取一个段落，生成一个`(instruction, input, output)`三元组。结构化输出意味着你的评估可以机械地进行。

{% raw %}

```python
# distill.py — 前沿模型将原始段落转化为训练对
import json, os, asyncio, aiohttp

TASK = os.environ.get("TASK", "extraction")   # "extraction" | "qa"

EXTRACTION_PROMPT = """你正在构建一个训练数据集。给定此10-K段落，只输出严格的JSON（没有markdown围栏）：
{{"instruction": "Extract the structured fields from this SEC filing section.",
  "input": "<the section text, verbatim>",
  "output": {{"section_type": "...", "key_risks": ["..."], "financial_figures": [{{"label":"...","value":"..."}}], "fiscal_period": "..."}}}}
仅包含实际存在的字段。段落：
---
{section}"""

QA_PROMPT = """给定此10-K段落，生成一个金融分析师会提出的高质量问题，以及仅基于文本的答案。只输出严格的JSON：
{{"instruction":"Answer the question using only the filing section provided.",
  "input":"Question: <q>\\n\\nSection: {section}",
  "output":"<concise grounded answer>"}}
段落：
---
{section}"""

PROMPT = EXTRACTION_PROMPT if TASK == "extraction" else QA_PROMPT

async def call(session, section):
    body = {
        "model": "deepseek-v4-pro",          # 你的顶级模型；也可换成 claude-opus
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": PROMPT.format(section=section)}],
    }
    headers = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
               "Content-Type": "application/json"}
    async with session.post("https://api.deepseek.com/v1/chat/completions",
                            json=body, headers=headers) as r:
        data = await r.json()
        return data["choices"][0]["message"]["content"]

async def main():
    sections = [json.loads(l)["text"] for l in open("sections.jsonl")]
    sem = asyncio.Semaphore(16)              # 并发数——根据你的速率限制调整
    async def worker(sec, fout):
        async with sem:
            try:
                raw = await call(session, sec)
                pair = json.loads(raw.strip().removeprefix("```json").removesuffix("```").strip())
                if {"instruction","input","output"} <= pair.keys():
                    fout.write(json.dumps(pair) + "\n"); fout.flush()
            except Exception as e:
                print("skip:", e)
    async with aiohttp.ClientSession() as session, open(f"pairs_{TASK}.jsonl","w") as fout:
        await asyncio.gather(*[worker(s, fout) for s in sections])

asyncio.run(main())
```

{% endraw %}

成本检查：5000个段落 × 约2000输入token + 约500输出token。V4-Flash输入 $0.14/M，输出 $0.28/M，大约**$1.50–3 总计**。即使V4-Pro也在$15以下。对你来说微不足道。在Air上运行——只是API调用。

**在训练前验证数据集**（垃圾对 = 垃圾学生）：

```python
# inspect.py — 合理检查
import json
pairs = [json.loads(l) for l in open(f"pairs_extraction.jsonl")]
print(f"{len(pairs)} 个对")
# 对于提取任务，检查输出是否符合预期模式
bad = sum(1 for p in pairs if not isinstance(p["output"], (dict,str)))
print(f"格式错误输出数: {bad}")
print(json.dumps(pairs[0], indent=2)[:800])
```

在训练前**立即**保留300个对作为评估集——`head -n 300 > eval.jsonl`，其余 → `train.jsonl`。

---

## 阶段3：对学生进行LoRA（Qwen3-8B + 4070）

使用 `unsloth`——这是在单张消费级GPU上最快的方法，通过4位量化将8B+LoRA塞进12GB，迭代速度符合你的vibe-coding工作流。（如果你想要更少的抽象，TRL/PEFT是更常规的选择。）

```python
# train_lora.py — 在4070上进行QLoRA
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
import json

model, tok = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-8B-unsloth-bnb-4bit",   # 4位，适配12GB
    max_seq_length=4096, load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32, lora_dropout=0,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
)

def fmt(ex):
    out = ex["output"] if isinstance(ex["output"], str) else json.dumps(ex["output"])
    msgs = [{"role":"user","content": ex["instruction"]+"\n\n"+ex["input"]},
            {"role":"assistant","content": out}]
    return {"text": tok.apply_chat_template(msgs, tokenize=False)}

ds = load_dataset("json", data_files="train.jsonl")["train"].map(fmt)

trainer = SFTTrainer(
    model=model, tokenizer=tok, train_dataset=ds,
    args=SFTConfig(
        per_device_train_batch_size=2, gradient_accumulation_steps=4,
        warmup_steps=20, num_train_epochs=3, learning_rate=2e-4,
        fp16=True, logging_steps=10, output_dir="out-sec-lora",
        optim="adamw_8bit", lr_scheduler_type="cosine",
    ),
)
trainer.train()
model.save_pretrained("out-sec-lora")   # 仅适配器，约100MB
```

在4070上，5000对 × 3个epoch ≈ **20–40分钟**。这是快速循环——在此迭代数据质量。一旦可行，可选择在MI300X上使用V4-Flash或32B学生运行*相同脚本*以获取“生产”版本；代码几乎不变。

---

## 阶段4：真正能内部落地的评估

这是区分“我训练了一个东西”和“这里有可测量的能力”的关键。在保留的300个对上三向比较：**老师（上限）vs 学生零样本（基线）vs 学生LoRA（你的结果）**。

```python
# eval.py — 关键成果
import json
from unsloth import FastLanguageModel

eval_set = [json.loads(l) for l in open("eval.jsonl")]

def score_extraction(pred, gold):
    # 字段级F1，适用于提取的关键字；对顺序不敏感
    try:
        p, g = json.loads(pred), gold if isinstance(gold,dict) else json.loads(gold)
    except: return 0.0
    pk, gk = set(map(str,_flatten(p))), set(map(str,_flatten(g)))
    if not gk: return 1.0 if not pk else 0.0
    tp = len(pk & gk)
    prec = tp/len(pk) if pk else 0; rec = tp/len(gk)
    return 2*prec*rec/(prec+rec) if (prec+rec) else 0.0

def _flatten(o, pre=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from _flatten(v, f"{pre}.{k}")
    elif isinstance(o,list):
        for v in o: yield from _flatten(v, pre)
    else: yield f"{pre}={o}"

def gen(model, tok, ex):
    msgs=[{"role":"user","content":ex["instruction"]+"\n\n"+ex["input"]}]
    ids=tok.apply_chat_template(msgs, return_tensors="pt", add_generation_prompt=True).to(model.device)
    out=model.generate(ids, max_new_tokens=512, do_sample=False)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)

# 加载基础（零样本）和LoRA版本，分别评分
for tag, adapter in [("zeroshot", None), ("lora", "out-sec-lora")]:
    model, tok = FastLanguageModel.from_pretrained("unsloth/Qwen3-8B-unsloth-bnb-4bit",
                    max_seq_length=4096, load_in_4bit=True)
    if adapter: model.load_adapter(adapter)
    FastLanguageModel.for_inference(model)
    scores=[score_extraction(gen(model,tok,ex), ex["output"]) for ex in eval_set]
    print(f"{tag}: mean F1 = {sum(scores)/len(scores):.3f}")
```

标题变成一张表：

| 模型 | 字段F1 | 每千次调用成本 | 延迟 |
|---|---|---|---|
| V4-Pro (老师) | 0.91 | $X | 高 |
| Qwen3-8B 零样本 | 0.58 | 本地 | 低 |
| **Qwen3-8B + LoRA (你的)** | **0.84** | **本地** | **低** |

*这就是内部推销：*“我将一个前沿模型蒸馏成一个8B模型，在本地运行，达到老师质量的92%，零API成本且没有数据离开银行。”对银行来说，**本地 + 无数据外泄**的角度比F1数值更有价值——这是合规胜利，而不仅仅是机器学习胜利。

---

## 构建顺序（最快获得信号）

1. **今天：** 阶段1+2在Air上运行 → 得到 `pairs_extraction.jsonl`，人工检查10个对。（约1小时，主要是API等待）
2. **明天：** 阶段3在4070上运行 → 30分钟训练，确认能生成有效JSON。（约2小时含调试）
3. **然后：** 阶段4 → 三向对比表。（约1小时）
4. **可选扩展：** 如果8B显示出信号且你想要更大标题，可在MI300X上以V4-Flash-LoRA重新运行学生。

总计得到一个可分享成果：大约一个周末，与GPT-2运行不同，输出是一个*可测量的任务胜利*加上一个可重用的蒸馏框架，你可以将其指向任何内部语料库——这才是真正可转移的资产。

提前提醒两个坑：(1) Qwen3有思考模式——在结构化提取中禁用它（聊天模板中设置 `enable_thinking=False`），否则它会在JSON外面包裹推理内容。(2) 使用贪婪解码（`do_sample=False`）以确保评估可重现，但检查老师是否在不同段落生成了几乎相同的输出，否则你测量的是记忆而非提取。

你是否希望我编写MI300X扩展版本（V4-Flash学生，多GPU LoRA配置）作为阶段3的即插即用方案，或者完善问答任务的评估（基于答案token的F1而非字段）？
