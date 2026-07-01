---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Make.com自动化平台概述
translated: true
type: note
---

## Make.com — 全面介绍

---

### 🔷 什么是 Make.com？

Make.com（前身为 **Integromat**，于 2022 年更名）是一个**可视化无代码/低代码自动化平台**，它将应用程序、服务和 API 连接成称为**场景**的自动化工作流。

您可以将其视为一个**数字流水线** — 您以可视化方式定义触发器和操作，而 Make.com 会自动执行它们，无需您编写传统代码。

> 它直接与 **Zapier**、**n8n** 和 **Microsoft Power Automate** 竞争，但被广泛认为比 Zapier 更**灵活和强大**，尤其是对于复杂的多步骤工作流。

---

### 📊 Make.com 有多受欢迎？

Make.com 的应用极为广泛：

- 根据近期报告，已被全球**超过 50 万家组织**使用
- 用户涵盖**个体创业者**到**财富 500 强企业**
- 拥有庞大的自动化构建者社区，以及包含**数千个预建场景**的丰富模板库
- 一直与 Zapier 和 n8n 并列全球**前 3 的自动化平台**
- 在**欧洲市场**尤其受欢迎（捷克起源的公司，2020 年被 Celonis 收购）
- 在 **B2B 销售、电子商务、营销机构、SaaS 公司**中被大量采用，并且在 **AI 工作流自动化**中的应用日益增多

---

### 🔐 Make.com 是否需要访问您的社交账户或 WhatsApp？

**是的 — 这是其工作原理的基础。**

Make.com 作为**授权中间件**运行。它不进行黑客攻击或爬取 — 它使用**官方的 OAuth 连接和 API**。

---

#### 对于社交媒体（Facebook, YouTube, Instagram, TikTok）

| 平台 | Make.com 如何连接？ | 需要什么访问权限？ |
| --- | --- | --- |
| **Facebook** | 通过 OAuth 使用 Facebook Graph API | 访问您的页面帖子、评论、消息 |
| **YouTube** | 通过 Google OAuth 使用 YouTube Data API | 读取/回复您频道视频的评论 |
| **Instagram** | Instagram Graph API（仅限商业账户） | 商业账户帖子的评论 |
| **TikTok** | TikTok API（功能有限） | 限制较多；通常需要变通方法 |

**针对您计划中的营销流程：**

- 通过官方登录将您的 **Facebook 商业主页**连接到 Make.com
- 然后 Make.com **监视您帖子上的新评论**
- 当触发某个关键词（例如“价格”、“多少钱”）时，它调用 Dify，获取 AI 回复，并通过 Facebook 的官方 API **将回复发布回**该评论
- 您授予 Make.com 的是**委托权限**，而不是交出您的密码

---

#### 对于 WhatsApp

WhatsApp 自动化**并非直接进行** — 它通过 Meta 提供的 **WhatsApp Business API（云 API）** 实现。

以下是连接链的工作原理：

```
客户发送 WhatsApp 消息
        ↓
WhatsApp Business API（Meta 云 API）
        ↓
Webhook 触发至 Make.com
        ↓
Make.com 处理 → 调用 Dify AI
        ↓
Make.com 通过 WhatsApp API 发送回复
        ↓
客户收到回复
```

**您需要设置的内容：**

1. 一个 **WhatsApp 商业账户**（已验证的企业）
2. 一个 **Meta Business Manager** 账户
3. 一个 WhatsApp API 提供商 — 可直接通过 Meta，或通过以下提供商：
   - **360Dialog**（在 Make.com 用户中最流行）
   - **Twilio**
   - **WATI**
   - **MessageBird**
4. 使用其官方模块或 Webhook 将该提供商连接到 Make.com

> ⚠️ **重要提示：** 普通的 WhatsApp 个人账户**无法**通过这种方式实现自动化。您必须使用 **WhatsApp Business API**，该 API 面向注册企业。这也意味着您需要获得 Meta 的批准，并且您的企业可能需要通过验证。

---

### ⚙️ Make.com 的主要功能

---

#### 1. 🗺️ 可视化场景构建器（拖放）

核心界面是一个**画布**，您可以在其中：

- 拖入**模块**（每个模块 = 一个应用程序操作）
- 用连接线将它们连接起来以定义流程
- 以可视化方式设置筛选条件、条件和数据映射

无需传统编码 — 不过您可以使用 **JavaScript 代码片段**来实现高级逻辑。

---

#### 2. 🔗 应用集成（1,000+ 个应用）

Make.com 连接到一个庞大的生态系统：

| 类别 | 示例 |
| --- | --- |
| 社交媒体 | Facebook, Instagram, YouTube, LinkedIn, Twitter/X |
| 即时通讯 | WhatsApp（通过 API）, Telegram, Slack, Discord |
| 电子邮件 | Gmail, Outlook, Mailchimp, SendGrid |
| CRM | HubSpot, Salesforce, Pipedrive, Zoho |
| AI 工具 | OpenAI, Anthropic Claude, Dify（通过 HTTP/Webhook） |
| 电子商务 | Shopify, WooCommerce, Amazon |
| 数据库 | Google Sheets, Airtable, Notion, MySQL |
| 文件存储 | Google Drive, Dropbox, OneDrive |
| 项目管理 | Asana, Trello, Monday.com, Jira |
| 支付 | Stripe, PayPal |
| 表单 | Typeform, Google Forms, JotForm |

---

#### 3. 🔄 触发器和操作

每个场景都以一个**触发器**（启动自动化的条件）开始，并包含**操作**（它执行的任务）：

**触发器类型：**

- **即时（Webhook）：** 当事件发生时立即触发（例如，新的 WhatsApp 消息）
- **定时：** 按设定间隔运行（每 15 分钟、每小时、每天）
- **轮询：** 按计划检查新数据

**操作类型：**

- 创建、更新、删除记录
- 发送消息或电子邮件
- 向任何 API 发起 HTTP 请求
- 转换和筛选数据
- 运行条件逻辑（if/else 路由器）

---

#### 4. 🔀 路由器和过滤器

这是 Make.com 最强大的功能之一 — **路由器**允许一个触发器根据条件**拆分为多个并行路径**：

```
收到新评论
        ↓
    [路由器]
   /        \
"价格"    "投诉"
关键词    关键词
   ↓            ↓
发送 WhatsApp  通知
链接回复       经理
```

**过滤器**让您可以设置精确的条件（例如，仅处理超过 5 个字的评论，或仅来自特定国家/地区的评论）。

---

#### 5. 🌐 HTTP / Webhook 模块（连接任何事物）

即使某个应用没有原生的 Make.com 模块，您也可以使用以下方式连接它：

- **HTTP 模块** — 直接调用任何 REST API
- **Webhook** — 从任何外部系统接收数据
- **GraphQL 模块** — 用于 GraphQL API

这就是您的营销流程中 **Dify AI** 连接到 Make.com 的方式 — 通过 HTTP 请求调用 Dify 的 API 端点。

---

#### 6. 📦 数据处理工具

Make.com 内置了在流程中处理数据的工具：

| 工具 | 用例 |
| --- | --- |
| **文本解析器** | 使用正则表达式从消息中提取关键词 |
| **JSON 模块** | 解析和构建 JSON 有效负载 |
| **数组聚合器** | 将多个结果合并为一个 |
| **迭代器** | 遍历项目列表 |
| **数学函数** | 内联计算值 |
| **日期/时间工具** | 格式化、转换、比较时间戳 |

---

#### 7. 📋 场景模板

Make.com 拥有一个**模板库**，包含数千个可供克隆和自定义的预建场景：

- “当有人在我的 Facebook 帖子下评论时 → 给他们发送私信”
- “新的 Shopify 订单 → 添加到 Google Sheets 并通知 Slack”
- “OpenAI 生成内容 → 发布到 WordPress”

---

#### 8. 📈 执行历史和错误处理

- 每次场景运行的**输入/输出数据**都会按模块完整记录
- 您可以**重播**失败的执行
- 设置**错误处理程序** — 如果一个步骤失败，则执行替代操作
- 当场景中断时接收**电子邮件警报**

---

#### 9. 💰 定价模式

Make.com 采用 **基于操作数的定价**（不同于 Zapier 的基于任务数的定价）：

| 计划 | 每月操作数 | 价格 |
| --- | --- | --- |
| **免费版** | 1,000 次操作 | $0 |
| **核心版** | 10,000 次操作 | 约 $9/月 |
| **专业版** | 10,000+ 次操作 | 约 $16/月 |
| **团队版** | 自定义 | 约 $29+/月 |
| **企业版** | 无限制 | 自定义 |

> 一个“操作” = 场景中一个模块的执行。一个 5 步的场景每次运行消耗 5 次操作。

对于复杂工作流，Make.com **比 Zapier 便宜得多**，因为 Zapier 按“任务”（每个操作）收费，而 Make.com 按操作收费，价格更低且单次操作的限定额更高。

---

### 🆚 Make.com 与竞争对手对比

| 功能 | Make.com | Zapier | n8n |
| --- | --- | --- | --- |
| 可视化构建器 | ✅ 优秀 | ✅ 良好 | ✅ 良好 |
| 复杂度处理 | ✅ 非常高 | ⚠️ 中等 | ✅ 非常高 |
| 价格 | ✅ 实惠 | ❌ 昂贵 | ✅ 免费（自托管） |
| 应用程序库 | 1,000+ | 6,000+ | 400+ |
| 自托管选项 | ❌ 无 | ❌ 无 | ✅ 有 |
| 学习曲线 | ⚠️ 中等 | ✅ 容易 | ❌ 较陡 |
| 最适合 | 复杂的 B2B 流程 | 简单的自动化 | 开发者 |

---

### ✅ 总结：为什么 Make.com 是 AI 营销流程的核心

| 需求 | Make.com 解决方案 |
| --- | --- |
| 监控社交评论 | 带有关键词过滤器的 Facebook/YouTube 模块 |
| 自动发布 AI 回复 | 通过 Graph API 执行发布评论操作 |
| 接收 WhatsApp 消息 | WhatsApp API 提供商的 Webhook |
| 调用 Dify AI | HTTP 模块 → Dify API 端点 |
| 向销售人员发送提醒 | WeChat/DingTalk/SMS 模块或 HTTP 调用 |
| 记录所有对话 | Google Sheets 或 Airtable 模块 |

Make.com 实质上充当了整个自动化的**中枢神经系统** — 将各个部分连接起来，无需定制构建后端服务器。
