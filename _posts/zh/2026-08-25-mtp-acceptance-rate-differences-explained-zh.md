---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MTP接受率差异解析
translated: true
type: note
---

**问题：** 在技术讨论组中，“MTP”是什么意思？DSv4 + mtp_1 在随机输入下能达到约90%的接受率，而GLM 5.2 + mtp_1 只有约60%，这正常吗？

---

**回答：**

**MTP = 多令牌预测 (Multi-Token Prediction)** —— 一种推测解码技术，模型利用其架构中内置的额外轻量级“草稿头”，在每次前向传播中预测多个未来令牌。MTP 并非一次生成一个令牌，而是以较低成本提议接下来的 1–N 个令牌，然后由主模型并行验证。消息中的“mtp_1”指的是使用 1 个推测步骤（提前草拟 1 个额外令牌）。

---

**接受率差异是否正常？正常，原因如下：**

**1. DSv4 的 MTP 在架构上针对高接受率进行了优化。**  
DeepSeek-V3 的实际应用数据显示，其 MTP 模块在预测下一个令牌时达到 80%–90% 的接受率，使生成 TPS 提升 1.8 倍。DSv4 基于同一技术路线，并持续改进 MTP。

**2. GLM 5.2 采用不同的 MTP 设计，权衡方式不同。**  
GLM-5.2 使用带有 KVShare 推测解码的 MTP 层，据 Z.ai 报道，这可将草稿令牌接受长度提升最多 20%——但其基线接受率低于 DSv4，尤其是在随机或分布外输入上。

**3. 随机输入是最坏情况，暴露了架构差异。**  
接受率关键取决于草稿模型的令牌分布与目标模型分布的接近程度。随机输入没有连贯的分布，因此 MTP 头与主干耦合更紧密的模型自然具有优势。

**4. 底层训练策略至关重要。**  
DeepSeek-V3 使用单个 MTP 层进行训练，但在推理时预测 2 个令牌——这种训练与推理的不一致降低了第二个令牌的接受率。GLM-5 通过在训练时共享 3 个 MTP 层的参数来解决此问题，在保持与 DeepSeek-V3 相同内存成本的同时提高接受率。GLM 5.2 继承了这一技术路线，但在*随机*输入（非真实提示）上，DSv4 在 mtp_1 上的原始接受率仍然占优，因为其头部经过了更激进的优化。

**5. mtp_1 达到 60% 仍在正常/健康范围内。**  
接受率低于 0.55 表明分布不匹配；此时建议减少 num_speculative_tokens。GLM 5.2 的 60% 高于此阈值，运行正常——你仍然能获得加速效果。

---

**总结表格：**

| 模型 | MTP_1 接受率（随机输入） | 备注 |
|---|---|---|
| DSv4 | ~90% | 高度优化的单个 MTP 头 |
| GLM 5.2 | ~60% | 不同架构；随机输入下较低，真实提示下更优 |

在真实提示（代码、聊天、文档）上，差距通常会缩小，因为 GLM 5.2 的共享参数 MTP 设计在更长的推测链上更稳定。

---

**参考资料：**
- [DeepSeek-V3 MTP 架构深度解析](https://arxiv.org/pdf/2505.09343)
- [GLM-5 MTP 参数共享设计](https://arxiv.org/html/2602.15763v1)
- [MTP 部署指南（vLLM/SGLang）](https://www.spheron.network/blog/multi-token-prediction-mtp-gpu-cloud-deployment-guide/)
- [Nebius 为 DeepSeek-V3 微调的 MTP](https://huggingface.co/nebius/MTP-DeepSeek-V3-0324)