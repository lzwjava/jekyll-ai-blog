---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 寻找6+2针GPU电源线
translated: true
type: note
---

**问题：** 如何在航嘉 Huntkey Super 500W 电源上为 Quadro 4000 找到正确的 PCIe 电源接口？

**回答：**

好消息——航嘉 500W 电源通常配备 **(6+2 — 6+2)P GPU 接口**，这意味着你所需的就是这个。

以下是物理查找方法：

**步骤 1——查看电源引出的线缆**

电源线束中包含多条不同线缆。寻找标注或形状如下所示的线缆：

| 线缆 | 外观 | 用途 |
| --- | --- | --- |
| 24-pin | 宽扁平接口 | 主板 |
| 4+4 pin | 两个 4-pin 块 | CPU |
| **6+2 pin** ← | **6 个孔 + 侧面 2 个额外孔** | **GPU ← 就是这个！** |
| SATA | 扁平 L 形 | 硬盘 |

**步骤 2——识别 6+2 pin PCIe 线缆**

它看起来像这样：

```
[  6-pin 主体  ][+2 个额外 pin]
```

“+2”部分可以**分离**——对于 Quadro 4000，你只需要**6-pin**部分。只需将**2-pin 卡扣**从侧面分开，只将 6-pin 端插入显卡。

**步骤 3——插入显卡**

- 将 **6-pin 端**插入 Quadro 4000 顶部**左侧接口**
- 它只能以一个方向插入——推入直到听到**咔哒**声
- 显卡右侧的 4-pin 端口保持不动

**总结：**
> 找到带有 **6+2 接口**的线缆 → 分离 2-pin 侧 → 仅将 6-pin 插入 Quadro 4000。完成。✅

**参考：**

- [航嘉 CP5000 500W 规格](https://en.huntkey.com/product/cp5000-power-supply/)
- [航嘉 WD500K 接口详情 – VillMan](https://villman.com/Product-Detail/huntkey_wd500k-500w-80plus-gold-power-supply-)
