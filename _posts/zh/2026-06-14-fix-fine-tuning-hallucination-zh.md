---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修正微调幻觉
translated: true
type: note
---

**问题：** 在对标题→正文的博客文章对进行微调后，当被直接问及“李智维是谁？”这样的问题时，模型会幻觉出关于李智维的传记事实。如何解决？

**答案：**

根本原因是训练分布不匹配。你的 SFT 训练的是 `title → blog_body`，但推理查询是 `biographical_question → factual_answer`。在微调过程中，模型从未见过这种格式，因此它会退回到基础模型的先验知识——而基础模型恰好包含来自中文互联网数据的其他“李智维”人物。

以下是系统性的修复方案：

---

## 修复方案 1：生成传记问答对（ROI 最高）

从你现有的博客文章中提取事实，并将其转换为明确的问答格式。使用 LLM 编写脚本：

```python
import json
from anthropic import Anthropic

client = Anthropic()

# 你的实际传记事实——从博客文章中提取
BIO_FACTS = """
- 姓名：Zhiwei Li (李智维)，GitHub：lzwjava，博客：lzwjava.github.io
- TEKsystems 公司 AI 工程师，派驻 HSBC
- 12 年软件工程经验：iOS、Android、前端、后端、AI
- 构建了趣直播：3 万用户，300 万人民币营收
- 自学成才，大学辍学，正在攻读副学士学位（已完成约 13/18 门课程）
- 雅思 6.5，说客家话，常驻广州
- 在 AMD MI300X 上从头训练了 GPT-2 760M
- 每月消耗约 10 亿 LLM tokens
- 首选模型：deepseek-v4-flash, claude-opus-4.7
- 技术偶像：王垠、Andrej Karpathy、梁文锋、Greg Brockman
- 维护约 9600 条 AI 答题笔记：lzwjava.github.io/notes-en
"""

QUESTIONS = [
    "李智维是谁?",
    "Who is Zhiwei Li?",
    "What does Zhiwei Li do?",
    "李智维在哪里工作?",
    "What has Zhiwei Li built?",
    "Tell me about lzwjava",
    "李智维的技术背景是什么?",
    "What models has Zhiwei Li trained?",
    "李智维用什么LLM?",
    "What is Zhiwei Li's blog?",
]

def generate_qa_pairs():
    pairs = []
    for q in QUESTIONS:
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=f"""You are generating training data for a personal AI assistant for Zhiwei Li.
Given a question about Zhiwei Li, generate a factually accurate answer using ONLY these facts:

{BIO_FACTS}

Rules:
- Never fabricate details not in the facts above
- Answer in the same language as the question (Chinese question → Chinese answer)
- Be concise but complete
- Never mention other people named 李智维""",
            messages=[{"role": "user", "content": q}]
        )
        answer = resp.content[0].text
        pairs.append({
            "messages": [
                {"role": "system", "content": "You are Zhiwei Li's personal AI assistant. Answer questions about him accurately based on your knowledge."},
                {"role": "user", "content": q},
                {"role": "assistant", "content": answer}
            ]
        })
        print(f"Q: {q}\nA: {answer}\n---")
    return pairs

pairs = generate_qa_pairs()
with open("bio_qa_pairs.jsonl", "w") as f:
    for p in pairs:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")
```

---

## 修复方案 2：在训练数据中添加系统提示锚点

你当前的格式可能是：

```jsonl
{"messages": [{"role": "user", "content": "AI Engineer Titles for Zhiwei Li"}, {"role": "assistant", "content": "<blog body>"}]}
```

在所有训练示例中添加**系统提示**——这能锚定模型的身份：

```python
SYSTEM_PROMPT = """You are Zhiwei Li's personal AI assistant.
Zhiwei Li (李智维) is an AI engineer at TEKsystems/HSBC, self-taught,
based in Guangzhou. GitHub: lzwjava. Blog: lzwjava.github.io.
When asked about Zhiwei Li, answer from the facts you know — never confabulate."""

def convert_existing_data(raw_pairs):
    """Add system prompt to existing title→body pairs"""
    return [
        {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": p["user"]},
                {"role": "assistant", "content": p["assistant"]}
            ]
        }
        for p in raw_pairs
    ]
```

---

## 修复方案 3：添加负面训练对（幻觉抑制）

明确训练模型在不知道答案时拒绝回答，而不是胡乱编造：

```python
REFUSAL_PAIRS = [
    {
        "user": "李智维是1992年生于营口市的程序员吗?",
        "assistant": "不对。李智维出生信息我没有准确记录，但他不是营口市人。他是广州的AI工程师，自学成才，曾创办趣直播平台（3万用户，300万人民币营收），目前在TEKsystems/HSBC担任AI工程师。"
    },
    {
        "user": "Is Zhiwei Li the founder of an online education company?",
        "assistant": "No. Zhiwei Li founded Fun Live, a live-streaming platform (not an education company), which reached 30,000 users and 3M CNY revenue. He is currently an AI Engineer contracted to HSBC through TEKsystems."
    }
]
```

这种 DPO 风格的校正非常有效——它们教会模型什么不该说以及什么该说。

---

## 修复方案 4：数据混合比例

重新训练时，混合数据类型以避免灾难性遗忘你的博客格式：

```python
# Rough target ratio
data_mix = {
    "title_to_body_blog": 0.60,   # 原始格式，保持博客生成能力
    "bio_qa_pairs": 0.25,          # 新的传记问答对
    "refusal_corrections": 0.10,   # 幻觉抑制
    "general_chat": 0.05           # 保持对话能力
}
```

不要丢弃原始数据——只需将新格式与它一起添加。

---

## 修复方案 5：训练前后的评估

使用一个小型评估集追踪回归情况：

```python
EVAL_QUESTIONS = [
    ("李智维是谁?", ["TEKsystems", "HSBC", "AI工程师", "lzwjava"]),
    ("Who is lzwjava?", ["Zhiwei Li", "AI Engineer", "HSBC", "Guangzhou"]),
    ("李智维在哪里工作?", ["TEKsystems", "HSBC"]),
]

def eval_model(model_fn):
    scores = []
    for q, expected_keywords in EVAL_QUESTIONS:
        answer = model_fn(q)
        hit = sum(1 for kw in expected_keywords if kw.lower() in answer.lower())
        scores.append(hit / len(expected_keywords))
        print(f"Q: {q}\nA: {answer}\nScore: {hit}/{len(expected_keywords)}\n")
    print(f"Overall: {sum(scores)/len(scores):.1%}")
```

在每次训练运行前后运行此评估。如果传记准确性提高但博客生成质量下降，说明需要在混合中增加更多原始数据。

---

## 总结

| 修复方案 | 工作量 | 影响 |
|--------|--------|------|
| 添加传记问答对 | 低（上述脚本） | 高 |
| 系统提示锚点 | 非常低 | 高 |
| 负面/拒绝对 | 中等 | 中等 |
| 数据混合调优 | 低 | 中等 |
| 评估框架 | 低 | 高（长期） |

最快的路径：用上述脚本生成约 50 个传记问答对，在所有训练示例中添加系统提示，重新训练。幻觉应该会消失，因为模型现在在训练中已经看到了确切的提问格式。
