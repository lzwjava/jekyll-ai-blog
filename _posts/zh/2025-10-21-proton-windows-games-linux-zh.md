---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Proton实现Linux系统运行Windows游戏
translated: true
type: note
---

### 什么是 Proton？

Proton 是由 Valve 开发的兼容层，直接集成在 Steam 客户端中，能够让仅支持 Windows 的游戏和应用程序在基于 Linux 的系统上无缝运行。它本质上是 Steam 内置的 "通过 Proton 实现 Linux 兼容" 解决方案，让用户无需安装 Windows 或配置双系统即可畅玩海量 PC 游戏库。

#### 运行原理

- **核心技术**：Proton 基于 Wine 构建，并通过 Valve 的专项优化增强，包括通过 DXVK 和 VKD3D 实现 DirectX 到 Vulkan 的转译，使其在游戏运行方面更具效率。
- **Steam 集成**：在 Steam 中只需右键点击游戏，进入属性 > 兼容性，勾选"强制使用特定 Steam Play 兼容性工具"并选择 Proton 版本即可。Steam 会自动处理后续流程——如需则下载 Proton，并像启动原生 Linux 游戏般运行游戏。
- **版本管理**：Proton 提供实验版和稳定版。截至 2025 年，最新稳定版已支持 ProtonDB 社区兼容性报告中数千款"白金"或"黄金"评级的游戏。

#### 为 Linux 游戏带来的优势

- **易用性**：多数游戏无需手动配置，在 Steam 中即插即用。
- **性能表现**：由于特别优化，在 Linux 系统上的性能往往媲美甚至超越原生 Windows 环境，尤其在 AMD GPU 硬件上。某些游戏在 Linux 掌机的运行表现甚至优于同配置 Windows 设备。
- **生态影响**：Proton 使 Linux 成为可行的游戏平台，不仅驱动了 Steam Deck 等设备，更推动了开源技术在游戏领域的广泛采用。

配置时请确保 Linux 发行版已安装 Vulkan 驱动。若遇问题，可查阅 ProtonDB 获取游戏专属解决方案。

#### 参考资源

- [Valve 的 Proton GitHub 仓库](https://github.com/ValveSoftware/Proton)
- [Steam 社区指南：Proton 入门](https://steamcommunity.com/app/221410/discussions/0/1636417404917541481/)
- [Rocky Linux 文档：使用 Proton 在 Linux 上游戏](https://docs.rockylinux.org/10/desktop/gaming/proton/)
