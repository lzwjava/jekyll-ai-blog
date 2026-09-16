---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI工程Pod服务计划
translated: true
type: note
---

问题：**为我制定一份AI原生软件外包公司的具体2026年计划：定位、客户、定价、交付体系、智能体技术栈、单位经济学，以及从$0到$100万/年的路径。**

答案：**我会将其打造为一个高端的“AI工程团队即服务”，而不是一个外包市场。**

市场信号足够强劲，值得现在进行测试：麦肯锡2026年调查显示，约20%的组织已经在规模化使用软件编码智能体，32%表示智能体编码促使他们在内部构建而非购买软件。([McKinsey & Company][1]) OpenAI当前的Codex栈明确支持长时间运行的智能体、子智能体、代码执行、仓库和后台工作；OpenAI也将其自身的智能体优先工程工作流描述为“人类引导，智能体执行”。([OpenAI][2])

我将构建的业务是：

```text
                  AI ENGINEERING CO.
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   新软件开发        AI集成         遗留系统重写
        │                │                │
        └────────────────┼────────────────┘
                         │
                资深人类工程师
                         +
               自主智能体
                         │
                         ▼
                 交付的软件
```

---

# 1. 从一个极其具体的客户开始

不要从以下开始：

> "我们为所有人构建软件。"

那会创造一个销售面无限宽的代理公司。

我会从以下开始：

> **需要软件但不想雇佣5-10人工程团队的美国初创公司和中型企业。**

理想客户：

```text
营收：        $100万–$5000万
员工：       10–200人
工程团队：   0–5名工程师
问题：       软件阻碍了增长
预算：       $1万–$4万/月
决策者：     创始人 / CTO / COO
```

示例：

```text
"构建我们的客户门户。"

"自动化我们的运营。"

"替换这个电子表格工作流。"

"集成Salesforce + Stripe + 我们的内部数据库。"

"构建一个AI支持系统。"

"现代化我们的旧Rails应用。"

"为我们的新产品构建MVP。"
```

你不需要说服他们AI有价值。

他们已经有一个软件问题。

**你销售的是解决方案。**

---

# 2. 你的第一个产品

我会这样打包：

## AI工程Pod

```text
$15,000/月
```

客户获得：

```text
1名资深工程师
+
AI工程智能体
+
QA智能体
+
DevOps自动化
+
架构设计
+
部署
+
维护
```

不要向客户暴露智能体的复杂性。

从他们的视角来看：

```text
周一
  ↓
"这是需求。"

周二
  ↓
"我们有一个可用的PR。"

周三
  ↓
"QA通过了。"

周四
  ↓
"部署到staging环境。"

周五
  ↓
"生产环境。"
```

这就是产品。

---

# 3. 三个定价层级

我会从以下开始：

| 产品                  |           价格 | 适用场景                       |
| -------------------- | -------------: | ---------------------------- |
| **构建冲刺**          | $1万–$2.5万固定 | 特定项目                       |
| **工程Pod**          |    $1.5万–$3万/月 | 持续开发                       |
| **专属Pod**          |    $3万–$5万/月 | 较大公司 / 关键系统             |

不要按小时出售。

永远不要说：

```text
$150/小时
```

因为那样客户会开始计算：

```text
"为什么我不直接雇个人？"
```

相反：

```text
$2万/月
→ 持续的工程能力
→ 可预测的交付
→ 无需招聘
→ 无需工程管理开销
```

你销售的是 **能力 + 责任**。

---

# 4. 你的第一个$10万

先别想着$100万。

你的第一个里程碑：

```text
3个客户 × $1.5万/月
=
$4.5万 MRR

6个客户 × $1.5万
=
$9万 MRR
```

这已经是：

```text
$108万 ARR
```

你不需要100个客户。

你需要 **6–10个好客户**。

这就是这个模式的美丽之处。

---

# 5. 交付架构

我认为这里你可以有真正的优势。

不要运行：

```text
客户
  ↓
人类开发者
  ↓
ChatGPT
```

构建一个内部的 **智能体工程操作系统**。

```text
                         客户
                            │
                            ▼
                     需求智能体
                            │
                            ▼
                     架构智能体
                            │
                            ▼
                    任务分解
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        代码智能体     代码智能体     研究智能体
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                       测试智能体
                            │
                            ▼
                       审查智能体
                            │
                            ▼
                     安全智能体
                            │
                            ▼
                     人类工程师
                            │
                            ▼
                          合并
                            │
                            ▼
                        部署
```

这就是你的技术背景发挥作用的地方。

---

# 6. 不要先构建编排器

这点很重要。

**不要花六个月构建一个“AI软件工厂”。**

最初使用现有的智能体。

OpenAI当前的Codex平台已经支持多智能体工作流、技能、后台任务和长时间运行。([OpenAI][3])

你的第一个版本可以就是：

```text
GitHub
Linear
Codex / Claude Code
Postgres
Docker
GitHub Actions
Sentry
Vercel / AWS
Slack
```

然后在它们之上创建你自己的薄层。

例如：

```text
客户仓库
     ↓
/agent
     ├── architect
     ├── implement
     ├── test
     ├── review
     └── deploy
```

你从 **真实客户** 中发现瓶颈。

只自动化那些真正痛苦的部分。

---

# 7. 你的内部仓库模板

这比听起来重要得多。

每个客户项目都应该从你的标准环境开始。

类似这样：

```text
customer-project/
├── AGENTS.md
├── README.md
├── docs/
│   ├── architecture.md
│   ├── product.md
│   ├── decisions/
│   └── api.md
├── src/
├── tests/
├── scripts/
├── infra/
├── .github/
│   └── workflows/
└── observability/
```

`AGENTS.md` 会变得极其有价值。

示例：

```md
# 工程规则

## 技术栈

- TypeScript
- Next.js
- PostgreSQL
- Drizzle
- Vitest
- Playwright

## 规则

- 每个功能都需要测试。
- 永远不要直接修改生产数据。
- 所有数据库迁移必须可逆。
- 每个API端点都需要验证。
- 未经论证不要引入依赖。
- 提交前运行 `npm test`。
- 对于面向用户的更改，运行Playwright。

## 架构

...

## 产品需求

...
```

智能体现在有了一个 **公司操作系统**。

OpenAI自身的“harness engineering”工作基本就是在阐述这个观点：当编码智能体能够写出大量代码时，工程瓶颈会转向规范、仓库结构、测试、文档和反馈循环。([OpenAI][4])

---

# 8. 你真正的护城河

不是：

```text
GPT
Claude
Codex
Gemini
```

那些都是商品。

你的护城河变成：

```text
                  你的数据
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   需求          架构          缺陷
        │            │            │
        └────────────┼────────────┘
                     ▼
              工程剧本
                     │
                     ▼
                智能体
                     │
                     ▼
              更好的交付
                     │
                     ▼
              更多客户
                     │
                     ▼
              更多知识
```

经过50个项目，你会知道：

```text
如何构建SaaS
如何集成Stripe
如何迁移Rails
如何构建RAG
如何部署AWS
如何实现身份验证
如何构建管理面板
如何实现可观测性
如何测试浏览器工作流
```

你的智能体编码了这些知识。

这就是复合循环。

---

# 9. 你的第一个垂直领域

我实际上会做得比“SMB”更窄。

例如：

### 选项A — AI原生初创公司

```text
创始人有了想法
        ↓
你构建MVP
        ↓
$2万–$4万
        ↓
每月工程服务费
```

非常容易演示。

但流失率可能较高。

### 选项B — 成熟的中型企业

```text
营收$500万的公司
        ↓
30名员工
        ↓
糟糕的内部软件
        ↓
$2万/月
        ↓
你成为他们的工程部门
```

这大概是我会优先测试的模式。

### 选项C — 遗留系统现代化

```text
旧的Rails/.NET/Java
        ↓
AI辅助分析
        ↓
测试
        ↓
增量迁移
        ↓
现代技术栈
```

这可以支持更大的合同，但需要更多的信任和领域专业知识。

---

# 10. 销售话术

不要说：

> "我们使用AI以10倍速度构建软件。"

那会引起怀疑。

要说：

> **"我们充当你的工程团队。你给出路线图；我们设计、构建、部署和维护软件。"**

然后：

> "与其雇佣五名工程师，你获得一位由AI原生交付系统支持的资深工程负责人。"

这是具体的。

---

# 11. 你的销售漏斗

保持极其简单。

```text
主动外联
   │
   ▼
30分钟技术发现
   │
   ▼
免费架构/自动化审计
   │
   ▼
$1万–$2万试点项目
   │
   ▼
成功交付
   │
   ▼
$1.5万–$3万/月服务费
```

试点项目很重要。

不要让人立刻信任你拿$30万的系统。

给他们：

```text
2–4周
一个有意义的项目
固定价格
生产环境部署
```

然后扩展。

---

# 12. 客户示例

想象一下：

```text
公司：
B2B物流公司

员工：
80人

工程团队：
2名开发者

问题：
运营使用17个电子表格。

需求：
"构建一个内部运营平台。"
```

传统代理公司：

```text
项目经理
设计师
架构师
4名工程师
QA
DevOps

6个月
$30万+
```

你的公司：

```text
1名资深工程师
+
智能体集群

6–10周
$5万初始构建

然后：

$1.5万/月
维护 + 新功能
```

内部：

```text
第1天
架构

第2天
数据库模式

第3天
CRUD

第4天
身份验证

第5天
第一个UI界面

...
```

智能体夜间工作。

人类早上审查。

麦肯锡2026年的研究将这种新兴模式描述为近乎持续的软件交付，并引用了一些组织报告3–5倍的生产力提升以及团队规模的大幅缩减。这些是报告的结果，而不是对新公司的保证，但它们说明了为什么这个交付模式值得测试。([McKinsey & Company][5])

---

# 13. 单位经济学

让我们模拟一个$2万/月的客户。

```text
收入                         $20,000

人类工程成本                 $5,000
AI推理成本                    $1,500
云/工具                       $1,000
项目经理/客户成功            $1,500
───────────────────────────────────────
毛贡献                     $11,000
```

那是：

```text
55% 毛利率
```

经过优化：

```text
收入                         $20,000

人类                         $3,500
AI                               $800
基础设施/工具                   $700
客户成功                       $800
────────────────────────────────
贡献                         $14,200
```

71%。

**不要假设你能获得这些利润率。**

去测量它们。

你的前10个项目本质上是一个实验，用来发现：

```text
人类工时 / 美元收入
token数 / 美元收入
缺陷数 / 项目
返工率 %
毛利率
生产上线时间
```

这些数字告诉你这家业务是否真的可行。

---

# 14. $100万/年目标

我会设定这个进度：

```text
第1–2个月
────────────────────────
1个试点项目
$1万–$2万收入


第3–4个月
────────────────────────
2–3个客户
$3万–$4.5万 MRR


第5–8个月
────────────────────────
4–6个客户
$6万–$10万 MRR


第9–12个月
────────────────────────
6–10个客户
$10万–$15万 MRR
```

你实际上不需要$15万 MRR。

在：

```text
$8.5万 MRR
```

你就已经达到：

```text
$102万 ARR
```

因此目标是：

> **获得6个客户，每个支付约$1.4万/月。**

而不是：

> 获得100个客户。

---

# 15. 招聘策略

我会尽可能长时间地抵制招聘开发者的冲动。

首先：

```text
你
+
AI
```

然后：

```text
你
+
资深工程师 #2
+
AI
```

然后：

```text
2名资深工程师
+
1名客户/产品负责人
+
AI
```

只有当瓶颈真正是人类工程能力时才增加工程师。

理想的组织最终可能看起来像这样：

```text
             创始人
                │
       ┌────────┴────────┐
       │                 │
   销售/产品           工程
                         │
              ┌──────────┼──────────┐
              │          │          │
           工程师     工程师     工程师
              │          │          │
            智能体     智能体     智能体
```

而不是：

```text
创始人
  ↓
20名初级开发者
```

---

# 16. 安全成为产品特性

这就是企业客户会挑战你的地方。

智能体可以：

```text
读取代码
执行命令
修改文件
访问API
部署基础设施
```

所以你需要硬边界。

OpenAI自身关于运行编码智能体的指南强调了访问控制、审批关卡、遥测以及针对高风险行动的明确边界。([OpenAI][6])

因此，你的标准环境应该具备：

```text
沙箱
   ↓
最小权限
   ↓
临时凭证
   ↓
默认无生产凭证
   ↓
需要PR
   ↓
需要CI
   ↓
人类审批
   ↓
生产环境
```

永远不允许：

```text
智能体 → 生产环境 → 任意shell
```

作为默认行为。

---

# 17. 只有在大约10个客户之后才构建你自己的“工厂”

起初：

```text
Codex
Claude Code
GitHub
Linear
Docker
CI
```

到第10个客户时，你会注意到重复的工作。

然后构建：

```text
             公司平台
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   项目设置      智能体        质量
                  编排          控制
       │            │            │
       ▼            ▼            ▼
   模板         任务队列      评估
```

一个特别有趣的方向是编排层。OpenAI的Symphony项目描述了将项目管理系统转化为一个控制平面，其中每个任务都可以获得一个智能体，智能体持续工作，人类审查结果。([OpenAI][7])

这非常接近于我最终会构建的内部基础设施。

---

# 18. 你的30天执行计划

如果你真的想做这件事，我会让第一个月极其具体。

### 第一周

构建：

```text
着陆页
+
一页纸的服务方案
+
标准仓库模板
+
智能体指令
+
部署模板
```

你的着陆页只需要：

```text
AI工程团队

我们为成长型公司
设计、构建和运营定制软件。

• 固定价格项目
• 月度工程Pod
• AI原生开发
• 生产环境部署
• 持续维护

预约技术评估。
```

---

### 第二周

构建2–3个令人印象深刻的演示。

不是玩具演示。

构建企业真正愿意付费的东西：

```text
1. CRM / 运营平台

2. AI文档处理工作流

3. 内部数据分析 / 管理平台
```

把代码放到GitHub上。

部署它们。

录制2分钟演示视频。

---

### 第三周

开始主动外联。

目标：

```text
100家公司
```

不是随机公司。

搜索那些说以下内容的公司：

```text
"我们正在招聘软件工程师"

"需要内部平台"

"手动流程"

"电子表格"

"遗留系统"

"AI自动化"

"正在寻找CTO"
```

话术：

```text
你好X，

我注意到你正在招聘 [工程问题]。

我们正在试验一种AI原生工程模式：
一名资深工程师 + 自主编码/QA智能体。

与其增加3–5名工程师，
我们可以负责 [特定项目]。

我很乐意免费做一次技术评估
针对 [他们的系统/问题]。

—— 智维
```

---

### 第四周

成交 **一个客户**。

不要优化网站。

不要构建SaaS平台。

不要雇佣十个人。

不要花六个月构建编排框架。

就：

```text
销售
 ↓
构建
 ↓
交付
 ↓
测量
 ↓
重复
```

---

# 19. 你的第一个内部仪表盘

我会从第一天起跟踪这些：

```text
客户
────────────────────────
MRR
项目收入
人类工时
AI成本
云成本
毛利率


工程
────────────────────────
每周PR数
每周智能体任务数
智能体成功率
测试通过率
每周缺陷数
返工率
每周部署次数


交付
────────────────────────
从线索到合同时间
从合同到首次PR时间
从合同到生产上线时间
生产事故数
客户满意度
```

以及一个高于一切的指标：

```text
                 客户价值
AI杠杆 = ─────────────────────
              人类工程投入
```

你希望这个数字每个月都在增长。

---

# 20. 战略终局

实际上有三个业务隐藏在其中。

### 阶段一 — 服务

```text
客户
  ↓
你 + 智能体
  ↓
软件
```

现金流。

学习问题。

---

### 阶段二 — 内部平台

```text
客户
  ↓
你的工程工厂
  ↓
智能体
  ↓
软件
```

更高的利润率。

更多的可重复性。

---

### 阶段三 — 产品

最终你可能会发现：

```text
"我们已经为30家物流公司
构建了相同的系统。"
```

然后：

```text
服务
   ↓
可重复的工作流
   ↓
垂直SaaS
```

现在你有了：

```text
服务收入
+
软件收入
```

这就是真正有趣的地方。

---

## 如果我是你，我会做什么

鉴于你现有的经验：构建产品、训练模型、构建CLI/智能体系统，**我根本不会从创建一家传统外包公司开始。**

我会创建：

> **一家AI原生工程公司，其生产单位是一名资深工程师 + 一个智能体集群。**

从以下开始：

```text
                    你
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Codex       Claude       自定义
                   Code        智能体
        │            │            │
        └────────────┼────────────┘
                     ▼
              你的HARNESS
                     │
                     ▼
               客户代码
                     │
                     ▼
               生产环境
```

**首个目标：3个客户 × $1.5万/月。**

一旦你能可靠地交付这个，推进到：

```text
6个客户
×
$1.5万/月
=
$9万 MRR
=
$108万 ARR
```

最大的问题不是AI能否写出足够的代码。2026年的证据强烈表明它可以。问题是 **你能否将智能体的能力转化为一个可靠、可重复的客户交付机器**。这才是值得构建的公司。([Gartner][8])

### 参考文献

* [McKinsey — The State of AI 2026](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai?os=av.&utm_source=chatgpt.com)
* [McKinsey — Rewiring software delivery for the agentic era](https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/rewiring-software-delivery-for-the-agentic-era?utm_source=chatgpt.com)
* [OpenAI — Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/?utm_source=chatgpt.com)
* [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/?utm_source=chatgpt.com)
* [OpenAI — Codex for software engineering teams](https://openai.com/business/solutions/engineering/?utm_source=chatgpt.com)
* [Gartner — Enterprise AI coding agents in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-says-the-market-for-enterprise-ai-coding-agents-is-entering-a-new-phase-of-expansion-and-competitive-realignment?utm_source=chatgpt.com)

[1]: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai?os=av.&utm_source=chatgpt.com "The State of AI: Global Survey 2026 | McKinsey"
[2]: https://openai.com/index/introducing-the-agents-api/?utm_source=chatgpt.com "Introducing the Agents API | OpenAI"
[3]: https://openai.com/index/introducing-the-codex-app/?utm_source=chatgpt.com "Introducing the Codex app | OpenAI"
[4]: https://openai.com/index/harness-engineering/?utm_source=chatgpt.com "Harness engineering: leveraging Codex in an agent-first world | OpenAI"
[5]: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/rewiring-software-delivery-for-the-agentic-era?utm_source=chatgpt.com "Rewiring software delivery for the agentic era | McKinsey"
[6]: https://openai.com/index/running-codex-safely/?utm_source=chatgpt.com "Running Codex safely at OpenAI | OpenAI"
[7]: https://openai.com/index/open-source-codex-orchestration-symphony/?utm_source=chatgpt.com "An open-source spec for Codex orchestration: Symphony. | OpenAI"
[8]: https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-says-the-market-for-enterprise-ai-coding-agents-is-entering-a-new-phase-of-expansion-and-competitive-realignment?utm_source=chatgpt.com "Gartner Says the Market for Enterprise AI Coding Agents Is Entering a New Phase of Expansion and Competitive Realignment"