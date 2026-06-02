---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Working with OpenAI Chat Completions Models
translated: false
type: note
---

You’ve linked to the Microsoft Learn article **“Work with chat completions models”** (published on **September 1, 2025**). Here’s a clear and concise summary of its core points:

---

### Key Highlights

* **Chat-oriented models**
  The newer chat models differ from earlier GPT-3 models. Instead of "text-in, text-out," they use a **conversation-in, message-out** format. Essentially, input is structured like a transcript (roles like *system*, *user*, *assistant*), and the model returns one message to continue the conversation ([Microsoft Learn][1]).

* **Designed for dialogue**
  This structure is optimized for multi-turn back-and-forth conversations. It also works well for single-prompt scenarios, but the conversational format enables smoother interactions ([Microsoft Learn][1]).

* **Don’t treat them like older models**
  These chat models are more verbose and often produce less useful answers if you approach them like GPT-3. It's recommended to use the new chat-style interface for best results ([Microsoft Learn][1]).

* **Sample code snippet**
  The article includes a basic code sample using Python-style syntax for calling Azure’s chat completions API:

  ```python
  from openai import OpenAI
  import os

  client = OpenAI(
      api_key=os.getenv("AZURE_OPENAI_API_KEY"),
      base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
  )

  response = client.chat.completions.create(
      model="gpt-4o",  # or deployment_name
      messages=[
          {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
          {"role": "user", "content": "Who were the founders of Microsoft?"}
      ]
  )

  print(response.model_dump_json(indent=2))
  print(response.choices[0].message.content)
  ```

  That shows how to properly send messages (with role separation) and retrieve the model’s answer ([Microsoft Learn][1]).

---

### Why It Matters

1. **Enhanced conversational context** — Chat models better maintain the flow and context across multi-turn interactions.
2. **Improved usability** — Using roles (system, user, assistant) allows for clearer instructions, personality setting, or constraints.
3. **Avoid pitfalls** — Treating chat models like previous-generation ones can lead to poor response quality; use the chat API interface as intended.

---

Let me know if you'd like help walking through the code sample, adapting it to your setup, or exploring related guides—happy to dive in!

And as per your preference, I kept this in a simple, readable format without tables.

[1]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/chatgpt?utm_source=chatgpt.com "Work with chat completion models - Azure OpenAI in ..."
