---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达 H200 涨价传闻被辟谣
translated: true
type: note
---

Question:
NVIDIA H200 的价格在去年缺货后，今年真的涨了 80 万吗？

Answer:
简短回答：**不是 —— NVIDIA H200 单卡本身并没有跳涨 80 万人民币。**
你可能混淆了**单颗 GPU 价格**与**整机服务器 / 8-GPU 节点价格**。

### 1. 单颗 H200 GPU 价格（实际市场情况）

* 典型的 **NVIDIA H200 单卡** 价格：约 **$30,000–$40,000**
* 折合人民币约为 **¥22万–¥30万**（估算）
* 这个价格区间一直相对**稳定**，并没有出现 +80 万的涨幅。([NVIDIA H200][1])

### 2. 8 显卡 H200 服务器价格（这是“80万”出现的地方）

* 4-GPU 模块 ≈ **$175,000**
* 8-GPU 系统 ≈ **$300,000+**
* 整机服务器（包含 CPU、内存、网络设备）通常在 **$300k–$320k**
  → 总额约为 **¥210万–¥230万人民币**。([ThePricer][2])

所以如果有人说：

* 去年约 140 万
* 今年约 220 万

这个 **差价 ≈ 80 万人民币** 是合理的 —— **但这指的是一台完整的 HGX H200 服务器**，而不是单颗 GPU。

### 3. 为什么价格“感觉上”暴涨了

原因有以下几点：

* H200 取代了 H100（拥有更大的显存：141GB HBM3e）
* AI 需求激增（LLM 训练）
* 中国出口限制 / 许可证变更
* 供应商将 NVLink + 网络设备 + CPU 进行捆绑销售
  这些因素推高了**系统价格**，而非单颗芯片的价格。

### 4. 市场现状速览

* 单颗 H200：约 25 万人民币
* 8× H200 服务器：约 200 万人民币
* 机柜级集群：轻松达到 **1000 万人民币以上**

因此，听到 **“涨了 80 万”** 只有在针对**整机服务器**时才是可信的，而非单颗 GPU。

### 结论

* ❌ H200 GPU 单卡价格上涨 80 万 → **不属实**
* ✅ H200 整机 AI 服务器上涨 80 万 → **有可能 / 很常见**
* 这种误解通常源于 **GPU 与 HGX 服务器** 概念的混淆。

如果你能提供更多背景信息，例如：

* 是云端租赁价格？
* 是购买服务器的价格？
* 是来自中文论坛的传闻？
* 还是在对比 H100 和 H200 的价格？

我可以为你准确分析你看到的是哪种情况。

References:

* [https://www.h200.info/faq](https://www.h200.info/faq)
* [https://cyfuture.cloud/kb/gpu/nvidia-h200-price-guide-costs-specs-and-2025-updates](https://cyfuture.cloud/kb/gpu/nvidia-h200-price-guide-costs-specs-and-2025-updates)
* [https://www.thepricer.org/how-much-does-nvidia-h200-cost/](https://www.thepricer.org/how-much-does-nvidia-h200-cost/)
* [https://veixus.com/2025/09/29/nvidia-h200-gpu-explained-the-complete-guide-to-ais-most-powerful-datacenter-accelerator/](https://veixus.com/2025/09/29/nvidia-h200-gpu-explained-the-complete-guide-to-ais-most-powerful-datacenter-accelerator/)

[1]: https://www.h200.info/faq?utm_source=chatgpt.com "H200 FAQ - Frequently Asked Questions About NVIDIA H200 GPU"
[2]: https://www.thepricer.org/how-much-does-nvidia-h200-cost/?utm_source=chatgpt.com "How Much Does Nvidia H200 Cost?"