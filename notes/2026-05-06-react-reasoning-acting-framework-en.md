---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReAct Reasoning and Acting Framework
translated: false
type: note
---

**Question:** What is ReAct (in the context of LLMs and prompting)?

**Answer:**

## ReAct — Reasoning + Acting

**ReAct** is a prompting framework/paradigm for Large Language Models (LLMs), introduced in a 2022 paper by Yao et al. The name is a portmanteau of **"Reasoning"** and **"Acting"**.

---

### The Core Problem ReAct Solves

Before ReAct, two capabilities of LLMs were studied separately:

- **Reasoning** — e.g., Chain-of-Thought (CoT) prompting, where the model thinks step by step
- **Acting** — e.g., using tools, searching the web, calling APIs

Chain-of-thought and action plan generation had primarily been studied as separate topics. ReAct explores using LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two.

---

### How ReAct Works

ReAct operates by intertwining reasoning and action within LLMs, allowing models to not only think through tasks but also act upon their conclusions in a dynamic, responsive manner. It prompts LLMs to generate reasoning traces — essentially a sequence of thoughts or logical steps — interwoven with task-specific actions. The model reasons through the implications of each step, executes the necessary action, observes the outcome, and then adjusts its reasoning based on this new information.

The loop looks like this:

```
Thought  →  Action  →  Observation  →  Thought  →  Action  →  ...
```

**Concrete example (from HuggingFace):**

```
Thought:  I need to find the latest weather in Paris.
Action:   Search["weather in Paris"]
Observation: It's 18°C and cloudy.
Thought:  Now that I know the weather...
Action:   Finish["It's 18°C and cloudy in Paris."]
```

---

### Why ReAct Is Better than CoT Alone

CoT prompting's lack of access to the external world or inability to update its knowledge can lead to issues like fact hallucination and error propagation. ReAct allows the system to perform dynamic reasoning while also enabling interaction with external sources such as knowledge bases or environments, leading to more reliable and factual responses.

In short:

- **CoT** = thinks deeply, but only from internal knowledge → can hallucinate
- **ReAct** = thinks + fetches real information from tools → more grounded and accurate

---

### Why It Matters Today (Connection to AI Agents)

Rather than implementing rule-based or otherwise predefined workflows, ReAct agents rely on their LLM's reasoning capabilities to dynamically adjust their approach based on new information or the results of previous steps.

This is why ReAct is considered the foundation of modern **AI agent** systems — tools like LangChain, AutoGPT, and Claude's tool-use all implement a ReAct-style loop under the hood.

---

### Comparison: CoT vs ToT vs ReAct

| Technique | What it does | Limitation |
|---|---|---|
| **CoT** | Step-by-step reasoning in one pass | No external tools, can hallucinate |
| **ToT** (Tree of Thoughts) | Explores multiple reasoning branches | Complex, limited real-world use |
| **ReAct** | Reasoning + real-world tool actions in a loop | Current gold standard for agents |

---

**In short:** ReAct is the reason modern AI assistants can search the web, run code, query databases, and still "think" about what to do next — all in one unified loop.

**References:**

- [ReAct Paper (arxiv)](https://arxiv.org/abs/2210.03629)
- [ReAct Project Page](https://react-lm.github.io/)
- [Prompt Engineering Guide — ReAct](https://www.promptingguide.ai/techniques/react)
- [HuggingFace Agents Course — ReAct](https://huggingface.co/learn/agents-course/unit1/thoughts)
