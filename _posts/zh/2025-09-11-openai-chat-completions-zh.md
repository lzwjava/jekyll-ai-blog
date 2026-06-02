---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 使用OpenAI聊天补全模型
translated: true
type: note
---

你链接的是微软学习文章《使用聊天补全模型》（发布于 **2025 年 9 月 1 日**）。以下是其核心要点的清晰概述：

---

### 关键亮点

* **面向对话的模型**
  新一代聊天模型与早期 GPT-3 模型不同。它们采用 **对话输入-消息输出** 模式，而非“文本输入-文本输出”。输入内容需按对话记录的结构化格式组织（包含 *system*、*user*、*assistant* 等角色），模型则返回单条消息以延续对话 ([Microsoft Learn][1])。

* **专为对话设计**
  这种结构针对多轮往复对话进行了优化，同时也适用于单次提示场景。对话式结构使得交互更为流畅 ([Microsoft Learn][1])。

* **切勿沿用旧模型的使用方式**
  这些聊天模型输出更详尽，若沿用 GPT-3 的使用方式，往往无法获得理想效果。建议使用新型聊天式交互界面以获得最佳体验 ([Microsoft Learn][1])。

* **示例代码片段**
  文章包含调用 Azure 聊天补全 API 的基础代码示例（采用 Python 风格语法）：

  ```python
  from openai import OpenAI
  import os

  client = OpenAI(
      api_key=os.getenv("AZURE_OPENAI_API_KEY"),
      base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
  )

  response = client.chat.completions.create(
      model="gpt-4o",  # 或 deployment_name
      messages=[
          {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
          {"role": "user", "content": "Who were the founders of Microsoft?"}
      ]
  )

  print(response.model_dump_json(indent=2))
  print(response.choices[0].message.content)
  ```

  该示例展示了如何正确发送带角色区分的消息并获取模型回复 ([Microsoft Learn][1])。

---

### 核心价值

1. **增强对话上下文理解** —— 聊天模型能更好地维持多轮对话的流程与语境连贯性。
2. **提升易用性** —— 通过角色划分（系统、用户、助手）可更清晰地设置指令、个性特征或约束条件。
3. **规避使用误区** —— 若将聊天模型视作前代产品使用会导致响应质量下降，请务必按设计规范使用聊天 API 接口。

---

如果需要协助理解代码示例、适配您的开发环境或探索相关指南，我随时可以提供支持！

根据你的偏好，本文档保持了简洁易读的格式，未使用表格。

[1]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/chatgpt?utm_source=chatgpt.com "Work with chat completion models - Azure OpenAI in ..."
