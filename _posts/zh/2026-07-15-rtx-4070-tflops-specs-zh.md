---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 TFLOPS 规格
translated: true
type: note
---

问题：RTX 4070 TFLOPS？

答案：

基础版 **RTX 4070**（5888个CUDA核心，AD104）：FP32：29.15 TFLOPS，FP16：29.15 TFLOPS，BF16：29.15 TFLOPS。张量核心吞吐量更高：184个第四代张量核心提供466个张量TFLOPS用于AI处理（这是INT8密集数据——FP16张量约为58 TFLOPS密集 / 117带稀疏性，根据WareDB数据）。

相关SKU供参考：

- **RTX 4070 Ti**：7,680个CUDA核心，提供40.09 TFLOPS的FP32性能
- **RTX 4070 SUPER**：FP32：35.48 TFLOPS，FP16：35.48 TFLOPS，BF16：35.48 TFLOPS

针对你训练GPT-2 760M的场景：单张4070的29 FP32 TFLOPS属于玩具级——你需要BF16张量吞吐量（约58 TFLOPS密集），并且注意12GB显存限制会在计算瓶颈之前就限制批量大小。你正在使用的MI300X拥有约163 TFLOPS FP32 / 更高的矩阵乘法吞吐量，因此4070实际上只是一个开发/推理设备，不适合进行超出小规模实验的训练任务。

参考文献：

- [WareDB RTX 4070规格](https://www.waredb.com/processor/nvidia-geforce-rtx-4070)
- [WareDB RTX 4070 SUPER规格](https://www.waredb.com/processor/nvidia-geforce-rtx-4070-super)
- [ComputePrices RTX 4070 Ti规格](https://computeprices.com/gpus/rtx4070ti)
