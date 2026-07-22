---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Model Evaluation and Next Steps
translated: false
type: note
---

Now I have a complete picture. Here's what you're working on:

---

## 🏗️ What You're Building

You're training **small decoder-only language models (140M–286M params)** using the **nanochat** framework, focused on **code generation**.

### Three Major Training Runs:

| Run | Params | Data | Status |
|-----|--------|------|--------|
| **codeparrot-d12** ⭐ | 286M | 24.7B Python tokens (codeparrot-clean) | ✅ Trained (87k steps) + **just evaluated** |
| code-sec-fineweb-d12 | 286M | GitHub code + SEC filings + FineWeb-Edu | ✅ Trained (50k steps) |
| d12 SFT (earlier) | ~140M | SmolTalk + custom code/SEC + MMLU | ✅ SFT'd & evaluated |

### Current Focus: **codeparrot-d12**

This is the latest — a **Python code-focused model** trained on 53 shards of deduplicated, filtered Python code (~5.3M files). You just finished:
1. ✅ **Pipeline** — download → convert → tokenize (committed as `run_pipeline.sh`)
2. ✅ **Training** — 87k iterations, batch=65536, seq=2048
3. ✅ **Short-prompt eval** — `codeparrot/eval/`
4. ✅ **Long-prompt eval** — `codeparrot/eval_long/` (committed 2 hours ago)

---

## 📊 How The Model Performs

The eval results reveal a clear picture:

- **Good**: Simple Python functions, syntactic patterns, code formatting
- **Bad**: Logic errors in tree algorithms (BST insert deletes children), **repetition loops** (function names repeat `_async_async_async_async...` endlessly), no coherent multi-step reasoning
- **The SFT model** (140M) can do palindrome functions but fails at arithmetic, ML knowledge, SQL, and creative writing

---

## 🎯 Your Next Goal

Based on the project trajectory, your **most logical next step** is one of:

### 1. 🥇 **SFT the codeparrot-d12 base model**
   - Take the 286M Python model and do supervised fine-tuning on code instructions
   - This could fix the logic errors and repetition loops
   - You already have SFT infrastructure from `fineweb-code-sec-gpt-sft/`

### 2. 🥈 **Scale up — train a deeper model (d16 or d20)**
   - The d12 (286M) is hitting fundamental capability limits
   - More params + more compute = better reasoning

### 3. 🥉 **Build a code chat/assistant**
   - Add instruction-following format on top of codeparrot-d12
   - Turn it into a usable Python coding assistant

**Which direction interests you?** I can help set up the SFT pipeline, analyze eval results more deeply, or fix any issues in the current code.