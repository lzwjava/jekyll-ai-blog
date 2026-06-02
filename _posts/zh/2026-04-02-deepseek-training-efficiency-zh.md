---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek 模型训练时间与效率
translated: true
type: note
---

直接回答您的问题：训练像 DeepSeek-V2（及其后续版本 V3）这样的模型需要大约 **两个月** 的连续计算时间。

因为 DeepSeek 使用了一个相对较小但高度优化的 GPU 集群，他们不需要一整年的训练周期。以下是该时间具体的使用分解：

### **训练时间线分解**

对于 **DeepSeek-V3**（最新且更大的版本），训练分为几个阶段完成：

* **Pre-training:** 不到 **2 个月**（具体约为 55–60 天）。
* **Rate of Progress:** 在他们的 **2,048 H800 GPUs** 集群上，他们能够每 3.7 天处理 **1 万亿 tokens**。
* **Context Extension:** 额外几天时间教模型处理长文档（最多 128k tokens）。
* **Post-training (SFT/RL):** 与主要预训练相比，非常短的时期（几天）。

### **为什么不会花费更长时间**

您可能想知道，为什么 2,048 个 GPU 的“较小”集群能在其他公司使用 20,000+ GPU 时这么快完成。

1. **Mixture-of-Experts (MoE):** 由于模型针对每个词只“激活”大约 $10\% - 15\%$ 的“脑力”，计算速度快得多。
2. **FP8 Training:** 他们使用了称为 **FP8**（8 位浮点数）的数据格式，与旧模型使用的传统 16 位格式相比，本质上将硬件速度加倍。
3. **High Stability:** DeepSeek 报告称他们的训练过程“异常稳定”，具有 **零不可恢复的损失峰值**。在 AI 训练中，“崩溃”或“故障”常常迫使工程师从一周前的备份重新开始；DeepSeek 完全避免了这些延迟。

### **“500 Million USD” 比较**

为了将您的 $500M 估计放在更清晰的视角中：

* **DeepSeek's Run:** 2,048 GPUs 上约 2 个月 $\approx$ **$5.6$ million**。
* **Meta's Llama 3 (405B):** 16,000 GPUs 上约 1 个月 $\approx$ **数亿美元**。

DeepSeek 花费较少不是因为训练时间较短；他们花费较少是因为他们的“汽车”（模型架构）的燃油效率比竞争对手高 10 倍。

---
**参考文献：**

* [DeepSeek-V3 Technical Report (arXiv)](https://arxiv.org/abs/2412.19437)
* [DeepSeek FAQ – Stratechery](https://stratechery.com/2025/deepseek-faq/)
