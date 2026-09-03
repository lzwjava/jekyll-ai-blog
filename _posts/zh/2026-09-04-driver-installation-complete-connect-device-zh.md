---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 驱动程序安装完成，连接设备
translated: true
type: note
---

驱动程序包的安装已完成。以下是操作摘要：

## 手册说明（usb-vendor-class-driver_im_en.pdf，Rev 1.2）

对于 Windows 10，操作步骤如下：在提升的命令提示符中运行 `pnputil -a <路径>\SMJUSBCOM.INF` → 通过 USB 连接 Star 打印机/读卡器 → Windows 通过即插即用绑定驱动程序 → 在设备管理器的 **端口（COM 和 LPT）** 下确认出现 **"SMJ USB Device (COM*)"**。

## 已执行的操作

1. **已验证环境** — Windows 11 Pro 64 位（内部版本 26100），Shell 以提升权限运行。
2. **已验证驱动程序签名** — `smjusbcom.cat` 由 **Microsoft Windows Hardware Compatibility Publisher**（WHQL，交叉认证链）有效签名，因此可接受用于 x64 内核加载。`.sys` 文件通过目录签名（无嵌入式签名），这对 PnP 驱动程序来说是正常的。
3. **已将驱动程序包安装到驱动程序存储区**（手册步骤 1）：

   ```
   pnputil /add-driver SMJUSBCOM.INF /install
   → 驱动程序包已成功添加。
   发布名称: oem152.inf
   ```

   在驱动程序存储区中确认：提供商 **Star Micronics**，类 **Ports**，版本 **02/19/2019 5.0.0.0**，签名者 **Microsoft WHQL**。

## 剩余步骤 — 设备连接（手册步骤 2）

**当前没有 Star USB 设备（VID_0519）连接到此机器**（通过 `pnputil /scan-devices` 和 PnP 枚举验证）。驱动程序已暂存，一旦插入兼容设备将自动安装。

要完成安装：

1. 通过 USB 线连接 Star 打印机 / Visual Card-Reader/Writer（TSP100/650/700II/800II、FVP10、HSP7000、SP500/700、TUP500/900、TCP300II/400）并通电。
   - **HSP7000**：将 DIP 开关 1-5 设置为 **ON**；其他打印机：**OFF**。
2. 等待 PnP 完成（将创建一个虚拟 COM 端口）。
3. 在 **设备管理器 → 端口（COM 和 LPT）** 中确认出现 **"SMJ USB Device (COM*)"**。

⚠️ 注意：此驱动程序官方目标系统为 Windows 7/8.1/10（根据 readme），但本机运行的是 **Windows 11 24H2**。WHQL 签名的包已成功暂存，设备连接后应能加载。如果设备显示错误（例如代码 52 / 签名驱动程序阻止），请告知我，我可以检查事件日志以帮助排查问题。
