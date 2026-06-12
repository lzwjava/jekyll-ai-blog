---
audio: false
generated: true
image: false
lang: zh
layout: post
title: cc-switch Claude代码提供商切换器
translated: true
type: note
---

**问题：** 什么是 Claude Code 生态系统中的 cc-switch？

**答案：**

cc-switch 是一个第三方、开源的 Claude Code（及其他 AI CLI）提供商/配置切换器——并非 Anthropic 产品，也不是 Claude Code 的内置命令。它是一款跨平台桌面助手，支持 Claude Code、Codex、OpenCode、OpenClaw、Gemini CLI 和 Hermes Agent，由 farion1231 开发。

**它解决的问题：** Claude Code 从 `~/.claude/settings.json` 或环境变量（如 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`）读取其后端配置（基础 URL、API 密钥、模型）。如果你在 Anthropic 官方、DeepSeek、OpenRouter、GLM、Kimi 等之间切换，就需要手动编辑 JSON 或处理 shell 导出变量。cc-switch 将这种环境变量切换操作简化为点击即可完成——它管理多个提供商配置文件，持久化到 `~/.claude/settings.json`，让你无需修改 shell 配置即可切换后端。

**主要功能：**

v3.16.1 通过系统托盘应用管理 7 个 AI CLI，内置约 50 个第三方提供商预设（DeepSeek、智谱 GLM、MiniMax、Kimi、通义千问/百炼、AWS Bedrock、NVIDIA NIM、OpenRouter，以及中继服务）——大多数预设只需填写 API 密钥，因为端点 URL 和协议已预填。它还处理 MCP 服务器、技能、提示词、本地代理路由、使用统计，并支持跨设备的 WebDAV 同步。在代理模式下，请求流为 Claude Code → localhost:8080 → CC-Switch 代理 → 上游 API，并且“Claude 修正器”功能（v3.10.0+）可修复与第三方 API 的兼容性问题。

**针对你的工作流：** 由于你重度使用 OpenRouter 类提供商的 deepseek-v4 和 MiMo，这与你的需求直接相关。有两种路径：

1. GUI：`farion1231/cc-switch` 桌面应用（基于 Tauri，在你的 M2 Air 上运行良好）
2. 终端优先（更符合你的风格）：`SaladDay/cc-switch-cli`——这是一个 TUI + CLI 分支，交互式 TUI 用于日常切换，纯 CLI 用于脚本和可重复工作流

不过其底层机制很简单——如果你不想使用额外工具，可以用一个 20 行的 shell 函数复现核心功能：

```bash
# ~/.zshrc — 简易版 cc-switch
ccs() {
  case "$1" in
    deepseek)
      export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
      export ANTHROPIC_AUTH_TOKEN="<API_KEY>"
      export ANTHROPIC_MODEL="deepseek-chat" ;;
    official)
      unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL ;;
  esac
  claude
}
```

cc-switch 在此基础上增加的：`settings.json` 中的配置文件持久化（使非 shell 启动也能生效）、本地代理及协议适配（OpenAI 风格响应 → Anthropic Messages 格式）、每次写入前的配置备份，以及多 CLI 管理。切换后，在 Claude Code 中运行 `/status` 可验证当前活动的基础 URL 和模型。

一个注意事项：该项目受到 API 中继/转售服务商的严重赞助（在 README 中随处可见），在评估预设端点时值得留意——在将密钥路由经过任何中继之前，请先对其进行审查。

**参考来源：**

- [farion1231/cc-switch (GitHub)](https://github.com/farion1231/cc-switch)
- [SaladDay/cc-switch-cli (GitHub)](https://github.com/saladday/cc-switch-cli)
- [CC-Switch 新手指南 (apiyi)](https://help.apiyi.com/en/cc-switch-beginner-guide-en.html)
- [Claude Code 后端切换教程 (ofox)](https://ofox.ai/blog/claude-code-switch-tutorial-2026/)
