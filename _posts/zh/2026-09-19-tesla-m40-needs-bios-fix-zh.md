---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla M40需要BIOS修复
translated: true
type: note
---

我已经有了完整的诊断结果。在安装之前，我需要 sudo 密码（不是免密的那种）。

## 我发现了什么

**GPU：** Tesla M40 12 GB（`10de:17fd`，GM200，VBIOS 84.00.56.00.02）——今天 17:15 安装的。`kern.log` 中早期的启动日志来自之前机箱内的一块*不同*的显卡（一块 Fermi `GF100` 2 GB）。

**驱动：** `nvidia-driver-580`（580.178.04）已确认正确：
- NVIDIA 官方 580.178.04 说明文档中列出了 `Tesla M40` 和 `Tesla M40 24GB`
- 590/595/610 仅支持 Turing 及更新架构（590 实际上是一个过渡别名 → 595）
- `ubuntu-drivers devices` 独立推荐针对 `v000010DEd000017FD` 使用 `nvidia-driver-580`

**一个你应该知道的阻碍点**——M40 目前**无法初始化**，单独安装驱动也无法解决这个问题：

```
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: can't assign; no space
pci 0000:01:00.0: BAR 3 [mem size 0x02000000 64bit pref]: can't assign; no space
nouveau 0000:01:00.0: bar: one-time init failed, -12
```

M40 需要 **16 GiB 的 64 位预取 BAR**（这对数据中心 GPU 来说很正常）。你的 BIOS 只提供了一个 16 MB 的 32 位窗口，并且根端口报告 `Prefetchable memory behind bridge: [disabled] [64-bit]`。结果是：即使安装了 580 驱动，`nvidia-smi` 也会报告 “No devices were found”（未找到设备）。

解决这个问题需要在 BIOS 中启用 **Above 4G Decoding**（MSI B150M PRO-VH，BIOS 1.80，日期 2016/07）。我无法从 MSI 的网站上确认 1.80 是否暴露了该选项——你可能需要更新 BIOS，因为 MSI 只是在部分主板的更新版本中才添加了该选项。

## 一旦你给我密码，计划如下

1. `apt update`
2. 安装 `build-essential dkms linux-headers-$(uname -r)`（DKMS 尚未安装）
3. 安装 `nvidia-driver-580`
4. 将 `nouveau` 加入黑名单（当前它绑定在该显卡上）
5. `update-initramfs -u`，然后重启
6. 用 `nvidia-smi` 验证

安全启动已禁用，因此无需 MOK 注册。M40 没有显示输出，所以你的桌面仍会使用 Intel HD 530，重启是安全的。

**你想怎么继续？**

- 把 sudo 密码发给我（或者为 `lzw` 启用 `NOPASSWD`），我会全部执行，或者
- 给我批准，你自己为第 5 步重启。

另外值得决定的是：你的主板是一块**被动散热**的 M40（专为服务器风道设计）——请确保它有强制风道，并注意 ECC 默认是开启的（这就是为什么 nouveau 看到的是 12288 MiB 中的 11520 MiB）。