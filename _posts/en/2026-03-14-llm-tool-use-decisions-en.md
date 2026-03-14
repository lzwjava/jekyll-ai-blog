---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Tool Use Decisions Explained
translated: false
type: note
---

**Question:** What is the LLM API feature called where the LLM decides whether or not to call a tool? Is this decision baked into the model through pre-training or through RLHF, and is the LLM actually good at making this decision?

---

**Answer:**

## What is This Feature Called?

The feature you're describing is called **Tool Calling** (also called **Function Calling**). It is a core capability of modern LLM APIs (OpenAI, Anthropic, Google, etc.) that allows a model to autonomously decide whether an external function/tool needs to be invoked, and if so, generate a structured call for it with the correct arguments.

Tool calling is the mechanism by which an LLM can invoke an external function or service to complete a task. Instead of hallucinating a response, the model passes specific requests to external tools — like sending a math problem to a calculator, checking a weather API for the forecast, or querying a database for customer details.

---

## How Does the "Decision" Work at Runtime?

When you send a request to the LLM API, you include a list of available tool definitions (name, description, JSON schema of parameters). The model reads these alongside the user's message, and then decides:

- **Yes, I need a tool** → it outputs a structured JSON tool call (not plain text)
- **No, I can answer directly** → it outputs a normal text response

The decision is still probabilistic — you shape it with prompts, schema, and `tool_choice`, but you don't program it like a deterministic rules engine.

You can also force specific behavior via the API's `tool_choice` parameter:
- **`auto`** — model decides on its own (most common)
- **`required`** — force the model to always call a tool
- **`none`** — forbid tool calls entirely
- **specific tool name** — force it to call a specific tool

---

## Is This Capability From Pre-Training or RLHF?

The answer is **both**, applied in layers. This is a multi-stage training process:

### 1. Pre-training (Base Knowledge)
During pre-training on massive text corpora, the model learns general reasoning, language patterns, and intent recognition. The LLM develops a deep understanding of language patterns, semantic relationships, and intent. When it encounters tool definitions, it learns to associate specific patterns in user queries with the functionalities described by the tool. This isn't explicit programming but rather an association learned from the training data.

### 2. Supervised Fine-Tuning (SFT) — The Main Mechanism
The primary way tool-calling is taught is through **SFT on tool-use trajectories** (examples of correct tool-calling behavior). Most modern tool-use corpora are synthetic or bootstrapped — Toolformer-style self-labeling or large-scale generation as in ToolBench. For training objectives, supervised fine-tuning (SFT) on tool trajectories teaches basic formatting and tool selection. This bootstraps the behavior and is often enough for establishing the foundation of the skill.

### 3. Preference Optimization (DPO / RLHF) — Refinement
After SFT, RLHF or DPO is used to refine *when* to call a tool vs. answer directly. Preference optimization (e.g., DPO) over trajectories can improve decisions about when to call a tool versus answer directly. For agentic tasks with multi-step tool use, RL with environment feedback (task success, constraint satisfaction) becomes the natural objective — the model learns from whether its tool-augmented actions actually solved the problem.

So the full pipeline looks like:

```
Pre-training → SFT on tool trajectories → DPO/RLHF for when-to-call decisions → RL from environment outcomes (for agents)
```

---

## Is the LLM Actually Good at This Decision?

**Generally yes, but not perfectly.** Here's a nuanced breakdown:

**The model is good at:**
- Recognizing obvious tool-needing queries (e.g., "what's the weather now?", "search for X")
- Selecting the right tool when tool descriptions are clear and well-named
- Formatting arguments correctly based on JSON schemas

**The model can struggle with:**
- Ambiguous cases where tool use is optional
- Choosing between multiple similar tools
- Knowing when *not* to call a tool (over-calling)
- Poor tool descriptions lead to bad decisions

Adding explicit guidance in the system prompt about when and how to use tools provides additional context. This may seem repetitive, but it helps the LLM make better decisions, especially with multiple tools.

Some models, especially reasoning models, are better at deciding when and how to call tools.

**Key insight:** The quality of your tool *descriptions* and *system prompt guidance* dramatically affects decision quality — it's a collaboration between training and runtime prompting.

---

## Summary Table

| Stage | Role in Tool Calling |
|---|---|
| Pre-training | Learns language, reasoning, semantic intent |
| SFT | Learns tool call format and basic selection |
| DPO/RLHF | Learns *when* to call vs. answer directly |
| RL (agentic) | Learns multi-step decision-making from outcomes |
| Runtime prompting | Shapes decisions further with descriptions & system prompt |

---

**References:**

- [What is LLM Tool Calling? — Portkey](https://portkey.ai/blog/what-is-llm-tool-calling/)
- [The Anatomy of Tool Calling in LLMs — martinuke0](https://martinuke0.github.io/posts/2026-01-07-the-anatomy-of-tool-calling-in-llms-a-deep-dive/)
- [How Tool Calling Works in LLMs — Scalable Thread](https://newsletter.scalablethread.com/p/how-tool-calling-works-in-llms)
- [Tool Use — RLHF Book by Nathan Lambert](https://rlhfbook.com/c/13-tools)
- [Function Calling — Prompt Engineering Guide](https://www.promptingguide.ai/agents/function-calling)