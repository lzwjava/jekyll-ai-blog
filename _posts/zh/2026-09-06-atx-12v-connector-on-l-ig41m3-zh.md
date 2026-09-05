---
audio: false
generated: true
image: false
lang: zh
layout: post
title: L-IG41M3上的ATX 12V连接器
translated: true
type: note
---

**问题：** 联想 L-IG41M3 主板上的 ATX 12V 接口是什么意思？

---

**回答：**

**ATX 12V 接口**是主板上一个**独立的小型电源接口**，与主流的 20/24 针 ATX 接口完全不同。你需要了解以下内容：

---

### 🔌 它是什么

这是一个**4 针或 8 针的方形接口**，专门为 CPU 提供 **+12V 电源**。在 L-IG41M3（较老的主板）上，它通常是 **4 针的 ATX12V 接口**，也称为 **"P4 接口"**。

```
[ +12V ][ +12V ]
[ GND  ][ GND  ]
```

---

### ⚡ 为什么存在

主板的 24 针接口为整个主板供电（内存插槽、PCIe、芯片组等），但 **CPU 需要一条专用的、干净的 12V 线路**，供 VRM（电压调节模块）降压为 CPU 实际工作电压（约 1.1V–1.4V）。如果未插入此接口，CPU 将**无电**，电脑完全无法启动。

---

### 🔧 在你的 Huntkey 280W 电源上

你的 Huntkey 280W 电源应带有一条 **4 针 ATX12V 线缆**——它是一个小型方形 4 针插头，**与主 20 针线缆分开**。你必须将其插入 L-IG41M3 主板上 CPU 插座旁边的小型方形插槽。

| 接口 | 用途 | 针数 |
| --- | --- | --- |
| 主 ATX 接口 | 为整块主板供电 | 20 针（你的电源） |
| ATX 12V 接口 | 仅为 CPU 供电 | 4 针方形 |

---

### ⚠️ 不要忽略它

如果你只插了主 20 针接口而忘记了 ATX 12V 4 针接口，系统会通电（风扇可能转动），但 **无法 POST 或启动**——这是一个非常常见的错误。

---

**参考：**

- [ATX 12V 电源接口详解 — computerhope.com](https://www.computerhope.com/jargon/a/atx.htm)
- [什么是 ATX 12V 接口？ — Tom's Hardware](https://www.tomshardware.com/reviews/psu-buying-guide,4229.html)
