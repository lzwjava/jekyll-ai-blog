---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tabby终端：面向资深开发者的工具
translated: true
type: note
---

**问题：** Terminus 终端应用是什么？为什么一些资深开发者会使用它？

**回答：**

你可能想说的是 **Tabby**（原名 Terminus）——它已经更名了。这是一款基于 Electron + Web 技术的开源跨平台终端模拟器。

**GitHub：** <https://github.com/Tabby/tabby>

### 它是什么

- 基于 Electron 的终端（类似 VS Code 的终端，但独立运行）
- 跨平台：macOS、Windows、Linux
- 内置 SSH 客户端，带有连接管理器
- 插件生态系统（使用 TypeScript/Angular 编写）
- 支持串口连接（嵌入式/硬件开发者非常喜欢此功能）

### 为什么一些资深开发者使用它

| 功能 | 为什么重要 |
|---|---|
| **内置 SSH 管理器** | 无需手动维护 `~/.ssh/config` 即可保存和管理连接 |
| **串口支持** | 终端中少见的功能——适用于固件/嵌入式开发 |
| **跨平台一致性** | Windows 开发者无需借助 WSL 即可获得类似 Unix 的终端体验 |
| **插件 API** | 使用 TypeScript 进行扩展——部分开发者会在此基础上构建内部工具 |
| **分屏 + 标签页** | 现已成标配，但实现得相当出色 |

### 针对你个人的客观看法

既然你已经在使用 **Warp**——Tabby 并没有明显优于你当前的工作流程。Warp 具备：

- AI 命令补全
- 基于块的输出（对于 LLM/代理输出解析来说好用得多）
- 更出色的 macOS 原生体验（非 Electron）

Tabby 真正的优势领域是 **Windows 用户** 以及 **SSH 密集型工作流**，即你希望拥有一款统一的终端 + 连接管理器，而无需使用 PuTTY 或单独的 SSH GUI。

那些对它推崇备至的资深开发者，通常处于混合操作系统环境，或从事嵌入式/串口相关工作。对于 macOS 上的纯 AI 工程而言，Warp 甚至 iTerm2 + tmux 的表现更胜一筹。
