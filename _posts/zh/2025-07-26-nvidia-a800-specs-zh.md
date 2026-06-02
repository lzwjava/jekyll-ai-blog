---
audio: false
generated: true
lang: zh
layout: post
title: NVIDIA A800 GPU：A100的变体版本
translated: true
type: note
---

NVIDIA A800 是英伟达公司推出的专业级图形处理器（GPU），主要面向高性能计算（HPC）、人工智能（AI）、数据科学及工作站工作流设计。该芯片基于英伟达安培架构，采用7纳米制程的GA100图形处理器。A800于2022年11月作为A100 GPU的衍生版本发布，专门为符合美国对特定地区（如中国）高端AI芯片的出口管制要求而调整。与A100的核心区别在于NVLink互连速度降低（A800为400 GB/s，A100为600 GB/s），这对多GPU扩展性能产生影响，但在单GPU任务中仍保持相近的核心性能。

### 关键规格（以A800 PCIe 40GB版本为例）

- **CUDA核心数**：6,912
- **张量核心数**：432（第三代）
- **显存**：40GB HBM2（高带宽内存）；部分版本提供80GB
- **显存带宽**：最高1.55 TB/s
- **性能指标**：
  - 单精度（FP32）：最高19.5 TFLOPS
  - 双精度（FP64）：最高9.7 TFLOPS
  - 张量性能（TF32）：最高312 TFLOPS
- **接口**：PCIe 4.0 x16
- **功耗**：约250-300W TDP（热设计功耗）
- **形态规格**：提供适用于服务器和工作站的被动或主动散热版本

A800在加速机器学习训练、推理、科学模拟和可视化等高性能任务方面表现卓越。基准测试显示，其性能可达A100的70-100%（具体取决于工作负载）——在单精度与双精度计算中几乎持平，但在需要高速多GPU通信的场景中受限于NVLink降速。

产品变体包括面向工作站的A800 40GB主动散热版，以及适用于服务器的A800 PCIe 80GB等型号。该产品并非面向消费级游戏市场，而是专为企业级和专业应用场景设计。

[NVIDIA A800 40GB 主动散热显卡](https://www.nvidia.com/en-us/design-visualization/a800/)
[NVIDIA A800 PCIe 40 GB 规格详情](https://www.techpowerup.com/gpu-specs/a800-pcie-40-gb.c3964)
[英伟达推出A800 GPU替代受禁运的A100中国版本](https://analyticsdrift.com/nvidia-introduces-a800-gpu-chips-to-replace-banned-a100-chips-for-china/)
[ThinkSystem NVIDIA A800 PCIe 4.0 GPU解决方案](https://lenovopress.lenovo.com/lp1813-thinksystem-nvidia-a800-pcie-gpu)
[英伟达AI芯片系列：A100 A800 H100 H800 B200](https://www.fibermall.com/blog/nvidia-ai-chip.htm)
