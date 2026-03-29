---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Importance of Manual CLI Testing
translated: false
type: note
---

Question: Why is it important to manually run the CLI to test AI-written code, rather than letting Claude Code handle all testing automatically?

Answer:

You are absolutely right. Here's a comprehensive breakdown of why manual CLI testing matters — especially when working with AI-generated code:

---

## 1. Understanding What the Code Actually Does

When Claude Code (or any AI) writes code for you, it produces a *black box* unless you run it yourself. Manual CLI testing forces you to:

- See the **actual output** vs. expected output
- Understand the **data flow** step by step
- Catch **edge cases** the AI didn't think of

---

## 2. AI-Written Tests Can Be Circular / Biased

If you let the AI write both the code **and** the tests, there's a serious problem:

> The AI tests what it *thinks* is correct — not what *you* actually need.

- The tests may pass but test the **wrong behavior**
- The AI may write tests that **always pass** by design
- You end up with false confidence in untested functionality

---

## 3. Manual Testing Builds Real Understanding

Running the CLI manually like you did:

```bash
python -m iclaw.main
```

...teaches you:

| What You Learn | Why It Matters |
|---|---|
| Startup sequence | What initializes first, what depends on what |
| Proxy/env handling | How config is loaded |
| Command structure | What's available and how it maps to code |
| Error messages | What breaks and why |
| Real UX | Is the feature actually usable? |

---

## 4. "Vibe Coding" Risk Without Manual Testing

A growing problem with AI-assisted development is **vibe coding** — accepting AI output without verification. The result:

- You ship code you **don't understand**
- You can't debug it when it breaks in production
- You can't extend it confidently
- You become **dependent** on the AI to fix what the AI broke

---

## 5. The Right Workflow

```
AI writes code
    ↓
You READ the code (understand intent)
    ↓
You RUN it manually (CLI / REPL / unit test)
    ↓
You OBSERVE behavior (does it match intent?)
    ↓
You ASK questions or fix gaps
    ↓
AI assists further — but YOU stay in control
```

---

## Summary

Manual CLI testing is not just QA — it is your **learning interface** into the AI-generated codebase. Without it, you're flying blind. The CLI run you showed is exactly the right instinct: **run it, observe it, understand it**.