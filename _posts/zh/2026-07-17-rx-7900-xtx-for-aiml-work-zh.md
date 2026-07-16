---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RX 7900 XTX 用于AI/ML工作
translated: true
type: note
---

问题：RX 7900 XTX 怎么样，特别是用于 AI/ML 工作？

答案：

**硬件（RDNA3, gfx1100）：**

- 96 个 CU，24GB GDDR6 @ 960 GB/s，355W TBP
- 61 TFLOPS FP32，无专用张量核心——矩阵运算通过着色器核心上的 WMMA 进行（每 FLOP 性能弱于 Nvidia 的张量核心，但 24GB VRAM 是实际卖点）
- 5nm TSMC，类似 Zen 的 chiplet MCD/GCD 设计

**当前价格/性能背景（2026 年中）：** DRAM/GDDR 短缺推高了所有价格——新卡现在约 1100-1400 美元，二手约 750-850 美元，但 Nvidia 涨价更猛（4090 达到 1800-2700+ 美元，5090 超过 3000 美元），因此 XTX 的相对价值实际上有所提升。

**软件栈——这对你来说才是关键：**

ROCm 已更新至 7.2.x 系列（最新补丁为 7.2.4），这是一个 Windows+Linux 合并版本，可自动检测 RDNA 3、RDNA 4 和 Strix Halo。gfx1100（你的显卡）仍受官方支持。

Ubuntu 上的安装：

```bash
# ROCm 7.2 安装
sudo apt update
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/noble/amdgpu-install_<version>_all.deb
sudo apt install ./amdgpu-install_*.deb
sudo amdgpu-install --usecase=rocm,hiplibsdk -y

# 验证
rocminfo | grep gfx
rocm-smi
```

PyTorch（ROCm wheel）：

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm6.2
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

（HIP 表现为 `torch.cuda.*`——与 CUDA 脚本相比无需修改代码，这正是 HIP 的意义所在）

**llama.cpp（最佳推理路径）：**

```bash
git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp
cmake -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1100 -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j
```

实际数据：Llama 3.1 8B 在 7900 XTX 上运行约 96 tok/s——大约为 RTX 4090 吞吐量的 75%，价格却低得多。

**与 CUDA 的差距：**

- FlashAttention 的 ROCm 分支现已覆盖 RDNA 3 和 RDNA 4——前向传播在 gfx11 上可用，但完整反向传播仅限 CDNA（因此使用 FA2 进行训练/微调受限；推理没问题）
- vLLM 通过 ROCm Docker 镜像运行，但预计会比 Nvidia 遇到更多麻烦
- 对于大规模训练，你仍会使用 MI300X（你已经有了）——7900 XTX 实际上是一块 **本地推理/开发机** 显卡，而非训练卡

**对你的配置而言的结论：** 鉴于你已经在用 MI300X 进行训练，配备 7900 XTX 的机器作为廉价的本地推理设备用于测试你的 GPT-2/代理项目是有意义的，无需占用集群时间——24GB 可以轻松容纳量化后的 32-70B 模型。

参考文献：

- [ROCm 本地 LLM 设置 2026 — 96 tok/s 基准测试](https://localaimaster.com/blog/amd-rocm-local-llm-setup)
- [RX 7900 XTX 本地 AI 2026 指南](https://localaimaster.com/blog/radeon-7900-xtx-local-ai)
- [AMD ROCm 支持的 GPU 2026](https://www.kunalganglani.com/blog/rocm-consumer-gpu-cuda-alternative-2026)
