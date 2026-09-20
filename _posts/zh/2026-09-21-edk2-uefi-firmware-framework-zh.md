---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EDK2 UEFI 固件框架
translated: true
type: note
---

**问题：** 什么是 tianocore/edk2？它有什么作用？

**回答：**

**EDK II（EFI 开发套件 II）** 是一个现代、开源 的固件开发框架，由 TianoCore 社区维护。它被描述为基于 <www.uefi.org> 上的 UEFI 和 PI 规范构建的现代、功能丰富、跨平台的固件开发环境。

通俗地说，它是用于构建 **UEFI 固件** 的代码库——这种软件负责初始化硬件并启动操作系统，广泛应用于大多数现代 PC、服务器及嵌入式设备。

**关键特性：**

- **语言：** 主要为 C 和 Python
- **许可证：** BSD-2-Clause Plus Patent License（部分组件采用 Apache、OpenSSL 等许可证）
- **托管方：** TianoCore 项目（tianocore.org）
- **星标 / 分支：** 约 6.2k 星标，约 3.3k 分支——一个发展成熟、活跃的项目

**仓库中的主要包**（每个均为独立的模块）：

| 包名 | 用途 |
| --- | --- |
| `MdePkg` | UEFI 核心库定义 |
| `MdeModulePkg` | 通用 UEFI 驱动和应用程序 |
| `OvmfPkg` | QEMU/KVM 虚拟机的 UEFI 固件 |
| `ArmPkg` / `ArmVirtPkg` | ARM 架构支持 |
| `NetworkPkg` | 网络栈（PXE、TLS、HTTP 启动） |
| `SecurityPkg` | 安全启动、TPM 支持 |
| `ShellPkg` | UEFI Shell（命令行环境） |
| `CryptoPkg` | 加密库（OpenSSL、MbedTLS） |
| `EmulatorPkg` | 在宿主操作系统模拟器中运行 UEFI 以进行测试 |

**CI 支持：** 该项目在 Windows（VS、CLANGPDB）和 Ubuntu（GCC、CLANGPDB、CLANGDWARF）工具链上运行持续集成。

**谁在使用它？** EDK II 是 Intel 平台、QEMU/OVMF（广泛应用于 Linux 虚拟化）以及众多嵌入式/服务器平台固件的上游基础。

参考：

- [tianocore/edk2 on GitHub](https://github.com/tianocore/edk2)
- [TianoCore 官方网站](http://www.tianocore.org)
- [EDK II 入门指南](https://www.tianocore.org/tianocore-wiki.github.io/development/tutorials-howto/getting_started_with_edk_ii.html)
