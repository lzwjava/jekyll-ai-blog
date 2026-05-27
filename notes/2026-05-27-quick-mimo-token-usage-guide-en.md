---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quick MiMo Token Usage Guide
translated: false
type: note
---

**Question:** How can I use the Xiaomi MiMo platform tokens before my Pro monthly plan expires in 2 days?

**Answer:**

Your plan has **106M tokens used out of 38B** — you've barely scratched the surface. With 2 days left, here's how to burn through useful work fast:

## High-Value Things to Do Right Now

### 1. Batch LLM API calls against your existing projects

Point your CLI agents (`ww`, `iclaw`, `zz`) at the MiMo endpoint instead of Anthropic/OpenAI. Check their docs for the base URL:**Answer:**

Got the docs. The API is OpenAI-compatible, so you can drop it into anything immediately.

## Quick Setup

```bash
export MIMO_API_KEY="your_key_here"
```

Base URL: `https://api.xiaomimimo.com/v1`  
Latest model: `mimo-v2.5-pro`

## High-Value Ways to Burn Tokens in 2 Days

Given your profile (CLI agents, blog, notes pipeline), here's what to actually do:

### 1. Wire it into your existing CLI agents as a cheap backend

Since it's OpenAI-compatible, just swap `base_url`:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MIMO_API_KEY"],
    base_url="https://api.xiaomimimo.com/v1"
)
```

Point `ww`/`zz`/`iclaw` here instead of OpenAI. Zero code change if you're already using OpenAI SDK.

### 2. Batch-process your blog posts or notes

You have ~400 blog posts and ~8,000 notes. Run bulk LLM passes on them:

```python
import os, glob
from openai import OpenAI

client = OpenAI(api_key=os.environ["MIMO_API_KEY"], base_url="https://api.xiaomimimo.com/v1")

for post in glob.glob("~/blog/_posts/*.md"):
    with open(post) as f:
        content = f.read()
    resp = client.chat.completions.create(
        model="mimo-v2.5-pro",
        messages=[
            {"role": "user", "content": f"Extract key technical concepts and generate 5 quiz questions:\n\n{content}"}
        ],
        max_completion_tokens=1024
    )
    print(resp.choices[0].message.content)
```

Ideas: generate flashcards, extract concept graphs, create summaries, find gaps in your notes.

### 3. Use it as a thinking/reasoning model for math/code problems

MiMo-V2.5-Pro has reasoning capability (`reasoning_content` field). Good for: algorithm derivation, proof-checking, transformer math you're studying.

```bash
curl -s -X POST 'https://api.xiaomimimo.com/v1/chat/completions' \
  -H "api-key: $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role":"user","content":"Derive the gradient of cross-entropy loss w.r.t. logits step by step"}],
    "max_completion_tokens": 2048,
    "temperature": 1.0
  }' | jq '.choices[0].message'
```

### 4. Hook it into Claude Code / Cline / OpenCode

The docs show a dedicated Claude Code integration page. You can use MiMo as the backend for your agentic coding sessions — free token burn at scale.

Set in your Claude Code config:
```json
{
  "api_url": "https://api.xiaomimimo.com/anthropic",
  "api_key": "your_mimo_key",
  "model": "mimo-v2.5-pro"
}
```

### 5. Multimodal / audio (if you have content)

They support image, audio, and video understanding. If you have any recorded talks, code screenshots, or diagrams to process, now's the time.

## TL;DR Priority Order

1. **Swap base_url** in your existing agents → instant token consumption on real workloads
2. **Batch your notes/blog** through summarization/QA generation pipelines
3. **Run reasoning-heavy tasks** (math, architecture design) where you'd normally pay more per token
4. **Configure in Claude Code/Cline** as backend for agentic coding

You have ~37.9B tokens remaining — even at aggressive API usage you won't make a dent in 2 days, so focus on tasks that produce real value, not burning for burning's sake.

**References:**

- [MiMo API Quick Start](https://platform.xiaomimimo.com/docs/zh-CN/quick-start/first-api-call)
- [MiMo Claude Code Integration](https://platform.xiaomimimo.com/docs/zh-CN/integration/claudecode)