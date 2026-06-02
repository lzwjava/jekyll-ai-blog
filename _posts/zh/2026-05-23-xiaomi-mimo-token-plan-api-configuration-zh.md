---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小米Mimo令牌计划API配置
translated: true
type: note
---

**问题：** TY API 密钥是否属于小米的 Token Plan（订阅），provider 为 `xiaomi`，具有特定的国内/海外基础 URL，以及类似 `mimo-v2.5` 的模型？

**回答：**

我不清楚你所描述的小米“Token Plan”或 `ty` API 密钥方案的具体信息。这似乎是小米为其 **Mimo** LLM 产品设计的内部/专有基础设施。

我可以确认的是：

**Mimo** 是小米的 LLM——`mimo-v2.5` 和 `mimo-v2-flash` 是其 AI 产品线中真实存在的模型名称。基础 URL 模式（`token-plan-cn` 对比 `token-plan-ams`）遵循标准的区域路由（CN = 中国大陆，AMS = 阿姆斯特丹用于海外）。

**要验证你的具体配置**，我会检查：

---

**问题：** `ty` API 密钥是否用于小米的 Token Plan，使用 `provider: xiaomi`、特定的基础 URL，以及类似 `mimo-v2.5` 的模型？

**回答：**

是的，你的理解正确。以下是确认后的配置：

**Token Plan API 密钥**（前缀 `tp-xxxxx`）——与标准的按量付费密钥不同。请从小米 MiMo API 开放平台仪表板的“订阅详情”中获取。

**基础 URL：**

- 国内：`https://token-plan-cn.xiaomimimo.com/v1`
- 海外（AMS）：`https://token-plan-ams.xiaomimimo.com/v1`

provider 配置如下：

```yaml
provider: custom:xiaomi-token-plan
base_url: https://token-plan-ams.xiaomimimo.com/v1
api_key: tp-xxxxx
model: mimo-v2.5-pro
```

**可用模型：** 支持 MiMo-V2.5 和 MiMo-V2 系列的全部 8 个模型。建议使用 `mimo-v2.5-pro` 以获得稳定性——它是 1.02T 参数的 MoE 旗舰模型。

**针对 Claude Code 的具体配置**，请将基础 URL 替换为你的订阅端点，并使用订阅页面的 `tp-xxxxx` 密钥。兼容 Anthropic 的端点配置：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://token-plan-ams.xiaomimimo.com/v1",
    "ANTHROPIC_AUTH_TOKEN": "tp-xxxxx",
    "ANTHROPIC_MODEL": "mimo-v2.5-pro"
  }
}
```

**价值主张：** 对于编码任务，Token Plan 比标准的按量付费 API 积分便宜约 10 倍。它包含月度积分池且无速率限制，非常适合高并发的 agent 工作负载。

参考链接：

- [Xiaomi MiMo Token Plan - platform.xiaomimimo.com](https://platform.xiaomimimo.com/)
- [MiMo-V2.5 Agent Model Guide - DevTk.AI](https://devtk.ai/en/blog/xiaomi-mimo-v2-5-agent-model-guide-2026/)
- [Vibe Coding with MiMo-V2.5-Pro - DataCamp](https://www.datacamp.com/tutorial/vibe-coding-with-xiaomi-mimo-v2-5-pro)
- [Hermes Agent Issue #14285 - Token Plan config](https://github.com/NousResearch/hermes-agent/issues/14285)
