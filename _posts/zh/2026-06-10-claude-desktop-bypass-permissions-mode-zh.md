---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude桌面版绕过权限模式
translated: true
type: note
---

**问题：** 在 Claude macOS 桌面应用中，没有像 Claude Code CLI 中那样的 `--dangerously-skip-permissions` 标志——它会持续提示“允许一次 / 始终允许”代码操作。如何在桌面应用中启用绕过模式？

**答案：**

桌面应用确实有等效功能，但需要通过设置开关启用（因为没有可传递的 CLI 标志）：

1. 打开 Claude 应用 → 点击左下角的个人资料菜单 → **设置** → **Claude Code** → 开启 **允许绕过权限模式**
2. 重新启动或打开一个新的 Claude Code 会话，然后使用发送按钮旁边的模式选择器，选择 **绕过权限**。自动和绕过权限模式只有在桌面设置中启用后才会出现在该选择器中。
3. 你也可以为特定项目文件夹设置按文件夹的权限模式为 `bypassPermissions`。

需要注意的几个问题：

- **已知 bug。** 目前此功能不稳定。Issue #62907（Desktop 1.9255.x，嵌入式 Claude Code 2.1.149）报告称，即使启用了开关，桌面启动器仍会以 `--permission-mode acceptEdits` 生成子进程 `claude`，而从未传递 `--dangerously-skip-permissions`，因此切换到绕过模式会失败，提示“无法将权限模式设置为 bypassPermissions，因为会话未使用 --dangerously-skip-permissions 启动”。Issue #29026 还报告称，`~/.claude/settings.json` 中的 `permissions.allow` 规则和 `defaultMode: "bypassPermissions"` 完全被桌面应用忽略。如果你遇到此问题，请先更新应用——如果问题仍然存在，CLI 是更可靠的选择。

- **设置中的 `defaultMode`。** 对于 CLI（理论上桌面应用修复后也适用），持久化等效配置如下：

  ```json
  // ~/.claude/settings.json
  {
    "permissions": {
      "defaultMode": "bypassPermissions"
    }
  }
  ```

  这相当于持久化地以 `--dangerously-skip-permissions` 启动——在用户级别设置一次后，每个新会话都会以绕过模式启动。

- **考虑改用 `auto` 模式。** 既然你使用的是 Opus 级别的模型，自动模式可以让 Claude 在没有常规权限提示的情况下执行操作——一个独立的分类器模型会审查操作，阻止诸如 `curl | bash`、强制推送、生产部署或泄露敏感数据等行为，而本地文件操作和依赖安装则可以自由运行。这样能消除约 95% 的提示疲劳，同时不会完全放弃安全护栏。启用方式相同：设置 → Claude Code，然后在模式选择器中选择 **自动**。对于在你的 MI300X 计算实例或工作站上的无人值守运行，在一次性环境中使用绕过模式是可行的；而在日常使用的 M2 Air 上，自动模式是更好的权衡。

**参考：**

- [选择权限模式 — Claude Code 文档](https://code.claude.com/docs/en/permission-modes)
- [Claude Desktop 未向子进程传递 --dangerously-skip-permissions (Issue #62907)](https://github.com/anthropics/claude-code/issues/62907)
- [桌面应用忽略 settings.json 中的权限设置 (Issue #29026)](https://github.com/anthropics/claude-code/issues/29026)
- [我们如何构建 Claude Code 自动模式 — Anthropic](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Claude Code Desktop 绕过权限 — Kanaries](https://docs.kanaries.net/topics/AICoding/claude-code-desktop-bypass-permissions)