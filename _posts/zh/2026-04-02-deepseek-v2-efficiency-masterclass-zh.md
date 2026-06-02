---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek-V2：效率大师课
translated: true
type: note
---

DeepSeek-V2 在 AI 世界中特别出名，因为它的成本远**低于**你提到的 5 亿美元数字。虽然像 OpenAI 和 Meta 这样的公司正在基础设施上花费数十亿美元，但 DeepSeek 的方法是效率的典范。

以下是 DeepSeek-V2 成本、GPU 小时和所用硬件的细分：

### **1. Training Cost**

DeepSeek-V2 与同行相比，训练成本惊人地低。

* **Estimated Cost:** 最终训练运行大约 **$2 million to $5 million USD**。
* **Context:** 相比之下，训练类似水平（像 Llama 3 70B 或 GPT-4）的模型通常成本数千万甚至数亿美元。DeepSeek 通过使用 **Mixture-of-Experts (MoE)** 架构实现了这一点，其中只有一小部分参数（236B 中的 21B）在任何给定任务中活跃，大幅减少了所需的计算量。

### **2. GPU Hours & Compute**

训练效率最好体现在总计算时间上：

* **Total GPU Hours:** DeepSeek 报告 V2/V3 训练周期使用了大约 **2.7 to 2.8 million GPU hours**。
* **Training Data:** 他们在此期间处理了海量的 **8.1 trillion tokens** 数据语料库。
* **Inference Efficiency:** 由于他们的 "Multi-head Latent Attention" (MLA) 技术，他们还将 KV cache（内存使用量）减少了 **93.3%**，使其成为训练完成后实际运行（推理）成本最低的模型之一。

### **3. Hardware (The "Cards")**

DeepSeek 的硬件选择具有战略性，部分原因是美国对中国高端芯片的出口限制。

* **GPU Model:** 他们主要使用了 **NVIDIA H800** GPUs。
  * H800 是旗舰 H100 的“中国专用”版本。它具有相同的原始计算能力，但互连速度（NVLink）受限以符合贸易法规。
* **Cluster Size:** 虽然他们拥有大约 **50,000 GPUs** 的庞大集群用于各种任务，但这些模型的具体训练运行通常一次使用大约 **2,000 to 10,000 GPUs** 的子集。
* **Alternative Hardware:** 他们历史上还使用过 **NVIDIA A100** 集群（特别是他们的 "Fire-Flyer 2" 集群，约有 5,000 个 A100）。

### **Summary Table**

| 特性 | DeepSeek-V2 详情 |
| :--- | :--- |
| **Total Parameters** | 236 Billion |
| **Active Parameters** | 21 Billion (per token) |
| **Training Cost** | ~$5 Million (Final Run) |
| **Hardware** | NVIDIA H800 / A100 |
| **GPU Hours** | ~2.8 Million |
| **Main Innovation** | Multi-head Latent Attention (MLA) & MoE |

---
**参考文献：**

* [DeepSeek-V2 Technical Report (arXiv)](https://arxiv.org/html/2405.04434v5)
* [Stratechery: DeepSeek FAQ](https://stratechery.com/2025/deepseek-faq/)
* [DeepSeek-V3 Training Cost Analysis](https://spreadsheets-are-all-you-need.ai/flops-demystified-ai-and-the-math-behind-deepseek-training-costs/)
