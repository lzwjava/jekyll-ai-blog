---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用OpenRouter与LangChain
translated: true
type: note
---

你可以通过指定基础URL和你的OpenRouter密钥，在实例化LLM时将LangChain指向OpenRouter。例如：

```python
import os
from langchain import OpenAI, LLMChain, PromptTemplate

# 1. （可选）在环境变量中设置OpenRouter密钥
os.environ["OPENAI_API_KEY"] = "pk-OPENROUTER_YOUR_KEY_HERE"
# 以及基础URL：
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# 2. 初始化使用OpenRouter的LLM
llm = OpenAI(
    model_name="gpt-4o",                # 或 "gpt-3.5-turbo" 等
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_type="open_router"       # 告知LangChain使用OpenRouter协议
)

# 3. 创建提示模板
template = PromptTemplate(
    input_variables=["product"],
    template="为以下产品撰写简短营销文案：{product}。"
)

# 4. 构建并运行链式调用
chain = LLMChain(llm=llm, prompt=template)
result = chain.run({"product": "无线降噪耳机"})
print(result)
```

**关键要点**

* **`openai_api_base`** 必须指向OpenRouter的API端点
* **`openai_api_type="open_router"`** 告知LangChain使用OpenRouter协议
* 通过`openai_api_key`参数（或`OPENAI_API_KEY`环境变量）提供你的OpenRouter密钥

这将用OpenRouter替换默认的OpenAI.com端点。
