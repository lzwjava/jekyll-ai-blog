---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Copilot Agent 在终端本地运行命令
translated: true
type: note
---

**Question:** 当在 VS Code 中使用 Copilot 的 agent mode 运行命令时，该命令是否实际上是在 VS Code terminal 中执行的？我们可以在嵌入式 terminal 中查看进度吗？

**Answer:**

是的，没错。

在 VS Code 的 **GitHub Copilot agent mode** 中（通过 Chat 视图或 Copilot Edits 视图选择 "Agent" 模式访问的本地交互式 agent），当 agent 需要执行 terminal 命令时（例如 `npm install`、`dotnet test`、`cargo build`、启动 dev server 等），它会在 VS Code 的 **integrated terminal** 中运行这些命令。

关于其工作原理的关键点：

- Agent 通常使用 **default terminal profile**（有时会创建一个新的 terminal 实例）。
- 命令是在你的本地环境（你的机器上）执行的，而不是在远程/云端 sandbox 中。
- Agent 在运行 terminal 命令之前通常需要你的确认（除非你在设置中启用了 auto-approve）。
- 你可以直接在 VS Code integrated terminal 面板中观察命令的执行及其输出。
- 在 Copilot chat 界面中，agent 通常会显示它运行（或想要运行）的命令，并提供类似 "Show Output"（内联显示）或 "Show Terminal" 的选项，以便跳转到完整的 terminal 视图。
- 进度、错误、build output、测试结果等都会实时显示在该 terminal 中 —— 就像你自己输入任何普通命令一样。
- Agent 可以读取 terminal 输出，以了解执行成功或失败的情况，并进行迭代（修复 bug、调整命令等）。

这与独立的 **GitHub-hosted Copilot coding agent** 不同（后者通过 GitHub Actions 在云端运行，不使用你的本地 VS Code terminal）。

所以，是的 —— 当在 VS Code 中使用 agent mode 且 Copilot 建议或运行命令时，你可以（也应该）查看嵌入式 terminal 以关注正在发生的情况，查看实时输出，并在需要时进行干预。

**References:**

- [Introducing GitHub Copilot agent mode (preview)](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)
- [Use tools in chat - Terminal commands](https://code.visualstudio.com/docs/copilot/chat/chat-tools)
- [Agent mode 101: All about GitHub Copilot's powerful mode](https://github.blog/ai-and-ml/github-copilot/agent-mode-101-all-about-github-copilots-powerful-mode)