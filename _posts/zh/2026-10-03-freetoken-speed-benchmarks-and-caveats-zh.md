---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeToken 速度基准与注意事项
translated: true
type: note
---

问题：FreeToken（FlashML-org/FreeToken）有多快？其服务速度是多少？

回答：

仓库的README中未提及具体速度数字，仅说明FreeToken能在游戏电脑上“以惊人的交互速度”运行290B+参数的MoE模型。这些数字来自该项目的论文（UC Berkeley / UT Austin作者）及第三方评测文章，均为作者自身结果，而非独立基准测试。

**解码速度（tokens/s）**

| 硬件 | 模型 | 速度 |
| --- | --- | --- |
| RTX 4060 笔记本电脑（8 GB VRAM，32 GiB RAM） | Qwen3.6-35B-A3B（NVFP4） | 39.3 tokens/秒 |
| RTX 5090（32 GB） | Qwen3.6-35B-A3B | 77–83 tok/s |
| RTX 5090（32 GB） | DeepSeek-V4-Flash（284B 总参数量） | 22–25 tok/s |
| RTX PRO 6000（96 GB） | GLM-5.2（753B 总参数量，40B 活跃参数） | 14.9 tokens/秒，而llama.cpp为7.3 tokens/秒 |

**与其他引擎的对比**

- 论文报告在所有工作负载下，解码吞吐量比最先进的边缘服务系统高出1.5–2.3倍。基准包括llama.cpp、Ollama、KTransformers和MoE-Infinity。
- Prefill速度在16000 tokens时达到6.7k tokens/秒。
- 首token延迟在最差情况下低于44秒（在评估的工作负载中）。相比之下，其他系统在处理最苛刻的工作负载时可能超时。
- 一项针对Ollama的第三方测试（使用超出VRAM大小的模型）显示，FreeToken的中位数速度为132.5 tokens/秒，而Ollama为58.8 tokens/秒，加速约2.25倍。
- 当模型完全适配VRAM时，无性能提升。同一测试中Ollama达到239.6 tokens/秒，FreeToken为225.3 tokens/秒。

**注意事项**

- 速度优势主要适用于模型大于VRAM容量的情况。
- 目前目标为NVIDIA RTX 30/40/50系列GPU。社区为AMD移植的版本在8 GB显卡上仅能达到约9 tok/s，但其作者认为差距源于硬件而非方法。
- 实际速度取决于你的RAM和PCIe带宽、量化格式以及工作负载。建议在自己的机器上运行`ft serve`以确认。

参考文献：

- [FreeToken GitHub仓库](https://github.com/FlashML-org/FreeToken)
- [FreeToken论文（HTML版本）](https://arxiv.org/html/2608.16157v1)
- [FreeToken AI评测：硬件、基准测试与设置（Wavect）](https://wavect.io/blog/freetoken-ai-inference-engine-review/)
- [FreeToken：在本地以2-4倍Ollama速度运行大规模MoE模型（Better Stack）](https://betterstack.com/community/guides/ai/freetoken-moe-inference/)
- [Emergent Mind论文摘要](https://www.emergentmind.com/papers/2608.16157)
- [FreeToken_AMD社区移植版](https://github.com/alpaslan-exe/FreeToken_AMD)
