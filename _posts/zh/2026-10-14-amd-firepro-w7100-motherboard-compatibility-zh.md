---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD FirePro W7100 主板兼容性
translated: true
type: note
---

**问题：** AMD FirePro W7100 可以使用哪些主板？

---

**答案：**

好消息是兼容性要求很简单——**几乎所有现代台式机或工作站主板都可以使用**，因为该显卡采用标准的 PCIe x16 插槽并且向后兼容。

**硬性要求**

| 要求 | 详情 |
|---|---|
| 插槽 | PCIe x16（物理） |
| 理想情况 | PCIe 3.0 x16 |
| 向后兼容 | PCIe 2.0 x16、PCIe 1.0 x16（带宽降低，但可用） |
| 外形规格 | 全高，单插槽 |
| 电源接口 | 来自 PSU 的 1× 6-pin PCIe |
| 最低电源 | 建议 ~300–350W |

---

**兼容平台示例**

**Intel 台式机（消费级）**

| 芯片组 | 插槽 | 备注 |
|---|---|---|
| Z87 / H87 | LGA1150（第4代 Core） | PCIe 3.0 ✅ |
| Z97 / H97 | LGA1150（第4/5代） | PCIe 3.0 ✅ |
| X99 | LGA2011-v3（Core i7/i9 Extreme） | PCIe 3.0 ✅ 理想选择 |
| Z170 / Z270 | LGA1151（第6/7代） | PCIe 3.0 ✅ |
| Z370 / Z390 | LGA1151（第8/9代） | PCIe 3.0 ✅ |
| Z490 / Z590 | LGA1200（第10/11代） | PCIe 4.0（向后兼容 ✅） |
| Z690+ | LGA1700（第12代及更高版本） | PCIe 5.0（向后兼容 ✅） |

**Intel 工作站**

| 平台 | 插槽 | 备注 |
|---|---|---|
| C612 (Wellsburg) | LGA2011-v3（Xeon E5 v3/v4） | 原始目标平台 ✅ |
| C236 | LGA1151（Xeon E3 v5/v6） | PCIe 3.0 ✅ |

**AMD 台式机**

| 芯片组 | 插槽 | 备注 |
|---|---|---|
| B450 / X470 | AM4（Ryzen 2000+） | PCIe 3.0 ✅ |
| B550 / X570 | AM4（Ryzen 3000+） | PCIe 4.0（向后兼容 ✅） |
| B650 / X670 | AM5（Ryzen 7000+） | PCIe 5.0（向后兼容 ✅） |

---

**需要注意的事项**

- **PCIe 2.0 主板** — 可以使用，但理论带宽减半。对于显示/CAD 使用场景，你永远不会注意到差异。
- **Mini-ITX 机箱** — 该显卡是**全高**（高 111mm），因此半高或 mini-ITX 配置无法安装。
- **没有外部供电** = 无法启动 — 它需要那个 **6-pin PCIe 供电接口**；非常基础的 OEM 电源可能没有。
- **4× DisplayPort 输出**需要 DisplayPort 显示器或主动式转接器 — 显卡上没有直接的 HDMI/DVI 接口。
- 该显卡兼容 PCIe 3.0，但也能在带有 PCIe 4.0 或 5.0 的主板上以向后兼容模式运行 — 因此较新的主板也没问题。

---

**总结** — 任何约 2012 年之后制造的、带有全尺寸 PCIe x16 插槽的主板都可以毫无问题地使用这张显卡。这是 W7100 最具“即插即用”特性的方面之一。

---

**参考资料：**
- [PCHardware.org – FirePro W7100 规格](https://pchardware.org/graphics-cards/amd-firepro-w7100/)
- [Puget Systems – FirePro W7100](https://www.pugetsystems.com/parts/Video-Card/AMD-FirePro-W7100-PCI-E-8GB-10817)
- [B&H – FirePro W7100 产品参数表](https://www.bhphotovideo.com/lit_files/210878.pdf)