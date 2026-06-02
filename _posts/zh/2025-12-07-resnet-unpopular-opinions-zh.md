---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 关于ResNet的冷门观点
translated: true
type: note
---

问题：关于 ResNet 有哪些非主流观点？

回答：

ResNet（残差网络）于 2015 年推出，通过跳跃连接实现了非常深的神经网络的训练，从而彻底改变了深度学习。然而，尽管它作为计算机视觉任务的骨干网络被广泛采用，但它在机器学习社区中引发了一些不同的观点。这些“非主流观点”通常挑战了围绕 ResNet 普遍性、深度痴迷和感知到的简单性的炒作。下面，我整理了从 Reddit 的 r/MachineLearning 等论坛、学术论文以及 X（前身为 Twitter）等平台上的专家评论中得出的关键观点。这些观点突出了对其局限性、过度依赖和不断演变的相关性的争论。

### 1. **ResNet 的成功并非主要归因于更好的梯度流——这是一个误解**
   - 许多人引用跳跃连接来“改善梯度流”以解决梯度消失问题，但这与最初的 ResNet 假设相矛盾。核心问题是深度普通网络中的优化退化（尽管容量更大，但训练误差更高），而不仅仅是信号消失。批标准化已经处理了范数，但噪声积累淹没了信号。跳跃连接使学习恒等映射变得微不足道（F(x) ≈ 0），从而简化了优化，而无需“完美地”流动梯度。教程和论文经常对此进行过分简化，导致了盲目模仿式的实现。

### 2. **你实际上不需要跳跃连接——不带跳跃连接的 ResNets 只要经过仔细初始化也能很好地工作**
   - “ResNet 假设”（残差对于深度至关重要）受到了质疑。像“Fixup Initializaion: Residual Learning Without Normalization”（ICLR 2019）这样的论文表明，如果初始化得当，普通网络（没有跳跃连接）可以有效地训练并取得良好结果。跳跃连接有帮助，但它们并非魔法；它们是懒惰优化的拐杖。这意味着 ResNet 的炒作忽略了更简单的修复方法，使其对于许多用例来说过度设计。

### 3. **对于大多数实际任务来说，ResNets 被高估了——Vision Transformers (ViTs) 或更简单的模型通常更好**
   - 从头开始在适度计算资源上训练时，ResNets 已经是“最好的了”，但并非革命性的——Vision Transformers（例如，通过 DINO 自监督）在类似资源下可以匹配或超越它们，尤其是在多样化数据集上。ViTs 随数据扩展性更好，并避免了 ResNet 的归纳偏置（如局部性），这可能在非自然图像上造成损害。当 RegNets 等替代方案提供类似性能且更简单时，ResNets 感觉“停留在 2015 年”。热门观点：99% 的 CV 应用程序可以使用基本的 ResNet，但这一个缺点而非优点——这是偷懒的工程。

### 4. **更深并非总是更好——更宽的 ResNets 优于更深的 ResNets，挑战了对深度的痴迷**
   - 对超深 ResNets（例如 ResNet-152）的追求忽略了证据表明宽度（更多通道）通常能以更少的参数和更快的训练获得更好的准确性。一篇 2016 年的 arXiv 论文（“Wider or Deeper”）表明，更浅、更宽的变体在 ImageNet 和语义分割上胜过深度 ResNets，同时使用更少的内存。深度增加了复杂性而没有成比例的收益，尤其是在 50 层之后——这是基准测试驱动的边际收益递减。

### 5. **ResNets 不适合 GAN 或非分类任务——定制架构胜出**
   - 在 GAN 判别器中，标准 ResNets（例如 ResNet-50）会破坏数据分布，创建阶梯函数决策边界，为生成器提供无用的梯度。SOTA GANs（StyleGAN、BigGAN）采用定制设计。这延伸到其他领域：ResNets 在 ImageNet 风格的分类中表现出色，但在生成任务或低数据场景中，如果不进行大量调整，会表现不佳，因此它们不是一个好的默认选择。

### 6. **ResNets 过于简单和可靠——它们扼杀了创新**
   - 它们的简单性（几分钟内预训练、快速训练）使其成为拐杖：从 ResNet-50 开始，微调，完成。但这种可靠性隐藏了更深层次的问题——当“足够好”有效时，为什么要创新？批评者认为它支撑了平庸的研究；你用 LSTMs 处理 NLP 或更浅的 CNNs 也能获得类似的结果。即使是粉丝也承认：“ResNet 仍然让我费解——其用于稳定训练的输入加法令人困惑地特别。”

这些观点反映了一个日渐成熟的领域，ResNet 受到尊重但不再是不可触及的。对于实践者而言，它仍然是一个坚实的起点，但尝试混合模型（例如，用于多路径的 ResNeXt）或替代方案对于边缘情况会带来回报。

参考文献：
- [Has the ResNet Hypothesis been debunked? (Reddit r/MachineLearning)](https://www.reddit.com/r/MachineLearning/comments/px3hzd/d_has_the_resnet_hypothesis_been_debunked/)
- [Are ResNets as good as it gets? (Reddit r/MachineLearning)](https://www.reddit.com/r/MachineLearning/comments/nbgb6a/d_are_resnets_as_good_as_it_gets/)
- [Why don't people use ResNet as GAN discriminator? (Reddit r/MachineLearning)](https://www.reddit.com/r/MachineLearning/comments/esj4m7/d_why_dont_people_use_typical_classification/)
- [Why do residual networks work? (Cross Validated)](https://stats.stackexchange.com/questions/237152/why-do-residual-networks-work)
- [Wider or Deeper: Revisiting the ResNet Model (arXiv)](https://arxiv.org/abs/1611.10080)
- [ResNets still don't make sense to me (X post)](https://x.com/_notapenguin/status/1995480100322586677)
- [99% of CV apps can be handled with simple ResNet (X post)](https://x.com/tunguz/status/1580594479211216900)
- [ViTs over classic ConvNets like ResNet (X post)](https://x.com/ZRozsypalek/status/1996217103246885243)
