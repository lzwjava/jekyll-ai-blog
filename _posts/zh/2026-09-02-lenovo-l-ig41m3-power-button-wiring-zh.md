---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想L-IG41M3电源开关接线
translated: true
type: note
---

问题：**在联想 L-IG41M3 的 11 针前置面板连接器上，应该将哪些引脚连接到机箱电源/开机按钮和小型前置面板电路板？**

答案：我找到了 **L-IG41M3 V1.1 的原理图**。该主板是联想使用的 ECS 设计，原理图中明确将前置面板电源开关信号标识为 **`PANSWH_L`**。（[Scribd][1]）

不过，**我建议不要盲目短接 11 针连接器上的两个引脚**。联想对前置面板连接器进行了定制，具体的物理引脚编号和方向很重要。

有用的信号名称如下：

```text
PANSWH_L   = 电源开关
SYS_RESET_L = 复位开关
FP_LED0    = 硬盘/活动指示灯
FP_LED1    = 电源/状态指示灯
GND        = 地线
```

原理图显示 `PANSWH_L` 连接到 Super I/O 芯片，并作为电源按钮输入。（[Scribd][2]）

### 针对您的实际主板

如果您能提供一张 **L-IG41M3 主板上 11 针连接器的清晰照片**，尤其是包含以下细节：

* 连接器本身
* 旁边印制的任何文字
* 引脚 1 标记 / 防呆缺口位置
* 小型联想前置面板 PCB 及其 11 针线缆

我可以将其映射为如下格式：

```text
11 针连接器

┌─────────────────────┐
│ 1  2  3  4  5  6   │
│ 7  8  9 10 11       │
└─────────────────────┘

        ↓

电源开关 → 引脚 X + 引脚 Y
复位     → 引脚 X + 引脚 Y
电源指示灯 → 引脚 X + 引脚 Y
硬盘指示灯 → 引脚 X + 引脚 Y
地线     → ...
```

**不要通过反复试错来连接 11 针前置面板板**，因为与标准的 ATX `F_PANEL` 不同，这个联想连接器是 OEM 特定的。L-IG41M3 原理图本身也注明前置面板连接器定义为联想定制。（[Scribd][2]）

参考资料：

* [L-IG41M3 原理图/手册来源](https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com)
* [L-IG41M3 技术讨论](https://vinafix.com/threads/l-ig41m3.19344/?utm_source=chatgpt.com)

[1]: https://www.scribd.com/document/522563336/ECS-ig41m3-g41t-lm3v1-1?utm_source=chatgpt.com "L-IG41M3 V1.1 主板概览 | PDF | 制成品 | 计算机架构"
[2]: https://www.scribd.com/document/984973046/Z490H6-LA-V1-1?utm_source=chatgpt.com "Z490H6-LA 框图指南 | PDF | 计算机网络 | 物理层协议"