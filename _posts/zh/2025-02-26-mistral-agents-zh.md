---
audio: false
generated: true
lang: zh
layout: post
title: Mistral AI智能体
translated: true
type: note
---

Mistral AI 智能体是基于大型语言模型（LLMs）的自主系统，旨在根据高层级指令执行复杂任务。借助先进的自然语言处理技术，这些智能体能够理解并完成特定目标，适用于客户支持、数据分析、工作流自动化和编程辅助等多种应用场景。它们能够规划任务、使用工具、采取行动，甚至通过协作达成特定目标，提供全新水平的自动化与智能体验。

---

## 创建智能体

Mistral AI 提供两种创建智能体的主要方式：**La Plateforme 智能体构建器**与**智能体 API**。

### 1. La Plateforme 智能体构建器
智能体构建器提供用户友好的界面，无需深厚技术背景即可创建智能体。创建步骤：
- 访问智能体构建器 [https://console.mistral.ai/build/agents/new](https://console.mistral.ai/build/agents/new)
- 通过选择模型、设置温度参数及提供可选指令来自定义智能体
- 配置完成后，可通过 API 或 Le Chat 部署并访问该智能体

### 2. 智能体 API
面向开发者，智能体 API 支持以编程方式创建智能体并将其集成至现有工作流。以下是通过 API 创建和使用智能体的示例：

#### Python 示例
```python
import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

chat_response = client.agents.complete(
    agent_id="your-agent-id",
    messages=[{"role": "user", "content": "法国最优质的奶酪是什么？"}],
)
print(chat_response.choices[0].message.content)
```

#### JavaScript 示例
```javascript
import { Mistral } from '@mistralai/mistralai';

const apiKey = process.env.MISTRAL_API_KEY;
const client = new Mistral({ apiKey: apiKey });

const chatResponse = await client.agents.complete({
    agentId: "your-agent-id",
    messages: [{ role: 'user', content: '法国最优质的奶酪是什么？' }],
});
console.log('Chat:', chatResponse.choices[0].message.content);
```

---

## 自定义智能体

Mistral AI 智能体支持通过以下选项进行个性化定制：

- **模型选择**：选择驱动智能体的核心模型，可选类型包括：
  - "Mistral Large 2"（默认，`mistral-large-2407`）
  - "Mistral Nemo"（`open-mistral-nemo`）
  - "Codestral"（`codestral-2405`）
  - 微调模型

- **温度参数**：调整采样温度（范围 0.0-1.0）以控制响应随机性。较高值增强创造性，较低值则提升专注度与确定性。

- **指令设置**：通过可选指令规范所有交互中的特定行为。例如创建仅用法语交流或直接生成Python代码无需解释的智能体。

### 示例：创建法语专用智能体
构建仅用法语回应的智能体：
- 选择 "Mistral Large 2" 模型
- 设置指令："无论输入使用何种语言，始终用法语进行回应"
- 提供少量示例强化行为模式

---

## 应用场景

Mistral AI 智能体可应用于多行业与任务场景，典型用例包括：

- **客户支持**：自动响应常见咨询，处理高频问题，复杂情况转接人工客服
- **数据分析**：创建可分析数据集、生成报告或根据输入执行计算的智能体
- **工作流自动化**：集成邮件系统、客户关系管理或支付处理工具，实现重复任务自动化
- **编程辅助**：设计用于生成代码、提供调试建议或创建单元测试的智能体

### 具体示例
- **法语专用智能体**：针对法语客户群体定制的交流智能体
- **Python代码生成器**：直接输出简洁代码片段的无解释编程助手

---

## 部署方式

智能体创建后可通过两种途径部署使用：

- **API 集成**：通过 Mistral AI API 将智能体集成至应用程序（详见“创建智能体”章节代码示例）
- **Le Chat 平台**：在 Mistral 的 Le Chat 平台直接启用对话功能

智能体可在组织内便捷共享，结合 Mistral Large 2 等模型的先进推理能力，可构建涉及多智能体的复杂工作流。

---

本文档基于官方文档 [https://docs.mistral.ai/capabilities/agents/](https://docs.mistral.ai/capabilities/agents/) 提供关于 Mistral AI 智能体的理解、创建、定制与部署的完整指南。通过运用这些工具，您可实现任务自动化、提升生产效率，并解锁工作流效能的新维度。更多细节请参阅 [Mistral AI 官方文档](https://docs.mistral.ai/capabilities/agents/)。
