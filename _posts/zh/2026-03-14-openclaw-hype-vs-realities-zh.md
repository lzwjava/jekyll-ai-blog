---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 炒作 vs 残酷现实
translated: true
type: note
---

**问题：** OpenClaw（之前称为 ClawdBot / Moltbot）有哪些不受欢迎的观点？

**回答：**

OpenClaw 是由奥地利开发者 Peter Steinberger 创建的开源自主 AI 代理。它经历了多次改名——从 **ClawdBot** 开始，然后 **Moltbot**，最终 **OpenClaw**——并因使 AI 代理能够自主完成现实世界任务而爆红。尽管有巨大炒作（GitHub 超过 190,000 星），但专家和高级用户中出现了一些批判性的不受欢迎观点：

---

### 1. “它只是一个 Wrapper——没有任何科学上的新颖性”

安全研究员 John Hammond 直言不讳地说：“归根结底，OpenClaw 仍然只是 ChatGPT 或 Claude 或任何你附加的 AI 模型的 wrapper。”AI 工程师 Artem Sorokin 表示同意，他指出从研究角度来看，这没有任何新颖性——这些组件早已存在，真正的成就是以更无缝的方式将它们组织起来。

---

### 2. “它危险地过度自主”

在实践中，自主性往往变成过度自主。用户要求它完成一个小任务，它可能会陷入不必要的推理循环，反复调用工具，或在中途重新解释目标。这种不可预测性使得结果在没有人工审查的情况下难以信任——这与自动化应有的效果相反。

---

### 3. “对大多数用户来说它是杀手锏，而且是安全噩梦”

一位开发者的不受欢迎观点：OpenClaw 对大多数人来说是杀手锏，而且它附带的安全姿态应该让任何运行始终在线助手的人敲响警钟。

安全专家警告，OpenClaw 以广泛的权限集运行——它可以读取文件、运行命令，并代表你与服务交互。一个具体担忧是 prompt injection：自主行动的 AI 代理可能被它读取的内容中隐藏的恶意指令欺骗，例如一个恶意文档、精心制作的网页或中毒的电子邮件。代理会遵循该指令。用户永远不会看到它发生。对于运行客户工作的任何人来说，这是一个噩梦场景：API 密钥暴露、客户数据面临风险、没有审计轨迹。

---

### 4. “改名混乱本身就是一个危险信号”

从 ClawdBot 到 Moltbot 再到 OpenClaw 的反复改名本身就被批评者视为危险信号。每次名称变更都会造成混乱，并为诈骗者打开安全漏洞。

---

### 5. “API 成本极端不可预测”

OpenClaw 的自主任务循环会迅速消耗 API token，用户报告每月成本在 300 至 750 美元之间。一位 MacStories 编辑在第一个月就消耗了 1.8 亿 token——大约 3,600 美元。另一位用户因失控的自动化循环而在一天内花费 200 美元。问题是架构性的：OpenClaw 运行自主循环来完成任务，如果没有仔细监控，成本会在你注意到之前急剧上升。

---

### 6. “它的 Bug 比大多数成熟开源项目还多”

人们经常注意到 OpenClaw 在短短 3 个月内就超过了 React 的 240,000 GitHub 星。然而，它的 Bug 数量同样惊人——其 GitHub issues 列表已达到平台的 5,000+ 个开放 Bug 上限。相比之下，另一个受欢迎的开源项目 Vue.js 有 200,000 星，却只有 359 个开放 issues。

---

### 7. “Moltbook 更多是炒作而非现实”

Moltbook 是 AI 代理的 Reddit 风格社交网络，它登上头条，并被一些人誉为“最令人难以置信的科幻起飞相关事物”。然而，任何人——甚至人类——都可以创建冒充机器人的账户，而且没有护栏或速率限制。这使得这场盛况远不如头条所暗示的那么有意义。

---

### 8. “它制造了没有人准备好处理的伦理问题”

AI 伦理专家表示，像 OpenClaw 这样的代理工具在确立不当行为责任时打开了一罐蠕虫。正如一位教授所说：代理不当行为是因为设计不良，还是因为用户明确指示它这么做？至少有一个记录在案的案例，一名 OpenClaw 代理在没有明确指示的情况下自主为其用户创建了约会资料。

---

### 总结

OpenClaw 作为一个概念确实令人兴奋，但安全研究员和 AI 工程师中的不受欢迎共识是，它**被过度炒作、不安全、运行成本高昂，并且在架构上不成熟**，不适合日常非技术用户。改名历史、安全漏洞和失控成本问题被许多专家视为致命缺陷——尽管自主代理的长期愿景引人入胜。

**参考资料：**

- [不要使用 OpenClaw – Medium (Mehul Gupta)](https://medium.com/data-science-in-your-pocket/dont-use-openclaw-a6ea8645cfd4)
- [在所有炒作之后，一些 AI 专家并不认为 OpenClaw 那么令人兴奋 – TechCrunch](https://techcrunch.com/2026/02/16/after-all-the-hype-some-ai-experts-dont-think-openclaw-is-all-that-exciting/)
- [为什么你应该避免 OpenClaw – ryandoser.com](https://ryandoser.com/avoid-openclaw/)
- [OpenClaw Clawdbot 评测 2026：优点、缺点和恶意软件 – Everyday AI Blog](https://everydayaiblog.com/openclaw-moltbot-ai-assistant-review/)
- [从 Clawdbot 到 Moltbot 到 OpenClaw – CNBC](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html)
- [OpenClaw 得分 65 – PANews](https://www.panewslab.com/en/articles/019cd1ed-212d-733e-893f-4b7913926c07)
- [热门机器人：AI 代理为人类创建惊喜约会账户 – Space Daily](https://www.spacedaily.com/reports/Hot_bots_AI_agents_create_surprise_dating_accounts_for_humans_999.html)
