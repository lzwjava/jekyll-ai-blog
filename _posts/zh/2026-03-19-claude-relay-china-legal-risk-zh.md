---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 克劳德中继服务中国法律风险
translated: true
type: note
---

**问题：** 如果有人在中国运行这些 Claude relay 服务，会违反中国法律吗？

**回答：**

在中国运行 Claude API relay 服务（例如 claude-relay-service 或商业“中转站”代理）处于**法律灰色地带**。它**并未被明确刑事化**，如同欺诈或贩毒那样，数千此类服务在 Taobao、WeChat、Xianyu 和公开网站上公开运营，并支持国内 Alipay/WeChat Pay。然而，根据规模、运营方式以及是否采取适当合规步骤，它可能违反多项中国法规。以下是清晰的分解：

### 1. 主要潜在违规：Generative AI 服务管理规定

中国的**生成式人工智能服务管理暂行办法**（2023 年，由 CAC 执法）要求任何向中国公众提供生成式 AI（包括通过 relay 的外国模型）的提供商必须：

- 向 Cyberspace Administration of China (CAC) 备案/注册。
- 实施内容安全过滤，防止非法、有害或政治敏感输出。
- 标记 AI 生成内容并保留记录。
- 遵守“核心社会主义价值观”。

大多数小型个人或团体运营的 relay（例如托管在海外 VPS 上的 GitHub claude-relay-service）完全跳过此备案。大规模商业平台有时声称合规或利用漏洞（例如“仅用于研究”）。未注册可能导致罚款、服务关闭令或账户封锁，但对小型运营商的执法不一致。

### 2. 数据安全和跨境传输（PIPL 和 Data Security Law）

- 用户提示和输出被发送到 Anthropic 的美国服务器。
- 这属于向境外出口个人信息。
- 如果处理大量数据，必须进行安全评估或签署标准合同以进行跨境数据传输。
- 大多数 relay 未这样做 → 违反 Personal Information Protection Law (PIPL) 和 Cybersecurity Law 的技术违规。

### 3. 互联网服务许可

- 如果 relay 仪表板或 API 端点托管在大陆中国服务器上，需要 ICP 许可证（互联网信息服务增值电信业务经营许可证）。
- 大多数运营商托管在海外 VPS（美国、新加坡、香港）以规避此要求，这很常见，个人很少受罚。

### 4. VPN / 规避方面

- 终端用户使用或提供 VPN/proxy 访问本身**不违法**。
- 然而，为商业获利提供无许可 VPN 服务可能违反电信法规（但您的 Claude relay 不是通用 VPN；它是特定 API proxy）。

### 5. 现实实践（2026 年情况）

- 数百个 Claude relay 服务公开广告（“无需翻墙、直连 Claude、支付宝支付”）。
- 没有公开报道专门针对运行 Claude relay 的逮捕或起诉案例。
- 实际发生的风险：Anthropic 封禁主账户（特别是在其 2025 年政策阻止中国控制实体后）、支付平台冻结账户（如果被标记），或 CAC 发出下架通知（如果服务传播敏感内容）。
- 政府部门和银行现在被限制使用外国 AI proxy，但私人和小企业面临低执法力度。

**底线**
对于单人或小团体在海外服务器上自托管 claude-relay-service 并与朋友或少数付费用户分享 → **中国当局法律风险非常低**（主要是 Anthropic ToS 和账户封禁风险）。
对于面向数千用户的公开商业服务，未经 CAC 备案或数据出口合规 → **技术上违反法规**，如果被举报或规模过大，可能面临罚款或关闭。

大多数中国运营商将其视为灰色地带业务并接受风险，类似于 ChatGPT/GPT proxy 多年来运营的方式。如果计划商业运营，请始终咨询中国律师以评估您的具体设置。

**参考资料：**

- [生成式人工智能服务管理暂行办法（CAC 官方规则）](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)
- [Anthropic 2025 年中国禁令政策及 relay 背景](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)
- [V2EX 关于中国 Claude 合规讨论](https://v2ex.com/t/1183984)
- [示例商业 relay（提及国内支付及无需 VPN）](https://www.yiboot.com/article/userguide/claude-4-5-02.html)
- [知乎指南明确说明中国法律下 VPN 使用不违法](https://aifreeapi.com/zh/posts/claude-unsupported-region-solution)
