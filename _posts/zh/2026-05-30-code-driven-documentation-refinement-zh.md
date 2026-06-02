---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码驱动的文档优化
translated: true
type: note
---

问题：

如果讨论的是代码，我们能否让 Copilot 或 Claude 根据实际代码来验证会议记录、文本内容、Excel 文件等？由于代码是精确的，对于编程/软件项目来说，会议记录、Confluence 和 Jira 最终是否能反映最终代码？代码完成后，我们能否反过来，利用代码库来完善原始文档和会议记录？

回答：

可以——实际上，这正成为现代 AI 辅助软件工程中最重要的流程之一。

你描述的是人类讨论（Zoom、会议、Jira、Confluence、Excel、文档）、AI 推理系统（Copilot、Claude、GPT）与实际源代码（最精确的产物）之间的**双向同步循环**。

而你的核心洞察是正确的：

> 在软件项目中，最终代码通常是最精确、最可执行的真理形式。

文档可能含糊不清。
会议可能被误解。
工单可能过时。

但代码必须能够编译、执行、通过测试并满足约束条件。

因此，团队越来越多地使用代码作为“基准事实”，并持续将人类产物与之对齐。

---

# 为什么这行得通

## 1. 人类沟通有损

会议记录和 Jira 工单包含：

* 假设
* 不完整的理解
* 过时的决策
* 模糊的措辞
* 被遗忘的边缘情况

示例：

* Jira 说“支持多种货币”
* 实际代码只支持 USD + EUR
* 会议记录说“实时更新”
* 后端每 5 分钟轮询一次

AI 可以检测这些不一致。

---

# 2. 代码结构精确

代码包含：

* API
* 模式
* 数据库模型
* 业务规则
* 验证逻辑
* 权限
* 实际工作流

AI 模型非常擅长：

* 阅读代码库
* 提取意图
* 将需求映射到实现
* 识别不匹配

这就是 AI 编码代理强大的原因：
它们可以将自然语言与可执行系统进行比较。

---

# 3. 从代码逆向生成文档

这在先进的工程组织中已经发生。

流程变为：

```text
会议 → Jira → 设计 → 代码
                 ↓
        AI 验证对齐
                 ↓
代码 → AI → 更新后的文档/规格/笔记
```

所以是的：
代码演化后，AI 可以重新生成或完善：

* Confluence 页面
* API 文档
* 架构图
* 入职文档
* 发布说明
* 会议摘要
* 需求文档

---

# 示例工作流

## 会议期间

每 5 分钟：

* 总结讨论
* 提取决策
* 提取待办事项
* 追加到 `meeting.md`

同时摄取：

* Jira 工单
* Excel 规格
* 架构文档
* 当前代码库

---

# AI 验证阶段

Claude/Copilot/GPT 比较：

```text
meeting.md
jira.json
requirements.xlsx
```

对照：

```text
/src
/backend
/openapi.yaml
/tests
/database schemas
```

AI 识别：

* 缺失的实现
* 过时的文档
* 矛盾
* 未实现的需求
* 废弃的功能
* 范围蔓延

---

# 逆向完善

然后 AI 生成：

```text
“基于实际代码实现：

- OAuth2 刷新令牌已实现
- SAML 支持部分完成
- 多区域故障切换未实现
- 货币支持仅限于 USD/EUR
”
```

这成为：

* 完善的会议记录
* 更新的 Jira
* 更新的 Confluence
* 发布文档

---

# 为什么这在 AI 时代变得更重要

大型系统对人类来说变得过于复杂，无法手动跟踪。

现代系统包含：

* 微服务
* 基础设施即代码
* Kubernetes
* CI/CD
* 功能标志
* AI 管道
* 事件流
* 数百个 API

人类无法完美同步：

* 会议
* 工单
* 代码
* 架构
* 文档

AI 成为同步层。

---

# 未来方向

可能的未来是：

## “以代码为中心的组织记忆”

其中：

* 会议持续更新 AI 记忆
* AI 将讨论映射到代码实体
* AI 自动检测漂移
* 文档持续重新生成
* Jira 工单成为可执行的规格说明

最终：

```text
人类意图 ↔ AI 推理 ↔ 可执行代码
```

成为一个持续循环。

---

# 重要限制

代码在技术上是精确的，但语义上并不总是完整的。

示例：

* 代码可能没有清晰地表达业务意图
* 遗留代码可能违反当前需求
* 可能存在临时方案/变通方法
* 可能存在死代码

因此，最佳系统结合了：

* 人类意图
* 架构推理
* 代码真理
* 运行时遥测
* 测试

AI 充当它们之间的协调引擎。

---

# 现有的相关工具/理念

一些现实世界的系统已经在朝这个方向前进：

* [GitHub Copilot](https://github.com/features/copilot?utm_source=chatgpt.com)
* [Claude Code](https://www.anthropic.com/claude-code?utm_source=chatgpt.com)
* [Sourcegraph Cody](https://sourcegraph.com/cody?utm_source=chatgpt.com)
* [Cursor IDE](https://cursor.com?utm_source=chatgpt.com)
* [OpenAPI Specification](https://www.openapis.org/?utm_source=chatgpt.com)
* [Backstage by Spotify](https://backstage.io/?utm_source=chatgpt.com)
* [LangGraph for workflow memory/orchestration](https://www.langchain.com/langgraph?utm_source=chatgpt.com)

这些工具越来越多地将：

* 代码
* 文档
* 工单
* 运行时系统
* 对话

视为一个互联的知识图谱。
