---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向AI开发者的华硕RTX 3090
translated: true
type: note
---

问题：为什么这是ASUS RTX 3090？ASUS是NVIDIA的合作伙伴吗？

答案：

是的。ASUS是NVIDIA的主要**AIB（Add-In Board）合作伙伴**之一。

NVIDIA自己设计GPU芯片：

```
NVIDIA
  |
  |-- GPU silicon (GA102 for RTX 3090)
  |-- reference design
  |-- CUDA / drivers
  |
  +---- ASUS
  +---- MSI
  +---- Gigabyte
  +---- Zotac
  +---- PNY
  +---- Palit
        |
        +-- custom PCB
        +-- cooler
        +-- power design
        +-- factory overclock
```

ASUS并不制造RTX 3090 GPU芯片。NVIDIA将GA102 GPU晶圆出售给合作伙伴，ASUS则构建最终的显卡。

---

ASUS RTX 3090产品线：

### ASUS TUF Gaming RTX 3090

目标：性价比 + 耐用性

* 三风扇散热器
* 厚散热鳍片
* 良好的VRM
* 通常价格较低
* 出厂超频略低

### ASUS ROG Strix RTX 3090

目标：发烧友

* 更大的散热器
* 更高的功耗限制
* 更好的PCB
* 更昂贵

### ASUS ProArt / workstation lines

目标：创作者

---

为什么ASUS有良好的声誉：

1. **悠久的GPU历史**

ASUS自1990年代起就开始制造NVIDIA显卡。

2. **强大的散热设计**

3090是一块非常热的GPU：

```
GA102 chip:
350W+ power
24GB GDDR6X memory
```

散热器至关重要。

ASUS TUF使用：

* 大型鳍片堆
* 多根热管
* 三个轴流风扇
* 良好的VRM散热

3. **更好的转售价值**

二手市场通常价值排序：

```
ASUS ROG Strix
    >
ASUS TUF
    >
MSI Gaming X Trio
    >
Gigabyte Gaming OC
    >
Zotac / Palit / Colorful lower models
```

（视国家/地区而定。）

---

对于AI使用，品牌的重要性低于：

```
VRAM size
+
cooling
+
power stability
+
memory temperature
```

CUDA性能几乎相同。

例如：

```
ASUS TUF RTX 3090
```

和：

```
MSI RTX 3090
```

使用相同的GA102芯片，训练你的PyTorch模型速度几乎相同。

我喜欢这个列表的原因不仅仅是'ASUS'，而是：

```
RTX 3090
+
24GB VRAM
+
good cooler
+
70°C stress temperature
```

这种组合正是AI开发者希望从二手GPU中得到的。