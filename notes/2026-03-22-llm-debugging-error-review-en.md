---
audio: false
generated: true
image: false
lang: en
layout: post
title: "LLM Debugging: Error Logs and Review"
translated: false
type: note
---

Question: When debugging with an LLM, is it especially effective to copy browser console logs or HTTP request errors, and while some say you don't need to read AI-generated code, isn't being able to quickly review it still a bonus for getting better help?

Answer:

## Debugging with LLMs: Console Logs, HTTP Errors & Code Review

### Why Console Logs and HTTP Errors Are Gold for LLMs

Yes — pasting raw browser console output or network errors is one of the **most efficient ways** to get useful help from an LLM, for several reasons:

**1. Errors are already structured information**

- Stack traces, error codes, and HTTP status messages are precise and unambiguous
- LLMs are trained on massive amounts of similar error patterns from Stack Overflow, GitHub issues, MDN, etc.
- There's no "translation loss" — you're giving the AI exactly what the runtime produced

**2. HTTP errors are especially diagnostic**

- A `401 Unauthorized` vs `403 Forbidden` vs `CORS error` each tells a completely different story
- Network tab details (request headers, response body, URL, method) give the LLM full context to pinpoint root cause
- The AI can immediately distinguish "your token is wrong" vs "your server isn't allowing cross-origin requests"

**3. Console logs remove ambiguity**

- Instead of you *describing* a bug ("it doesn't work"), the log *shows* the bug
- Null reference errors, type mismatches, undefined variables — all self-evident in a log

---

### The "You Don't Need to Read AI Code" Debate

Some people argue you can just blindly run AI-generated code. That's partially true for simple scripts — but **quick review is genuinely valuable**, and here's why:

| Scenario | Skip Review | Quick Review |
|---|---|---|
| Simple 5-line utility | ✅ Fine | ✅ Also fine |
| Code touching auth/security | ❌ Risky | ✅ Essential |
| Code modifying database/files | ❌ Risky | ✅ Essential |
| Large multi-function output | ❌ Hard to debug later | ✅ Catches mismatches early |
| You need to maintain it later | ❌ You'll be lost | ✅ You'll understand it |

**Even a 30-second skim helps you:**

- Spot if the AI misunderstood your intent
- Notice hardcoded values that should be variables
- Catch obvious logic errors before running
- Give better follow-up feedback ("you used POST but I need GET")

---

### The Feedback Loop: The Real Power

The real synergy is the **cycle**:

```
You paste error → AI explains & fixes → You skim the fix
→ You run it → New error appears → You paste that error
→ AI narrows down faster because context is building
```

Each paste of a real error **grounds the conversation in reality** rather than speculation. The AI isn't guessing what might be wrong — it's reading what *is* wrong.

---

### Practical Tips

- **Paste the full error**, not a summary — details like line numbers and stack frames matter
- **Include the relevant code block** alongside the error for even faster diagnosis
- **Network tab > Console** for API issues — copy the full request/response
- A quick scan of AI code is a **low-cost, high-reward habit** — even 20 seconds of review pays off
