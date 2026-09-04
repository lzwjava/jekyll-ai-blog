---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 4000 电源连接器指南
translated: true
type: note
---

**问题：** 在 Quadro 4000 显卡上，哪一侧是 6-pin PCIe 电源接口——左侧还是右侧？右侧的 4-pin 接口是什么？

**答：**

**6-pin PCIe 电源接口位于左侧**（朝向显卡顶部/后部）。这是你需要将电源线插入的接口。

**右侧的 4-pin 接口**是一个 **Molex 样式转接端口**——它是 NVIDIA 随附的 **Y 型转接线**的一部分。示意图如下：

```
显卡顶部边缘：
┌─────────────────────────────────┐
│  [6-pin PCIe] ← 在此插入电源线  [4-pin] ← Molex 转接头（如果电源已有 6-pin 则忽略）
└─────────────────────────────────┘
```

**总结：**

| 接口 | 用途 | 是否使用？ |
| --- | --- | --- |
| **6-pin（左侧）** | 主 PCIe 电源输入 | ✅ 是——在此插入电源线 |
| **4-pin（右侧）** | Molex 转接端口 | ❌ 仅当电源没有 6-pin 接口时使用 |

显卡附带一根 6-pin 转两个 4-pin 的转接线——该转接头适用于没有专用 PCIe 电源接口的电源。如果你的电源已有 6-pin（或可拆分 2-pin 的 8-pin）PCIe 线缆，**完全忽略 4-pin 侧**，直接插入 6-pin 接口即可。

**参考来源：**

- [如何将 Quadro 4000 连接到电源 – Tom's Hardware 论坛](https://forums.tomshardware.com/threads/how-to-connect-quadro-4000-to-psu.791303/)
- [Quadro 4000 规格 – eBay 商品页](https://www.ebay.com/itm/167837856419)
