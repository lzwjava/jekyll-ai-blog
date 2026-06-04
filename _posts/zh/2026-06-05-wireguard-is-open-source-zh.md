---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WireGuard 是开源的
translated: true
type: note
---

**问题：** WireGuard 是开源的吗？

**答案：**

是的。WireGuard 是免费且开源软件，其 Linux 内核组件基于 GPLv2 许可，其他实现则基于 GPLv2 或其他免费/开源许可。

**官方代码仓库：**

官方代码仓库托管于 git.zx2c4.com（并提供 GitHub 镜像）。主要项目包括：

- **wireguard-linux** — 内核模块（Linux）
- **wireguard-go** — 用户空间实现（Go 语言，可移植）
- **wireguard-windows** — NT 内核驱动（Windows）
- **wireguard-apple** — iOS/macOS
- **wireguard-android** — Android
- **wireguard-tools** — 配置工具（`wg`、`wg-quick`）

该项目由 Jason A. Donenfeld 于 2015 年创建，当前稳定版本为 1.0.20260223（2026 年 2 月）。

您可以直接审计代码——不含任何专有组件。这正是 Tailscale 选择 WireGuard 作为其基础的原因：该协议经过公开审查、实战检验，且可独立验证。

**参考资料：**

- [WireGuard 官方网站](https://www.wireguard.com/)
- [官方代码仓库](https://www.wireguard.com/repositories/)
- [WireGuard GitHub（镜像）](https://github.com/WireGuard)
- [技术白皮书（PDF）](https://www.wireguard.com/papers/wireguard.pdf)
