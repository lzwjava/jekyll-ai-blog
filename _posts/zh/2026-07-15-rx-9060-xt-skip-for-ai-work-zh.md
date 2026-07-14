---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RX 9060 XT：跳过AI工作
translated: true
type: note
---

问题：什么是 Sapphire RX 9060 XT 16GB（METAL 合金设计）显卡？它对于 LLM/AI 工作好吗？

回答：

这是一款游戏级显卡，并非真正的 AI 计算卡——鉴于你的使用场景（在 MI300X 上训练 GPT-2、代理推理），这一点需要提前明确。

**硅片**
- GPU：Navi 44 XT，RDNA 4 架构，4nm，199mm²，29.7B 晶体管
- 2048 个流处理器，32 个光线追踪核心，64 个“Tensor Cores”（AMD 对 RDNA4 矩阵/WMMA 单元的营销术语——软件生态成熟度不及 Nvidia Tensor Cores）
- 完整 PCIe 5.0 x16 主机接口，相比上一代 RX 7600 的 PCIe Gen 4 x8 接口有所提升

**显存**
- 16GB GDDR6，128-bit 总线，320 GB/s 带宽

**频率/功耗（Pulse 版本，即此“METAL”散热器）**
- 游戏频率 2700 MHz，加速频率最高 3290 MHz，显存频率 2500 MHz（有效速率 20 Gbps）
- 典型板卡功耗 170W，单 8-pin 接口，长度 24cm，双槽厚度

**价格/定位**
- AMD 官方建议零售价：16GB 版本 $349（8GB 版本 $299）。Sapphire Pulse OC 型号定价约 $365。“METAL”（金属脉动）只是 Sapphire 在中国市场对 Pulse 散热器外壳/背板的营销名称——硅片与国际版 Pulse SKU 相同。

**对于你的实际工作负载——结论：跳过它。**
- 320 GB/s 带宽且没有 CUDA，意味着你只能走 ROCm/HIP 路线，而 RDNA4 消费级显卡的 ROCm 支持相比你的 MI300X（拥有完整的 CDNA3 + 全栈 ROCm/HIP + 高得多的 HBM3 带宽）显得参差不齐。
- 16GB 显存仅能支撑小规模本地推理（大约 7B Q4 量化级别），远不足以在真实批量大小下处理你的 GPT-2 760M 训练场景。
- 国内零售列表中的“DeepSeek AI”/“人工智能”标签只是借 DeepSeek 风潮的营销——该卡没有任何特殊的 DeepSeek 优化，硬件与全球 Pulse 16GB SKU 完全相同。

如果你想要一个廉价的本地推理盒子用于 llama.cpp/vLLM 实验，这款 $349 的游戏卡恰好有 16GB 显存，是不错的选择。如果你正在评估它作为训练节点，那就算了——坚持使用你的 MI300X 或租用云端算力。

参考资料：
- [SAPPHIRE PULSE Radeon RX 9060 XT 16G GDDR6](https://www.sapphiretech.com/en/consumer/pulse-radeon-rx-9060-xt-16g-gddr6)
- [SAPPHIRE RX 9060 XT 16GB PULSE spec database](https://videocardz.net/sapphire-radeon-rx-9060-xt-16gb-pulse)
- [TechPowerUp: Sapphire RX 9060 XT Pulse OC 16GB Review](https://www.techpowerup.com/review/sapphire-radeon-rx-9060-xt-pulse-oc/)
- [PC Perspective: RX 9060 XT 16GB Sapphire PULSE Review](https://pcper.com/2025/06/amd-radeon-rx-9060-xt-16-gb-review-sapphire-pulse-tested/)