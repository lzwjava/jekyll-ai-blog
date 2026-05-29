---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codex CLI 安装与更新说明
translated: true
type: note
---

以下是您找到的内容：

=== 当前 Codex 安装情况 ===

位置：       /opt/homebrew/bin/codex（指向 npm 全局安装的符号链接）
已安装：      @openai/codex@0.128.0
最新 npm 包： @openai/codex@0.135.0
你落后了 7 个版本。

=== 如何更新 ===

在此 Mac 上更新 CLI 的最简单方法：

    npm install -g @openai/codex@latest

这将拉取 0.135.0 版本并替换 /opt/homebrew/bin/codex 处的二进制文件。

=== 架构概览 ===

位于 /Users/lzwjava/projects/codex 的 codex 仓库是一个单体仓库，包含：

1. npm 包 (@openai/codex) — 打包 Rust 二进制文件的 TypeScript CLI
2. Rust 工作区 (codex-rs/) — 实际的二进制源代码
   - codex-rs/cli/ — `codex` 二进制文件（Rust）
   - codex-rs/tui/ — `codex-tui` 二进制文件（基于 ratatui 的 TUI）
   - 100+ 内部 crate（core、config、mcp-server、tools 等）

npm 包为每个平台（darwin-arm64、linux-x64 等）提供了预构建的 Rust 二进制文件，因此 `npm install -g` 会同时安装 JS 包装器和原生的 Rust codex 二进制文件。

=== 从源码构建（可选，用于开发） ===

如果你想从本仓库本地构建 Rust 二进制文件：

    cd /Users/lzwjava/projects/codex
    cargo build -p codex-cli        # 构建 codex 二进制文件
    cargo build -p codex-tui        # 构建 codex-tui

或者通过 just 命令：
    just codex                      # cargo run --bin codex
    just test -p codex-tui          # 运行 TUI 测试

需要我现在运行 `npm install -g @openai/codex@latest` 来更新吗？