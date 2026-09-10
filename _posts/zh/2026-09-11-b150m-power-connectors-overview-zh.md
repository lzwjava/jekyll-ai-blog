---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B150M 电源连接器概述
translated: true
type: note
---

问题：**像微星 B150M PRO 这样的主板上主要的电源连接器有哪些？**

回答：

对于典型的 **B150M 主板**，主要的电源连接器是：

```text
        PSU
         │
         ├── 24-pin ATX ──────────► 主板主电源
         │
         └── 4/8-pin CPU EPS ─────► CPU 电源
```

### 1. 24-pin ATX — 主板主连接器

通常标记为：

```text
ATX_PWR1
JPWR1
ATX_PWR
```

它是主板右侧边缘的 **大 24-pin 连接器**。

它提供多个电压轨：

* +12 V
* +5 V
* +3.3 V
* GND
* 5VSB
* PS_ON#
* PWR_OK

这是主板正常工作时绝对需要的连接器。

### 2. 4/8-pin CPU 电源 — EPS12V

通常靠近 CPU 插槽，标记类似：

```text
CPU_PWR1
JPWR2
ATX12V
```

典型形式：

```text
4-pin        或        8-pin
┌──────┐              ┌────────┐
│12V GND│              │12V GND │
│12V GND│              │12V GND │
└──────┘              └────────┘
```

这为 **CPU VRM 专门提供 12V**。

对于你的 B150 + i5-6500 配置，通常需要 **同时连接 24-pin ATX 和 CPU 的 4/8-pin 连接器**。

### 3. 前面板连接器不是电源输入连接器

你之前找的 `JFP1` 连接器是不同的：

```text
JFP1
 ├── 电源开关
 ├── 复位开关
 ├── HDD LED
 └── 电源 LED
```

**电源开关引脚只告诉主板启动**。它们不提供主板电源。

因此，对于裸机测试：

```text
PSU
 │
 ├── 24-pin ATX ──► 主板
 │
 └── CPU EPS ─────► CPU 电源

然后短暂短接：
JFP1 PWR_SW 引脚
```

这模拟了按下机箱电源按钮。

如果你正在调试你的 **MSI B150M PRO**，我也可以带你一步步了解 **24-pin ATX 连接器的每个引脚，以及你应当用万用表/示波器测量到的电压值**。