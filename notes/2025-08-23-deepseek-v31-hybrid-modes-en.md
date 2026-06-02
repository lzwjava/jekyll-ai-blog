---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V3.1 Hybrid Modes Explained
translated: false
type: note
---

Here’s how the **DeepSeek V3.1 API** handles its new hybrid inference architecture (“Think” vs “Non‑Think” modes):

---

### API Changes Overview

#### 1. **Two Distinct Endpoints (Modes)**

* **`deepseek-chat`** corresponds to **Non‑Thinking mode**—optimized for quick responses.
* **`deepseek-reasoner`** corresponds to **Thinking mode**—built for more deliberate, multi-step reasoning tasks.
  Both endpoints now operate on the same V3.1 model with a 128K token context window. ([DeepSeek API Docs][1], [Data Science Dojo][2])

#### 2. **Expanded Context Support**

* Both modes support the extended 128K token context, which is a major upgrade allowing handling of very long inputs. ([DeepSeek API Docs][1], [Hugging Face][3])

#### 3. **Improved Format & Capabilities**

* **Anthropic API compatibility** is now supported, making it easier to integrate DeepSeek with Anthropic-style client libraries. ([DeepSeek API Docs][1])
* **Strict Function Calling** is supported (in beta), allowing more robust and validated tool invocation through the API. ([DeepSeek API Docs][1])

#### 4. **UI Toggle vs API Invocation**

* On their web UI (“DeepThink” button), users can switch between modes interactively.
* In the **API**, you must explicitly choose the mode by setting the `model` parameter to either `"deepseek-chat"` (for non‑thinking) or `"deepseek-reasoner"` (for thinking). ([DeepSeek API Docs][1])

#### 5. **Other Enhancements**

* **More API resources** and an overall smoother developer experience have been introduced. ([DeepSeek API Docs][1])
* The underlying tokenizer and chat templates have been updated to support mode-based behavior (e.g., inserting `<think>` and `</think>` tokens appropriately). ([Hugging Face][3])

---

### Summary: What's Changed — Without a Table

* **New naming**:

  * `deepseek-chat` → Non‑Thinking mode
  * `deepseek-reasoner` → Thinking mode

* **Shared architecture**: Both are built on the same 671B-parameter model with a long 128K-token context window.

* **Enhanced integration options**:

  * Supports Anthropic-style APIs.
  * Offers strict function calling (beta), enabling safer, schema-based tool interactions.

* **Template updates**: The API now uses special tokens (`<think>`, `</think>`) in prompts to differentiate modes, and has revamped the chat templating logic.

* **Developer experience**: The platform includes more resources, updated docs, and a smoother integration process overall.

---

### Example Usage (Python/HTTP)

**Non-Thinking (fast responses):**

```python
import openai  # or DeepSeek-compatible SDK
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role":"user","content":"Tell me a joke."}],
)
```

**Thinking (deeper reasoning):**

```python
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[{"role":"user","content":"Explain why the sky is blue."}],
)
```

**Function Calling (strict mode, beta):**
You can define functions (tools) with JSON schemas and let the model invoke them, receiving structured calls you can execute and feed back—great for building autonomous agents. ([DeepSeek API Docs][1], [Reddit][4], [apidog][5])

---

Let me know if you'd like help crafting prompts for tool use, optimizing for cost or speed, or exploring the Anthropic-compatible interface in more detail!

[1]: https://api-docs.deepseek.com/news/news250821?utm_source=chatgpt.com "DeepSeek-V3.1 Release"
[2]: https://datasciencedojo.com/blog/deep-seek-v3-1/?utm_source=chatgpt.com "Deep Seek v3.1: The Next Leap in Open-Source Large ..."
[3]: https://huggingface.co/deepseek-ai/DeepSeek-V3.1?utm_source=chatgpt.com "deepseek-ai/DeepSeek-V3.1"
[4]: https://www.reddit.com/r/LocalLLaMA/comments/1munvj6/the_new_design_in_deepseek_v31/?utm_source=chatgpt.com "The new design in DeepSeek V3.1 : r/LocalLLaMA"
[5]: https://apidog.com/blog/deepseek-v3-1-api/?utm_source=chatgpt.com "How to Use DeepSeek-V3.1 API ?"
