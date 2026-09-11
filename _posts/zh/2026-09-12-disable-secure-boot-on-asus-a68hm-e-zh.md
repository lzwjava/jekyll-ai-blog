---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用华硕A68HM-E上的安全启动
translated: true
type: note
---

Question: **如何禁用 ASUS A68HM-E UEFI BIOS 上的 Secure Boot？**

Answer: 在 **ASUS A68HM-E** 上，Secure Boot 位于 **Boot → Secure Boot**。A68HM-E 手册明确显示了 Boot 菜单中的 **CSM** 和 **Secure Boot**。([ASUS Download Center][1])

### 禁用它

1. 开机时按 **Del** 进入 BIOS。
2. 按 **F7** → **Advanced Mode**。
3. 转到：

```text
Boot
 ├── CSM (Compatibility Support Module)
 └── Secure Boot
```

4. 打开 **Secure Boot**。
5. 查找：

```text
OS Type
```

将其设置为：

```text
Other OS
```

而不是：

```text
Windows UEFI mode
```

在 ASUS UEFI 固件上，`Other OS` 是用于非 Secure Boot 操作系统的设置。([ASUS Download Center][2])

6. 按 **F10** → **Yes** 保存并重启。

### 如果 `Secure Boot State` 仍然显示 Enabled

在这一代 ASUS 固件上，你可能还需要处理 **CSM**。

试试：

```text
Boot
  → CSM
      → Launch CSM = Enabled
```

对于老旧测试/维修机器，**CSM 已启用 + Secure Boot 实际上未强制执行** 通常是你想要的，尤其是当你引导旧版 Linux/工具或传统 Option ROM 时。ASUS 文档说明 CSM 专门用于与非 UEFI 设备的兼容性。([ASUS Download Center][2])

对于你的 **GPU 维修/MATS/MODS 测试机**，我实际会使用：

```text
Boot
├── CSM
│   └── Launch CSM = Enabled
│
└── Secure Boot
    └── OS Type = Other OS
```

这能为你提供与旧 GPU、传统启动介质和诊断环境的最大兼容性。

如果你给我看一张 **A68HM-E 当前 Secure Boot 页面的照片/截图**，我可以确切告诉你该改哪个字段。

我还可以逐步讲解 **A68HM-E BIOS 设置，特别是如何在测试有问题的独立 GPU 时使用 iGPU 作为主显示**，这可能对于你的 MATS 工作更有用。

[1]: https://dlcdnet.asus.com/pub/ASUS/mb/SocketFM2/A68HM-E/E9808_A68HM_Series_Manual_Print_vendor_only.pdf?utm_source=chatgpt.com "2.8 Boot menu"
[2]: https://dlcdnets.asus.com/pub/ASUS/mb/SocketFM2/A68HM-F/E10355_A68HM-F_Manual_WEB.pdf?utm_source=chatgpt.com "Launch CSM [Enabled]"
