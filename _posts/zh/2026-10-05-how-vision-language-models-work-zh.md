---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 视觉语言模型的工作原理
translated: true
type: note
---

问题：视觉语言模型（VLM）是如何工作的？

答案：视觉语言模型接收图像（有时包括视频）和文本，并生成文本，例如标题、关于图片的问题答案或图表描述。大多数现代VLM有三个主要部分。

**1. Vision encoder.** 图像被分割成小块（例如14×14或16×16像素）。Vision Transformer (ViT) 将每个小块转换为向量，并通过自注意力机制处理，生成一组视觉特征向量。编码器通常经过预训练，常用对比学习方法如CLIP，该方法学会将图像与其匹配的标题在同一个嵌入空间中靠近。

**2. Connector (projector).** 视觉特征存在于与语言模型词嵌入不同的"空间"中，因此需要一个桥梁。它可以是一个简单的线性层或小型MLP（如LLaVA中），或更复杂的模块，如交叉注意力或Q-Former（如Flamingo和BLIP-2中），将图像压缩成固定数量的"视觉token"。

**3. Large language model (LLM).** 视觉token与提示的文本token一起放入LLM的输入序列中。LLM逐token生成答案，同时关注图像token和文本。对LLM而言，图像实际上是一串额外的"单词"。

**训练**通常分为几个阶段：

- *Alignment pretraining:* 在大量图像-标题对上进行训练，使连接器学会将视觉特征转换为LLM能理解的内容。此时编码器和LLM通常冻结。
- *Instruction tuning:* 在基于图像的对话、问答、OCR、图表和推理任务上进行微调，使模型能够遵循关于图像的指令。
- *Optional preference tuning (RLHF or similar):* 减少幻觉，提高有用性。

**示例流程：** 你上传一张狗的照片并问"这是什么品种？" → 图像被编码为，比如，几百个视觉token → 它们被投影到LLM的嵌入空间 → LLM读取这些token加上你的问题 → 它生成"这看起来像一只金毛寻回犬。"

**常见局限性：** VLM可能会幻觉出图像中不存在的细节，在精细空间推理和计数方面表现不佳，并且当高分辨率图像被缩小时可能错过小文字（较新的模型通过平铺图像或使用动态分辨率来解决这个问题）。

参考文献：

- [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)
- [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)](https://arxiv.org/abs/2010.11929)
- [Flamingo: a Visual Language Model for Few-Shot Learning](https://arxiv.org/abs/2204.14198)
- [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and LLMs](https://arxiv.org/abs/2301.12597)
- [Visual Instruction Tuning (LLaVA)](https://arxiv.org/abs/2304.08485)
