---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在Ubuntu系统上安装Rust
translated: true
type: note
---

### 在 Ubuntu 22.04 LTS 上安装 Rust

推荐使用官方工具链安装程序 `rustup` 来安装 Rust。这种方法简单直接，支持轻松更新，并适用于 64 位 Ubuntu 22.04 系统。除基础 Ubuntu 环境外，通常无需额外依赖。

#### 详细步骤说明

1. **更新软件包列表**（可选但推荐）：
   ```
   sudo apt update
   ```

2. **使用 rustup 安装 Rust**：
   运行以下命令下载并执行安装脚本：
   ```
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```
   - 这将通过 HTTPS 安全下载脚本
   - 出现提示时选择默认安装选项（按 `1` 并回车）
   - 安装程序会将 Rust 二进制文件添加至 `~/.cargo/bin` 并更新 shell 配置文件（如 `~/.bashrc` 或 `~/.profile`）

3. **重新加载 shell 配置**：
   如需立即生效而无需重启终端：
   ```
   source ~/.cargo/env
   ```
   或直接关闭并重新打开终端

4. **验证安装**：
   检查 Rust 是否安装成功：
   ```
   rustc --version
   cargo --version
   ```
   您将看到类似 `rustc 1.82.0`（或最新稳定版本）及对应的 Cargo 版本信息

#### 补充说明
- **卸载方式**：如需卸载可运行 `rustup self uninstall`
- **更新 Rust**：使用 `rustup update` 获取最新版本
- **开发环境**：建议通过编辑器安装 `rust-analyzer`（如 VS Code 扩展）以获得更好的代码补全
- 默认安装稳定版。如需 nightly 或 beta 版本，可在安装后使用 `rustup install nightly`

若遇到错误（如 curl 未找到），请通过 `sudo apt install curl` 安装

[官方 Rust 安装指南](https://www.rust-lang.org/tools/install)
