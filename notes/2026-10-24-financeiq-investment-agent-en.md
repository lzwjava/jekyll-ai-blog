---
audio: false
generated: true
image: false
lang: en
layout: post
title: FinanceIQ Investment Agent
translated: false
type: note
---

Done. **FinanceIQ** is built, tested end-to-end, and committed.

## What you got

```
finance_agent/
  agent.py      LlamaIndex FunctionAgent + grounding system prompt
  tools.py      search_market_news (Tavily) · get_company_news · get_stock_quote (yfinance) · get_market_indices
  llm.py        DeepSeekLLM — OpenAI-compatible adapter for llama-index
main.py         CLI: one-shot or interactive chat
README.md · requirements.txt · .env.example · .gitignore
```

## How it works

The LlamaIndex **FunctionAgent** (DeepSeek `deepseek-chat` as reasoning LLM) answers investment questions by: **③ searching live news 2–3×** (macro, sectors, plus `site:finance.yahoo.com` queries) → **② pulling live quotes for every candidate ticker** → **③** returning a structured report — market snapshot, 3–5 ideas (thesis tied to cited headlines, catalysts, risks, sizing, horizon), a "watch out for" list, and a disclaimer.

## Verified live

Ran a full session: it caught the AI-infrastructure selloff, crude >$100 on Middle East escalation, and a 5% 10-year yield; recommended energy (XLE/CVX/SLB), NVDA on the dislocation, utilities (XLU), and gold (GLD) — each with real quote levels (e.g. CoreWeave down ~40%, flagged as the big risk). Both modes tested:

```bash
python3 main.py "What should I invest in today?"    # one-shot
python3 main.py                                     # interactive chat
```

## One important call

You asked for the **LLM API's native web search** — I tested all of them in your env: the `OPENAI_API_KEY` is **rejected** by api.openai.com, `ANTHROPIC_API_KEY` is **empty** (and the sssaicode Claude relay rejects third-party clients), and the **Gemini** key works but has **depleted credits**. DeepSeek/Groq don't expose native web search. So I wired the industry-standard replacement — **Tavily** (`TAVILY_API_KEY` in your env) — as the agent's search tool. If you later get a valid OpenAI/Anthropic key, swapping in their native web-search tool is a 10-line change.
