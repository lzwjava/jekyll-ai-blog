---
audio: false
generated: true
image: false
lang: en
layout: post
title: Webpage Intelligence Filter Prompt
translated: false
type: note
---

Question: Can you give me a smart prompt that helps me automatically extract and understand relevant information from webpages without reading everything manually?

Answer:

Yes — what you’re trying to build is essentially a **“webpage intelligence filter prompt”**: it reduces reading, extracts relevance, and prioritizes only what matters to your goal (like your exam planning case).

Here is a **high-quality reusable prompt template** you can use with ChatGPT or any LLM:

---

## 🧠 Webpage Intelligence Filter Prompt (Reusable)

```
You are my information filtering assistant.

I will give you a webpage URL or pasted content.

Your task is:

1. First, identify my goal from context (ask if unclear).
2. Extract ONLY information relevant to my goal.
3. Ignore all unrelated sections (ads, admin info, unrelated notices).
4. Group results into:
   - 🔴 MUST READ (directly affects my goal / actions I must take)
   - 🟡 USEFUL CONTEXT (helps understanding but not required)
   - ⚪ IGNORE (irrelevant or administrative content)

5. For each relevant item:
   - Summarize in 1–2 lines
   - Include deadline / requirement if any
   - Highlight keywords like dates, codes, actions

6. Also extract:
   - Important titles/headlines only (as a bullet list)
   - Anything that affects timing, registration, or eligibility

7. Finally, output:
   - “What I should do next” (clear action steps)
   - “What I can ignore safely”

Be strict: prefer missing non-important details rather than including noise.
```

---

## ⚙️ Even More Powerful Version (for automation / repeated use)

If you want it more “system-like”:

```
Act as a high-precision information extraction engine.

Goal: help me avoid reading full documents while preserving decision-critical information.

Rules:
- Do not summarize everything.
- Only extract actionable or decision-relevant information.
- Always rank information by importance.
- Treat deadlines, eligibility rules, exam registration, and changes as HIGH PRIORITY.
- Treat explanations, background text, and institutional wording as LOW PRIORITY.

Output format:
1. Critical Actions
2. Key Deadlines
3. Relevant Items (bullet list)
4. Ignored Content Summary (one line)
5. Final Recommendation
```

---

## 🚀 Why this works (important insight)

What you are building here is basically:

> **Attention compression → decision extraction → action planning**

This is exactly how experienced people read:

* lawyers scan contracts
* engineers scan docs
* exam candidates scan notices
* PMs scan product updates

They don’t “read pages”, they extract **decisions + constraints + deadlines**

---

## 🧩 How you can upgrade further (your use case)

Since you are doing exams, you can extend the prompt like this:

* “Map extracted info to my exam courses”
* “Highlight only practical exam relevance”
* “Warn me if I might miss deadlines”
* “Cross-check with my schedule”

---

If you want, I can also help you build a **fully automated workflow**:

* paste link → auto extract → auto match with your exam plan → output checklist
* or even turn it into a small tool / script / LangChain pipeline

Just tell me 👍