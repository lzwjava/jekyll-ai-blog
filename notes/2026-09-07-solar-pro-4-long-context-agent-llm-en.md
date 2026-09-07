---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Solar Pro 4: Long-Context Agent LLM"
translated: false
type: note
---

Question: **What is Upstage Solar Pro 4, and why is it interesting?**

Answer:

Upstage's **Solar Pro 4 (SP4)** is a closed-source LLM released in August 2026. The interesting part isn't simply "another frontier model"—it's explicitly optimized for **long-horizon agent work**: reading lots of context → calling tools → reasoning over intermediate results → producing a final artifact. ([Upstage AI][1])

### 1. The headline specs

|                   |           Solar Pro 4 |
| ----------------- | --------------------: |
| Context           |    **524,288 tokens** |
| Max output        |    **131,072 tokens** |
| Input             | **$0.03 / 1M tokens** |
| Output            | **$0.12 / 1M tokens** |
| Cached input      |       **$0.006 / 1M** |
| Reasoning         |                   Yes |
| Tool calling      |                   Yes |
| Structured output |                   Yes |
| Input modality    |                  Text |
| Released          |          Aug 10, 2026 |

The 524K number is especially interesting. You can put roughly **a large codebase or hundreds of pages of documents** into one context without doing your own aggressive chunking/RAG. ([OpenRouter][2])

And the price is *extremely* low:

```text
1M input  = $0.03
1M output = $0.12

10M input + 2M output
= 10 × $0.03 + 2 × $0.12
= $0.54
```

That's unusually attractive for agents that make many model calls.

---

### 2. The important thing: it's an **agent model**

Upstage's positioning is quite explicit:

> Don't just answer the question. **Finish the job.**

For example:

```text
20 documents
      │
      ▼
┌───────────────┐
│ Solar Pro 4   │
│               │
│ reason        │
│ inspect       │
│ call tools    │
│ verify        │
└───────┬───────┘
        │
        ├── Excel
        ├── Report
        └── PowerPoint
```

Upstage demonstrated a workflow where SP4 read a policy document plus six market-data files, screened ten candidate locations, then produced an Excel workbook, report, and slide deck. ([Upstage AI][1])

That's different from benchmarking:

```text
prompt → answer
```

They're targeting:

```text
goal
 ↓
plan
 ↓
read context
 ↓
tool call
 ↓
observe result
 ↓
reason
 ↓
tool call
 ↓
verify
 ↓
deliverable
```

This is much closer to what you are doing with CLI agents.

---

### 3. Its benchmark profile is interesting

Upstage reports:

* **Terminal-Bench v2.1: 57**
* **τ³-Banking: 23**
* **AA-LCR long-context: 71**

The important one for me is **AA-LCR = 71** because it measures reasoning across roughly 100K-token documents. Upstage says this is where SP4 has particularly strong performance. ([Upstage AI][1])

Their broader Artificial Analysis score was reported as **42**, putting it in the general frontier-model neighborhood while being dramatically cheaper than typical frontier APIs. ([Upstage AI][3])

So I'd characterize it as:

```text
                 Intelligence
                      ↑
                      │       frontier models
                      │
                      │   Solar Pro 4
                      │
                      │
                      │
                      └──────────────────→
                         cost efficiency
```

Not necessarily **the smartest model**, but potentially a very good **$/completed-agent-task** model.

---

### 4. The 524K context is actually useful

For example, imagine your coding agent has:

```text
system prompt          10K
repository              80K
README                  10K
issue history           20K
tool results             50K
previous conversation    30K
tests                    20K
────────────────────────────
total                   220K
```

You can keep almost everything in one context:

```python
messages = [
    system_prompt,
    repo_context,
    issue,
    conversation,
    tool_results,
]
```

instead of constantly doing:

```text
retrieve → summarize → retrieve → summarize
```

That can be a **major advantage for agent reliability** because every summarization is information loss.

---

### 5. The price makes it particularly interesting for your agents

OpenRouter currently lists:

```text
Solar Pro 4

input:       $0.03 / 1M
cached:      $0.006 / 1M
output:      $0.12 / 1M
```

([OpenRouter][4])

Suppose your agent does:

```text
100 calls
average context: 100K
average output:   5K
```

That's approximately:

```text
input  = 100 × 100K = 10M tokens
output = 100 ×   5K = 0.5M tokens

cost
= 10 × $0.03
+ 0.5 × $0.12
= $0.36
```

Even if your actual workload is several times larger, you're still talking about **dollars rather than tens/hundreds of dollars**.

That's why I think SP4 is more interesting as an **agent backend** than as a ChatGPT replacement.

---

### 6. It's also OpenAI-compatible

This is nice for your stack.

OpenRouter exposes:

```text
model = "upstage/solar-pro4"
```

and supports tool/function calling and structured outputs. ([OpenRouter][2])

So an existing OpenAI-style agent can essentially do:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="..."
)

response = client.chat.completions.create(
    model="upstage/solar-pro4",
    messages=messages,
    tools=tools,
)
```

The model supports reasoning as well, so you can use it as the "brain" inside a tool-using loop rather than merely a text generator. ([Pi][5])

---

### 7. Where I'd actually use it

For your kind of work, I'd test it on:

**① Coding agents**

```text
repo
 ↓
Solar Pro 4
 ↓
bash
 ↓
pytest
 ↓
inspect error
 ↓
edit
 ↓
pytest
 ↓
commit
```

**② Huge-document agents**

```text
10 × 50-page PDFs
        ↓
     SP4
        ↓
cross-document reasoning
        ↓
structured answer
```

**③ Research agents**

```text
search
 ↓
100 documents
 ↓
extract evidence
 ↓
cross-check
 ↓
write report
```

**④ Office automation**

```text
CSV + PDF + policy
       ↓
    SP4 agent
       ↓
Excel + report + PPT
```

These are exactly the workloads Upstage says it optimized for. ([Upstage AI][1])

---

### 8. One important distinction: Solar Pro 4 ≠ Solar Pro 3

Don't confuse them.

Solar Pro 3 was a **102B total / 12B active MoE** model. ([OpenRouter][4])

Solar Pro 4 is positioned much more around **agentic behavior + long context + reliability**, and Upstage hasn't presented it simply as "a bigger Solar Pro 3."

So I would think:

```text
Solar Pro 3
    ↓
efficient general LLM / MoE

Solar Pro 4
    ↓
production agent model
    ├── long context
    ├── reasoning
    ├── tools
    ├── structured output
    └── document workflows
```

### My take

**Solar Pro 4 is one of the more interesting "cheap agent brain" models right now.**

The combination is unusual:

```text
524K context
+
reasoning
+
tool calling
+
structured output
+
$0.03/M input
+
$0.12/M output
```

The real question isn't *"is SP4 smarter than GPT/Claude/Gemini?"*

I'd test:

> **How much does it cost to successfully finish a real agent task?**

That's the metric that matters for `ww`, `iclaw`, or any production coding/research agent.

[Upstage's Solar Pro 4 announcement](https://www.upstage.ai/blog/en/solar-pro-4?utm_source=chatgpt.com)
[Solar Pro 4 on OpenRouter](https://openrouter.ai/upstage/solar-pro4?utm_source=chatgpt.com)

I can also benchmark-design a **Solar Pro 4 vs Qwen / Claude / GPT coding-agent test** using the same repo and tool loop, which would tell you much more than leaderboard numbers.

[1]: https://www.upstage.ai/blog/en/solar-pro-4?utm_source=chatgpt.com "Solar Pro 4: The Agentic Model That Finishes the Job"
[2]: https://openrouter.ai/upstage/solar-pro4?view=api&utm_source=chatgpt.com "Solar Pro 4 - API Pricing & Benchmarks | OpenRouter"
[3]: https://www.upstage.ai/news/upstage-ai-unveils-solar-pro-4-scoring-42-on-artificial-analysis-index-to-rank?utm_source=chatgpt.com "Upstage AI Unveils Solar Pro 4, Scoring 42 on Artificial Analysis Index to Rank Among Global Frontier Models"
[4]: https://openrouter.ai/provider/upstage?utm_source=chatgpt.com "Upstage | OpenRouter"
[5]: https://pi.dev/models/openrouter/upstage-solar-pro4?utm_source=chatgpt.com "Upstage: Solar Pro 4 · Models · Pi"
