---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 支持ReBAR的X99主板
translated: true
type: note
---

**问题：** 哪些 LGA2011-3 X99 主板原生支持 Resizable BAR 和 Above 4G Decoding？

**答案：**

下面按类别清晰分类——从原生支持这些功能的主板，到可以通过 BIOS 修改获得这些功能的主板。

---

**第一类——原生支持（开箱即用）**

如果 ReBAR 和 Above 4G Decoding 对你很重要，这些是最佳选择：

**华南金牌 X99 BD4（DDR4）**
华南金牌 BD4 的 BIOS 原生包含 Above 4G Decoding 和 Resizable BAR 支持，以及智能风扇控制、内存超频、Secure Boot 和 TPM 支持。在 LGA2011-3 平台的廉价国产主板中，这块板是 ReBAR 的黄金标准。它使用 DDR4 内存，ATX 板型。这是改装社区中最常被推荐作为即插即用解决方案的主板。

**华南金牌 X99 F8D（双路，DDR4）**
对于双路 Xeon 平台，F8D 是其更大的兄弟型号，继承了相同的 BIOS 功能。虽然不太常见，但如果你在组建多 CPU 工作站，这块板值得考虑。

---

**第二类——可通过刷入华南金牌 BD4 的 BIOS 实现**

改装版华南金牌 BD4 BIOS 已确认可在 Jingsha X99-8D3 和 X99-D8 主板上正常工作，改装版 BIOS 中默认启用了 Above 4G Decoding 和 ReBAR。ReBAR 也已确认可通过此改装版华南金牌 BD4 BIOS 在精粤 X99 系列上正常工作，并已使用 Nvidia RTX 3070 和 AMD RX 5700 XT 及 RX 6600 XT 进行过个人实测。

社区中的关键经验是，可以通过更换 ME（Management Engine）区域同时保留 BD4 的 BIOS 区域，将华南金牌 BD4 的 BIOS 移植到多款兼容的国产 X99 主板上。这需要使用 CH341A 硬件编程器。

---

**第三类——需要 BIOS 修改，已确认可用**

以下品牌主板有 WinRaid 社区提供的修改版 BIOS，其中注入了 ReBAR + Above 4G Decoding：

- **华硕 X99 Deluxe** — 提供修改版 BIOS，Above 4G 偏移位于 `0x173`
- **华硕 X99-A / X99-A USB 3.1** — 提供来自 WinRaid 的修改版 BIOS
- **华硕 X99-E WS / X99-E WS USB 3.1** — 提供修改版 BIOS
- **技嘉 X99 UD4P / X99 Gaming 5 / X99 Designare EX** — 提供修改版 BIOS

---

**汇总表**

| 主板 | 内存类型 | 原生 ReBAR | 难度 |
| --- | --- | --- | --- |
| 华南金牌 X99 BD4 | DDR4 | ✅ 是 | 无 |
| Jingsha X99-D8 / 8D3 | DDR4 | 通过 BIOS 互换 | 中等（需要 CH341A） |
| 华硕 X99 Deluxe/A | DDR4 | 通过 BIOS 修改 | 中等 |
| 精粤 X99M-D D3 / GD4 ARGB | DDR3/4 | ❌ 否 | 困难/不确定 |

**结论：** 如果你的目标是在 LGA2011-3 平台上以最省事的方式获得完整的 ReBAR + Above 4G Decoding 支持，**华南金牌 X99 BD4** 是社区明确推荐的选择。它也是 AliExpress 上广泛有售的型号，价格通常与其他国产 X99 主板相当。

---

**参考链接：**

- [指南：国产 X99 主板超频 BIOS 修改 – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [求助：为 Jingsha X99-D8 修改 ReBAR – WinRaid](https://winraid.level1techs.com/t/request-mod-jingsha-x99-d8-with-rebar-4g-encoding/110083)
- [求助：修改精粤 X99I-SERVER – WinRaid](https://winraid.level1techs.com/t/request-mod-jginyue-x99i-server-with-rebar-4g-decoding/114076)
- [提供：支持 ReBAR 的华硕 X99-A 系列 BIOS 修改 – WinRaid](https://winraid.level1techs.com/t/offer-asus-x99-a-series-bios-mods-with-rebar-support/116496)
