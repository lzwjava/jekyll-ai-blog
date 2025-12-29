---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GLOM：部分与整体层级结构
translated: true
type: note
---

**Question**: Geoffrey Hinton 在他的 Stanford CS25 讲座中说了什么？

**Answer**:

Geoffrey Hinton 在 Stanford 的 CS25: Transformers United 课程中发表了一次客座讲座（具体是在该系列研讨会的早期版本中）。演讲的主题是 "Representing Part-Whole Hierarchies in a Neural Network"，重点探讨了他提出的名为 **GLOM** 的架构。

### Hinton 讲座的关键点：

- Hinton 介绍了 **GLOM**，这是一个构想中的 Neural Network 系统，旨在更好地表示视觉感知中的 **part-whole hierarchies**（部分与整体的层级结构，例如物体的各个部分如何构成整体，就像面部特征如何构成面部本身）。
- 他认为，目前的 Transformer-based 系统虽然强大，但在将场景解析为连贯的“部分-整体”结构以及直观地解释表示（representations）方面仍面临困难。
- GLOM 结合了多项研究进展的想法：
  - Transformers（用于 attention 机制）
  - Capsules（他早期关于 dynamic routing 的研究）
  - Neural fields
  - Contrastive representation learning
  - Distillation 技术
- 其核心思想是使用 **island-like distributed representations**，通过相似的向量随着时间的推移聚集形成“岛屿（islands）”，来表示不同层级结构中的实体，从而提高可解释性，尤其是在 Vision 任务中。
- 如果取得成功，GLOM 可以让 Transformer-like models（应用于 Vision 或 Language）中的表示对人类来说更具可解释性。
- Hinton 强调，这可以解决现代 Deep Learning 模型在处理组合结构（compositional structures）时与人类感知相比存在的局限性。

这次演讲是一场特别/客座讲座，不属于常规讲师系列，于 2022 年 8 月在 YouTube 上发布（录制时间更早）。它反映了 Hinton 对在标准 Transformers 基础上改进 Neural Networks 的持续思考，并与其关于 AI 表示和理解的更广泛观点相联系。

References:  

- [Stanford CS25: Represent part-whole hierarchies in a neural network, Geoff Hinton (YouTube Video)](https://www.youtube.com/watch?v=CYaju6aCMoQ)  
- [CS25 Course Website (mentions Hinton as a past speaker)](https://web.stanford.edu/class/cs25/)  
- [Speaker Deck Summary of CS25 Lectures (includes Hinton's GLOM talk)](https://speakerdeck.com/sadahry/cs25-transformers-united-2785d644-be02-4be6-8812-e8d9c93790ae)