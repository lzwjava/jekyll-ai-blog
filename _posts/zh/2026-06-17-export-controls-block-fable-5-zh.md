---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 出口管制封锁寓言5
translated: true
type: note
---

**问题：** 为什么 Claude Fable 5 目前在 Claude Code 中不可用？

**答案：**

这是美国政府的出口管制情况，并非故障或服务器宕机。

**时间线：**

- **2026年6月9日** — Anthropic 发布了 Claude Fable 5，这是其公开推出的最强大模型，专为长周期自主任务而设计。同日，该模型通过 Claude API、AWS、Microsoft Foundry 等渠道上线。

- **2026年6月12日** — Anthropic 收到美国政府根据国家安全出口管制权限发布的指令，要求其暂停 Fable 5 及其更大版本 Mythos 5 的访问权限。该指令涵盖所有外国国籍人士——无论其身处美国境内还是境外，包括 Anthropic 自身的外国籍员工。由于 Anthropic 无法在客户合同、员工及云交付路径中实时按国籍筛选访问权限，因此选择对所有地区的所有客户暂停这两个模型，以避免违规风险。

**Fable 5 的实际定位：**

Fable 5 是 Mythos 5 的公开、带防护的版本——它们共享相同的底层模型和已发布的规格。两者默认均支持 1M token 上下文窗口，每次请求最多 128K 输出 token，定价为每百万输入 token 10 美元、每百万输出 token 50 美元。

**当前状态：**

Fable 5 和 Mythos 5 暂时对全球所有用户不可用。Opus 4.8、Sonnet 4.6 和 Haiku 4.5 正常运行。目前尚未公布恢复日期。

**具体针对 Claude Code** — API 返回 404 `not_found_error`，并带有消息："Claude Fable 5 不可用。请使用 Opus 4.8。"

**应对措施：** 在 Claude Code 配置中切换至 `claude-opus-4-8` 或 `claude-sonnet-4-6`。两者均可正常使用。

**参考链接：**

- [Anthropic 关于 Fable/Mythos 访问权限的声明](https://www.anthropic.com/news/fable-mythos-access)
- [InfoQ: Anthropic 发布并暂时暂停 Claude Fable 5](https://www.infoq.com/news/2026/06/claude-5-release/)
- [Claude Code GitHub Issue #68121](https://github.com/anthropics/claude-code/issues/68121)