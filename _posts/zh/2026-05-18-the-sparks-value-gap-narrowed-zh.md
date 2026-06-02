---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 火花的价值差距缩小
translated: true
type: note
---

**问题：** 我两个月前研究过 DGX Spark 和 AMD Ryzen AI Max+ 395 迷你电脑，当时两者差价约 1 万元人民币。现在 AMD 395 机型涨到了 2.5 万元——这是否意味着 DGX Spark 现在更划算？

**回答：**

你的判断基本正确——两者之间的价值差距已经显著缩小，原因如下：

## 价格变化

**NVIDIA DGX Spark** 也涨价了。NVIDIA 将 DGX Spark 的建议零售价从 3,999 美元上调至 4,699 美元，涨幅 18%，原因是全球内存供应紧张。所以并非只有 AMD 机型涨价，Spark 同样受到 LPDDR5X 短缺的影响。

**配备 128GB 内存的 AMD Ryzen AI Max+ 395 迷你电脑** 受到重创。截至 2026 年 3 月 24 日，128GB AMD 395 机型价格从 2,399 美元（Bosgame M5）到 3,810 美元（MINIX ER939-AI）不等，热门选项包括 Framework Desktop（2,851 美元）、Corsair AI Workstation 300（2,499 美元）和 GMKtec EVO-X2（3,000 美元）。内存价格是主要原因——近几个月来内存和存储价格飙升，让这些原本就昂贵的电脑更加遥不可及。

## DGX Spark 现在更划算吗？

**不一定——这取决于你的使用场景。** 具体分析如下：

**DGX Spark 优势：**

- GB10 Grace Blackwell 超级芯片提供高达 1 petaFLOP 的 AI 推理性能（FP4），配备 128GB LPDDR5X 一致统一内存，以及速率高达 200 Gbps 的 ConnectX 7 NIC。
- 预装 NVIDIA AI 软件栈（CUDA、TensorRT-LLM），开箱即用体验完善，文档丰富且附带预配置的 playbook。
- CES 2026 的软件更新通过 TensorRT-LLM 优化和 NVFP4 量化，在特定工作负载上实现了最高 2.5 倍的性能提升。

**AMD 395 迷你电脑优势：**

- 即便在涨价后，最便宜的 128GB AMD 395 机型（Corsair 约 2,499 美元，Bosgame 约 2,399 美元）仍明显低于 DGX Spark 的 4,699 美元。
- AMD Strix Halo 平台每美元带来的 token 生成吞吐量更高——Framework Desktop（2025 年 12 月定价 2,566 美元）每美元每秒产生的 token 数高于定价 4,000 美元的 DGX Spark。
- AMD 395 机型运行标准 Windows 或 Linux，在 AI 之外的一般工作负载上具有更高灵活性。

**性能细节：**
在 GPT-OSS 120B 等大型模型上，DGX Spark 在 prompt 处理（计算密集型）方面表现出色，但在 token 生成（内存密集型）方面则显得吃力，此时 273 GB/s 的 LPDDR5X 带宽成为瓶颈。

## 总结

如果最便宜的 AMD 395 选项（Corsair、Bosgame）在您所在市场已无货，且价格确实涨到与 DGX Spark 相近的水平（AMD 2.5 万对 DGX Spark 相近价格），那么 Spark 确实显得更合理——因为您获得了 CUDA 生态系统、更好的 AI 软件支持以及更开箱即用的体验。但如果您仍能以 1.8–2 万元人民币找到 AMD 395 选项，那么 AMD 的价值优势依然存在，尤其是在灵活通用 AI 工作方面。

**参考资料：**

- [NVIDIA DGX Spark 涨价——Tom's Hardware](https://www.tomshardware.com/desktops/mini-pcs/nvidia-dgx-spark-gets-18-percent-price-increase-as-memory-shortages-bite-founders-edition-now-usd-usd4-699-up-from-usd3-999)
- [AMD 395 迷你电脑价格汇总——Liliputing（2026 年 3 月 24 日）](https://liliputing.com/more-ryzen-ai-max-395-mini-pcs-with-128gb-are-now-available-if-you-can-afford-one/)
- [DGX Spark vs AMD Strix Halo 基准测试与价值分析——AIMultiple](https://aimultiple.com/dgx-spark-alternatives)
- [NVIDIA DGX Spark 规格与价格历史](https://www.aitooldiscovery.com/ai-infra/nvidia-dgx-spark-explained)
