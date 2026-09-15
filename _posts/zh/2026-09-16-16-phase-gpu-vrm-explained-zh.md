---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 16相GPU VRM详解
translated: true
type: note
---

**问题：** GPU VRM 中的“16相”是什么意思？为什么要用16相？

**回答：**

把GPU VRM想象成 **16个并联工作的小型降压转换器**，它们共同为同一个GPU核心电压轨供电。

一个简化的单相结构如下：

```text
             12V
              │
          ┌───▼───┐
          │ MOSFET│  ← 高频开关
          └───┬───┘
              │
           ┌──▼──┐
           │     │
           │ L   │  ← 电感
           │     │
           └──┬──┘
              │
              ├────────── GPU Vcore ≈ 0.8~1.0V
              │
            caps
              │
             GND
```

**16相** 设计大致如下：

```text
                    ┌─ 相0 ─ MOSFET ─ L ─┐
                    ├─ 相1 ─ MOSFET ─ L ─┤
12V ────────────────┼─ 相2 ─ MOSFET ─ L ─┼─── Vcore
                    │          ...            │
                    └─ 相15 ─ MOSFET ─ L ─┘

                         ↑
                     uP9512U
                    PWM 控制器
```

各相在时间上是**交错工作的**。它们不是16个独立的电压源，而是16个同步的功率级共享一个输出轨。多相VRM采用这种布局来分担电流并降低输出纹波。([Cadence PCB Resources][1])

---

### 为什么不用一个超大功率的转换器？

假设GPU需要：

```text
V = 0.9 V
I = 400 A

P ≈ 0.9 × 400 = 360 W
```

如果只有一相，那么全部的 **400A** 电流都要流过这一组功率元件。

如果是16相，理想情况下：

```text
400 A / 16 = 25 A 每相
```

所以每一相在概念上可以看作：

```text
相0:   25A ─┐
相1:   25A ─┤
相2:   25A ─┤
   ...           ├── 总计 400A
相15:  25A ─┘
```

这极大地有助于：

1. **电流处理能力** — 每个MOSFET/电感处理的电流更小。
2. **热性能** — 传导损耗大致遵循 `I²R`，因此分流电流至关重要。
3. **瞬态响应** — 多个相位可以响应GPU快速的负载变化。
4. **纹波** — 各相彼此错开，因此它们的纹波部分相互抵消。([VoltGround][2])

---

### 但从电气角度看，“相”到底是什么意思？

这是最有趣的部分。

假设每相开关频率为：

```text
f_sw = 500 kHz
```

使用4相时，可以将它们错开：

```text
相0: |████|        |████|
相1:     |████|        |████|
相2:         |████|        |████|
相3:             |████|        |████|
```

对于16相：

```text
P0   ↑
P1     ↑
P2       ↑
P3         ↑
...
P15                            ↑
```

它们相隔大约：

$$
\frac{360^\circ}{16}=22.5^\circ
$$

因此，尽管每个相位各自以500 kHz的频率开关，但组合输出的纹波抵消频率高得多。

这就是为什么 **“16相”并不意味着16倍的开关频率**。每个转换器仍然以自身的开关频率进行开关；各相只是**在时间上交错**。

---

### 为什么恰好是16相？

16这个数字并没有什么神奇之处。

这是一种工程权衡。

对于高端GPU：

```text
             更少的相数
                  │
                  ▼
        ┌──────────────────┐
        │  4相            │
        │  每相 100 A      │
        └──────────────────┘
                  │
                  │
        ┌──────────────────┐
        │  8相            │
        │  每相 50 A       │
        └──────────────────┘
                  │
                  │
        ┌──────────────────┐
        │ 16相            │
        │ 每相 25 A        │
        └──────────────────┘
```

更多的相位通常意味着 **更多的元件、PCB面积、成本、栅极驱动损耗和控制复杂性增加**。所以你不会无限地增加相数。([AI Data Centers][3])

而且重要的是，**16相并不自动优于12相**。实际的功率级额定电流、MOSFET/DrMOS效率、电感、开关频率、热设计、PCB铜皮以及控制器实现都很重要。

---

### 关于你的uP9512U的一个有趣细节

uP9512系列是专门为**多相GPU降压控制器**设计的。其数据手册描述了各相之间的相电流检测和电流平衡功能。它还可以在轻载时动态减少激活的相数（“相数节减”）。([UPI Semi][4])

所以概念上：

```text
GPU 空闲
   ↓
可能激活 2~4 相
   ↓
GPU 负载增加
   ↓
8 相
   ↓
重负载
   ↓
16 相
```

具体相数取决于特定的uP9512变体/板卡实现——原始的uP9512文档本身指定了可选1-8相操作，因此如果你的主板宣传为**16相**，则很可能涉及额外的倍相/交错电路或相关的控制器实现。([Alldatasheet][5])

**我建议你保留的心智模型很简单：**

```text
"16相VRM"
       =
"16个并联的小型降压转换器，
 分担GPU的巨大电流，
 且其开关时钟交错分配。"
```

如果你正在对实际的GPU PCB进行逆向工程，我还可以详细说明**如何查看板卡并通过电感、DrMOS/MOSFET、PWM走线和uP9512引脚来识别这16个相**。

[1]: https://resources.pcb.cadence.com/pcb-design-blog/2019-what-is-a-vrm-and-why-does-my-cpu-gpu-need-one-2?utm_source=chatgpt.com "什么是VRM以及为什么我的CPU/GPU需要它？| 高级PCB设计博客 | Cadence"
[2]: https://voltground.com/hardware/gpu-vrm-phases-power-delivery/?utm_source=chatgpt.com "GPU VRM相数与供电：相数对超频实际意味着什么——VoltGround"
[3]: https://aidatacenterguide.com/part-7-compute-silicon-and-system-integration/7-12-on-package-power-delivery-and-power-integrity?utm_source=chatgpt.com "封装上供电与电源完整性 · AI数据中心权威指南"
[4]: https://www.upi-semi.com/upisemi/products/ic/dc-dc-controller/multiple-phase-buck-controller/up9512p/?utm_source=chatgpt.com "uP9512P | uPI Semi"
[5]: https://www.alldatasheet.net/html-pdf/2289152/UPI/UP9512/61/1/UP9512.html?utm_source=chatgpt.com "UP9512 数据手册(第1/31页) UPI | 8/7/6/5/4/3/2/1相同步整流降压控制器，带SMBus数字接口"
