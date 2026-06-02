---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenWrt 仓库结构详解
translated: true
type: note
---

这是 **OpenWrt** 的源代码——用于嵌入式设备（主要是路由器和网络设备）的官方开源 Linux 发行版。

以下是仓库结构分解：

```
openwrt/
├── Config.in          # 顶层 Kconfig 菜单 (make menuconfig)
├── Makefile           # 主构建编排器
├── rules.mk           # 所有包共享的构建规则
├── feeds.conf.default # 外部包 feed 源 (GitHub 仓库)
├── target/            # 目标平台定义 (SoC、板卡、架构)
├── toolchain/         # 交叉编译工具链 (gcc、musl/glibc、binutils)
├── package/           # 核心包 (基础系统、网络、内核模块)
├── tools/             # 固件构建所需的主机工具 (squashfs、zstd 等)
├── scripts/           # 构建辅助脚本 (feeds、元数据、配置)
├── include/           # 共享的 Makefile 包含文件
├── config/            # 构建系统配置片段
└── LICENSES/          # 许可证文件 (GPL 等)
```

关键信息：

- 最新提交来自 **2026-05-23** —— 这是主分支非常新的检出
- 近期活动包括内核驱动补丁 (hwmon、realtek NIC)、fstools 更新以及 x86 ONIE 安装器支持
- 构建系统基于 **Kconfig + Makefile** — 通过 `make menuconfig` 配置，然后执行 `make` 交叉编译完整的固件映像
- `feeds.conf.default` 从外部 Git 仓库拉取数百个额外包

这本质上是用于创建自定义路由器固件的 **构建系统 + 核心源码**。你可以用它为你那台 IP 为 192.168.1.1 的中国电信网关路由器（从你的记忆中看到它已运行 LuCI/OpenWrt）构建自定义映像。

你打算用这个来构建自定义固件、修改某个包，还是做其他事情？
