---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: LLMs, Code Reasoning, and Tool Use
translated: false
type: note
---

Great question! You're essentially asking how something like **Anthropic's Claude (and similar LLMs)** internally handles:

1. **Code execution or code-related reasoning**
2. **JSON schema checking/structured output validation**
3. **Tool-use and routing between tools**

Let me break it down in detail.

---

### 1. Code reasoning & execution
Claude (and other frontier LLMs) don’t actually *execute* code directly inside the model—they **simulate code reasoning** by predicting tokens of code or logic steps.

- In **normal text mode**, Claude can "write" code by continuing a pattern, but it doesn’t internally run it.
- When used with a **backend (like Anthropic’s Workbench, or OpenAI’s Code Interpreter)**, the system can catch those code snippets and then actually *run* them in a sandboxed environment.
- The results can then be fed back to the model as context, so it can chain reasoning like:
  → Generate code → Execute externally → Receive output → Decide next step.

So the intelligence is in the loop: LLM generates → external runner executes → LLM interprets results.

---

### 2. JSON schema checking
Many APIs (Claude, OpenAI, etc) now support **structured output mode**, where you can attach a JSON schema. Here’s how it works internally:

- You pass a **JSON schema definition** with your request.
- The LLM is guided to output **only valid JSON** that conforms.
- If it tries to output invalid JSON, the system detects it (using a validator like [jsonschema](https://pypi.org/project/jsonschema/)) and asks the model to “repair” the output.
- Under the hood, this is often a **constrained decoding** or **grammar-based decoding** mechanism—basically, restricting token generation so only `"valid next tokens in the schema"` are allowed.

This ensures the output is syntactically and semantically correct JSON, which is critical for tool-use automation.

---

### 3. Tool-use & routing
Tool-use is handled via something like a **router layer** between the LLM and a tool execution environment:

- **Routing logic**: The model is prompted to *decide which tool to call* (or to respond directly).
- **Schema enforcement**: Each tool has an input schema. The LLM is required to produce valid JSON for that tool.
- **Execution adapters**: The orchestration layer (outside the model) takes the LLM’s JSON, validates against schema, executes the tool, and then feeds results back as context.
- **Chained reasoning (ReAct-style)**: The LLM “thinks aloud” (might produce reasoning steps hidden from user), then issues tool calls when necessary, progressively arriving at a final answer.

For example:
```json
{
  "tool": "web_search",
  "query": "latest research on quantum error correction"
}
```
→ Router sees `"tool": "web_search"`, validates schema, runs web search, puts results back into model’s context, and the model continues reasoning.

Anthropic’s Claude, OpenAI’s GPTs, LangChain, and others all support this pattern.

---

### 🔑 Summary
- **Claude code**: Doesn’t run code internally; generates code → sandbox executes → results returned → iterative reasoning.
- **JSON schema checking**: Uses constrained decoding / schema validation to ensure valid structured output.
- **Tool use routing**: LLM selects tool calls in JSON, orchestration engine validates & executes them, feeds results back in loop.

---

👉 Would you like me to **draw a diagram** showing the flow (LLM ↔ tool router ↔ schema validator ↔ execution engine) so it’s clearer visually?
