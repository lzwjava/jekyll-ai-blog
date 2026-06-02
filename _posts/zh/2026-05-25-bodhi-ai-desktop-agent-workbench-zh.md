---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 菩提AI桌面代理工作台
translated: true
type: note
---

== Bodhi AI ==

Bodhi AI 是一款基于 Tauri 2 构建的桌面应用，作为桌面 AI 代理工作台。它采用三层架构中的“桌面壳”层：

  bodhi  = Tauri 桌面壳（本仓库）
  lotus  = React + Vite 前端 UI（同级仓库 @bigduu/lotus）
  bamboo = Rust 后端运行时（同级仓库，以 bamboo-agent crate 发布在 crates.io）

== 功能说明 ==

一款 AI 代理桌面应用，具备以下能力：
- 规划任务、运行工具、连接 MCP 服务器
- 保持长期运行的上下文（记忆、会话笔记、梦境笔记本）
- 将成功的运行转化为工作流并设置定时任务
- 展示其工作过程（代理循环、工具调用、状态变化均可见）

可以理解为：一款类似 Hermes/Claude Code 风格的代理，但被打包为带有 GUI 的原生桌面应用。

== 技术栈 ==

  语言：     Rust (Tauri 2) + TypeScript (React/Vite)
  后端：     bamboo-agent crate（actix-web HTTP 服务器，以内嵌进程方式运行，端口 9562）
  前端：     lotus（React 独立构建，以静态 dist 形式提供）
  Tauri 插件：dialog、fs、global-shortcut、shell、process、notification、log

== 关键源文件 ==

  src-tauri/src/main.rs          -- 入口点，调用 lib::run()
  src-tauri/src/lib.rs           -- Tauri 构建器、插件、设置、命令
                                    - 注册全局快捷键 Cmd/Ctrl+Shift+Space 用于切换窗口
                                    - 启动内嵌 bamboo HTTP 服务器在 127.0.0.1:9562
                                    - 命令：copy_to_clipboard、proxy config、theme、notifications
  src-tauri/src/embedded/mod.rs  -- 管理内嵌 bamboo-agent WebService 的生命周期
                                    - 从多个候选路径解析静态前端 dist
                                    - 健康检查循环（10 次尝试，间隔 200ms）
  src-tauri/src/app_settings.rs  -- 重新导出 bamboo 路径辅助函数（数据目录、config.json）
  src-tauri/src/command/copy.rs  -- 剪贴板复制命令

== 架构亮点 ==

1. bamboo 后端以内嵌进程方式运行（非 sidecar）——EmbeddedWebService 直接将
   bamboo_agent::server::WebService 包装在 Tauri 应用内部。

2. 同时支持独立运行模式：可单独在端口 9562 运行 bamboo，并独立运行 lotus
   以进行开发/调试。

3. 内部/公开构建模式控制是否显示启动确认对话框。

4. lotus 前端 dist 从多个候选路径解析（环境变量、配置、
   .lotus-dist 目录、macOS 应用包布局）。

5. 版本：2026.4.24，已打标签（最新标签：app-v2026.5.5），通过 GitHub Actions 进行 CI。

== 相关仓库（期望同级目录） ==

  ../bamboo  -- 核心 Rust 代理运行时（本地开发时通过 Cargo.toml 进行补丁引用）
  ../lotus   -- React 前端
