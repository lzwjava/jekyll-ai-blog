---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tool Use vs Function Calling Explained
translated: false
type: note
---

Let’s break down the difference between **tool use** and **function calling** in the context of LLM APIs:

---

## 1. Tool Use

* **Concept**: Tool use is a broad idea where the LLM is augmented with external capabilities. Instead of just generating text, it can "use a tool" to fetch information, run code, query a database, or generate an image.
* **Implementation**: In practice, "tools" are external APIs or systems registered with the LLM runtime (e.g., a search API, Python execution environment, or a calendar API).
* **LLM’s Role**: The model decides when to call the tool, with what arguments, and integrates the results back into the conversation.
* **Example**:

  * User: "What’s the weather in Guangzhou?"
  * LLM: Calls the `weather` tool with `{city: "Guangzhou"}` → gets `28°C, sunny`.
  * LLM: Replies, "It’s 28°C and sunny."

Think of **tool use** as a general orchestration framework where the LLM doesn’t just answer with words—it coordinates actions with external systems.

---

## 2. Function Calling

* **Concept**: Function calling is a *structured* mechanism provided by some LLM APIs (like OpenAI, Anthropic, etc.), where you define functions (with names, parameters, schemas), and the LLM can return JSON arguments to call them.
* **Implementation**: You provide the model with JSON schemas describing the functions. The model’s output is then either text or a structured function call object.
* **LLM’s Role**: Instead of “hallucinating” API usage, the model outputs valid structured arguments for predefined functions.
* **Example**:

  * You define a function:

    ```json
    {
      "name": "getWeather",
      "description": "Get current weather",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        },
        "required": ["city"]
      }
    }
    ```
  * User: "What’s the weather in Guangzhou?"
  * LLM: Outputs → `{ "name": "getWeather", "arguments": {"city": "Guangzhou"} }`
  * Your system executes the function and passes results back.

This makes **function calling** a specific, safe, schema-driven way to do **tool use**.

---

## 3. Key Differences

* **Scope**:

  * Tool use = general concept (LLM augmented with external systems).
  * Function calling = one standardized API design for structured calls.
* **Control**:

  * Tool use may be more free-form (LLM decides and formats).
  * Function calling enforces strict schemas, reducing ambiguity and hallucination.
* **Interoperability**:

  * Tool use can involve many external systems (search, code execution, image generation).
  * Function calling is best when you want precise, structured arguments (like APIs or database queries).

---

## 4. Mental Model

* Function calling is a **subset** of tool use.
* If tool use is the *general strategy*, function calling is the *safe, structured method* most APIs expose.

---

Would you like me to also show a **side-by-side workflow example** (like user prompt → LLM output → execution) to illustrate the difference more concretely?
