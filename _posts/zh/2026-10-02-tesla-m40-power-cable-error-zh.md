---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 特斯拉M40电源线错误
translated: true
type: note
---

是的——那台机器里确实有一张 Tesla M40，但它的电源连接不正确，导致驱动无法将其启用。

**在 `192.168.1.34` 上发现的情况：**

| 项目 | 结果 |
|------|------|
| GPU | `NVIDIA GM200GL [Tesla M40]` 位于 `0000:01:00.0` ✅ |
| 驱动 | 已加载 580.178.04（内核模块 `nvidia`、`nvidia_uvm` 等） |
| `nvidia-smi` | ❌ `未找到任何设备` |

**实际错误信息**（来自 `journalctl`）：

```
NVRM: GPU 0000:01:00.0: GPU 未连接必要的电源线。
NVRM: GPU 0000:01:00.0: RmInitAdapter 失败! (0x24:0x1c:1603)
NVRM: GPU 0000:01:00.0: rm_init_adapter 失败，设备次编号 0
```

显卡在 PCIe 总线上被检测到，驱动也枚举了它（`/proc/driver/nvidia/gpus/` 中显示 `Model: Tesla M40`），但 GPU UUID 显示为 `GPU-????-????-...`，因为初始化未完成——这是**电源问题，而非驱动或软件问题**。

**关于 Tesla M40 的重要提示：** 它使用的不是标准的 PCIe 8-pin 显卡电源线，而是 **8-pin EPS（CPU）电源接口**（250W 显卡）。这是 M40 上出现此错误最常见的原因——人们插上了 PCIe 8-pin 电源线（或者干脆没插），显卡就会报告“电源线未连接”。

**解决办法：**
1. 关闭机器电源。
2. 使用电源供应器的 **EPS 8-pin** 电源线连接到 M40 的电源接口（M40 只有一个 8-pin EPS 接口）。
3. 确保电源供应器能为显卡提供约 250W 的功率。
4. 开机后再次检查 `nvidia-smi`。

需要我检查那台机器的电源供应器/线缆信息或其他内容吗？