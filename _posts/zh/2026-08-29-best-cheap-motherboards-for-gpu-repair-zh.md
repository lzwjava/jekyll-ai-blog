---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 显卡维修最佳廉价主板
translated: true
type: note
---

问题：除了 H81，还有哪些主板适合搭建廉价的显卡维修测试平台？

答案：

是的，关键**不在于非要用 H81**。你朋友真正需要的是：

```text
廉价主板
+ 带核显的廉价 Intel CPU
+ 物理 PCIe x16 插槽
+ 主板视频输出接口
+ 稳定的 BIOS
```

为此，我给老 Intel 平台排个序：

| 芯片组       | 插槽类型  | 适合显卡维修？ | 我的评价                        |
| ------------ | --------- | -------------: | ------------------------------ |
| **H81**      | LGA1150   |          ⭐⭐⭐⭐⭐ | 最便宜 / 最简单                |
| **B85**      | LGA1150   |          ⭐⭐⭐⭐⭐ | 可能我的首选                   |
| **H87**      | LGA1150   |          ⭐⭐⭐⭐⭐ | 同样优秀                       |
| **H97**      | LGA1150   |           ⭐⭐⭐⭐ | 不错但可能更贵                 |
| **H61**      | LGA1155   |           ⭐⭐⭐⭐ | 非常便宜，较老                 |
| **B75**      | LGA1155   |          ⭐⭐⭐⭐⭐ | 极佳的廉价替代品               |
| **H67/Z68**  | LGA1155   |            ⭐⭐⭐ | 能用，但没有理由优先选择       |
| **B250/H270**| LGA1151   |          ⭐⭐⭐⭐⭐ | 更新，通常更贵                 |

Intel 8 系列芯片组官方包括 H81、B85、H87、Q87 等；H81/B85/H87 都是 LGA1150 时代的平台。([Intel][1])

### 我更推荐买 B85

针对你的使用场景：

```text
B85 主板
+
i5-4570 / i5-4590
+
8–16 GB DDR3
+
廉价 SSD
```

为什么选 B85？

与 H81 相比，B85 提供了更多的扩展、存储和 USB 接口，同时保留了相同的 LGA1150 + Haswell 基本架构。更重要的是，CPU 提供了核显，这样你正在维修的独立显卡可以作为**测试中唯一的 PCIe 显卡**。([Tom's Hardware][2])

结构类似于：

```text
              i5-4570
                 │
        ┌────────┴────────┐
        │                 │
     Intel HD           CPU PCIe
        │                 │
        ▼                 ▼
   主板输出           PCIe x16
   HDMI/DVI/VGA          │
        │                │
        ▼                ▼
     显示器          待测显卡
```

这正是维修台上需要的架构。

### 在二手市场搜索时建议

不要只搜 `H81`。

尝试：

```text
H81 LGA1150
B85 LGA1150
H87 LGA1150
H97 LGA1150
B75 LGA1155
H61 LGA1155
```

CPU 搜索：

```text
i5-4570
i5-4590
i5-3470
i5-3570
```

**重要提醒：** 确保具体主板带有 **HDMI/DVI/VGA 输出接口**。芯片组本身并不能保证主板厂商实际在板上放置了哪些显示接口。([Puget Systems][3])

如果你专门为了**显卡维修**购买，我宁愿花 **20–30 美元买一块 B85/H81 + i5 套装**，而不是把钱花在 X99/X299 平台上。你不需要 CPU 性能，你需要一台无聊但能可靠启动的机器，因为你正在调试的是那块昂贵的显卡。

参考链接：

* [Intel 8 Series Chipsets](https://www.intel.com/content/www/us/en/ark/products/series/98459/intel-8-series-chipsets.html?utm_source=chatgpt.com)
* [H81/B85/H87 comparison — Tom's Hardware](https://www.tomshardware.com/reviews/asrock-b85m-dgs-asrock-h81m-hds-asus-h81m-e-msi-h91m-e34%2C4099.html?utm_source=chatgpt.com)
* [Z87/H87/H81/B85 comparison — Puget Systems](https://www.pugetsystems.com/labs/articles/Z87-H87-H81-Q87-Q85-B85-What-is-the-difference-473/?utm_source=chatgpt.com)

[1]: https://www.intel.com/content/www/us/en/ark/products/series/98459/intel-8-series-chipsets.html?utm_source=chatgpt.com "Intel® 8 Series Chipsets"
[2]: https://www.tomshardware.com/reviews/asrock-b85m-dgs-asrock-h81m-hds-asus-h81m-e-msi-h91m-e34%2C4099.html?utm_source=chatgpt.com "Four LGA-1150 Motherboards Under $60 - Tom's Hardware | Tom's Hardware"
[3]: https://www.pugetsystems.com/labs/articles/Z87-H87-H81-Q87-Q85-B85-What-is-the-difference-473/?utm_source=chatgpt.com "Z87, H87, H81, Q87, Q85, B85 - What is the difference? | Puget Systems"