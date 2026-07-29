---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attn CUDA构建挂起修复
translated: true
type: note
---

问题：为什么 `pip install flash-attn==2.8.4` 会卡在 `Building wheel for flash-attn`？

答案：

实际上并非卡在下载阶段，而是已经进入了 **CUDA 扩展编译阶段**。

`flash-attn` 不是一个纯 Python 包。当出现以下信息：

```
Building wheels for collected packages: flash-attn
  Building wheel for flash-attn (s/tup.py) ... \
```

这意味着 pip 正在执行类似这样的命令：

```
python setup.py bdist_wheel
```

该命令会编译 C++/CUDA 内核。

针对你的环境：

* Python：3.12（由 `/home/lzw/.local/lib/python3.12` 显示）
* PyTorch CUDA：很可能是 CUDA 13.0 包
* GPU：RTX 4070（Ada 架构，sm_89）
* flash-attn：2.8.4

编译过程可能需要 **10–60 分钟**，尤其是在编译多种架构的情况下。

检查是否真的在运行：

```bash
top
```

或：

```bash
htop
```

查找以下进程：

```
nvcc
g++
c++
ninja
```

如果正在编译，CPU 占用率应该很高。

此外，也可以检查：

```bash
ps aux | grep nvcc
```

你可能会看到类似：

```
nvcc -c flash_attn_2_cuda.cu
```

---

## 为什么这么慢

FlashAttention 需要构建大量 CUDA 内核：

```
flash_attn/
 ├── softmax 内核
 ├── 融合注意力前向
 ├── 融合注意力反向
 ├── dropout 内核
 └── 不同的头维度
```

构建矩阵非常庞大：

```
GPU 架构：
sm80  (A100)
sm86  (RTX 30)
sm89  (RTX 40)
sm90  (H100)
...
```

如果编译所有架构，会浪费大量时间。

---

## 针对 RTX 4070 的更快构建

你的 GPU 是 Ada 架构：

```
计算能力：8.9
```

设置：

```bash
export TORCH_CUDA_ARCH_LIST="8.9"
```

然后重新安装：

```bash
pip uninstall flash-attn -y

MAX_JOBS=8 TORCH_CUDA_ARCH_LIST="8.9" \
pip install flash-attn==2.8.4 --no-build-isolation
```

`MAX_JOBS` 控制并行编译的作业数。

根据你的 CPU 核心数，可以运行：

```bash
nproc
```

然后设置：

```bash
MAX_JOBS=$(nproc)
```

---

## 另一个可能的问题：CUDA 版本不匹配

你的日志显示：

```
nvidia-cuda-nvrtc==13.0.88
nvidia-nvjitlink==13.0.88
```

但你之前的问题提到：

```
Python 3.14 + CUDA 13.2 与 torch CUDA 12.8 版本不匹配
```

Flash-attn 对以下组件的版本非常敏感：

```
NVIDIA 驱动
        |
        v
CUDA 运行时
        |
        v
PyTorch CUDA
        |
        v
flash-attn 编译用的 CUDA
```

检查版本：

```python
import torch

print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.get_device_name())
```

预期输出类似：

```
2.x.x
12.8
NVIDIA GeForce RTX 4070
```

如果 PyTorch 显示 CUDA 12.8，但 pip 拉取了 CUDA 13 的包，后续编译可能会失败。

---

## 如果只是想运行实验

你并不需要 flash-attn。

PyTorch 的 SDPA（缩放点积注意力）已经可以满足需求：

```python
import torch.nn.functional as F

out = F.scaled_dot_product_attention(
    q, k, v,
    is_causal=True
)
```

它已经使用了优化的内核：

```
FlashAttention 后端
        |
        +-- 可用？ 是 -> 使用
        |
        +-- 不可用 -> 内存高效 SDPA
        |
        +-- 回退 -> 数学内核
```

对于 nanoGPT/vLLM 的学习，SDPA 通常已经足够。

---

根据这个日志，我的判断是：

1. 它正在编译，并非卡死。
2. 首次构建很容易超过 20 分钟。
3. 如果 CPU 空闲超过 5 分钟，请中断它。
4. 重新尝试运行：

```bash
MAX_JOBS=8 TORCH_CUDA_ARCH_LIST="8.9" \
pip install flash-attn==2.8.4 --no-build-isolation
```

这应该可以将构建从通用的长时间 CUDA 构建缩短为仅针对 RTX 4070 的特定构建。