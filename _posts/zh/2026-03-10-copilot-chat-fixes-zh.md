---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot 聊天修复指南
translated: true
type: note
---

**问题：** 为什么在 VS Code 中的 GitHub Copilot 有时不允许发送消息，只有打开新的 Copilot 窗口后才能工作？

**答案：**

这是 VS Code 中 GitHub Copilot Chat 扩展的一个已知且广泛报告的 bug/问题。以下是对根本原因以及修复方法的全面解释。

---

## 根本原因

### 1. 扩展未能激活（最常见）

当您点击 Send Chat Feedback 时，状态栏会显示“Activating Extensions...”的消息，但什么都没发生——这表明 Copilot Chat 扩展处于“尚未激活”状态。这意味着扩展进程在 VS Code 启动时没有完全初始化。打开新窗口会强制启动一个全新的扩展主机进程，这就是为什么在新窗口中有效的原因。

### 2. 扩展状态损坏 / 会话过期

禁用 GitHub.copilot-chat 扩展、重新加载窗口，然后再次启用它，已被发现能为许多用户解决问题。这指向内存中过时或损坏的扩展状态——一个进入损坏状态但未完全崩溃的会话。

### 3. 认证 / 账户令牌过期

转到 Accounts（左下角）→ “Manage extension account preferences” → “Github Copilot Chat” → 重新选择您的账户，已为一些用户解决问题。这是因为认证令牌在会话间静默过期或出现混淆。

### 4. 聊天输入中粘贴文本的 Bug

当光标位于上下文引用的开头时粘贴文本，会导致某些问题，从而无法发送提示。这是 Copilot Chat 扩展中的一个特定 bug，它会损坏聊天输入状态，而不会向用户显示明显的错误。

### 5. 扩展版本与 VS Code 不匹配

您必须使用最新版本的 Visual Studio Code，并且必须安装最新版本的 GitHub Copilot 和 GitHub Copilot Chat 扩展。过时的 VS Code 版本可能会导致扩展激活静默失败。

### 6. 免费计划月度限制的过期缓存

如果您使用免费计划，后端可能会读取旧的过期数据，并注册您已经用完了本月的免费额度，即使月份才刚开始。UI 会冻结，而不会清楚说明消息无法发送的原因。

---

## 修复方法（按顺序尝试）

**快速修复（无需重新安装）：**

1. **重新加载 VS Code 窗口** — 按 `Ctrl+Shift+P` → 输入 `Developer: Reload Window` → Enter。这是修复最快的方法。
2. **禁用 → 重新加载 → 重新启用 Copilot Chat 扩展** — 转到 Extensions 面板，禁用 `GitHub Copilot Chat`，重新加载窗口，然后重新启用它。
3. **重新选择您的 GitHub 账户** — 转到 Accounts（左下角图标）→ “Manage extension account preferences” → “GitHub Copilot Chat” → 重新选择您的账户。
4. **退出登录并重新登录** — 退出所有 GitHub 账户并重新登录，已为一些用户解决问题。
5. **检查 Output 日志** — 在 VS Code 的 Output 窗格中检查 “Window” 类别下的错误消息，以了解发送按钮为什么不起作用。

**深度修复（如果上述无效）：**

6. **更新 VS Code** — 运行 `Help → Check for Updates`。
7. 转到 Extensions，如果 GitHub Copilot 显示蓝色的 “Reload Required” 按钮，请按它。
8. **删除 `.vscode` 配置文件夹** — 删除 `.vscode` 文件夹（例如 Windows 上的 `C:\Users\<YOUR USER>\.vscode`）并重启，已为一些用户解决问题。
9. **完全重新安装** — 完全卸载 VS Code 并全新重新安装。

---

## 为什么新窗口能修复它？

打开新的 VS Code 窗口会创建一个**全新的扩展主机进程**。旧窗口有一个损坏/卡住的扩展运行时（认证状态、激活状态或输入状态损坏），而新窗口从头干净启动一切——因此 Copilot 正确激活，聊天输入再次工作。

**参考资料：**

- [GitHub Issue: Can't send messages to copilot chat #941](https://github.com/microsoft/vscode-copilot-release/issues/941)
- [GitHub Issue: Unable to submit chats #565](https://github.com/microsoft/vscode-copilot-release/issues/565)
- [GitHub Issue: Missing send button in copilot chat #262645](https://github.com/microsoft/vscode/issues/262645)
- [GitHub Discussion: Copilot Chat Not Working Even After Reinstalling VS Code](https://github.com/orgs/community/discussions/167353)
- [VS Code Copilot FAQ – Official Troubleshooting](https://code.visualstudio.com/docs/copilot/faq)
- [Tim Taurit Blog: Send and Dispatch button broken diagnosis](https://taurit.pl/vs-code-github-copilot-send-and-dispatch-button-not-working/)
