---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: CNNs被高估且过时了
translated: true
type: note
---

问题：关于卷积神经网络（CNN）有哪些不受欢迎的观点？

回答：

以下是关于CNN的一些真正不受欢迎或与主流观点相悖的看法，你在深度学习社区中很少会看到它们被推崇：

- **对于当今大多数实际视觉任务来说，CNN被高估了**
  在给定相同计算资源和数据的情况下，Vision Transformers（ViT）和基于MLP的架构（例如，ConvNeXt，MLP-Mixer）在大型数据集上一直优于CNN。许多人仍然将“CNN=图像最佳选择”奉为圭臬，但自2021年左右以来，证据表明，当数据足够多时，像平移不变性和局部性这样的归纳偏置通常是不必要的，甚至可能有害。

- **卷积操作本身在很大程度上已经过时**
  现代高性能的“CNN”（ResNet-50→ConvNeXt，ResNeXt→Swin Transformer等）几乎都用深度可分离卷积、大核卷积或直接注意力机制取代了3x3卷积。经典的堆叠3x3卷积使AlexNet/VGG成名，但它们现在已很少是最佳的构建块了。

- **CNN的成功主要是由于历史偶然性，而不是因为卷积天生就适合图像**
  在2010年代初期，卷积在GPU上计算成本低廉（共享权重→更少的MACs），完美契合cuDNN内核，并且在小数据集+重度正则化（dropout，数据增强）下表现良好。如果Transformer早五年成熟，CNN可能仍是一个小众想法。

- **大多数对CNN的理论解释都是事后诸葛亮**
  “卷积强制平移不变性”或“分层感受野模仿视觉皮层”等说法听起来不错，但经不起推敲。在没有池化/数据增强的情况下，真实的CNN并非平移不变的，而视觉皮层类比也受到了神经科学家的严厉批评。

- **对于小/中型数据集，手工特征（SIFT，HOG）+线性SVM或随机森林在许多工业环境中仍然胜过轻量级CNN**
  人们常常忘记这一点，因为学术基准使用巨大的带标签数据集，但在医学图像、遥感或缺陷检测等图像数量少于10k的场景中，经典方法往往更robust且更具可解释性。

- **在过去十年中，CNN造成了大量的计算浪费**
  社区花费数年时间将ResNet扩展到1000多层，并集成巨大的CNN，然而，一个简单的ViT甚至一个精心调优的MLP，配合现代优化器，可能在样本效率和训练速度上都更优。

- **“CNN”这个词已经变得几乎毫无意义**
  今天它仅仅意味着“在Transformer出现之前我们拥有的任何ImageNet赢家”。将Swin Transformer或ConvNeXt称为“CNN”主要是出于市场营销/历史沿袭的考虑。

简而言之：CNN在2012-2018年间具有革命性意义，但在2025年仍然固守它们作为默认的视觉架构，在某些圈子中，这越来越被视为一种智力惯性。

参考文献：

- [Dosovitskiy et al., “An Image is Worth 16x16 Words” (ViT论文)](https://arxiv.org/abs/2010.11929)
- [Liu et al., “A ConvNet for the 2020s” (ConvNeXt)](https://arxiv.org/abs/2201.03545)
- [Tolias et al., “What Neural Network Architects Can Learn from Neuroscience (and vice versa)”](https://www.nature.com/articles/s42256-021-00354-y)
- [Touvron et al., “Training data-efficient image transformers” (DeiT)](https://arxiv.org/abs/2012.12877)
