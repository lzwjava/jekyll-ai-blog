---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 思科交换机导论
translated: true
type: note
---

问题：请您全面介绍一下Cisco交换机？

回答：

思科系统公司是企业网络领域的主导者，其交换机产品组合是全球最大、部署最广泛的之一。Cisco 交换机涵盖了从用于家庭/中小型企业的非托管小型设备，到构成最大数据中心和服务提供商骨干的巨型模块化机箱交换机。

### 1. Cisco 交换机系列（截至 2025 年）

| 系列              | 主要用例                          | 主要型号（示例）                  | 外形尺寸                  | 主要功能/定位 |
|---------------------|-------------------------------------------|----------------------------------------|------------------------------|----------------------------|
| **Catalyst 9000**   | 企业园区和分支机构（旗舰产品）     | 9200/9300/9400/9500/9600               | 固定式和模块化              | 意图导向网络，Cisco DNA Center，Wi-Fi 6/6E/7 支持，高级安全性 |
| **Catalyst 8000**   | 边缘路由 + 交换                  | 8200/8300/8500                         | 固定式                        | SD-WAN 重点，高吞吐量路由 |
| **Catalyst 1000**   | 小型企业/接入层             | 1000-8P, 1000-24T                      | 固定式 8–48 端口              | 价格实惠，基本 L2/L3，无风扇选项 |
| **Catalyst 1200/1300** | SMB 和基本企业                  | 1200-8T, 1300-16P                      | 固定式                        | SF/SG 系列的继任者，现代 IOS-XE Lite |
| **Meraki MS**       | 云管理交换                   | MS120, MS210, MS350, MS410, MS450      | 固定式和模块化              | 100% 云仪表板，零接触配置 |
| **Nexus 9000**      | 数据中心（ACI 或 NX-OS 模式）           | 9200/9300/9500/9600                     | 固定式和模块化              | VXLAN/EVPN，10/25/40/100/400/800G，可编程 |
| **Nexus 7000/7700** | 传统高端数据中心/核心        | 7004/7009/7010/7710                    | 大型模块化机箱        | 正在被 9000 系列取代 |
| **Industrial Ethernet** | 恶劣环境（IE 系列）      | IE-2000, IE-3000, IE-4000, IE-5000, IE-9300 | DIN 导轨/坚固型         | 宽温，抗震，PROFINET 等。 |
| **Catalyst 8000V / CSR1000v** | 虚拟交换机/路由器              | 仅软件                          | 虚拟机/容器               | 运行在任何虚拟机管理程序或云上 |

### 2. Cisco 交换机上的操作系统

| 操作系统                  | 用于                              | 主要特点 |
|---------------------|--------------------------------------|---------------------|
| **Classic IOS**     | 较旧的 Catalyst (2950, 3560, 3750 等) | 大多数情况下已达 EOL |
| **IOS-XE**          | 所有现代 Catalyst 9000, 8000, 1000/1200 | 模块化，独立的控制/数据平面，In-Service Software Upgrade (ISSU) |
| **IOS-XE Lite**     | Catalyst 1000/1200/1300              | 适用于 SMB 的精简版本 |
| **NX-OS**           | Nexus 系列                         | 以数据中心为中心，功能丰富的 CLI, ISSU, 强大的 VXLAN/BGP-EVPN |
| **Meraki Dashboard**| Meraki MS 交换机                   | 无本地 CLI (现在提供有限的 API/CLI)，100% 云 |
| **ACI**             | ACI 模式下的 Nexus 9000               | Application Centric Infrastructure – 策略驱动，APIC 控制器 |

### 3. 第 2 层与第 3 层功能

- 几乎所有现代 Cisco 交换机（Catalyst 9200 及更高版本、Nexus、Meraki）都是 **L2/L3** 交换机。
- 入门级 Catalyst 1000/1200 提供基本的静态路由，甚至在更高级的 SKU 中提供完整的动态路由。
- 高端型号（9300/9400/9500、Nexus 9300/9500）支持完整的路由表、BGP、OSPF、EIGRP、MPLS、Segment Routing 等。

### 4. 关键技术和功能

| 功能                  | 描述                                                                 | 典型系列 |
|--------------------------|-----------------------------------------------------------------------------|----------------|
| StackWise / StackWise Virtual | 物理或逻辑堆叠（9600 上最高 480 Gbps 堆叠带宽）      | Catalyst 9300/9500/9600 |
| Virtual Switching System (VSS) / Multichassis EtherChannel (MEC) | 较旧的多机箱技术（已大部分被 StackWise Virtual 取代）   | 6500/6800, 9400/9600 |
| Cisco DNA Center / Catalyst Center | 意图导向网络、保证、自动化、遥测                 | Catalyst 9000 |
| Encrypted Traffic Analytics (ETA) | 无需解密即可检测加密流量中的恶意软件                   | Catalyst 9000 |
| Application Hosting (Docker/Kubernetes) | 直接在交换机上运行容器                                   | 9300/9400/9500/9600 |
| 400G / 800G 光模块       | 最高密度数据中心交换                                       | Nexus 9300-EX/FX/GX/HX |
| MACsec & TrustSec        | 链路层加密和基于 SGT 的策略执行                        | 大多数 Catalyst 9000 和 Nexus |
| NetFlow / sFlow / Telemetry | 丰富的可视化功能                                                            | 所有现代平台 |

### 5. 许可（简化 – 2025）

Cisco 已转向 **Cisco DNA Advantage / Premier**（现在主要更名为 **Cisco Catalyst Subscription** 或 **Cisco DNA Subscription for Switching**）：

- **Network Essentials / Advantage** → 现在是 **Network Stack**（永久）+ 可选的 **Catalyst Subscription**（3/5/7 年）
- 更高层级的订阅提供 DNA Center 功能、保证、SD-Access、ISE 集成等。
- Meraki 纯粹是订阅制（每台交换机，1/3/5/7/10 年）。

Nexus 使用 **NX-OS Essentials / Advantage / Premier** 附加组件。

### 6. 典型部署层级（园区）

- 接入层：Catalyst 9200 / 9300 或 Meraki MS120/250
- 汇聚层/核心层：Catalyst 9400 或 9600（或在较小园区中使用 9500）
- 数据中心：Nexus 9300 (leaf/spine) + 9500/9800 (spine/super-spine)

### 7. 快速选择指南（2025）

| 需求                                 | 推荐系列          |
|--------------------------------------|-----------------------------|
| 小型办公室，8-24 端口，PoE        | Catalyst 1000 或 1200       |
| 中大型园区，高级功能| Catalyst 9300 / 9400       |
| 云管理，零接触            | Meraki MS                   |
| 高密度 100G/400G 数据中心   | Nexus 9300-FX3/GX2/HX       |
| 工业/户外                 | IE-4000 / IE-9300           |
| SD-WAN 边缘                          | Catalyst 8300 / 8500        |

Cisco 交换机仍然是大多数企业的事实标准，因为它们可靠、功能深度大、支持周期长（通常超过 10 年），并且拥有庞大的工程师生态系统。

如果您有特定的用例（园区、数据中心、工业、预算、端口速度等），我可以提供更有针对性的建议。
