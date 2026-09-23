---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 红外电磁辐射概述
translated: true
type: note
---

问题：什么是 **红外线电磁波 (infrared electromagnetic radiation)**？

答案：

**红外线（IR）是波长比可见红光更长、比微波更短的电磁辐射。**

电磁波谱大致为：

```text
short wavelength                                      long wavelength
    │                                                      │
    ▼                                                      ▼
   γ-rays → X-rays → UV → visible → infrared → microwave → radio
                              │
                         red → IR
```

典型的红外波长：

$$
\boxed{700\text{ nm} \sim 1\text{ mm}}
$$

更精确地说，它与可见光的分界通常约为 **700–750 nm**，与微波的分界约为 **1 mm**。

### 关键的物理原理

与可见光一样，红外线也是由**光子**组成的。光子的能量为

$$
E = h\nu = \frac{hc}{\lambda}
$$

因此波长越长，光子能量越低。

例如：

* 可见红光：\\(\lambda \approx 650\text{ nm}\\)
* 近红外：\\(\lambda \approx 850\text{ nm}\\)
* 热红外：\\(\lambda \approx 10\ \mu m\\)

所以红外光子的能量低于可见光光子。

### 为什么我们会把红外线与热联系在一起？

因为室温下的普通物体会在红外波段辐射大量电磁波。

对于黑体，峰值波长近似满足 Wien's law：

$$
\lambda_{\max} = \frac{b}{T}
$$

对于室温，\\(T\approx300K\\)：

$$
\lambda_{\max}
\approx
\frac{2.9\times10^{-3}}{300}
\approx 9.7\ \mu m
$$

这属于**红外线**。

所以，当你感受到来自以下对象的热量时：

```text
your hand
   ↓
infrared photons
   ↓
your skin
```

你实际上是在接收由温度更高的物体发出的电磁辐射。

这也是为什么**热像仪**能在黑暗中“看到”人：它不是看到可见光子，而是在探测与物体温度相关的红外辐射。

### 红外线并不是单一的一种

可以将其分为以下几类：

```text
Near IR       ~0.7–1.4 μm
Short-wave IR ~1.4–3 μm
Mid-wave IR   ~3–8 μm
Long-wave IR  ~8–15 μm
Far IR        ~15 μm–1 mm
```

不同波长的红外线与物质的相互作用也不同。

例如：

* **850/940 nm 红外 LED** → 遥控器、传感器、摄像头
* **~1.3/1.55 μm** → 光纤通信
* **~3–5 μm** → 许多热/工业传感应用
* **~8–14 μm** → 热成像，因为地球大气在这个波段有一个有用的透射窗口

关键点在于：

> **红外线并不是“一种热”。它是电磁辐射。热是系统之间转移的能量；红外线只是这种能量得以转移的一种机制。**

而从数学描述上看，**红外线就是波长比可见红光更长、频率比可见红光更低的光。**

References:

* [NASA — Infrared Waves](https://science.nasa.gov/ems/07_infraredwaves/)
* [Encyclopaedia Britannica — Infrared radiation](https://www.britannica.com/science/infrared-radiation)
* [NIST — Electromagnetic Spectrum](https://www.nist.gov/pml/owm/metric-si/si-units-quantities)