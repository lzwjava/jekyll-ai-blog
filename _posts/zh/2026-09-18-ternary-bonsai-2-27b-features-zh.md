---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ternary Bonsai 2-27B 特性
translated: true
type: note
---

**问题：** 什么是 Ternary-Bonsai-2-27B-gguf，它有什么特别之处？

**回答：**

**Ternary Bonsai 2 27B** 是由 **Prism ML** 发布的高度压缩大型语言模型，旨在让完整的 27B 级推理在笔记本电脑和单块 GPU 等消费级硬件上运行。以下是它的特别之处：

---

### 它是什么

这是一个基于三元（约 2 比特）权重表示构建的文本生成模型，兼容 llama.cpp，支持 CUDA、Metal 和 CPU。

基础模型源自 **Qwen3.8-27B**，一个 27B 混合注意力因果语言模型，其架构保持不变。

---

### 关键创新：三元权重

每个权重取值为 {−1, 0, +1}，每 128 个权重共享一个 FP16 缩放因子。一个三元值携带 log₂3 ≈ 1.585 比特信息，有效存储成本约为 1.71 比特/权重——相比 FP16 实现约 9.3 倍的理想压缩。

权重以**旋转基**存储：每个矩阵在分配三元值前，先通过正交 Hadamard 旋转按块变换，推理时运行时会匹配应用变换到激活值上，且不增加额外内存开销。

---

### 规模与保留的智能

模型从约 54 GB（FP16）缩小到 **5.95 GB**（PTQ1_0 密集打包）或 **7.21 GB**（PQ2_0 打包），同时保留 **98.2% 的 FP16 智能**——在 14 个思维模式基准测试中平均得分 84.78。

与相同基础模型的其他压缩版本相比：

传统“2 比特”IQ2_XXS 构建实际为 2.8 比特/权重（9.4 GB），但在相同 14 个基准上仅得 72.59 分。Bonsai 2 以不到其三分之二的体积，领先超过 **12 分**。

---

### 硬件性能

在 Apple M5 Max 笔记本上，模型运行速度约为 **47 tokens/秒**。在 RTX 5090 上，达到约 130 tokens/秒。在低功耗 72W L4 数据中心 GPU 上，仍能维持约 30 tokens/秒。

该模型还支持 **262K-token 上下文窗口**，得益于其混合注意力骨干网络（约 75% 线性注意力），在设备上保持可用性。

---

### 两种 GGUF 打包

**PTQ1_0** 密集打包三进制（1.75 比特/权重，5.95 GB），在 Ada 代 GPU 和 L4 上速度更快。**PQ2_0** 将每个三进制存储为 2 比特槽（2.13 比特/权重，7.21 GB），在 H100、A100、Blackwell 显卡上及所有场景的提示处理中速度更快。

---

### 重要注意事项

标准 llama.cpp **无法运行**这些文件——它们需要定制的 [PrismML-Eng/llama.cpp 分支](https://github.com/PrismML-Eng/llama.cpp)，该分支包含三元混合注意力内核。标准 llama.cpp 会拒绝这些文件，或静默产生乱码输出。

---

**参考资料：**

- [prism-ml/Ternary-Bonsai-2-27B-gguf · Hugging Face](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- [Bonsai 演示与示例（GitHub）](https://github.com/PrismML-Eng/Bonsai-demo)
- [PrismML llama.cpp 分支](https://github.com/PrismML-Eng/llama.cpp)
