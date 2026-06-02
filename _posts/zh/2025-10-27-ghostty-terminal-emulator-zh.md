---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Ghostty：快速跨平台终端模拟器
translated: true
type: note
---

Ghostty 是一款跨平台终端模拟器，专为追求速度、功能丰富以及 macOS 与 Linux 系统原生集成而设计（Windows 支持正在开发中）。它主要采用 **Zig** 构建——这是一种专注于安全性、性能与简洁性的现代系统编程语言，而非您询问的 Rust。

### 核心实现细节
- **架构设计**：共享核心（负责终端模拟、渲染及大部分逻辑）采用 Zig 编写，通过底层控制实现高性能，并支持 Metal（macOS）或 Vulkan/OpenGL（跨平台）的 GPU 加速。
- **平台适配层**：为实现原生体验，使用平台专用工具包构建 GUI：
  - macOS：采用 Swift/AppKit 处理窗口管理与界面。
  - Linux：采用 GTK 处理窗口管理。
  - 通过 Zig 编写的共享渲染管线实现整体整合。
- **设计亮点**：
  - 极速启动与渲染（可无延迟处理大体积输出）。
  - 支持连字字体、表情符号与高级排版功能。
  - 支持 Lua 脚本配置实现功能扩展。
  - 无冗余设计——在保持极简主义的同时集成标签页、搜索、OSC 52 剪贴板等核心功能。
- **开发理念**：由 Mitchell Hashimoto（HashiCorp 创始人）创建，强调正确性与运行效率，摒弃了 xterm 等传统终端常见的兼容性妥协方案。本项目采用 MIT 许可证开源。

若您有兴趣参与开发或二次创作，可访问 GitHub 代码库获取 Zig 代码与构建指南（需 Zig 0.13+ 环境）。

### 参考资源
- [Ghostty GitHub 代码库](https://github.com/ghostty-org/ghostty)
- [Ghostty 技术解读（Mitchell Hashimoto 博客）](https://mitchellh.com/writing/ghostty-and-useful-zig-patterns)
- [Ghostty 1.0 版本发布说明](https://dansasser.me/posts/ghostty-1-0-a-terminal-emulator-built-for-speed-features-and-native-integration/)
