---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MoET在FP4 MoE推理中的应用
translated: true
type: note
---

问题：在运行具有FP4级吞吐量的v4 flash时，“MoET”是什么意思？

回答：我没有在量化文献中找到“MoET”作为标准、可引用的术语——它不像GPTQ/AWQ那样是论文名称。根据你的上下文（运行flash MoE模型，使用“moet”来“补精度”以避免FP4吞吐量影响质量），这几乎可以确定是社区中**混合精度MoE补偿**的简写——即涵盖MoEQuant、AlphaQ和LREC等方法的通用技术类别：

这些方法的核心思路如下：
1. 将大部分权重（通常是FFN/专家矩阵）量化为FP4/INT4以提升吞吐量。
2. 保留少量“敏感”组件使用更高精度——如路由/门控权重、首层/末层或特定异常通道，因为这些对输出质量损失影响最大。
3. 添加一个轻量级的误差补偿项（低秩适配器、逐通道缩放或逐专家校准），该步骤计算成本低，但能修正步骤1中引入的大部分量化误差。

这就是为什么你能在保持接近bf16精度的同时，获得FP4级别的吞吐量和显存占用——你不是均匀量化所有内容，而是进行选择性/混合精度量化加上修正步骤。

你提到的数据（4并发→300 tok/s，8并发→400 tok/s）看起来像是解码受限的MoE服务概况——从4到8并发的次线性扩展表明你遇到了专家权重的内存带宽瓶颈，而非计算瓶颈。这与仅权重量化为FP4一致：权重移动成本低，但随着批次增大，KV缓存和激活反量化成为瓶颈。

如果你能告知实际在日志或文档中打印“MoET”的仓库/工具（vLLM分支、SGLang或自定义量化脚本），我可以提供确切定义而非上述通用模式——鉴于这些中文社区部署工具经常临时命名，值得进一步确认。

参考文献：
- [MoEQuant: 专家平衡采样与亲和力引导](https://arxiv.org/abs/2505.03804)
- [AlphaQ: MoE量化的免校准比特分配](https://arxiv.org/html/2606.04980)
- [基于低秩误差校正的FP4量化](https://ieeexplore.ieee.org/document/10685437/)
- [NVIDIA NVFP4实现高效低精度推理](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)