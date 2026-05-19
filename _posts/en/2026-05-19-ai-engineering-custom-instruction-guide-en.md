---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Engineering Custom Instruction Guide
translated: false
type: note
---

Done. Here's what I created and why:

---

**File written:** `/Users/lzwjava/projects/jekyll-ai-blog/original/2026-05-19-custom-instruction-en.md`

**What's in it and why:**

I distilled your entire identity — 12 years of shipping, startup founding, model training, heavy LLM usage, self-taught CS — into a custom instruction that pushes AI answers toward your long-term goal of AI engineering. Here's the structure and the thinking behind each section:

| Section | What it does |
|---|---|
| **Who I Am** | Tells the AI your actual biography — startup founder, bank engineer, GPT-2 trainer, top 6% AI user. This prevents it from assuming you're a junior or a generic user. |
| **Long-Term Goal** | Makes explicit that you're transitioning into AI engineering — training, agents, LLM internals. Every answer should accelerate this. |
| **Technical depth (Karpathy-style)** | Forces first-principles explanations — show the math, walk through the forward pass, reference the code. No hand-waving. |
| **Code-first, build-first** | Your vibe coding ethos: always prefer code over prose, minimal implementations over long explanations. |
| **AI and LLM bias** | When there's a choice between a traditional approach and an AI-native one, the AI picks AI. This compounds over hundreds of answers — you accumulate AI knowledge by default. |
| **Practical > theoretical** | Working code > white papers. If citing a paper, show the 50-line Python implementation. |
| **CS fundamentals** | Tells AI you have solid foundations — don't dumb down, but connect new ideas to what you know. |
| **English first** | Your professional language. No Chinese in answers. |
| **Search-first** | Evidence-based answers with sources — you're building real systems, not collecting plausible guesses. |
| **Vibe coding ethos** | CLI-first, scripting-heavy, AI-augmented. No GUI workflows. Terminal-native. |

**Where to paste this:**

This works as-is in:
- **Claude / ChatGPT** — paste into custom instructions or system prompt
- **Cursor** — paste into `.cursorrules` or Rules for AI
- **Any AI coding tool** — this is the "who I am" preamble

The post is also ready to publish on your Jekyll blog once you run the pipeline — it's in `original/` following your standard naming convention.