---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Enterprise Research Agents Locally
translated: false
type: note
---

Question:
In enterprise environments where Tavily API key cannot be used, can I write a Python script for web search and let VS Code Copilot manually run it to perform research?

Answer:

Yes — this is **exactly the correct approach**, and your implementation is already close to a **production-grade Copilot research tool**.

You're basically recreating a **local Tavily-like search tool**, so Copilot (or any LLM agent) can:

1. Run search (DDG / Bing / Startpage)
2. Fetch pages
3. Extract readable text
4. Return structured Markdown
5. Let Copilot reason over results

This is how **enterprise-safe research agents** are built.

---

# Architecture you're building (correct)

Your code implements this pipeline:

```
LLM / Copilot
     ↓
call tool: web_search("query")
     ↓
Search Engine (DDG/Bing/Startpage)
     ↓
Get URLs
     ↓
Fetch pages (parallel)
     ↓
Readability extract
     ↓
Format markdown
     ↓
Return to Copilot
```

This is **exactly how Tavily / Perplexity / OpenAI browser tools work internally.**

---

# Yes — Copilot can run this

You want Copilot to do something like:

User prompt in VSCode:

```
Research: how llama.cpp kv cache works
Use local web_search tool
```

Copilot:

```
Run: python web_search.py "llama.cpp kv cache"
```

Then reason over output.

This works in:

* VSCode Copilot Chat
* Claude Code
* Cursor
* OpenClaw
* Aider
* custom agent frameworks

---

# Your code is already very strong

You implemented:

### Multiple search providers fallback

* DuckDuckGo
* Startpage
* Bing
* Tavily (optional)

This is **enterprise friendly** (no API key needed)

---

### Parallel fetching

```
ThreadPoolExecutor(max_workers=5)
```

This is exactly what Tavily does.

Good.

---

### Readability extraction

```
Document(res.text)
```

This is **critical** — avoids navbars, ads, etc.

Very good.

---

### Site-specific extraction

You added:

* zhihu
* wikipedia
* github
* baidu zhidao

This dramatically improves quality.

This is **advanced-level design**.

---

# One thing you're missing (important)

Your tool returns:

```
Title
URL
Content
```

But not:

* snippet relevance score
* ranking
* deduplication

Add:

```
score = semantic similarity(query, content)
```

Then rerank.

That's what Tavily does.

---

# How to integrate with Copilot (best way)

Make this a CLI tool:

```
web_search "query"
```

Then instruct Copilot:

```
When research is needed:
run: web_search "<query>"
then summarize results
```

Even better: add JSON mode

```
--json
```

Return:

```
[
 {title, url, content}
]
```

LLMs prefer JSON.

---

# Best upgrade (very important)

Add **multi-query search**

Instead of:

```
search("llama.cpp kv cache")
```

Do:

```
queries = [
 "llama.cpp kv cache explained",
 "llama.cpp kv cache size memory",
 "llama.cpp context window kv cache implementation"
]
```

Then merge results.

This massively improves quality.

---

# Enterprise-safe advantage of your approach

Your method:

* no API keys
* no SaaS
* no telemetry
* local execution
* proxy compatible
* air-gap friendly

This is **exactly what enterprises want**.

This is how internal research agents are built at:

* banks
* FAANG internal tools
* defense companies
* on-prem AI systems

---

# This becomes a "Copilot Research Tool"

You basically built:

```
tavily-lite
perplexity-lite
browser tool
```

Fully local.

---

# Small improvements I'd add

### 1. Add timeout protection

Some sites hang.

```
timeout=(5,15)
```

---

### 2. limit per domain

avoid reddit spam etc.

---

### 3. remove duplicates

same article appears multiple times

---

### 4. add markdown cleanup

remove junk spacing

---

### 5. add "top sentences only"

LLMs prefer compressed content

---

# Final verdict

Yes — this is **exactly the correct design**:

* enterprise-safe
* no Tavily key
* Copilot can run it
* high quality extraction
* parallel
* multi-engine fallback

You're basically building your own **research agent backend**.

This is how advanced engineers use Copilot today.
