---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 菩提AI集成阻塞修复
translated: true
type: note
---

以下是完整的说明：

== Bodhi AI 是什么 ==

由 bigduu 开发的 Tauri 2 桌面 AI 智能体工作台。三层架构：
  bodhi  = Tauri 外壳（此仓库，/Users/lzwjava/projects/Bodhi-AI）
  lotus  = React+Vite 用户界面（zenith 仓库中的子模块）
  bamboo = Rust 智能体运行时（crate: bamboo-agent，747 个依赖，基于 actix-web，端口 9562）

功能：包含 28 个工具的智能体循环、会话管理、记忆/梦想笔记本、工作流、MCP 集成、技能商店、全局快捷键（Cmd+Shift+Space）。

== 我们做了什么 ==

1. 克隆了 zenith 单体仓库（<git@github.com>:bigduu/Zenith.git）→ ~/projects/zenith
2. 初始化了子模块（bamboo, lotus, bodhi, pavilion, bodhi-server）
3. 创建了符号链接：~/projects/lotus → zenith/lotus，~/projects/bamboo → zenith/bamboo
4. 在 Bodhi-AI 和 lotus 中分别执行 npm install
5. 首次 Rust 构建：747 个 crate，耗时 2 分 05 秒
6. 应用成功启动 - Tauri 窗口打开，后端在 127.0.0.1:9562 启动

== 当前阻塞点：LLM 提供者配置 ==

应用可以启动，但智能体对话失败。有两个问题：

1. 配置覆盖：应用在启动时重新生成 provider_instances，使用新的 UUID 并重置为 gemini 类型，忽略我们对 config.json 的编辑。我们的 OpenRouter 配置被覆盖。

2. Gemini API 拒绝：即使配置了 Gemini，Google 的 API 拒绝 bamboo 的工具定义，因为工具定义在 JSON Schema 中包含了 additionalProperties，而 Gemini 不支持此字段。

配置文件位置：~/.bamboo/config.json
数据目录：~/.bamboo/（会话、技能、日志、metrics.db）

== 需要修复的内容 ==

方案 A：修复 bamboo 的 Gemini 提供者，在发送到 Google API 之前去除 additionalProperties（修改 provider_factory.rs 或 Gemini 提供者的代码）

方案 B：弄清楚为什么 config.json 在启动时被覆盖并阻止这种行为，以便 OpenRouter 配置能够持久保存

方案 C：通过 Bodhi AI 用户界面设置来配置提供者（假设设置向导能正确写入配置）

应用本身已完全构建并可运行——只是 LLM 集成需要一个能正常工作的提供者配置。
