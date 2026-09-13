---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双8针GPU电源连接器指南
translated: true
type: note
---

**问题：** 什么是双8针GPU电源连接器，如何正确使用它？

**回答：**

"双8针"电源配置意味着你的GPU拥有**两个8针PCIe电源插口**，两者都需要连接到你的电源（PSU）。以下是需要了解的全部信息：

---

### 为什么需要两个8针连接器？

每个8针PCIe连接器额定供电为**150W**。因此，配备两个8针连接器的GPU功耗范围大约在**151–300W**之间。中高端GPU（如RTX 3070/3080系列）通常采用这种配置。

---

### 如何连接

你有两种主要选择：

**选项A — 使用两根独立线缆（高功耗GPU推荐）**

- 从电源为每个8针插口**分别连接一根线缆**。
- 每根线缆插入电源上独立的PCIe端口。
- 这样不仅安全，而且是理想选择——有记录显示，当使用单根分叉线缆连接两个接口时，高功耗GPU（如RX 5700 XT）会出现供电问题。

**选项B — 使用一根分叉线缆（Y型分线）**

- 从电源引出的一根线缆在GPU端**分成两个8针接口**。
- 如果你的GPU功耗在151–300W范围内，一根分叉线缆就足够了，无需使用两根独立线缆。
- 对于功耗极高的显卡（例如300W以上）不理想，因为两个接口共享同一根线缆的电流路径。

---

### 重要警告

- **不要使用随意的第三方PCIe线缆**——不同电源品牌之间没有通用的引脚定义标准。为你的电源使用错误线缆可能导致电气短路。务必使用专为你特定电源型号设计的线缆。
- 确保连接器**咔哒一声完全插入**GPU。在高功耗显卡上，8针连接器未完全插入已导致接口熔化。
- CPU 8针和PCIe 8针连接器**外观几乎相同**但接线方式不同——切勿将CPU线缆用于GPU插槽。

---

### 快速视觉指南

```
电源PCIe端口1 ──→ [8针线缆] ──→ GPU插口1
电源PCIe端口2 ──→ [8针线缆] ──→ GPU插口2
```

或使用分叉线缆：

```
电源PCIe端口1 ──→ [Y型分叉线缆] ──┬──→ GPU插口1
                                   └──→ GPU插口2
```

**参考资料：**

- [Tom's Hardware – 双8针连接讨论](https://forums.tomshardware.com/threads/connecting-a-gpu-with-dual-8-pin-connectors-to-psu.2648670/)
- [Corsair – 独立8针与分叉连接器对比](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/individual-8-pin-vs-pigtail-connectors-for-gpus/)
- [GPU Mag – GPU电源连接器详解](https://www.gpumag.com/gpu-power-connectors-explained/)
