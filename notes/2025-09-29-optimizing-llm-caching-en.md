---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Optimizing LLM Caching Through Prompt Structure
translated: false
type: note
---

Got it! Let me translate and explain your ideas clearly in English:

---

As large language models consume more and more tokens, caching becomes increasingly important to reduce costs. Manus (a company/tool you mentioned) brought up one optimization: fixing the JSON serialization order so that repeated requests can be cached more effectively.

I just thought of another idea: when constructing prompts or context, it’s best to put the variables or dynamic content **at the end**. This way, the earlier parts remain stable and can hit the cache more consistently.

Of course, for individual users with relatively low usage, this optimization doesn’t matter much. But for companies offering copilots (where users pay a flat subscription fee per month), the backend provider (like Manus, Claude, Code, or Cursor) needs strong caching technology in order to control costs at scale.

---

✅ So yes, your reasoning is correct:
- **Stable ordering** → better cache hits.
- **Dynamic content at the end** → preserves the longer reusable prefix.
- **High-volume services (copilot-style)** benefit much more from this optimization than individual low-usage users.

---

👉 Do you want me to also explain some **practical caching strategies** that companies actually use with LLMs?
