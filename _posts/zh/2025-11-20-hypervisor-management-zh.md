---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 管理程序与虚拟机管理
translated: true
type: note
---

**虚拟机监控程序**（也称为**虚拟机管理器**或 VMM）是在物理主机上创建、运行和管理**虚拟机**的核心软件（有时是固件/硬件）。它通过抽象和共享物理硬件资源（CPU、内存、存储、网络等）给多个隔离的虚拟机，从而实现了虚拟化。

### 两种主要类型的虚拟机监控程序

| 类型 | 描述 | 是否直接在硬件上运行？ | 示例 | 优点 | 缺点 |
|------|-------------|-----------------------------|----------|------|------|
| **类型 1（裸机）** | 直接安装并运行在物理硬件上。虚拟机监控程序下方没有主机操作系统。 | 是 | VMware ESXi、Microsoft Hyper-V（在虚拟机监控程序模式下）、Xen、KVM（裸机使用时）、Proxmox VE、Oracle VM Server | 最佳性能、更高的安全性、更低的开销，用于生产/数据中心环境 | 对初学者来说更难管理，内置驱动/工具较少 |
| **类型 2（托管）** | 作为应用程序运行在常规操作系统（Windows、macOS、Linux）之上。主机操作系统拥有硬件。 | 否（运行在主机操作系统上） | VMware Workstation、VMware Fusion、VirtualBox、Parallels Desktop、QEMU（与主机操作系统一起使用时） | 易于安装和使用，适用于台式机/笔记本电脑，可以使用主机操作系统的驱动和工具 | 性能稍低，由于主机操作系统而具有更大的攻击面 |

### 虚拟机监控程序的工作原理（简化）

1.  **资源抽象** – 虚拟机监控程序向每个虚拟机呈现虚拟 CPU、虚拟 RAM、虚拟磁盘、虚拟网卡等。
2.  **隔离** – 每个虚拟机完全隔离；一个虚拟机崩溃或受损通常不会影响其他虚拟机。
3.  **调度** – 虚拟机监控程序调度哪个虚拟机在任何给定时刻使用物理 CPU/RAM（分时共享）。
4.  **陷入和模拟** – 当虚拟机尝试执行特权指令（例如，更改页表、访问硬件）时，CPU 会陷入到虚拟机监控程序，由它安全地模拟或处理该请求。
5.  **硬件加速** – 现代 CPU 具有虚拟化扩展（Intel VT-x、AMD-V），这使得陷入和模拟过程非常快速（接近本机性能）。

### 常见用例

-   服务器整合（在一台物理服务器上运行数十个虚拟机）
-   云计算（AWS EC2、Azure VM、GCP Compute Engine 底层都使用虚拟机监控程序）
-   开发/测试环境
-   桌面虚拟化（在 macOS 上运行 Windows 或多个 Linux 发行版并存）
-   安全沙箱和恶意软件分析

### 当前流行的虚拟机监控程序

-   **VMware ESXi** – 在企业中占主导地位（现属博通公司）
-   **Microsoft Hyper-V** – 内置于 Windows Server 和 Windows 10/11 Pro 中
-   **KVM** – Linux 中的默认选项，为大多数 OpenStack 和公有云提供支持（Google Cloud、AWS Nitro 等）
-   **Proxmox VE** – 基于 Debian + KVM + LXC 的开源 Type-1 虚拟机监控程序
-   **Xen** – 被 Oracle Cloud、AWS（旧世代）、XCP-ng 使用
-   **VirtualBox** – Oracle 提供的免费 Type-2 虚拟机监控程序，个人使用非常流行
-   **Nutanix AHV** – 用于超融合基础设施的 Acropolis Hypervisor（基于 KVM）

简而言之：虚拟机监控程序是让多个操作系统安全高效地共享同一台物理计算机的“管弦乐队指挥”。类型 1 常见于数据中心和云环境；类型 2 则是桌面用户通常安装的类型。
