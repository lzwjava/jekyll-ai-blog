---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI回答改变微调策略
translated: true
type: note
---

**问题：** 这1万条笔记是AI生成的回答（我提的问题，AI写的回复）——并非我自己的写作。这会改变计划吗？

**回答：**

是的，这会改变微调所能带来的效果——以及真正的资产是什么。

## 你实际上在训练什么

在AI撰写的答案上进行SFT = **知识蒸馏**。模型学习的不是“lzwjava的语气”——而是模仿那些写出答案的模型（deepseek、gpt等）的风格，并压缩成一个更小的学生模型。这仍然是一个合理且有趣的项目，但你需要清醒地看待：

- **质量上限 = 教师模型。** 你克隆的是它们2023–2026年的风格和错误，且是冻结的。
- **不一致的教师。** 来自不同模型/时期/风格的1万条答案 → 学生学到的是一个模糊的平均值。混合教师的SFT数据在效果上明显低于单一教师数据。
- **许可说明：** OpenAI的服务条款禁止使用其输出训练竞争模型；DeepSeek的输出则采用宽松许可。如果你的笔记混合了多个来源，这在涉及公开使用时至关重要。

## 真正的资产：你的1万条问题

答案是可替代的——如今任何前沿模型都能更好地重新生成它们。**问题才是不可替代的部分**：一套精心设计的课程，展现了自学者在AI工程师之路上实际会提出的问题，按顺序涵盖内核内部→GPU计算→Transformer。这是一个高质量的提示分布，是任何公开数据集都不具备的。

因此，更好的流程是：**保留你的问题，扔掉过时的答案，用同一个一致的教师模型重新生成。**

```python
# regen_answers.py — 使用单一的最新教师模型重建数据集
import json, asyncio
from openai import AsyncOpenAI  # OpenRouter

client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1")
MODEL = "deepseek/deepseek-v4-pro"   # 宽松许可输出，单一一致风格

SYSTEM = """你是一位针对经验丰富的自学工程师的技术导师。
从基本原理出发，代码优先，尽量减少废话，使用英文回答。"""

sem = asyncio.Semaphore(20)

async def regen(q):
    async with sem:
        r = await client.chat.completions.create(
            model=MODEL, max_tokens=2000,
            messages=[{"role": "system", "content": SYSTEM},
                      {"role": "user", "content": q}])
        return {"conversations": [
            {"role": "user", "content": q},
            {"role": "assistant", "content": r.choices[0].message.content}]}

async def main():
    qs = [json.loads(l)["conversations"][0]["content"]
          for l in open("notes_sft.jsonl")]
    results = await asyncio.gather(*[regen(q) for q in qs])
    with open("notes_sft_v2.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

asyncio.run(main())
```

成本估算：1万条问题 × 约1.5k输出token ≈ 1500万token——在deepseek定价下微不足道，或者只需使用部分免费的小米MiMo配额，将mimo-2.5-pro蒸馏到本地。然后在我之前回答中提到的Unsloth训练流程上，对`notes_sft_v2.jsonl`运行完全相同的训练。你将得到：一个基于*你的*问题分布蒸馏而成的4B–8B本地模型——一个个人离线导师，其能力恰好集中在你的好奇心上。这对于M2 Air上的GGUF来说是一个真正有用的成果。

## 如果你想要一个带有*你自身风格*的模型

你大约400篇博客文章是你唯一的人工撰写语料库。这可能只有0.5–200万token——单独用于SFT太小了，但有两种可行方案：

1. **在蒸馏模型上叠加风格LoRA**：在SFT阶段之后，使用低学习率（5e-5）、在原始博客文本上进行1个epoch的继续预训练。足以调整语气，但不足以注入知识。
2. **挖掘你的Git历史**：如果你在仓库中对任何AI回答进行过手动编辑，`git log -p`会为你提供（AI草稿 → 你的编辑）配对——这是免费的DPO数据，也是整个仓库中最能体现“你”的信号。

```bash
# 查找初始提交后你实际编辑过的文章（DPO候选）
cd jekyll-ai-blog
git log --format= --name-only --diff-filter=M -- '_posts/*.md' | sort | uniq -c | sort -rn | head -50
```

## 结论

1. 不要对过时的混合教师答案进行SFT——利用你的问题，用一个教师模型重新生成。
2. 蒸馏到Qwen3-4B/8B（4070用于迭代，MI300X用于大规模运行）。
3. 可选地，从你的400篇博客文章中叠加一个风格LoRA，并挖掘Git编辑以获取DPO配对。

这个版本的项目在简历上也更有优势：“构建了一个蒸馏流程（提示挖掘 → 合成重新生成 → SFT → DPO）”是真正的数据集工程，这正是你所说的想锻炼的能力。
