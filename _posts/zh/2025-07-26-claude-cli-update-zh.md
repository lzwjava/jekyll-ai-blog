---
audio: false
generated: true
lang: zh
layout: post
title: 更新Claude代码命令行工具
translated: true
type: note
---

你好！看起来你正在使用 Anthropic 公司的 Claude Code CLI 工具。根据你粘贴的输出内容，它似乎已经尝试自动更新到 1.0.61 版本，但如果更新没有成功或者你需要手动更新，可以按照以下方法操作：

要更新 Claude Code CLI：
- 打开终端
- 运行命令：`claude update`
这个内置命令应该会获取并安装最新版本。

如果更新失败（比如由于权限或网络问题），你可以尝试通过 npm 重新安装（假设你已安装 Node.js 和 npm）：
- 运行：`npm install -g @anthropic-ai/claude-code`

更新后，你可能需要重新登录，运行 `claude /login`（或者根据版本不同，有时是 `claude login`）。如果你仍然看到错误，请检查网络连接，确保 API 密钥有效，或参考官方故障排除文档。

要了解更多命令详情，你可以像之前那样运行 `claude --help`，这应该会显示更新版本中的选项。

[CLI 参考 - Anthropic API](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
[如何专业地设置和使用 Claude CLI 工具](https://medium.com/@riccardo.bernardi.advisor/unlocking-claude-pros-power-how-to-set-up-and-use-the-claude-cli-tool-like-a-pro-against-github-d29f8f682a03)
[GitHub - anthropics/claude-code](https://github.com/anthropics/claude-code)
[Claude Code 概述 - Anthropic API](https://docs.anthropic.com/en/docs/claude-code/overview)
