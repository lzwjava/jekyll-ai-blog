---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla GPU最佳主板推荐
translated: true
type: note
---

问题：推荐哪些主板与 NVIDIA Tesla M40 或 P100 GPU 搭配使用？

回答：

以下是被广泛认可且已知可与 M40/P100 级别显卡配合使用的主板，按使用场景分类。由于您已持有 E5-2676 v3（LGA 2011-3），下列所有选项均保留该插槽，因此您的 CPU 可继续使用。

---

## 🏆 首选推荐（LGA 2011-3，兼容 E5-2676 v3）

**1. ASUS X99-E WS / X99-E WS USB3.1** — 综合最佳选择

社区测试已确认，该主板在开启 Above 4G Decoding 后，可稳定启动最多 6 张 Tesla P40。另有社区修改版 BIOS 可用，解锁 Resizable BAR 支持，将 MMIO High 空间从 256 GiB 增至 1 TiB，并更新所有微码——使其成为 X99 系列中非常适合计算 GPU 工作的主板之一。它配备 7 个 PCIe 3.0 x16 插槽，通过 PLX 交换机，可在四张卡同时使用时提供完整的 x16 带宽。

- 插槽：LGA 2011-3 | DDR4 | E-ATX
- Above 4G Decoding：✅ 支持（BIOS → Boot → Above 4G Decoding）
- ReBAR：✅ 通过社区 BIOS 修改
- 是否需要副显示 GPU：是（M40/P100 无视频输出）

**2. Supermicro X10SRA / X10SRA-F** — 工作站最佳选择

X10SRA-F 采用 C612 芯片组，支持 Intel Xeon E5-2600 v3 和 v4 系列，提供 4 个 PCIe 3.0 x16 插槽（运行于 16/16/NA/8 或 16/8/8/8），并配备双端口 Intel GbE LAN。Supermicro 的服务器级 BIOS 可稳定开启 Above 4G Decoding，处理大 BAR 显卡时比消费级主板更少出现异常。PCIe 插槽与桌面易用性（音频、USB 3.0）之间取得了良好平衡。

- 插槽：LGA 2011-3 | DDR4 ECC | ATX
- Above 4G Decoding：✅ 支持（可靠的服务器 BIOS）
- ReBAR：⚠️ 官方不支持

**3. Supermicro X10SRL-F** — 服务器/无头计算最佳选择

X10SRL-F 是 ATX 尺寸主板，采用 C612 芯片组，支持 E5-2600 v3 和 v4，共提供 7 个 PCIe 插槽（包括两个物理 x16 插槽对应的 PCIe 3.0 x8），10 个 SATA 6Gbps 端口，以及双 Intel i210 GbE LAN。这是一款扎实、无冗余设计的服务器主板，板载 VGA 可用于无头管理。如果要在 Linux 下运行推理/训练任务，这是个不错的选择。

- 插槽：LGA 2011-3 | DDR4 ECC RDIMM（最高 1TB） | ATX
- Above 4G Decoding：✅ 支持
- ReBAR：⚠️ 官方不支持，但可进行 BIOS 修改

---

## 快速对比

| 主板 | 板型 | PCIe x16 插槽数 | Above 4G | ReBAR 修改 | 内存类型 | 二手价格 |
|---|---|---|---|---|---|---|
| ASUS X99-E WS | E-ATX | 7（PLX） | ✅ | ✅ | DDR4 | ~$80–150 |
| Supermicro X10SRA-F | ATX | 4 | ✅ | ⚠️ | DDR4 ECC | ~$60–120 |
| Supermicro X10SRL-F | ATX | 7 | ✅ | ⚠️ | DDR4 ECC RDIMM | ~$50–100 |

---

## ⚠️ 重要提示

- **您现有的 DDR3 内存无法继续使用**——上述所有主板均采用 DDR4。如果想保留 DDR3，则需要选择国产 X99 克隆主板（华南、精粤、金悦等），但这些主板在未经 BIOS 修改的情况下，均无法可靠地启用 Above 4G Decoding。
- 对于 **M40/P100**，您仍需要一块廉价的显示 GPU（如 GT 710、Quadro 600 等）用于视频输出，因为这些显卡是无视频输出的纯计算卡。
- **电源**：三块主板均使用标准 ATX 24-pin + 8-pin EPS 接口。M40/P100 需要额外的 CPU 8-pin 电源适配器。

**ASUS X99-E WS** 是社区中专门针对 Tesla 级别显卡工作的热门选择，因其已确认支持多 GPU 且提供可用的 BIOS 修改。

---

**参考资料：**
- [ASUS X99-E WS BIOS Mod with ReBar + Multi-Tesla confirmed](https://winraid.level1techs.com/t/offer-asus-x99-e-ws-usb3-1-bios-mods-incl-rebar-support/116427)
- [Supermicro X10SRL-F specs](https://www.supermicro.com/zh_cn/products/motherboard/X10SRL-F)
- [Supermicro X10SRA-F specs](https://www.supermicro.com/ja/products/motherboard/X10SRA-F)