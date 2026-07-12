---
audio: false
generated: false
image: false
lang: zh
layout: post
title: AI课程：从神经网络到智能体
translated: true
---

我提供AI辅导。每节课50元人民币（每节30分钟）。订阅1到100+节课——定制你自己的学习路径。我很乐意分享我所学到的。

## 我的背景

- 男，1995年出生，中国公民，现居广州。2011年广东NOIP排名前300，在线解决约1000道算法题。
- 此前经历包括LeanCloud、北京平方根、博彦科技（外派至新加坡某银行）、法本信息（外派至英国某国际银行）以及TEKsystems（外派至英国某国际银行）。
- 累计11年专业经验。专注于移动端（Android、iOS）和全栈工程，有1年机器学习/大数据经验。
- 熟练掌握HTML、CSS、JavaScript、Vue、React、Angular、iOS/Android、Java、Spring、MySQL、Redis、分布式系统以及云平台（阿里云、AWS、Azure）。
- 趣直播 — [GitHub](https://github.com/lzwjava/live-mobile-web)，一个基于微信的面向iOS、Android、后端和AI内容的技术直播平台。2016年至2017年运营，约有3万用户。
- 个人博客 — [lzwjava.github.io](https://lzwjava.github.io)，一个AI驱动的一站式博客系统，具备AI翻译等功能。2021年至今运营，月浏览量约6万（Cloudflare）。
- 母语为中文，英语熟练（雅思6.5分）。阅读超过320本书。
- AI爱好者——在H200、AMD MI300X和RTX 4070 GPU上训练过小型LLM（nanoGPT），并使用OpenRouter和Claude Code构建过项目（约使用30亿tokens）。
- 更多详情：[简历](https://lzwjava.github.io/resume-en) · [软件作品集](https://lzwjava.github.io/portfolio-en) · [AI作品集](https://lzwjava.github.io/ai-portfolio-en) · [生活作品集](https://lzwjava.github.io/life-portfolio-en)

## 课程理念

受王垠的[CS视频课程](https://www.yinwang.org/posts/cs-video-course)及其[CS课程原则](https://www.yinwang.org/posts/cs3)启发，我坚信：

* 打印变量来理解——而不只是阅读
* 阅读真实代码（nanoGPT，而不仅仅是教科书）
* 自己训练小型模型
* 构建系统，而非只学理论
* 像训练LLM一样迭代——第一次无法完美

## 你将能够做到

你将深入理解神经网络，理解transformer，从头训练GPT，修改nanoGPT，微调模型，构建AI代理，并构建一个类似OpenClaw的平台。

从数学到GPT再到AI系统。这就是路径。

## 适合谁

* 从高中生到博士生的学生，任何专业——文理背景皆欢迎。只要有好奇心和毅力，任何人都能学会AI。
* 在职专业人士，包括软件工程师、IT经理以及其他希望加深AI理解的技术岗位。
* 任何对AI感兴趣并将其作为爱好或职业转型的人。

## 课程形式

* 每节课50元人民币（每节30分钟）。订阅1到100+节课。
* 每位学生一对一辅导。
* 前几位学生将通过Zoom或腾讯会议进行实时授课并录制。后续学生将收到这些录制的视频课程，而非实时会议。
* 每节课约30分钟。
* 在进入下一节课之前，你必须完成当前课的作业。
* 课间，除睡眠时间外，可进行简短文字讨论（不超过30分钟）。
* 我亲自辅导每位学生，确保没有人被不必要的障碍卡住。
* 按课付费，无长期承诺。
* 加入一个由3000+中国工程师组成的微信社区，进行交流与讨论。微信联系：**lzwjava**。

要报名，请发送邮件至 <lzwjava@gmail.com>，主题为“AI课程报名”。请附上你的简短自我介绍以及学习AI的动机。你也可以[点击此处了解更多](https://lzwjava.github.io/contact-en)。

## 我们可以涵盖的主题

以下为主题示例。你可以选择任意子集，或在任何领域深入——我们根据你的需求定制课程。

### 从基本原理理解神经网络

理解神经网络究竟在计算什么。标量、向量、矩阵计算。逐步前向传播。通过手动导数理解反向传播直觉。激活函数、损失函数。

实践：打印每个变量（禅意神经网络风格）。用纯Python实现一个2层神经网络。在MNIST上训练。

之后，你将理解神经网络中的每一个数字。

### 从神经网络到深度学习

梯度下降、学习率、收敛。过拟合与泛化。正则化、dropout、批量/小批量/SGD。

实践：训练一个3层分类器。可视化损失曲线。手动实现dropout。

之后，你将理解深度学习实际是如何训练的。

### PyTorch最小框架

Tensor基础、autograd、nn.Module设计、优化器机制、Dataset和DataLoader。

实践：用PyTorch重建MLP。训练CIFAR分类器。检查梯度。

之后，你将能阅读任何PyTorch模型。

### 语言建模基础

分词（BPE）、n-gram模型、RNN/LSTM直觉、下一个token预测、用于语言模型的交叉熵。

实践：构建一个字符级语言模型。在小型莎士比亚文本上训练。生成文本。

之后，你将理解GPT预测什么。

### Transformer架构

自注意力、Q K V解释、多头注意力、位置编码、前馈块、残差连接。

实践：实现单头注意力。构建一个mini transformer。可视化注意力。

之后，你将理解GPT架构。

### nanoGPT深度解析

这是关键课程。nanoGPT训练循环、GPT模型架构、权重初始化、数据管道、采样。

实践：在小型数据集上训练nanoGPT。修改模型大小。在中文语料上训练。更换分词器。

之后，你将能训练自己的GPT。

### GPT训练工程

GPU内存优化、梯度累积、混合精度、检查点保存、多GPU训练、数据集扩展。

实践：训练一个1亿参数模型。恢复训练。微调模型。

之后，你将能运行真实的GPT训练。

### 指令微调与对齐

SFT微调、指令数据集、RLHF概述、奖励模型概念、LoRA微调。

实践：用聊天格式数据集微调nanoGPT。构建一个指令跟随模型。

之后，你将能构建一个聊天模型。

### LLM代理（Claude Code / OpenClaw）

工具调用、代理循环、规划与执行、记忆系统、CLI代理设计。

实践：构建一个编码代理。构建一个CLI自动化代理。构建一个多步推理代理。

之后，你将能构建一个类似OpenClaw的系统。

### 个人AI系统（毕业项目）

本地模型部署、检索（RAG）、长上下文记忆、多代理系统、CLI工具包集成。

最终项目选项：个人编码AI、研究助手、CLI AI工具包、或自主开发代理。

之后，你将拥有自己的AI系统。