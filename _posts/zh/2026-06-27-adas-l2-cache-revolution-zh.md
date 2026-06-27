---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 艾达的二级缓存革命
translated: true
type: note
---

问题：关于NVIDIA的Ada Lovelace GPU架构，有哪些鲜为人知或不为人知的事实？

答案：

最被低估的事实：**Ada Lovelace（AD10x）的L2缓存相比Ampere大幅增加，这才是真正的架构故事，而非原始计算能力。**

AD102芯片的L2缓存从GA102的6 MB跃升至**98 MB**——提升了约16倍。这直接复制了AMD的“Infinity Cache”策略，也默默承认了GDDR6X带宽的增长速度不够快。4090的内存总线（384-bit）实际上比其定位预期的更窄，而巨大的缓存掩盖了这一点。对于你的推理工作来说，这一点很重要：当工作集在缓存内时，Ada的有效带宽远优于规格表上1 TB/s的表现，但一旦你的KV缓存加权重超过L2，性能就会断崖式下跌。

其他真正冷门的事实：

1. **Ada上存在FP8（E4M3/E5M2）张量核心，但软件层面相比Hopper被限制了。** Ada的第四代张量核心支持FP8，但NVIDIA将全速率的FP8带FP32累加以及Transformer Engine的完整功能集留给了Hopper。在消费级Ada上，你能得到FP8矩阵乘法，但Transformer Engine的路径被削弱了——如果你在用4090和H100对比训练性能，这点很相关。

2. **Ada没有NVLink。** 就连4090也去掉了3090上配备的NVLink接口。这是故意的市场细分，旨在将多GPU训练用户推向H100/数据中心SKU。对于你的双GPU实验，4090只能通过PCIe对等通信。

3. **“AD102几乎未被充分使用”这一事实。** 4090搭载的AD102被大幅削减——144个SM中仅启用了128个。完整芯片从未出现在消费级显卡中；它被留给了RTX 6000 Ada / L40。因此，这一代最强大的游戏GPU实际上是一个次品芯片。

4. **SER（着色器执行重排序）** 被宣传用于光线追踪，但它其实是一种用于发散工作负载的通用延迟隐藏机制——在图形领域之外几乎无人讨论。

5. **Ada的张量核心新增了FP8但*未移除*任何东西——然而稀疏性（2:4结构化）仍然几乎未被使用**，因为主流训练框架无法可靠地利用它，这使得一半的“稀疏TFLOPS”营销数字在实践中毫无意义。

对于你的4070（AD104，36 MB L2，12 GB）：缓存的故事解释了为什么它在小模型上能超越其带宽等级的表现，但一旦模型超出约10 GB就会卡住。

参考文献：

- [NVIDIA Ada GPU架构白皮书](https://images.nvidia.com/aem-dam/Solutions/Data-Center/l4/nvidia-ada-gpu-architecture-whitepaper-v2.1.pdf)
- [Chips and Cheese — Ada的L2缓存分析](https://chipsandcheese.com/)

（注意：我没有进行实时搜索——这些内容来自已发布的白皮书和架构报道。如果你希望我根据来源验证每个芯片的具体SM/缓存数量，我可以进行搜索。）