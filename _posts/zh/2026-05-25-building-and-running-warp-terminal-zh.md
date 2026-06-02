---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建和运行 Warp 终端
translated: true
type: note
---

== Warp 构建摘要 ==

前置条件
-------------
- Rust 1.92.0（通过 Homebrew 安装）
- protoc（通过 `brew install protobuf` 安装）
- Xcode 命令行工具（已存在）

构建命令
--------------
cd /Users/lzwjava/projects/warp

# 检查（仅类型检查，约2分钟）
cargo check --bin warp-oss --features gui

# 构建（编译二进制，约4.5分钟）
cargo build --bin warp-oss --features gui

# 运行
./target/debug/warp-oss

发生了什么
-------------
1. cargo 从 Cargo.lock 解析了约500多个依赖项
2. 从 crates/ 目录编译了65多个本地包
3. 链接了 macOS 框架（Cocoa, Metal, CoreFoundation）
4. 生成单个二进制文件：target/debug/warp-oss（调试版721 MB，通过 strip 可减小发布版体积）

架构
------------
- 语言：Rust
- UI 框架：自定义 warpui/warpui_core（GPU 加速，Metal 后端）
- 终端后端：Alacritty 的 VT 解析器 + 自定义 PTY 层
- 异步运行时：Tokio
- 构建系统：包含65多个包的 Cargo 工作空间
- 二进制文件：warp-oss（开源渠道）或 warp（内部渠道）

关键包
----------
warp_terminal  - PTY、Shell 集成、终端状态
warpui         - GPU 渲染、窗口管理、输入
ai             - LLM 集成、代理功能
mcp            - 模型上下文协议支持
editor         - 代码编辑器组件
vim            - Vim 模式支持

构建配置文件
--------------
cargo build                          # 调试版（721 MB，未优化）
cargo build --release                # 发布版（优化，更小）
cargo bundle --bin warp-oss --features gui  # macOS 的 .app 包

官方脚本
----------------
./script/bootstrap --skip-common-skills -y  # 安装所有依赖
./script/run                                 # 构建并以 .app 形式启动
./script/presubmit                           # 格式化 + Clippy + 测试
