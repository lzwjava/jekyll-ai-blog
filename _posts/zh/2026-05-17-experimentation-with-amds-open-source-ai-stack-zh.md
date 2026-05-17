---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 对AMD的开源AI栈的实验
translated: true
type: note
---

问题：我花了两天时间研究，由于我已经有一块 RTX 4070，我首先尝试了使用云平台。我成功创建了一个 AMD Developer Cloud 实例，准备了一份带文字和图片的一分钟笔记，并发布在 GitHub 上；它将在两小时后更新到我的博客。我对 AMD 特别感兴趣，因为我信奉开源的力量。我认为 ROCm/ROCm-W 能够赶上 CUDA，最终实现完全开源的的大模型训练和推理栈。除了芯片，其他部件我们无法自行制造，但除此之外，我更倾向于开源。AMD 目前市值大约 7000 亿美元，我想与之共同成长。有了 AI，学习速度也更快。这个做法合理吗？

回答：

是的，你的做法是合理的，且从目标来看具有战略意义：

1. **从云平台入手：** 使用 AMD Developer Cloud 进行初期实验是明智的。这避免了前期硬件投资，让你无需接触物理 GPU 即可验证 ROCm 在你工作流程中的能力。

2. **聚焦开源栈：** ROCm（ROCm-W 或上游 ROCm）是 AMD 完全开源的 CUDA 替代方案。虽然 NVIDIA 的 CUDA 生态系统更成熟，但 AMD 的栈正在快速追赶，PyTorch 和 TensorFlow 等开源框架对 ROCm 的支持也日益增强。这与你的完全开源模型训练/推理管线的目标高度一致。

3. **硬件灵活性：** 本地保留一块 RTX 4070，让你在仅支持 CUDA 的框架中拥有高性能选项，同时可并行实验 ROCm。这种混合方法很实用，可以对比性能、兼容性和开发体验。

4. **学习加速：** 深入参与 AMD 的开源生态系统，能加速你对 GPU 架构、内核级操作和跨平台机器学习优化的理解——这些技能具有很高的可迁移性。

5. **投资视角：** 如果你相信开源 AI 软件与硬件创新之间的长期协同效应，关注 AMD 的增长是合理的。你参与生态系统发展的兴趣也能让你更早洞察趋势。

几点实用建议：

* 关注 ROCm 对你使用的具体 AMD 云硬件以及本地工作流的兼容性。某些模型库可能需要补丁或特定版本。
* 在 ROCm 和 CUDA 上对常见工作负载进行基准测试，以便量化性能差异。
* 如果遇到 bug，可以参与开源项目提交问题；这既能提升你的技能，也有助于社区。

总体而言，将云实验、本地硬件使用以及对开源的关注结合起来，既有利于技术成长，也符合长期战略规划。

参考：

* [ROCm 官方站点](https://rocmdocs.amd.com/)
* [AMD Developer Cloud](https://developer.amd.com/solutions/compute/rocm/)
* [PyTorch ROCm 支持](https://pytorch.org/get-started/locally/#start-locally)
* [CUDA 与 ROCm 对比](https://www.phoronix.com/scan.php?page=article&item=rocm-vs-cuda)