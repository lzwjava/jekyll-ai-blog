---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 二手AI服务器成本估算
translated: true
type: note
---

**问题：** 在公开市场上购买一台双路 Broadwell 服务器（48 线程、62 GiB 内存、2× Tesla P100 12 GB）需要多少钱？

**答案：**

这套系统包含三个成本组成部分。以下是基于当前市场数据（2026 年 9 月）的详细分析：

---

### 1. 基础服务器（双路 Broadwell，约 48 线程，约 64 GB 内存）

符合此规格的典型服务器（如 Dell PowerEdge R730 或 HP DL380 Gen9，双路 Xeon E5-2600 v4 Broadwell，约 64 GB 内存）在二手市场广泛可得。目前 eBay 上双路 Intel 服务器（64 GB 内存）的翻新设备价格大约在 **200–550 美元** 之间，具体取决于 CPU 型号、硬盘配置和成色。一台配置为 48 线程 + 约 64 GB 内存的成色不错的 R730/DL380 Gen9 价格大约在 **250–400 美元**。

---

### 2. 两张 Tesla P100（每张 12 GB）

截至 2026 年 9 月 14 日，Tesla P100 16 GB 版本在 eBay 上的二手价格约为 **99 美元** 起，Newegg 上的全新价格约为 94 美元起。12 GB SXM2 版本（常见于 DGX-1）较为稀有，但 PCIe 12 GB 版本价格与之相近或略低。预算大约为每张 **80–120 美元**，因此两张合计约 **160–240 美元**。

---

### 3. 总估价

| 组件 | 估价 |
|---|---|
| 双路 Broadwell 服务器（约 64 GB 内存） | 250–400 美元 |
| 2× Tesla P100（每张 12 GB） | 160–240 美元 |
| **总计** | **约 400–650 美元** |

---

### 值得注意

P100 适合运行 14B 参数模型；运行 30B 模型需要激进量化，且其较旧的 Pascal 架构可能与新的推理栈存在兼容性问题。若要搭建完整的 AI 工作站，你可能还需要为 NVMe 存储（32 GB 根磁盘空间紧张）以及兼容的 PCIe 转接卡/支架预留预算，前提是 P100 并未预装在服务器机箱内。

综上，使用二手零件组装的话，总花费大约在 **400–700 美元** 之间——这相当于一个拥有 24 GB 总显存的 GPU 计算节点，性价比极高。

---

**参考资料：**
- [Tesla P100 16GB 二手价格与历史（2026 年 9 月）— GPUDojo](https://gpudojo.com/tesla-p100)
- [Intel 服务器 64 GB 内存 双处理器 — eBay](https://www.ebay.com/b/Intel-Computer-Servers-64-GB-RAM-2-Processors/11211/bn_42004041)
- [用于本地 LLM 的二手服务器 GPU — CraftRigs](https://craftrigs.com/guides/used-server-gpus-tesla-p40-a100-ebay/)