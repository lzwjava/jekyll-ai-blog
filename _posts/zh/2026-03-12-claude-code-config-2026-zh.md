---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude 代码配置指南 2026
translated: true
type: note
---

**问题：** 如何在 Claude Code 中使用此类设置？

**答案：**

您展示的文件是 **Claude Code** 的用户级配置文件（Anthropic 的编码代理/CLI 工具，通常在终端中使用或通过 VS Code 扩展）。

将此文件放置在以下位置：

- `~/.claude/settings.json` (Linux/macOS)
- `%USERPROFILE%\.claude\settings.json` (Windows)

Claude Code 会自动读取此文件（CLI 版本和官方 Anthropic VS Code 扩展在最近版本中均支持）。

您当前的配置文件设置了三项主要内容：

```json
{
  "feedbackSurveyState": {
    "lastShownTime": 1753996737780
  },
  "skipDangerousModePermissionPrompt": true,
  "env": {
    "ANTHROPIC_BASE_URL": "https://v2-as.pincc.ai",
    "ANTHROPIC_AUTH_TOKEN": "sk-8a25bb9202a81c57xx",
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0"
  }
}
```

### 每个设置的作用及其使用方法

- **`env.ANTHROPIC_BASE_URL`**
  更改 Claude Code 连接的 API 端点（而非官方 api.anthropic.com）。
  → 您将其指向反向代理 / 第三方提供商 / 自定义 Anthropic 兼容服务器。

- **`env.ANTHROPIC_AUTH_TOKEN`**
  发送到该自定义端点的 API 密钥 / bearer token。
  → 格式通常以 `sk-` 开头（与官方 Anthropic 密钥相同）。

- **`env.CLAUDE_CODE_ATTRIBUTION_HEADER`** 设置为 `"0"`
  很可能禁用某些提供商强制添加的归属 / “Powered by Claude” 头部或水印。

- **`skipDangerousModePermissionPrompt`: true**
  在使用危险工具（文件写入、shell 命令等）时自动接受 / 跳过确认提示。
  → 对于全自动化工作流很有用，但会增加风险。

### 如何使其生效

1. **正确保存文件**
   确保路径精确为 `~/.claude/settings.json`（如果 `.claude` 文件夹不存在，请创建）。

2. **重启 Claude Code 会话**
   - 终端：关闭并重新打开终端，然后再次运行 `claude`
   - VS Code 扩展：重新加载 VS Code 窗口（Windows/Linux: `Ctrl+R`，Mac: `Cmd+R`）或重启扩展

3. **测试它**
   在终端中运行：

   ```
   claude
   ```

   或使用 VS Code 侧边栏 / 命令面板 → "Claude Code"。

   如果配置正确，您将不会看到登录提示，并且它会连接到 `https://v2-as.pincc.ai` 而非直接连接 Anthropic。

### 注意事项 / 常见问题（2026 状态）

- 某些较旧版本的 VS Code 扩展忽略 `~/.claude/settings.json` → 确保使用最近版本的 **官方 Anthropic Claude Code** 扩展。
- 如果仍提示登录 → 尝试在启动前临时在 shell 中设置相同变量（`export ANTHROPIC_BASE_URL=...`），或检查 GitHub issues 以获取您确切版本的信息。
- 许多代理提供商（LiteLLM、AskSage、302.ai、自定义网关等）正是使用此 settings.json + `ANTHROPIC_BASE_URL` 模式。

这是 Claude Code 中使用自定义端点 / 密钥 / 行为调整的标准且推荐方式。

**参考资料：**

- [Claude Code settings documentation](https://code.claude.com/docs/en/settings)
- [AskSage Claude Code integration guide](https://docs.asksage.ai/docs/integrations/claude-code.html)
- [GitHub issue – VS Code extension custom endpoint support](https://github.com/anthropics/claude-code/issues/8727)
- [GitHub issue – regression with custom ANTHROPIC_BASE_URL](https://github.com/anthropics/claude-code/issues/9010)
