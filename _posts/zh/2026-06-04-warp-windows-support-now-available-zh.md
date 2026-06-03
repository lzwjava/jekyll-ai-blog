---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp Windows 支持现已可用
translated: true
type: note
---

问题：为什么 Warp 不能在 Windows 上运行？

**答案：**

简短回答：**现在可以了。** Warp 于 2025 年 2 月正式推出 Windows 支持，支持 PowerShell、WSL 和 Git Bash，兼容 x64 和 ARM64 架构。

但了解“为何花了这么长时间”的历史背景也很有价值：

## 延迟的技术原因

**图形渲染：** Warp 是用 Rust 编写的完全原生应用，采用直接 GPU 渲染，而非基于 Electron 或 VS Code 的包装器。这意味着团队需要为三种不同的图形 API 实现平台特定的图形调用：
- macOS：Metal
- Linux：Vulkan
- Windows：Direct3D 12

每种 API 的事件处理、驱动集成和性能特性各不相同。构建一个能跨这三种平台无缝扩展、同时不牺牲性能的统一终端绝非易事。

**Shell 复杂性：** Windows 支持需要“大量时间”来与 PowerShell、Git Bash 和 WSL 无缝对接，方式类似于 Windows Terminal，让用户能在不同的 shell 环境中启动会话。这不仅仅是生成进程——还需要管理 ConPTY（伪控制台）、处理 Windows 特有的 shell 问题，并与 Windows 包管理器（WinGet）集成。

**用户需求与工程投入的权衡：** macOS + Linux 覆盖了核心开发者群体（终端工具中倾向于 Unix/Linux 的偏好）。Windows 的 shell 环境较为碎片化（PowerShell、WSL、Git Bash），每种都需要略有不同的处理方式。团队可能做了经过权衡的决策：先为 80% 的用户最大化价值，等到架构足够稳固后再攻克 Windows。

## 这对你意味着什么

如果你在使用 Windows 或正考虑使用，Warp 现在是一个可行的终端选择。基于 Rust 的方法为你带来：
- 零开销 GPU 加速（无 Electron 臃肿）
- 跨平台相同的 AI 原生功能
- 与 WSL 原生集成（如果你需要在 Windows 上进行 Linux 开发工作，这很有用）

依然使用 macOS + Ubuntu？你处于最佳状态——Warp 已在这些平台上经过多年实战测试，拥有最深入的功能一致性。

---

参考：

- [Warp 登陆 Windows](https://www.warp.dev/blog/launching-warp-on-windows)（2025 年 2 月 26 日）
- [The New Stack：Warp AI 终端 Windows 版发布](https://thenewstack.io/warp-launches-ai-first-native-terminal-app-for-windows/)（2025 年 2 月 26 日）
- [Warp 2025 年度回顾](https://www.warp.dev/blog/2025-in-review)（2025 年 12 月 30 日）