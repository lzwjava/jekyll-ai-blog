---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V3.1混合模式详解
translated: true
type: note
---

以下是 **DeepSeek V3.1 API** 处理其新型混合推理架构（“思考”与“非思考”模式）的方式：

---

### API 变更概览

#### 1. **两个独立的端点（模式）**

* **`deepseek-chat`** 对应 **非思考模式**——专为快速响应优化。
* **`deepseek-reasoner`** 对应 **思考模式**——专为需要更审慎、多步骤推理的任务构建。
  两个端点现在都基于相同的 V3.1 模型运行，并具有 128K token 的上下文窗口。（[DeepSeek API 文档][1], [Data Science Dojo][2]）

#### 2. **扩展的上下文支持**

* 两种模式均支持扩展的 128K token 上下文，这是一个重大升级，允许处理非常长的输入。（[DeepSeek API 文档][1], [Hugging Face][3]）

#### 3. **改进的格式与能力**

* 现在支持 **Anthropic API 兼容性**，使得将 DeepSeek 与 Anthropic 风格的客户端库集成更加容易。（[DeepSeek API 文档][1]）
* 支持**严格的函数调用**（测试版），允许通过 API 进行更强大且经过验证的工具调用。（[DeepSeek API 文档][1]）

#### 4. **UI 切换与 API 调用**

* 在其 Web UI 上（“DeepThink”按钮），用户可以交互式地切换模式。
* 在 **API** 中，您必须通过将 `model` 参数设置为 `"deepseek-chat"`（非思考模式）或 `"deepseek-reasoner"`（思考模式）来明确选择模式。（[DeepSeek API 文档][1]）

#### 5. **其他增强功能**

* 引入了**更多的 API 资源**和整体上更流畅的开发者体验。（[DeepSeek API 文档][1]）
* 底层的分词器和聊天模板已更新，以支持基于模式的行为（例如，适当地插入 `` token）。（[Hugging Face][3]）

---

### 总结：变更内容 — 无表格版

* **新命名**：
  * `deepseek-chat` → 非思考模式
  * `deepseek-reasoner` → 思考模式

* **共享架构**：两者都构建在相同的 671B 参数模型之上，并具有 128K token 的长上下文窗口。

* **增强的集成选项**：
  * 支持 Anthropic 风格的 API。
  * 提供严格的函数调用（测试版），支持基于模式的、更安全的工具交互。

* **模板更新**：API 现在在提示中使用特殊 token（``）来区分模式，并改进了聊天模板逻辑。

* **开发者体验**：平台提供了更多资源、更新的文档以及整体上更流畅的集成过程。

---

### 使用示例 (Python/HTTP)

**非思考模式（快速响应）：**

```python
import openai  # 或兼容的 DeepSeek SDK
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role":"user","content":"给我讲个笑话。"}],
)
```

**思考模式（深度推理）：**

```python
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[{"role":"user","content":"解释一下为什么天空是蓝色的。"}],
)
```

**函数调用（严格模式，测试版）：**
您可以定义带有 JSON 模式的函数（工具），让模型调用它们，接收结构化的调用请求，您可以执行并反馈结果——这对于构建自主代理非常有用。（[DeepSeek API 文档][1], [Reddit][4], [apidog][5]）

---

如果您需要帮助来设计工具使用的提示、优化成本或速度，或者探索 Anthropic 兼容接口的更多细节，请告诉我！

[1]: https://api-docs.deepseek.com/news/news250821?utm_source=chatgpt.com "DeepSeek-V3.1 Release"
[2]: https://datasciencedojo.com/blog/deep-seek-v3-1/?utm_source=chatgpt.com "Deep Seek v3.1: The Next Leap in Open-Source Large ..."
[3]: https://huggingface.co/deepseek-ai/DeepSeek-V3.1?utm_source=chatgpt.com "deepseek-ai/DeepSeek-V3.1"
[4]: https://www.reddit.com/r/LocalLLaMA/comments/1munvj6/the_new_design_in_deepseek_v31/?utm_source=chatgpt.com "The new design in DeepSeek V3.1 : r/LocalLLaMA"
[5]: https://apidog.com/blog/deepseek-v3-1-api/?utm_source=chatgpt.com "How to Use DeepSeek-V3.1 API ?"
