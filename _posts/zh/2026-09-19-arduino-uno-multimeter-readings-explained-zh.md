---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino Uno万用表读数详解
translated: true
type: note
---

问题：在 Arduino Uno 中，内部有哪些电子元件？万用表在引脚之间测到的蜂鸣 / 电阻 / 电压读数到底意味着什么？

回答：**不完全是。** 关键在于，万用表的测量结果很大程度上取决于你使用的**是哪个模式**。

![Image](https://images.openai.com/static-rsc-4/Kua_dCnY0422nFAgQlWc2RNp4tQOT7ElXsNPa6G_48ZJYQxqaI-2USKm1trlgPzhoy-ERv2AhGNZybdxCdTmfb6cr9ecJp1Ai4e7DNPSTmADmebohVkRvfq6r5BHSV9aN_10gfOfXqZFGPJB5KbuZfwBfbR0Qyk7oW4F1rjcrAavsQXYVJmp1pxbBeT0-WWm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pc0nX9jDViAsYG-YgAGokEWt_nnTwAjaDsrQrELp_xa7-mCmA2KlBQDQcdFFNNOYdrtrvHMYD18ZYgzLSvJ0Ee1ZyU0tGs4eiJiytEFHye73KBUtr4aq5WbWgg8dcr6ql-v-3UBqC9r1wdRkbMkRSPhXHEF0bvWkesg1s3B_kD-q_KPVvATcLA82nMyqqgF6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ylLqDDusDBdnr6e8ZwEIr7ynCCu90ll9YW9-WjMBnZl_kxIJDoXapEU43WhLL04mcNQqfrkm_7lZsFMO1HhkLx5AP0HjPczTvM5RtqBG0uyegGa-_MlDnaIrkSFWlUXQEo3bJ_qfZUx8gK-yXrJgYS6pkdUaFSyf6EwOMmrbGjmaVsGZXIDfKR3gpczaJxKC?purpose=fullsize)

### 1. Arduino Uno 内部到底有什么？

Uno R3 上的重要元件包括：

```text
                    USB
                     │
             ┌───────▼───────┐
             │ USB interface  │
             │ ATmega16U2     │
             └───────┬───────┘
                     │ UART
                     │
       ┌─────────────▼─────────────┐
       │       ATmega328P          │
       │       Main MCU             │
       │                             │
       │ CPU + Flash + SRAM + GPIO  │
       │ ADC + timers + UART + SPI  │
       └──────┬──────────────┬──────┘
              │              │
           GPIO pins      Analog pins
              │              │
       ┌──────▼──────────────▼──────┐
       │ LEDs / resistors / headers  │
       └─────────────────────────────┘

Power:
USB / VIN / 5V
       │
       ▼
 voltage regulators
       │
       ▼
      5V / 3.3V
```

**ATmega328P** 是主微控制器。

还有：

* 电阻
* 电容
* 二极管
* 稳压器
* 晶振
* USB 转串行/接口 MCU
* 复位电路
* 电源选择/保护电路
* LED
* 排针/连接器

所以，Arduino 的某个引脚并不是简单连接到一个电阻或一根导线上。它最终会进入 **ATmega328P 内部的半导体电路**。

---

### 2. 如果万用表通断模式蜂鸣

假设你接成：

```text
black probe → GND
red probe   → some pin
```

然后万用表蜂鸣。

这通常意味着：

```text
R ≈ very small
```

例如：

```text
GND ──────────────── GND
       copper trace

R ≈ 0 Ω
```

万用表会注入一个小电流，并检查电压降是否足够小。

**但蜂鸣 ≠ “这两个引脚直接相连。”**

例如，许多万用表会在阻值低于大约 30–50 Ω 时蜂鸣（确切阈值因表而异）。

所以：

```text
0 Ω       → probably direct connection
10 Ω      → probably still beeps
100 Ω     → probably doesn't beep
1 kΩ      → definitely doesn't mean direct connection
```

具体蜂鸣阈值取决于你使用的万用表。

---

### 3. 电阻模式则不同

如果切换到 Ω 模式：

```text
Probe A ───── circuit ───── Probe B
```

看到：

```text
0.2 Ω
```

那基本上就是短路 / 直接的铜走线路径。

如果看到：

```text
1.0 kΩ
```

那么两点之间存在某种 **电阻性路径**。

但这里有个关键点：

> **非零电阻读数并不一定意味着引脚之间存在一个物理电阻器。**

例如：

```text
Pin A ── resistor ── Pin B
```

会得到一个电阻值。

但是：

```text
Pin A ── semiconductor ── Pin B
```

也可能给出类似电阻的读数。

还有：

```text
Pin A ── capacitor ── Pin B
```

可能会产生奇怪/变化的读数，因为电容会先被万用表的测试电流充电。

ATmega328P 内部有 **海量的晶体管**、二极管、MOSFET 结构等，所以用欧姆表测量其引脚之间时，可能会得到令人惊讶的奇怪数值。

---

### 4. 你观察到的 `1.xx V` 可能才是最重要的区别

如果你的万用表处于 **直流电压模式**，并且看到：

```text
1.23 V
```

这 **并不** 意味着：

> “这两个引脚之间有一个电阻。”

电压是 **电位差**。

例如：

```text
       5 V
        │
       1kΩ
        │
        ●──── probe
        │
       2kΩ
        │
       GND
```

中点可能大约是：

```text
3.33 V
```

因为这两个电阻构成了分压电路。

但你也可能从晶体管、二极管、IC 输出、上拉/下拉电阻、漏电流等得到：

```text
1.23 V
```

所以：

```text
Resistance mode:
    1.2 kΩ
       ↓
    tells you about an apparent resistive path

Voltage mode:
    1.2 V
       ↓
    tells you about electrical potential difference
```

它们是根本不同的测量。

---

### 5. 非常重要：不要在已通电的 Arduino 上使用 Ω 模式

这是一个常见的电子测量错误。

如果 Arduino 已通电：

```text
USB connected
      ↓
Arduino powered
      ↓
DO NOT measure resistance between arbitrary pins
```

电阻模式会使万用表向电路注入它自己的测试电流。

通常你应该：

```text
Power OFF → resistance / continuity measurement

Power ON  → voltage measurement
```

例如，排查 Arduino 接线时：

```text
POWER OFF

        continuity
             ↓
GPIO 13 ───────── LED/resistor ─── GND
             ↑
        beep / resistance
```

然后：

```text
POWER ON

        DC voltage
             ↓
GPIO 13 ─────────────── GND
             ↑
       measure voltage
```

---

### 6. 一个特别有意思的 Arduino 例子

Arduino Uno 板载 LED 的连接大致如下：

```text
ATmega328P
    │
    │ PB5 / Arduino D13
    │
    ├──── resistor ──── LED ──── GND
    │
```

所以如果你在**断电**状态下测量，可能会看到经过这条电路的电阻/通路。

但如果在**通电**状态下测量，你可能会看到：

```text
D13 → GND

LOW  → ~0 V
HIGH → ~5 V
```

这个 5 V 并不是告诉你 D13 和 GND 之间存在电阻。它告诉你的是，MCU 的输出电路正在把该引脚驱动至高电平。

更深层的图景是：

```text
                    ATmega328P
                 ┌───────────────┐
                 │               │
                 │    MOSFET     │
D13 ─────────────┤─────┬─────────┤
                 │     │         │
                 │   output      │
                 │   driver      │
                 └─────┬─────────┘
                       │
                      ...
```

这就是为什么 **Arduino GPIO 引脚是有源电子电路**，而不仅仅是从芯片引出的导线。

如果你正通过 Uno 学习电子，我还可以带你完成一个 **在 D13、5V、3.3V 和 GND 上的真实万用表实验**，展示在通断、电阻和电压模式下你应该看到什么读数。