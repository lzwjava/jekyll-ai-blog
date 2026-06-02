---
audio: false
generated: true
image: false
lang: en
layout: post
title: Logging Without LLM Overuse
translated: false
type: note
---

Question:
How can I design a simple logging system (like `wwlogs/log-history.txt`) using timestamp-based filenames with an optional friendly name, to avoid overusing LLM APIs for naming/searching logs, and is overuse of AI (like at Meta) leading to wasted tokens?

Answer:

You’re pointing at a very real and practical problem: **people are overusing LLMs for tasks that should be deterministic and cheap**. Naming logs is a perfect example.

Let’s separate this into two parts: **system design** and **the AI overuse question**.

---

# 1. A clean, practical logging design (no LLM needed)

Your idea is solid. In fact, it's *better than using AI* for this use case.

### ✅ Core design

* Default filename:
  `yyyyMMdd_HHmmss` (e.g., `20260417_153045.txt`)
* Optional flag:
  `--friendly-name "vpn_issue_coffee_shop"`

Final filename:

```
20260417_153045__vpn_issue_coffee_shop.txt
```

---

## Why this works better than LLM naming

* **Deterministic** → no randomness
* **Searchable** → grep / fzf / ripgrep works instantly
* **Cheap** → zero token cost
* **Composable** → works in shell pipelines
* **Stable** → no hallucination / weird naming

You’re basically applying a classic principle:

> If a problem can be solved with a function, don’t use a model.

---

## Suggested CLI design

Example command:

```bash
wwlog "VPN failed at coffee shop" --friendly-name vpn_issue
```

Generated file:

```
wwlogs/20260417_153045__vpn_issue.txt
```

---

## Minimal implementation (bash)

```bash
#!/bin/bash

LOG_DIR="wwlogs"
mkdir -p "$LOG_DIR"

timestamp=$(date +"%Y%m%d_%H%M%S")

friendly=""

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --friendly-name) friendly="$2"; shift ;;
    *) message="$1" ;;
  esac
  shift
done

if [ -n "$friendly" ]; then
  filename="${timestamp}__${friendly}.txt"
else
  filename="${timestamp}.txt"
fi

echo "$message" > "$LOG_DIR/$filename"

echo "Saved: $LOG_DIR/$filename"
```

---

## Searching logs (no AI needed)

```bash
# search by keyword
rg vpn wwlogs/

# fuzzy find
fzf --preview "cat {}" < <(ls wwlogs)

# filter by time
ls wwlogs | grep 20260417
```

---

## Optional upgrade: structured logs (still no AI)

Instead of plain text:

```json
{
  "time": "2026-04-17T15:30:45",
  "tag": "vpn_issue",
  "content": "VPN failed at coffee shop"
}
```

Now you can:

```bash
jq '.tag == "vpn_issue"' *.json
```

Still **zero tokens used**.

---

# 2. Should you use LLM for naming/searching?

Short answer: **almost never**.

Use LLM only when:

* You need **semantic clustering** ("group similar logs")
* You forgot keywords and want **natural language retrieval**
* You want **auto summaries**

Otherwise:

> filename + grep > LLM

---

# 3. About AI overuse (e.g., Meta internal push)

Your intuition is directionally correct, but slightly incomplete.

### Yes, waste exists

When companies push “use AI everywhere”:

* trivial tasks → LLM calls
* repeated prompts → token explosion
* no caching → duplicated cost

This leads to:

* higher infra cost
* latency overhead
* sometimes worse UX

---

### But it's not purely waste

Companies like Meta are optimizing for:

* **behavior change** (force adoption early)
* **data collection** (how people actually use AI)
* **long-term leverage**, not short-term efficiency

So internally, they accept:

> inefficiency now → capability later

---

# 4. The real principle (important)

You’re already thinking in the right abstraction:

### Use this decision rule:

| Task type            | Tool          |
| -------------------- | ------------- |
| Deterministic        | Code / script |
| Structured retrieval | grep / DB     |
| Fuzzy / semantic     | LLM           |
| Creative / unknown   | LLM           |

---

# 5. Your idea (refined)

What you’re building is essentially:

> **"LLM-minimal personal knowledge system"**

Key traits:

* timestamp-based indexing
* human-readable tags
* shell-native retrieval
* optional LLM layer (not default)

This is actually *more scalable* than “LLM everything”.

---

# Final take

* Your logging design is **correct and efficient**
* Using LLM for naming logs is **overengineering**
* Yes, there is real token waste in current AI usage trends
* But companies are trading cost for learning and speed

---

If you want, I can extend this into:

* a full `wwlog` tool (with tagging, search, summaries)
* or a hybrid system (local logs + optional LLM semantic search)

That’s where it gets really powerful.
