---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 检查 Mac 上的 Codex 安装方法
translated: true
type: note
---

**Question:** 如何确定在 Mac 上是通过 npm 全局安装还是通过 Homebrew cask 安装的 Codex？

**Answer:**

您目前的安装版本是 **Homebrew cask** 版本。

以下是确定的原因以及如何确认使用了哪种方法：

- `codex --version` 的输出显示：
  `codex-cli 0.36.0`
  官方 OpenAI Codex CLI 的近期版本（特别是切换到基于 Rust 的 native binary 之后）会以这种精确格式显示版本：`codex-cli X.Y.Z`。这与两种安装方法的输出都匹配，因此仅凭版本字符串无法区分它们。

- 在 macOS 上区分两者的可靠方法：

  1. **检查哪个命令指向该 binary**（最确切的方法）：
     运行：

     ```
     which codex
     ```

     - 如果结果类似于：
       `/opt/homebrew/bin/codex` 或 `/usr/local/bin/codex` (Homebrew 路径)
       → **您正在使用 Homebrew cask 版本**。

     - 如果结果类似于：
       `/usr/local/bin/codex`（但实际是从 `~/.npm-global/bin/codex` 或类似路径 symlinked 过来）或 `/Users/yourname/.nvm/versions/node/vXX.XX.XX/bin/codex`
       → **您正在使用 npm 版本**。

  2. **检查 Homebrew cask 状态**：

     ```
     brew list --cask | grep codex
     ```

     - 如果显示 `codex` → 通过 Homebrew cask 安装。

     或者运行：

     ```
     brew info --cask codex
     ```

     如果已安装，您将看到包括版本和 "Installed" 状态在内的详细信息。

  3. **检查 npm 全局包**：

     ```
     npm list -g @openai/codex
     ```

     - 如果显示该 package（带有版本号）→ 通过 npm 安装。
     - 如果显示 "empty" 或未找到 → 未通过 npm 安装。

在实际操作中，大多数在 macOS 上能看到清晰的 `codex` 命令且没有路径问题，同时在使用 Homebrew 的用户，往往倾向于通过 `brew install --cask codex` 安装，尤其是该项目官方将其推荐为两个同等选项之一。

您的版本 (0.36.0) 似乎是 2025 年末或 2026 年初的旧版本 —— 建议考虑更新以获取最新的 features 和 models：

- 对于 Homebrew：`brew upgrade --cask codex`
- 对于 npm：`npm install -g @openai/codex@latest`

**References:**

- [https://www.npmjs.com/package/@openai/codex](https://www.npmjs.com/package/@openai/codex)
- [https://formulae.brew.sh/cask/codex](https://formulae.brew.sh/cask/codex)
- [https://github.com/openai/codex](https://github.com/openai/codex)
- [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
