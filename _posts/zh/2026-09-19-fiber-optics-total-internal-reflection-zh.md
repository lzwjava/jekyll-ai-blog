---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 光纤：全内反射
translated: true
type: note
---

Question: 光纤是如何工作的？它利用了光的什么特性？

Answer: 光纤主要利用 **total internal reflection** 将光引导通过一根非常细的玻璃/塑料纤维。

![Image](https://images.openai.com/static-rsc-4/f51fuex8FuD4qyclLZ_BnLQU2c6OFdKZGk92OfafDXeOtAnP7zkhm5penu23805uXwk2HbSLfRUXQhbtdE0NW2HvmkwuXM70IZ-rlB4piOMzR5N9oVF2WblcW6QmU52XNiDH0vjNvYxh5dZ2EXO8oar84E8YTC-Av5qvVuujjUEbikbcq2CZj-IJjpcfPz62?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0S3l63Q-gF9DnsDBxB2bw7LrhzrgiZZGb5yjx6wQsDcl1mlAIn--0heyFbozXMMGyh-IOBPnNLwoAgiCYyeHaedK9PxoAx6XW_bnS3rOeKANaHA2wlTnOHerqFpAFdiSY9M3d-um-8VTw9s5wqFsvEuLxcgwc3dyCRpHnzKr2s7Ul3jVN_TEwnuYwRJY-Ncm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/J5a13Mv4V2mIqTcshqZpFGPlhNoy7--IGhIrm1B4GlKr6fvUvIo-qehLK7LKWvyiGrv18TRxkYfGuXkmkepCYBAhXy-2TvJwsfoM8ZOjstptUCCpkUMMERFCyF-e7p1G5iixSMxIwRsre7QyK4i9XIC7pwfpaTOPWn2uCen1ZX5oxzv8tFn72RyNvNetT2G7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Hj8_y7IVtNtjOSvjR7obHq4wBzL1gF8Iqbp_v6fpnj5IIeeVnUx020vSz0lxEt7SlXVEKXOG5DNiudEZ00oDcqeuCCX8OD7h_Ohfz_SEBq82wdrzVKScAenmHzaih-BK5f1-rd9oLKtSMB41-wcGxNsbU7OZXHyJmX_sF9Ld0TSjFvHGVxUNLOAQzBVjHi5V?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/FVUq0zZExp6kYTu2oTkVDZAyeJWn_M0PtBxdVseTp-twA0SHh7qJlZJmODz1j1iCq_dsN9jAu_C1SV4k5JAeb_p4iYcS4PlgGEnWKgP5HPD-GmczW5D2shC3UuOX14R8rwdvJ7GUYV1M5q1TtS7-mJjnHdcn3k_1T6WBxbXdNxSct2kwRDy6Th5QUsv93Lsh?purpose=fullsize)

核心思想是：

```text
        cladding (lower refractive index)
   ┌─────────────────────────────────────┐
   │  ↘       ↗       ↘       ↗         │
   │    ↘   ↗           ↘   ↗           │
   │      ↘               ↘             │
   │        ↘             ↗             │
   │          ↘         ↗               │
   └─────────────────────────────────────┘
             ↑
           core
       higher refractive index
```

### 1. 它利用光的 **electric field** 来承载信息

发射器将电数据转换为：

```text
10110010...
    ↓
laser / LED
    ↓
light pulses
```

例如：

```text
1 → light ON
0 → light OFF
```

更复杂的系统利用光波的几种属性来编码信息，包括：

* **Intensity/amplitude**
* **Phase**
* **Frequency / wavelength**
* **Polarization**

现代相干光纤通信可以利用振幅和相位的组合，在每个符号中编码多个比特。

### 2. 为什么光不会泄漏？

光纤有两层：

```text
        Cladding
   ┌─────────────────┐
   │    ┌───────┐    │
   │    │ CORE  │    │
   │    │       │    │
   │    └───────┘    │
   └─────────────────┘
```

**core 的 refractive index 高于 cladding**：

```text
n_core > n_cladding
```

当 core 内部的光以足够大的角度射向 core/cladding 边界时，会发生 **total internal reflection**。

临界角为

$$
\theta_c = \sin^{-1}\left(\frac{n_{cladding}}{n_{core}}\right)
$$

因此光被限制在 core 内。

### 3. 真正有趣的部分：光纤本质上是一个 waveguide

很容易想象成：

```text
laser → bouncing photon → bouncing photon → receiver
```

但物理上，电磁场是以 **guided optical modes** 传播的。

因此更好的思维方式是：

```text
electrical bits
      ↓
electro-optical modulation
      ↓
electromagnetic wave
      ↓
fiber waveguide
      ↓
photodetector
      ↓
electrical bits
```

在接收端，一个 photodiode 将光信号转换回电信号。

### 4. 为什么光纤能承载巨大的带宽

可见光的频率在数百 **THz** 范围内。

电信通常使用以下波长的光：

```text
850 nm
1310 nm
1550 nm
```

1550 nm 对应大约

$$
f = \frac{c}{\lambda}
  \approx \frac{3\times10^8}{1.55\times10^{-6}}
  \approx 193\text{ THz}
$$

这与普通电缆相比，是一个巨大的电磁带宽。

而现代系统不仅使用 ON/OFF。它们可以使用 **WDM (wavelength-division multiplexing)**：

```text
1550.1 nm ──┐
1550.3 nm ──┤
1550.5 nm ──┤──→ same fiber
1550.7 nm ──┤
1550.9 nm ──┘
```

每个波长可以承载独立的高速数据流。

所以最短的答案是：

> **Optical fiber 利用电磁光波，光纤的 refractive-index 结构将这些波引导通过 core。通过调制 intensity、phase、frequency 和 polarization 等属性来编码信息。**

接下来我可以逐步讲解 **一个以太网数据包从 CPU → NIC → optical transceiver → fiber → 接收 NIC 的过程**，包括电信号在何处变成光子以及如何变回电信号。
