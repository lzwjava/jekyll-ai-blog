---
audio: false
generated: true
image: false
lang: en
layout: post
title: Core Essentials of LLM Applications
translated: false
type: note
---

Yes, you’re thinking about it in the right direction. For most real-world applications built on LLMs (or any agent framework), the *essential information* comes down to a few fixed pieces. Everything else can usually be generated or scaffolded dynamically. Let me break it down:

---

### 1. **Customized or Vertical Agent Code**

This is your application’s unique “glue.” It defines:

* The **specialized logic** for your vertical (finance, healthcare, e-commerce, etc.).
* The **integration points** (APIs, databases, internal tools).
* The **workflow orchestration** (how the agent reacts step by step, what functions it calls, what state it keeps).

This is what differentiates your app from a generic chatbot.

---

### 2. **Original Logs / Data**

Your application’s **real data** is gold.

* Transaction logs, knowledge bases, user histories, product catalogs, etc.
* This is the source of truth that makes your agent contextually relevant and useful.

The more structured and trustworthy this data is, the stronger your application becomes.

---

### 3. **Prompt and Context**

This is where you tell the model:

* **How to think**: rules, tone, guardrails, task-specific instructions.
* **What to see**: injecting relevant context (from logs, user query, memory, or retrieval).

Prompts are the “interface” between the raw model and your customized code/data.

---

### 4. **Everything Else Can Be Generated**

UI scaffolding, boilerplate templates, summaries, natural-language expansions, even parts of the integration code — these can often be generated automatically or semi-automatically. The differentiators (logic, data, prompt/context design) are the parts you can’t outsource to generation alone.

---

👉 So your summary is on point:
The **essentials** are (1) your agent logic/code, (2) your real logs/data, and (3) the prompt/context shaping. The rest (like response formatting, helper text, or generic flows) can indeed be generated.

---

Would you like me to sketch a **minimal stack diagram** that shows these layers visually (essential vs. generatable)? That might make the separation clearer.
