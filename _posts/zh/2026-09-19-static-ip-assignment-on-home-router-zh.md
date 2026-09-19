---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 家用路由器静态IP分配
translated: true
type: note
---

以下是家用路由器在带有交换机的情况下如何设置静态IP的清晰示意图：---

**问题：** 如何让带有交换机和Wi-Fi的家用路由器上的IP地址保持静态且稳定？

**回答：**

有两种主要方法。**方法A（推荐）** 在路由器上完成；**方法B** 在每台设备上完成。

---

**方法A — DHCP保留（最佳选择）**

路由器继续自动分配IP，但会根据设备的MAC地址，始终将*相同*的IP分配给同一台设备。设备无需重新配置。

步骤（适用于大多数路由器——TP-Link、ASUS、Netgear等）：

1. 打开路由器管理面板——通常在浏览器中输入 `http://192.168.1.1` 或 `http://192.168.0.1`。
2. 登录（查看路由器底部的贴纸获取凭据）。
3. 进入 **DHCP设置** → 查找“地址保留”、“静态DHCP”或“DHCP绑定”。
4. 在已连接客户端列表中找到设备，记下其 **MAC地址**。
5. 添加保留：将该MAC地址绑定到固定IP，如 `192.168.1.10`。
6. 为每台设备（PC、打印机、NAS等）重复此操作。
7. 重启设备，使其获取保留的IP。

> 您的交换机无需任何配置——它只负责转发流量。交换机在IP分配中不起作用。

---

**方法B — 设备上的静态IP**

您可以在Windows、macOS、Linux或Android/iOS设置中直接配置IP。仅当您无法访问路由器管理面板时使用此方法。

执行时，请确保设置：

| 字段 | 示例值 |
| --- | --- |
| IP地址 | `192.168.1.10` |
| 子网掩码 | `255.255.255.0` |
| 默认网关 | `192.168.1.1`（您的路由器） |
| DNS | `8.8.8.8` 或您的路由器IP |

**重要提示：** 选择*超出*路由器DHCP池范围的IP（例如，如果DHCP分配 `.100`–`.200`，则使用 `.10`–`.50`），以避免冲突。

---

**选择哪种方法：**

- **DHCP保留** — 集中管理，每台设备无需设置任何内容，最易于管理。✅ 推荐。
- **设备静态IP** — 无需访问路由器即可使用，但每台设备需要手动配置，且存在IP冲突风险。

**参考资料：**

- [如何设置DHCP保留 — TP-Link](https://www.tp-link.com/us/support/faq/170/)
- [静态IP与DHCP保留的区别 — How-To Geek](https://www.howtogeek.com/184310/ask-htg-whats-the-difference-between-dhcp-and-static-ip-addresses/)
- [如何在Windows/Mac/Linux上查找MAC地址 — Lifewire](https://www.lifewire.com/how-to-find-your-mac-address-2542)。
