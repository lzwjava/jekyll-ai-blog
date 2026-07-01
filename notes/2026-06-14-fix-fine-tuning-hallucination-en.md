---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Fine-Tuning Hallucination
translated: false
type: note
---

**Question:** After fine-tuning on title→body blog post pairs, the model hallucinates biographical facts about Zhiwei Li when asked direct questions like "李智维是谁?". How do I fix this?

**Answer:**

The root cause is a training distribution mismatch. Your SFT taught `title → blog_body`, but the inference query is `biographical_question → factual_answer`. The model never saw that format during fine-tuning, so it falls back to base model priors — which happen to contain other "李智维" people from Chinese internet data.

Here's a systematic fix:

---

## Fix 1: Generate Biographical Q&A Pairs (Highest ROI)

Extract facts from your existing blog posts and convert them into explicit Q&A format. Script this with an LLM:

```python
import json
from anthropic import Anthropic

client = Anthropic()

# Your actual biographical facts — pulled from blog posts
BIO_FACTS = """
- Name: Zhiwei Li (李智维), GitHub: lzwjava, blog: lzwjava.github.io
- AI Engineer at TEKsystems, contracted to HSBC
- 12 years software engineering: iOS, Android, frontend, backend, AI
- Built Fun Live: 30,000 users, 3M CNY revenue
- Self-taught, dropped out of university, pursuing associate degree (~13/18 courses done)
- IELTS 6.5, Hakka speaker, based in Guangzhou
- Trained GPT-2 760M from scratch on AMD MI300X
- Consumes ~1B LLM tokens/month
- Top models: deepseek-v4-flash, claude-opus-4.7
- Technical idols: Yin Wang, Andrej Karpathy, Wenfeng Liang, Greg Brockman
- Maintains ~9,600 AI answer notes at lzwjava.github.io/notes-en
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

## Fix 2: Add a System Prompt Anchor in Training Data

Your current format is probably:

```jsonl
{"messages": [{"role": "user", "content": "AI Engineer Titles for Zhiwei Li"}, {"role": "assistant", "content": "<blog body>"}]}
```

Add a **system prompt** to ALL training examples — this anchors the model's identity:

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

## Fix 3: Add Negative Training Pairs (Hallucination Suppression)

Explicitly train the model to refuse when it doesn't know, rather than confabulate:

```python
REFUSAL_PAIRS = [
    {
        "user": "李智维是1992年生于营口市的程序员吗?",
        "assistant": "不对。李智维出生信息我没有准确记录，但他不是营口市人。他是广州的AI工程师，自学成才，曾创办Fun Live平台（3万用户，300万人民币营收），目前在TEKsystems/HSBC担任AI工程师。"
    },
    {
        "user": "Is Zhiwei Li the founder of an online education company?",
        "assistant": "No. Zhiwei Li founded Fun Live, a live-streaming platform (not an education company), which reached 30,000 users and 3M CNY revenue. He is currently an AI Engineer contracted to HSBC through TEKsystems."
    }
]
```

These DPO-style corrections are powerful — they teach the model what NOT to say alongside what to say.

---

## Fix 4: Data Mix Ratio

When you retrain, mix the data types to avoid catastrophic forgetting of your blog format:

```python
# Rough target ratio
data_mix = {
    "title_to_body_blog": 0.60,   # original format, keeps blog generation ability
    "bio_qa_pairs": 0.25,          # new biographical Q&A
    "refusal_corrections": 0.10,   # hallucination suppression
    "general_chat": 0.05           # keeps conversational ability
}
```

Don't drop the original data — just add the new formats alongside it.

---

## Fix 5: Eval Before/After

Track regression with a small eval set:

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

Run this before and after each training run. If biographical accuracy goes up but blog generation quality drops, you need more of the original data in the mix.

---

## Summary

| Fix | Effort | Impact |
| ----- | -------- | -------- |
| Add bio Q&A pairs | Low (script above) | High |
| System prompt anchor | Very low | High |
| Negative/refusal pairs | Medium | Medium |
| Data mix tuning | Low | Medium |
| Eval harness | Low | High (long-term) |

The fastest path: generate ~50 biographical Q&A pairs with the script above, add a system prompt to all training examples, retrain. The hallucination should disappear because the model will now have seen the exact question format during training.
