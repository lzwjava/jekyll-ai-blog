---
audio: false
generated: true
image: false
lang: en
layout: post
title: Real Workloads Behind Billions of Tokens
translated: false
type: note
---

Question: How do people consume 1B or 5B LLM tokens per day/week? What are the real workloads behind these numbers?

Answer:

The key idea: **nobody types enough chat messages manually to reach billions of tokens.** The huge token volumes come from **automation, agents, products, and pipelines**.

1B tokens/day sounds huge, but it is actually reachable:

- 1B tokens/day ≈ 11,500 tokens/second continuously
- 5B tokens/week ≈ 8,300 tokens/second average

A single human conversation is tiny:

- Normal ChatGPT conversation: ~5k–50k tokens
- Long coding session: ~100k–1M tokens
- Agent coding task: can reach millions of tokens because it loops, reads files, runs tools, retries, reasons, etc. [arXiv](https://arxiv.org/abs/2604.22750?utm_source=chatgpt.com)

So the trick is **many machines doing work in parallel**.

---

## 1. AI coding agents

Example:

A company has:

- 10,000 developers
- each developer uses an agent 2 hours/day
- each agent consumes 100k tokens/hour

Calculation:

```
10,000 developers
× 2 hours
× 100k tokens/hour

= 2 billion tokens/day
```

The agent is not just answering:

```
User:
"fix this bug"

Agent:
- reads repo
- reads docs
- searches code
- generates plan
- edits files
- runs tests
- sees errors
- fixes again
- reviews diff
```

Every loop burns tokens.

Agent workflows are much more token hungry than normal chat because they repeatedly interact with tools and context. [arXiv](https://arxiv.org/abs/2604.22750?utm_source=chatgpt.com)

---

## 2. Customer-facing AI products

Imagine an AI customer service company:

```
10 million users
× 20 conversations/day
× 5,000 tokens/conversation

= 1 trillion tokens/day
```

Examples:

- AI search engines
- AI tutors
- AI translators
- AI companions
- AI shopping assistants
- AI call centers

The user sees:

> "Ask AI a question"

but behind the scenes:

```
query
 ↓
retrieve documents
 ↓
summarize
 ↓
reason
 ↓
call tools
 ↓
generate answer
```

Many internal tokens are invisible.

---

## 3. Data processing pipelines

Companies run millions of documents through models:

Example:

```
10 million documents
× 10,000 tokens/document

= 100B tokens
```

Tasks:

- summarize contracts
- extract invoices
- classify emails
- analyze customer feedback
- migrate old code
- translate documents

A bank could process years of:

```
PDFs
emails
tickets
logs
source code
```

through LLMs.

---

## 4. Autonomous agents running 24/7

This is probably the future big consumer.

Instead of:

```
human → AI → answer
```

it becomes:

```
AI agent
 |
 +-- reads emails
 +-- monitors systems
 +-- writes reports
 +-- creates PRs
 +-- negotiates APIs
 +-- researches competitors
 +-- updates databases
```

A company might have:

```
1000 agents

each:
1M tokens/day

=

1B tokens/day
```

Enterprise AI usage is already moving from simple chat toward delegated agent workflows. [OpenAI](https://openai.com/signals/enterprise-data/?trk=public_post_comment-text\&utm_source=chatgpt.com)

---

## 5. Training and evaluation

Labs also consume huge tokens:

Example:

```
100,000 benchmark tasks
× 100k tokens/task

= 10B tokens
```

Used for:

- model evaluation
- synthetic data generation
- RL training
- red teaming
- prompt optimization

---

## A realistic "5B tokens/week" startup

A small AI company could reach it:

```
20 engineers using coding agents
    ↓
20 × 50M tokens/week

= 1B tokens/week


10 customer AI agents
    ↓
10 × 300M tokens/week

= 3B tokens/week


document processing
    ↓
1B tokens/week

TOTAL:
5B tokens/week
```

This is not science fiction. Large organizations already report extremely large-scale AI token processing, and token consumption is increasingly driven by agents rather than only chat usage. [McKinsey & Company](https://www.mckinsey.com/capabilities/quantumblack/our-insights/is-that-ai-agent-worth-it-agentic-economics-and-the-modern-operating-model?utm_source=chatgpt.com)

---

## Why this matters for an AI consultancy/startup

For a traditional software company:

```
sell hours
↓
10 engineers × 160 hours/month
```

For an AI-native company:

```
sell intelligence
↓
100 agents × millions of tokens/day
```

Your "factory" becomes:

```
customer problem
      |
      v
AI agents
      |
      v
tokens + GPUs + tools
      |
      v
business output
```

The companies that build these systems will naturally become high token consumers.

A useful next step would be to design a **small AI consultancy architecture that can realistically generate 1B tokens/month and convert that into paying customer value**. I can help map that out.
