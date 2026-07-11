---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SYS_FAN2与SYS_FAN3解析
translated: true
type: note
---

问题：这块微星主板上的SYS_FAN2和SYS_FAN3接口是什么意思？

回答：

`SYS_FAN2` 和 `SYS_FAN3` 是该主板上四个 **4针系统/机箱风扇接口**（`SYS_FAN1~4`）中的两个，用于给机箱风扇供电并控制其转速——与 `CPU_FAN1`（CPU散热器）和 `PUMP_FAN1`（一体式水冷泵）不同。

**针脚定义（4针）：**

| 针脚 | PWM模式 | DC模式 |
|---|---|---|
| 1 | 接地 | 接地 |
| 2 | +12V | 电压控制 |
| 3 | 测速（转速反馈） | 测速 |
| 4 | 转速控制信号 | 未连接 |

**电气/模式规格：**

| 接口 | 默认模式 | 最大电流 | 最大功率 |
|---|---|---|---|
| `CPU_FAN1` | PWM | 2A | 24W |
| `PUMP_FAN1` | PWM | 3A | 36W |
| `SYS_FAN1~4` | **DC模式** | 2A | 24W |

关键细节：`SYS_FAN1~4` 默认工作于 **DC模式**，而非 PWM模式。这意味着微星通过调节12V供电轨的电压（针脚2）来控制转速，而不是通过针脚4上的PWM占空比信号。如果接入一个4针PWM风扇，期望通过针脚4进行PWM控制，那么它可能会以固定/接近满速的状态旋转，直到你在BIOS中将该接口切换为PWM模式。

**在哪里修改：** BIOS → 硬件监控面板，针对每个风扇的独立设置，可在DC/PWM模式之间切换，并启用或禁用智能风扇（温度曲线）控制。如果将3针纯DC风扇插入设为PWM模式的接口（反之亦然），转速控制将无法正常工作——务必根据风扇实际信号类型，在BIOS中设置与之匹配的接口模式。

**物理位置：** 在该主板的布局中，`SYS_FAN1` 位于靠近底部边缘（`JCI1`下方），`SYS_FAN2` 和 `SYS_FAN3` 集中在右侧USB接口（`JUSB1`/`JUSB2`）附近，而 `SYS_FAN4` 则靠近内存插槽/`ATX_PWR1` 区域。因此，将哪个物理风扇连接到哪个接口，主要取决于线缆走线与长度是否方便，而非功能上的差异（这四个接口均为等效的DC模式接口）。

参考链接：

- [微星 MAG B760M MORTAR WIFI II 用户指南（PDF）](https://gzhls.at/blob/ldb/8/2/2/3/f5692b3e4562b5b05ac5b7fe142b249bca4e.pdf)
- [微星 MAG 系列主板用户指南](https://manuals.plus/m/253c081013a7d1d08c025f4e32d8538557f50913ffc8b0ccddc406969d425e32)