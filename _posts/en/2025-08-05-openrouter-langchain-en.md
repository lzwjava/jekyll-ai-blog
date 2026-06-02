---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use OpenRouter with LangChain
translated: false
type: note
---

You can point LangChain at OpenRouter by specifying its base URL and your OpenRouter key when you instantiate the LLM. For example:

```python
import os
from langchain import OpenAI, LLMChain, PromptTemplate

# 1. (Optionally) set your OpenRouter key in env
os.environ["OPENAI_API_KEY"] = "pk-OPENROUTER_YOUR_KEY_HERE"
# and the base URL:
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# 2. Initialize the LLM to use OpenRouter
llm = OpenAI(
    model_name="gpt-4o",                # or "gpt-3.5-turbo" etc.
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_type="open_router"       # tell LangChain it’s OpenRouter
)

# 3. Create your prompt template
template = PromptTemplate(
    input_variables=["product"],
    template="Write a short marketing blurb for the product: {product}."
)

# 4. Build and run the chain
chain = LLMChain(llm=llm, prompt=template)
result = chain.run({"product": "wireless noise-cancelling headphones"})
print(result)
```

**Key points**

* **`openai_api_base`** must point to OpenRouter’s API endpoint.
* **`openai_api_type="open_router"`** tells LangChain to speak OpenRouter’s protocol.
* Supply your OpenRouter key via `openai_api_key` (or `OPENAI_API_KEY` env).

That will replace the default OpenAI.com endpoint with OpenRouter.
