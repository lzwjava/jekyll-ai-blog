---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 斯坦福 CS231n 核心主题概览
translated: true
type: note
---

Question: What is the course syllabus for Stanford CS231n by Andrej Karpathy?

Answer:

Stanford CS231n，标题为 "Convolutional Neural Networks for Visual Recognition"（现在通常称为 "Deep Learning for Computer Vision"），最初是由 **Andrej Karpathy** 在其早期开课期间（2015年冬季和2016年冬季学期）设计并担任主讲的。他创作了基础的 lecture notes、assignments 以及大部分沿用至今的课程结构。

来自 Andrej Karpathy 时期（2016年冬季）的经典教学大纲涵盖了大约 20 讲中的以下主要主题：

- **Introduction to Computer Vision** 与课程概览
- **Image Classification**（数据驱动方法，k-Nearest Neighbor）
- **Linear Classification**（score functions，损失函数如 SVM 和 Softmax）
- **Optimization**（gradient descent，stochastic gradient descent，backpropagation）
- **Neural Networks**（fully connected networks，activation functions，architectures）
- **Training Neural Networks**（initialization，regularization，dropout，batch normalization，data augmentation）
- **Convolutional Neural Networks (ConvNets)**（convolution，pooling，architectures 如 AlexNet，VGG，GoogLeNet，ResNet）
- **Understanding and Visualizing ConvNets**（saliency maps，gradients，deconvolutions）
- **Object Detection**（sliding window，region proposals，R-CNN 家族）
- **Localization and Segmentation**（semantic segmentation，instance segmentation）
- **Recurrent Neural Networks (RNNs)** 及其应用，如 image captioning
- **Advanced topics**（transfer learning，efficient convolutions，modern practices）

该课程包括实现这些概念的动手作业（例如：kNN、fully-connected nets、使用 PyTorch/TensorFlow 等框架实现 ConvNets、network visualization）以及一个期末项目。

请注意，当前版本的 CS231n（例如 2025年春季）在 Fei-Fei Li 等讲师的指导下已经有所演进，加入了诸如 generative models、Transformers in vision (ViTs) 和 human-centered AI 等较新的主题，同时保留了 Karpathy 原始设计的核心结构。

Karpathy 时代的原始 lecture notes 仍然公开可用，且仍是该课程资料中被引用最多的版本。

References:

- [Original CS231n Course Website (current, with links to past offerings)](https://cs231n.stanford.edu/)
- [CS231n Lecture Notes (classic version by Andrej Karpathy)](https://cs231n.github.io/)
- [Winter 2016 Syllabus and Slides](https://cs231n.stanford.edu/2016/)
- [Andrej Karpathy's Academic Page mentioning CS231n](https://cs.stanford.edu/people/karpathy/)
