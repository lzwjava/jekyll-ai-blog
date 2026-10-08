---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕Z170-A启动设备LED故障排除
translated: true
type: note
---

**这台ASUS Z170-A遇到什么问题？**

**答案：你照片中的红色LED是`BOOT_DEVICE_LED`。** 这是一个非常有价值的线索。

ASUS记载Z170-A有四个POST指示灯：**CPU、DRAM、VGA、BOOT_DEVICE**。如果其中一个保持亮起，POST检测到该组件出现故障。（[ASUS Download Center][1]）

在你的照片中：

* CPU指示灯：显然 **未亮**
* DRAM指示灯：显然 **未亮**
* VGA指示灯：显然 **未亮**
* **BOOT_DEVICE_LED：红色 → 亮起**
* 因此主板成功通过了CPU/RAM/VGA初始化，并在 **启动设备阶段** 停止。

### 最可能的原因：无可引导的SSD/HDD

我可以看到主板右侧的SATA接口，但没看到连接了SATA硬盘。

如果你是在 **没有SSD/HDD** 的情况下测试这块主板，那么这种行为是正常的。

POST序列大致如下：

```text
开机
   ↓
CPU初始化       ✓
   ↓
DRAM初始化      ✓
   ↓
PCIe / VGA初始化 ✓
   ↓
寻找启动设备      ← 红色LED
   ↓
启动Windows/Linux
```

所以这 **看起来不像主板故障**。

ASUS特别指出，启动设备故障应通过重新连接SATA/M.2硬盘、SATA线缆/端口，并尝试使用已知良好的硬盘来检查。（[ASUS Global][2]）

### 如果你的目的只是测试主板

你实际上并不需要硬盘来确认主板能否POST。

连接以下组件：

```text
Z170-A
├── 24-pin ATX电源
├── 8-pin CPU EPS
├── CPU + 散热器
├── 1根内存
├── PSU
└── 显卡（仅当CPU没有可用的集成显卡时）
```

然后开机。

如果能看到 **BIOS/UEFI画面**，核心平台基本就是活的。

如果你使用的是带有集成显卡的Intel CPU，也可以直接测试主板的视频输出。

### 我注意到一个重要的细节

你的散热器很大，并且非常接近内存插槽区域。这没关系，但为了排除故障，我会简化系统：

```bash
# 最小POST测试
CPU
1 × 内存
PSU
主板
显示器
```

然后逐个添加显卡、SSD、其他PCIe设备。

如果你告诉我 **你在这块Z170-A上安装了哪款CPU和哪种内存**，以及你是否得到了 **画面输出或仅仅是红色BOOT指示灯**，我可以给你下一步的确切诊断步骤。

参考：

* [ASUS Z170-A用户手册](https://www.asus.com/supportonly/z170-a/helpdesk_manual/?utm_source=chatgpt.com)
* [ASUS Q-LED故障排除](https://www.asus.com/us/support/faq/1043948/?utm_source=chatgpt.com)

[1]: https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/Z170-A/E10611_Z170-A_UM_V2_WEB.pdf?model=z170-a&utm_source=chatgpt.com "1.8 板载LED指示灯"
[2]: https://www.asus.com/us/support/faq/1043948/?utm_source=chatgpt.com "[主板] 常见的Q-CODE（错误代码）及故障排除 | 官方支持 | ASUS美国"
