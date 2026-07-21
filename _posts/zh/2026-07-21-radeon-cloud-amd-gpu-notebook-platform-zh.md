---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Radeon云AMD GPU笔记本平台
translated: true
type: note
---

问题：什么是 `https://radeon-global.anruicloud.com`？

答：

`radeon-global.anruicloud.com` 似乎是 **Radeon Cloud**，一个由 Anrui Cloud 运营的 AMD Radeon GPU 云笔记本平台。它提供浏览器可访问的 GPU 实例用于 AI 开发，类似于 Google Colab / Kaggle 笔记本，但面向 AMD GPU 和 ROCm。([Radeon Cloud][1])

主要思路：

```
Your browser
     |
     v
Radeon Cloud
     |
     +-- AMD GPU server
     |      |
     |      +-- ROCm
     |      +-- PyTorch
     |      +-- Jupyter/OpenCode environment
     |
     v
Run AI workloads
```

该页面目前提供：

* **GPU Notebook**
* 预构建的 AMD 容器镜像
* ROCm 环境
* 持久化存储
* 多 GPU 选择

显示的示例配置：

```
Image:
amd-oneclick-base:rocm7.2.1-py3.12-v20260416

GPU:
1 GPU / 1 credit per hour

CPU:
16 cores

Memory:
55 GiB

Disk:
100 GB
```

([Radeon Cloud][2])

---

### 为什么这对 AI 很有趣

对于 AMD 用户来说，最大的问题通常是：

```
CUDA ecosystem  >>> mature

ROCm ecosystem  >>> improving but smaller
```

Radeon Cloud 环境消除了烦人的设置：

```bash
# normally on your own AMD GPU

install ROCm
install matching PyTorch ROCm wheel
fix kernel version
fix HIP libraries
debug driver issues
```

相反：

```python
import torch

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

然后开始训练。

---

### 与 NVIDIA 云服务对比

典型的 NVIDIA 技术栈：

```
GPU:
A100/H100/4090

Software:
CUDA
cuDNN
TensorRT
vLLM
FlashAttention
```

AMD 技术栈：

```
GPU:
Radeon / Instinct

Software:
ROCm
HIP
MIOpen
Triton ROCm
vLLM ROCm
```

Radeon Cloud 基本上是让第二个技术栈更容易使用的一种尝试。

AMD 也围绕 Instinct GPU 提供官方开发者云计划（例如 MI300X 访问），但此 Radeon Cloud 服务专注于 Radeon GPU 笔记本访问。([AMD][3])

---

### 对于你的用例（LLM 训练/推理）

潜在用途：

#### 1. 测试 ROCm 兼容性

示例：

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm6.3

python train.py
```

适用于：

* nanoGPT
* Qwen 微调
* LoRA
* Stable Diffusion
* ComfyUI

---

#### 2. 对比 AMD 与 NVIDIA

你可以进行基准测试：

你的 RTX 4070：

```
CUDA
12GB VRAM
```

对比 Radeon Cloud：

```
AMD GPU
ROCm
larger VRAM possibly
```

测量：

```bash
tokens/sec
memory usage
training throughput
```

---

#### 3. 黑客马拉松 / AMD GPU 演示

鉴于你之前对 Radeon GPU 的兴趣和 ROCm 实验，这可能正是为那些希望在不拥有 AMD 硬件的情况下提交 AMD 优化 AI 演示的开发者设计的。

---

我的猜测：这在本质上类似于 **Google Colab，但是以 AMD ROCm 为先**。

有趣的问题是其背后的物理 GPU 是什么。该页面未在登陆页面上公开公开硬件型号。可能是 Radeon PRO / AI PRO 卡，而不是 Instinct MI300 级硬件。([Radeon Cloud][2])

对于严肃的 LLM 训练：

* 本地 RTX 4090 / 3090 → 仍然更简单
* MI300X → 严肃训练
* Radeon Cloud → 非常适合 ROCm 实验、演示和 AMD 兼容性测试

参考：

* [Radeon Cloud](https://radeon-global.anruicloud.com/?tab=notebook&utm_source=chatgpt.com)
* [AMD AI & HPC Cloud Access](https://www.amd.com/en/developer/resources/cloud-access.html?utm_source=chatgpt.com)

[1]: https://radeon-global.anruicloud.com/profile?utm_source=chatgpt.com "Profile - Radeon Cloud"
[2]: https://radeon-global.anruicloud.com/?tab=notebook&utm_source=chatgpt.com "Radeon Cloud"
[3]: https://www.amd.com/en/developer/resources/cloud-access.html?utm_source=chatgpt.com "AI & HPC Cloud Access"
