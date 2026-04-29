---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启需重复危险旗帜
translated: true
type: note
---

问题：当使用 `--resume` 恢复之前的 Claude 会话时，我是否仍然需要传递 `--dangerously-skip-permissions`？

答案：

是的——在大多数 CLI 设计中（包括 Claude Code 风格的工具），恢复会话时您仍然需要再次显式传递 `--dangerously-skip-permissions`。

### 为何有此要求

* **出于安全考虑，标志不会被持久保存**
  类似 `--dangerously-skip-permissions` 这样的安全相关标志被视为*每次执行的显式同意*，而非存储在会话状态中。

* **恢复功能仅恢复对话，而非执行策略**
  `--resume <session-id>` 通常重新加载：

  * 聊天记录
  * 工具上下文
  * 之前的输出

  但它并**不会自动重新启用已绕过的权限模式**，因为这会造成先前安全的会话隐式变得不安全的潜在风险。

* **设计原则：“每次运行均需重新确认”**
  尤其是对于以下类型的标志：

  * 绕过文件系统限制
  * 允许执行不安全工具
  * 禁用沙盒保护

  命令行工具通常要求每次进程启动时都重新声明这些标志。

### 实际影响

因此您的命令是正确的：

```bash
claude --resume d79629a0-c3a2-40e7-8f36-b21bf7d0d53c --dangerously-skip-permissions
```

如果省略该标志，恢复的会话很可能会：

* 回退到默认的权限检查，或
* 阻止先前能够执行的操作

### 概念模型

可以这样理解：

* `--resume` = “重新加载记忆”
* `--dangerously-skip-permissions` = “以提升的特权启动”

二者作用于不同层级，因此必须同时指定。

参考：

* [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)（通用 CLI 行为模式）