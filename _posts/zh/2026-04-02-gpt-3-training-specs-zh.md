---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-3 训练成本与硬件规格
translated: true
type: note
---

## GPT-3 的训练细节

要训练 GPT-3（特别是 175B 参数版本），OpenAI 使用了 Microsoft 提供的海量超级计算机基础设施。下面是其开发中使用的估计成本、时间和硬件。

---

### **1. 训练成本**

GPT-3 单次训练运行的成本估计在 **460 万美元至 500 万美元** 之间。

* **计算费用：** 这个数字主要涵盖了云端（Microsoft Azure）高端 GPU 实例的租赁或运营成本。
* **总预算：** 虽然原始计算成本约为 500 万美元，但 OpenAI 的总成本——包括研究、人员以及多次失败或实验运行——很可能要高得多。

### **2. 训练时间**

最终模型的实际训练时间估计使用了高度并行化的集群，耗时 **34 天**。

* **并行性：** 为实现这一点，OpenAI 使用了 **1,024 个 NVIDIA A100 GPU** 同步工作。
* **假设比较：** 如果你尝试在单个 NVIDIA Tesla V100 GPU 上训练 GPT-3，将大约需要 **355 年** 才能完成。

### **3. 硬件（“卡片”）**

OpenAI 使用了数据中心级 GPU，而不是消费级显卡。

* **主要卡片：** 该模型最初在自定义 Microsoft 超级计算机的 **NVIDIA Tesla V100** GPU 上开发和训练。
* **集群规模：** 该超级计算机配备了超过 **10,000 个 GPU** 和 285,000 个 CPU 核心，以处理海量工作负载。
* **当前标准：** 后来的优化和再现（例如 2021 年的估计）通常将 **NVIDIA A100** 或 **H100** 视为此类规模模型的标准硬件。

---

### **总结表格**

| 类别 | 详情 |
| :--- | :--- |
| **计算成本** | 每次运行 ~460 万美元 – 500 万美元 |
| **持续时间** | ~34 天（在 1,024 个 GPU 集群上） |
| **主要硬件** | NVIDIA Tesla V100（后为 A100/H100） |
| **总参数** | 1750 亿 |

**参考文献：**

* [OpenAI Presents GPT-3 Technical Overview](https://developer.nvidia.com/blog/openai-presents-gpt-3-a-175-billion-parameters-language-model/)
* [Demystifying GPT-3 Training Costs](https://lambda.ai/blog/demystifying-gpt-3)
* [GPT-3 Wikipedia Technical Summary](https://en.wikipedia.org/wiki/GPT-3)
