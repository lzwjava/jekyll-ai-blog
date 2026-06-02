---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot CLI 无危险模式
translated: true
type: note
---

Question: 如何让 Copilot CLI 绕过权限检查，类似于 Claude Code 的 “dangerous” 模式？

Answer:

你 **无法安全或官方地绕过 GitHub Copilot CLI 中的权限检查**。Copilot 的设计初衷是 **执行系统和 cloud security 策略**，因此它会阻止需要提权、访问敏感文件或进行不安全系统更改的操作。它 **没有内置像 Claude Code 样式的 “dangerous” 模式** 来允许执行任意操作。

以下是几个关键点：

1. **Copilot CLI vs. Claude Code**

   * Claude Code 有时会在沙箱化的 “execute commands” 模式下使用。一些用户尝试通过脚本将其与具有完整系统权限的命令结合运行。
   * Copilot CLI 主要是一个 **code suggestion tool**，而不是远程执行引擎。它 **无法运行超出你当前用户权限的任意系统命令**。

2. **安全的替代方案**

   * 如果你需要与系统文件交互或需要提权的脚本：

     * 通过 Copilot 编写脚本。
     * **手动运行它**，使用 `sudo` 或提供适当的权限。
   * 示例：

     ```bash
     % copilot
     > Write a bash script to delete old log files
     ```

     然后保存并运行：

     ```bash
     sudo bash cleanup_logs.sh
     ```

3. **尝试绕过的风险**

   * 试图通过 hack Copilot CLI 来绕过权限可能会导致：

     * 损坏你的安装程序。
     * 危害系统的安全性。
     * 违反 GitHub 的 terms of service。

4. **推荐做法**

   * 将 Copilot 视为一个 **safe coding assistant**。
   * 如果你的目标是进行系统级更改，请将其与 **手动提权执行 (manual elevated execution)** 相结合。
   * **不要** 尝试从内部禁用权限检查 —— CLI 不支持这样做，而且不安全。

简而言之：Copilot 不能也不应该被设置为自动执行具有不安全权限的命令。如果你想要像 Claude Code 那样的完全 “dangerous execution”，你需要一个 **具有直接命令执行功能的 custom local LLM setup**，而不是使用 Copilot。

---

如果你需要，我可以展示一种 **通过 Copilot suggestions + sudo scripts 来模拟 Claude Code 式命令执行的安全方法**，这样你可以在不破坏安全性的情况下获得类似的功能。

需要我展示那个方法吗？
