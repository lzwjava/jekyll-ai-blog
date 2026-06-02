---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Prompting Mistakes to Avoid
translated: false
type: note
---

Question: What are the common ways people wrongly or inefficiently use AI/LLM tools (like Claude, Copilot, etc.), particularly in terms of writing simple prompts without providing proper context or clear questions?

Answer:

Yes, you are absolutely right. This is one of the most widespread and well-documented problems in AI usage today. Here is a comprehensive breakdown:

---

## The Core Problem: "Prompt and Pray" Mentality

One of the most common mistakes is submitting vague, general prompts and expecting AI to "read your mind." Weak prompts create a "priming problem" where the AI lacks sufficient context to provide a relevant response.

Bad prompting isn't limited to end users — people building applications that hit LLM APIs commonly write short prompts that lack detail, resulting in unsatisfactory and inconsistent results.

---

## The Main Ways People Use AI Inefficiently

### 1. Vague, Imprecise Language

Using subjective or imprecise language like "make it more professional" or "summarize this" gives the LLM no context for what "professional" means to you. This leads to non-deterministic, inconsistent outputs that are impossible to rely on.

**Example of weak vs. strong prompt:**

- ❌ Weak: `"How do I add numbers in Excel?"`
- ✅ Strong: `"How do I add up a row of dollar amounts in Excel? I want to do this automatically for a whole sheet of rows with all the totals ending up on the right in a column called 'Total'."`

---

### 2. Missing Context (No Background, Audience, or Purpose)

One frequent mistake is leaving out important background details like the target audience, tone, or purpose. A vague prompt like "Create an article on market segmentation" doesn't provide enough direction for focused results.

For Claude Code and Copilot specifically, this means not telling the AI:

- What language/framework you are using
- What the existing codebase looks like
- What the feature is supposed to do for the end user

---

### 3. No Clear Goal / Wrong Problem Framing

A "Type III Error" happens when a prompt is well-crafted and followed precisely by the model, but the output is irrelevant or unhelpful because the underlying task was misunderstood. The model does exactly what it was asked to do, but the prompt was aimed at the wrong goal. The failure is not in the execution, but in the framing.

---

### 4. Not Specifying Output Format or Length

Not specifying the desired output length or level of detail causes the model to guess — it might give you a sentence when you need a paragraph, or a full essay when you just need a brief summary.

---

### 5. Overloading a Single Prompt

Cramming too much into a single prompt can result in confusion and diluted outputs. Instead, breaking requests into smaller, focused parts makes it easier for the AI to process and deliver coherent results.

---

### 6. Not Telling the AI What to *Exclude*

Telling the LLM what to include but not what to exclude can lead to the model including boilerplate text, disclaimers, or specific topics you don't want — forcing you to manually edit the output, which defeats the purpose of automation.

---

### 7. Hidden Assumptions — Assuming the AI Knows What You Know

You can't assume the AI knows what you know, because your expertise might not be in its training data. Therefore you should always look at a prompt and ask "Could I solve this with only the info provided?" A lot of the time, what you think is obvious based on your own experience is not obvious at all.

---

### 8. Not Iterating — Expecting Perfect Results on the First Try

Common mistakes include expecting prompts to work perfectly on the first try, not iterating based on results, not isolating variables when testing, or giving up too quickly when things don't work. Treat prompting as iterative and experimental — hypothesize, isolate, and refine systematically.

---

### 9. Trusting AI Output Without Verification

Common mistakes include trusting the model's confidence, not fact-checking important information, assuming coherence means correctness, or not verifying logical consistency.

---

## Quick Reference: What a Good Prompt Should Include

| Element | Example |
|---|---|
| **Role/Context** | "You are a senior Python developer..." |
| **Task** | "...refactor this function to be async..." |
| **Constraints** | "...without changing the existing API signature..." |
| **Output format** | "...and explain the changes in bullet points." |
| **Audience** | "Assume the reader is a junior dev." |
| **Exclusions** | "Do not use third-party libraries." |

---

## The Golden Rule

Even the smartest LLMs like GPT-4 or Claude can't read your mind — vague prompts drain your compute budget, increase errors, and erode trust. Be explicit — never assume the AI "knows" your business.

Think of the AI as a very capable but brand-new contractor: they need a proper brief, not just a rough idea.

References:

- [10 Common LLM Prompt Mistakes Killing Your AI's Performance](https://www.goinsight.ai/blog/llm-prompt-mistake/)
- [Thinking Clearly with LLMs: Mental Models and Cognitive Pitfalls](https://dev.to/puritanic/thinking-clearly-with-llms-mental-models-and-cognitive-pitfalls-in-prompt-engineering-3dmm)
- [Common AI Prompt Mistakes and How to Fix Them](https://www.godofprompt.ai/blog/common-ai-prompt-mistakes-and-how-to-fix-them)
- [Common Prompt Engineering Mistakes to Avoid in 2026](https://treyworks.com/common-prompt-engineering-mistakes-to-avoid/)
- [Beyond "Prompt and Pray": 14 Prompt Engineering Mistakes](https://odsc.medium.com/beyond-prompt-and-pray-14-prompt-engineering-mistakes-youre-probably-still-making-c2c3a32711bc)
- [Overcoming Bad Prompts with Help from LLMs](https://www.dbreunig.com/2025/03/16/overcoming-bad-prompts-with-help-from-llms.html)
- [Tricks to Fix Stubborn Prompts](https://incident.io/building-with-ai/tricks-to-fix-stubborn-prompts)
