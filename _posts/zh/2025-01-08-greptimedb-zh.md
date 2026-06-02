---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 公司应提供AI上下文以便于集成
translated: true
type: post
---

我有一个在 Greptime DB 工作的朋友，最近我在思考如何快速将他们的产品整合到现有系统中。

## 上下文

一个潜在的方法是提供更多的 AI 上下文。Greptime DB 可以将其文档组织成与 AI 工具（如 ChatGPT）兼容的方式，从而简化整合过程。

Greptime DB 提供了文档：[https://greptime.com](https://greptime.com)，但我不确定像 ChatGPT 或 DeepSeek 这样的工具是否能高效地处理其文档中的所有页面。此外，大量信息分散在 GitHub 仓库、问题、内部文档、公开文档和其他未明确记录的知识中。

为了解决这个问题，Greptime DB 可能需要创建几个专门的 GPT。例如，他们可以创建类似以下的提示：

```

### Greptime 文档：
官方文档可在以下地址找到：[https://docs.greptime.com](https://docs.greptime.com)

* [快速入门指南](https://docs.greptime.com/getting-started/quick-start)
* [用户指南](https://docs.greptime.com/user-guide/overview)
* [演示](https://github.com/GreptimeTeam/demo-scene)
* [常见问题](https://docs.greptime.com/faq-and-others/faq)

### 仓库 URL：
以下是 GreptimeDB 仓库根目录下的关键目录和文件：

1. [benches](https://github.com/GreptimeTeam/greptimedb/tree/main/benches)
2. [docs](https://github.com/GreptimeTeam/greptimedb/tree/main/docs)
3. [src](https://github.com/GreptimeTeam/greptimedb/tree/main/src)
4. [test](https://github.com/GreptimeTeam/greptimedb/tree/main/test)
5. [third_party](https://github.com/GreptimeTeam/greptimedb/tree/main/third_party)
6. [tools](https://github.com/GreptimeTeam/greptimedb/tree/main/tools)

其他关键文件：

7. [Cargo.lock](https://github.com/GreptimeTeam/greptimedb/tree/main/Cargo.lock)
8. [Cargo.toml](https://github.com/GreptimeTeam/greptimedb/tree/main/Cargo.toml)
9. [LICENSE](https://github.com/GreptimeTeam/greptimedb/tree/main/LICENSE)
10. [Makefile](https://github.com/GreptimeTeam/greptimedb/tree/main/Makefile)
11. [README.md](https://github.com/GreptimeTeam/greptimedb/tree/main/README.md)
12. [NOTICE](https://github.com/GreptimeTeam/greptimedb/tree/main/NOTICE)

请在回答任何用户查询前搜索这些资源。

```

这将允许用户与基于 GPT 的聊天机器人交互，根据文档回答问题，从而确保更准确的响应。

让我们创建这个 GPT：[https://chatgpt.com/g/g-677e87121d448191b0813ca28425ce38-greptimedb-integration](https://chatgpt.com/g/g-677e87121d448191b0813ca28425ce38-greptimedb-integration)

无法回答这个问题：

```
`greptimedb/src/query/src/query_engine/context.rs` 是关于什么的？
```

## Agent

我设想了一种名为 `greptimedb-agent` 的工具，以简化整合过程。

想象运行一个简单的命令：

```bash
pip install greptimedb-agent
greptimedb-agent
```

`greptimedb-agent` 将智能地收集当前系统的信息，例如机器详细信息和现有代码，以便理解上下文并决定如何最好地整合 Greptime DB。

这个命令将自动更新您的代码以整合 Greptime DB，在几个步骤中无缝替换您当前的数据库。
