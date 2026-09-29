---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于令牌的AI咨询计费
translated: true
type: note
---

**问题：有没有人做软件咨询，按 token 用量收费，一个项目对应一个客户 API key？**

有的。这种模式正在兴起，尤其是**为 LLM agent、RAG 系统、自动化工作流和内部 copilot 提供服务的 AI 工程咨询公司**。它还不是传统软件咨询的主流模式，但这种模式是真实存在的：**按客户/项目计量 AI 消耗，并转嫁或加价 token 成本**。（[OneBill][1]）

常见架构如下：

```
Client A
  |
  | API key / project key
  v
Your AI Gateway
  |
  +--> OpenAI / Anthropic / Gemini / self-hosted models
  |
  +--> Usage ledger
        - input tokens
        - output tokens
        - model
        - tool calls
        - embeddings
        - GPU seconds
        - cost
        - markup
```

然后开具账单：

```
Client A
January usage:

GPT-5:
  input tokens:   120M
  output tokens:   15M
  cost:            $850

Agent platform fee: $2,000

AI usage markup (30%): $255

Total: $3,105
```

### 这种模式的现有案例

1. **AI 代理公司 / AI 自动化咨询公司**

许多公司正在从：

```
$20k fixed project
```

转向：

```
$5k setup
+
$500/month platform
+
usage
```

因为客户的 AI 工作负载在部署完成后仍在持续运行。

2. **AI SaaS 基础设施公司**

构建 AI 计费基础设施的公司明确支持这种模式：计量 token、API 调用、agent 操作，并将其转化为账单。（[GitHub][2]）

3. **Agent 平台**

一些 agent 框架已经实现了：

```
project -> usage -> invoice
```

支持按项目跟踪 token 和客户端账单导出。（[Pepe Agent][3]）

---

对于咨询公司而言，我实际上建议不要向客户提供你的原始 OpenAI/Anthropic key。

更好的做法：

```
client-api-key
       |
       v
your gateway
       |
       +-- project_id=acme
       +-- budget_limit=$1000/mo
       +-- allowed_models=[...]
       +-- logging
       +-- invoice events
```

最小化实现示例：

```python
from openai import OpenAI

client = OpenAI(
    api_key="<YOUR_MASTER_KEY>"
)

def chat(project, messages):
    r = client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )

    usage = r.usage

    ledger.append({
        "project": project,
        "input": usage.prompt_tokens,
        "output": usage.completion_tokens,
        "model": "gpt-5"
    })

    return r
```

数据库：

```sql
CREATE TABLE usage_events (
    project_id TEXT,
    model TEXT,
    input_tokens INT,
    output_tokens INT,
    created_at TIMESTAMP
);
```

然后：

```sql
SELECT
 project_id,
 SUM(input_tokens),
 SUM(output_tokens)
FROM usage_events
GROUP BY project_id;
```

---

真正有意思的商业模式不是纯 token 转售。纯 token 加价的利润率很低。

更强的模式是：

```
Consulting retainer
        +
AI platform fee
        +
token pass-through
        +
outcome fee
```

示例：

* 每月 $5k 的 AI 工程顾问服务费
* 每月 $500 的托管/平台费
* LLM 成本 + 20% 加价
* 每个自动化工作流完成可选 $50

这更接近云公司的演变路径：AWS 不只是卖服务器，它卖的是计量基础设施加更高级别的服务。

几年后，"AI 工程师"咨询公司可能会看起来更像小型托管式 AI 基础设施提供商，而不是传统的软件承包商。

如果有需要，我还可以为**多客户 AI 咨询计费网关**（类似 Stripe metering + OpenRouter proxy + Langfuse 的组合）绘制一份生产级架构草图。

[1]: https://www.onebillsoftware.com/outcome-based-consumption-pricing-ai-agents/?utm_source=chatgpt.com "Outcome-Based Billing for AI Agents and GenAI Platforms | OneBill"
[2]: https://github.com/getlago/lago?utm_source=chatgpt.com "GitHub - getlago/lago: Open Source Metering and Usage Based Billing API ⭐️ Consumption tracking, Subscription management, Pricing iterations, Payment orchestration & Revenue analytics · GitHub"
[3]: https://pepe-agent.com/en/docs/billing/?utm_source=chatgpt.com "Billing & limits · Pepe docs"
