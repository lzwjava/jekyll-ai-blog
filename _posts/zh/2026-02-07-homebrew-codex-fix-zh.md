---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Homebrew Codex 二进制文件冲突
translated: true
type: note
---

**Question:** 为什么在 macOS 上执行 `brew install --cask codex` 会失败，并提示错误 "It seems there is already a Binary at '/opt/homebrew/bin/codex'"？该如何修复？

**Answer:**

出现这个错误的原因是 **Homebrew 检测到在 `/opt/homebrew/bin/codex` 路径下已经存在一个 `codex` Binary**（这是 Apple Silicon Mac 上 Homebrew 链接 Binary 的标准位置）。为了避免意外破坏你当前的配置，Homebrew 的 Cask 安装程序会拒绝覆盖或替换该处已有的文件。

在你的案例中，最常见的原因（考虑到你之前的 `codex --version` 显示的是 `codex-cli 0.36.0`）是你 **之前通过 npm 安装过 Codex** (`npm install -g @openai/codex`)。这会将它的 Binary 放置在全局 npm bin 目录下（在 Apple Silicon 上，如果使用 Homebrew 安装的 Node，通常就是 `/opt/homebrew/bin`；或者在 `~/.npm-global/bin` 中并带有 Symlink）。随后当你尝试使用 Homebrew Cask 方式安装时，由于两种方法都试图在同一路径管理同一个命令名 (`codex`)，从而产生了冲突。

### 如何确认当前的安装来源

执行：

```bash
which codex
```

- 如果显示 `/opt/homebrew/bin/codex` → 很可能来自 npm (Symlinked) 或者是一个旧的/未完成的 Homebrew 安装。
- 执行 `ls -l /opt/homebrew/bin/codex` 查看它是否是一个 Symlink（如果指向一个 npm 路径，则说明是 npm install 安装的）。

### 推荐的解决方案（任选其一）

1. **继续使用 npm（如果你更倾向于 npm 生态，这是最简单的）**
   - 首先卸载尝试安装的 Cask（如果存在部分安装）：

     ```bash
     brew uninstall --cask codex
     ```

   - 将现有的 npm 版本更新到最新（截至 2026 年 2 月，版本通常在 0.9x 范围内）：

     ```bash
     npm install -g @openai/codex@latest
     codex --version   # 应该显示类似 0.98.0 或更高版本
     ```

2. **切换到 Homebrew Cask（许多 macOS 用户的推荐做法，可避免 npm/Node 依赖）**
   - 首先，移除冲突的 Binary（极有可能来自 npm）：

     ```bash
     npm uninstall -g @openai/codex
     ```

     - 如果该 Binary 仍然存在，手动删除 Link：

       ```bash
       rm /opt/homebrew/bin/codex
       ```

       （注意：仅当你确定它来自 npm 且不再需要时才执行此操作。）
   - 现在重试 Cask 安装：

     ```bash
     brew install --cask codex
     ```

   - 安装应该会成功，并在 `/opt/homebrew/bin/codex` 放置一个新的 Binary。
   - 验证：

     ```bash
     codex --version   # 预期会看到一个较新的基于 Rust 的版本，如 0.98.0+
     ```

3. **彻底清理并重新通过一种方式安装**
   - 卸载两者：

     ```bash
     brew uninstall --cask codex   # 如果未安装则忽略
     npm uninstall -g @openai/codex
     rm -f /opt/homebrew/bin/codex   # 如果 Symlink/Binary 仍在，强制移除
     ```

   - 然后通过你首选的方法安装（npm 或 brew --cask）。

**备注：**

- 官方文档目前将 `npm i -g @openai/codex` 作为主要的安装方式，Homebrew 作为备选。
- 在最近的版本中（约 0.5x 之后），两种方法安装的都是相同的基于 Rust 的 Codex CLI Binary，因此功能是完全一致的。
- 切换安装方法后，你可能需要重新进行身份验证（`codex login`）或重新配置相关设置。
- 你的 Proxy 设置 (127.0.0.1:7890) 已被成功检测并用于下载，因此这并非导致问题的原因。

**参考资料：**

- [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
- [https://github.com/openai/codex](https://github.com/openai/codex)
- [https://www.npmjs.com/package/@openai/codex](https://www.npmjs.com/package/@openai/codex)
- [https://github.com/openai/codex/issues/5607](https://github.com/openai/codex/issues/5607)（相关的 Homebrew Formula 与 Cask 的混淆问题，尽管你的案例是 Binary 冲突）
- [https://formulae.brew.sh/cask/codex](https://formulae.brew.sh/cask/codex)
