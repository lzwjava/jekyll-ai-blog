---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp的核心技术栈
translated: true
type: note
---

以下是 Warp 使用的主要库：

== 主要外部依赖 ==

GPU 与渲染
----------------
wgpu 29.0.1        - GPU 抽象层（macOS 上使用 Metal，Linux 上使用 Vulkan）
metal               - Apple Metal API 绑定（macOS GPU 渲染）
cocoa 0.26.0        - macOS Cocoa 框架绑定
core-foundation     - macOS Core Foundation（窗口、事件、字体）
objc2-app-kit       - macOS App Kit 绑定
font-kit            - 字体加载与光栅化（Warp 分支版本）

异步与网络
------------------
tokio 1.47.1        - 异步运行时（核心支柱）
hyper 1.6.0         - HTTP 客户端/服务器
reqwest 0.13        - HTTP 客户端（API 调用、AI 端点）
axum 0.8.4          - HTTP 服务器框架
tower 0.5.2         - 服务中间件
rustls              - TLS（多数场景替代 OpenSSL）
actix-web           - 附加 HTTP 服务器
prost               - Protobuf 序列化（gRPC API）

数据与存储
--------------
serde               - 序列化框架
serde_json          - JSON
diesel 2.3.8        - SQLite ORM（持久化层）
libsqlite3-sys      - SQLite 绑定
tantivy 0.26.0      - 全文搜索引擎（命令面板、搜索）
git2                - Git 仓库操作

终端与文本
---------------
syntect             - 语法高亮
arborium-*          - 基于 Tree-sitter 的解析器（30+ 种语言）
regex               - 正则表达式

AI 与认证
---------
oauth2 5.0.0        - OAuth2 认证
firebase            - Firebase 认证集成
sentry              - 错误追踪与崩溃报告

工具库
---------
clap 4.5            - CLI 参数解析
chrono              - 日期/时间处理
uuid                - UUID 生成
image 0.25.9        - 图像处理
nix 0.26.4          - Unix 系统调用（信号、进程管理）
anyhow              - 错误处理
log                 - 日志门面

== 架构模式 ==

- 通过 wgpu 实现的 GPU 加速 UI（而非原生工具包控件）
- 自定义渲染管线（类似游戏引擎）
- 异步优先，基于 Tokio
- SQLite 用于本地持久化
- Tantivy 用于快速搜索
- Tree-sitter 用于代码理解
- Protobuf/gRPC 用于后端通信
