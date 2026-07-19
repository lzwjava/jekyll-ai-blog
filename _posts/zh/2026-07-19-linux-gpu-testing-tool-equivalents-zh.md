---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux GPU测试工具对应版本
translated: true
type: note
---

问题：**有哪些类似 FurMark、GPU-Z、3DMark 的 Linux GPU 测试工具？Linux 下的对应工具有哪些？**

答案：

在 Windows 系统上，人们通常使用：

* **GPU-Z** → 硬件信息/监控
* **FurMark** → 极限 GPU 压力测试（"烧机"）
* **3DMark** → 游戏性能基准测试
* **OCCT** → 稳定性 + 电源测试

Linux 有对应的工具，但生态相对分散。

## 1. GPU 信息工具（GPU-Z 对应）

### `nvidia-smi`（NVIDIA）

适用于 RTX 3090 / 4070 / A100 等显卡：

```bash
nvidia-smi
```

示例输出：

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 575.xx       Driver Version: 575.xx      CUDA Version: 12.x      |
| GPU  Name        Memory-Usage  Temp  Power |
| RTX 3090         10000MiB     70C   320W |
+-----------------------------------------------------------------------------+
```

持续监控：

```bash
watch -n 1 nvidia-smi
```

更详细信息：

```bash
nvidia-smi -q
```

对应 GPU-Z 的功能：

* 显存使用率
* 温度
* 功耗
* 频率
* PCIe 链路
* ECC 错误（专业卡）

---

### `nvtop`（Linux 下的 GPU 版 htop）

安装方法：

Ubuntu 系统：

```bash
sudo apt install nvtop
```

运行：

```bash
nvtop
```

界面类似：

```
GPU  RTX 3090
利用率：99%
显存：23GB/24GB
温度：72C
功耗：350W
```

支持：

* NVIDIA
* AMD
* Intel

对 AI 工作负载非常实用。

---

## 2. FurMark 对应工具（GPU 压力测试）

FurMark 的核心功能是：

> "最大化 GPU 着色器负载 + 热量输出"

Linux 下的选择：

---

### GPU Burn（最接近 FurMark）

适用于 NVIDIA 显卡：

[https://github.com/wilicc/gpu-burn](https://github.com/wilicc/gpu-burn)

编译：

```bash
git clone https://github.com/wilicc/gpu-burn
cd gpu-burn
make
```

运行：

```bash
./gpu_burn 600
```

含义：

600 秒压力测试。

示例输出：

```
GPU 0：RTX 3090
时间：600 秒
性能：35000 Gflop/s
```

测试期间：

```bash
watch nvidia-smi
```

你可以检查：

* 温度
* 功耗稳定性
* 是否崩溃
* 驱动是否重置

对于从闲鱼购买的二手 RTX 3090，这是我优先运行的首批测试之一。

---

### `stress-ng`

CPU/GPU 压力测试：

```bash
sudo apt install stress-ng

stress-ng --gpu 1 --timeout 10m
```

针对性不如 GPU Burn 强。

---

## 3. 3DMark 对应工具

3DMark 测量游戏性能：

* DirectX
* 光线追踪
* 光栅化
* FPS

Linux 没有官方版 3DMark。

替代方案：

---

### Unigine Heaven

经典的 Linux GPU 基准测试。

Unigine Heaven Benchmark

示例：

```bash
./heaven
```

测量：

* FPS
* GPU 负载
* 稳定性

适用于对比：

RTX 3090 与 RX 7900 XT。

---

### Unigine Superposition

更现代的版本：

Unigine Superposition Benchmark

测试：

* Vulkan
* OpenGL
* 高负载场景

---

### Phoronix Test Suite

Linux 基准测试框架：

Phoronix Test Suite

安装：

```bash
sudo apt install phoronix-test-suite
```

示例：

```bash
phoronix-test-suite benchmark unigine-superposition
```

可以测试：

* GPU
* CPU
* 内存
* 存储

---

## 4. AI 工作负载 GPU 测试（对你可能更相关）

由于你的使用场景是 LLM 训练/推理，游戏基准测试意义不大。

我会测试：

### CUDA 带宽

```bash
nvidia-smi --query-gpu=memory.total,memory.free --format=csv
```

---

### PyTorch CUDA 测试

```python
import torch

print(torch.cuda.get_device_name())

x=torch.randn(
    (10000,10000),
    device="cuda"
)

for i in range(100):
    y=x@x

print("OK")
```

这会测试：

* CUDA 核心
* 显存
* 内存控制器

---

### LLM 推理测试

示例：

```bash
python -m vllm.entrypoints.openai.api_server \
 --model Qwen/Qwen3-30B \
 --tensor-parallel-size 2
```

然后测量：

* tokens/秒
* 显存使用量
* 稳定性

对于你 2 张 3090 的方案，这比 FurMark 有意义得多。

---

## 二手 GPU 检查流程（RTX 3090 / 7900 XT）

如果是购买二手显卡：

### 第 1 步：确认身份

NVIDIA：

```bash
nvidia-smi
```

AMD：

```bash
rocminfo
```

---

### 第 2 步：压力测试

```bash
./gpu_burn 600
```

监控：

```bash
nvtop
```

检查：

* 温度 < 85°C
* 驱动无崩溃
* 功耗稳定

---

### 第 3 步：显存测试

NVIDIA：

```bash
gpu-burn
```

或：

```bash
memtest_vulkan
```

显存问题在二手矿卡上很常见。

---

### 第 4 步：实际 AI 工作负载

运行：

```bash
llama.cpp
```

或：

```bash
vllm
```

加载大模型直到显存接近占满。

---

对于你的情况（购买二手 RTX 3090 / RX 7900 XT 用于 AI），我的优先级是：

1. `nvidia-smi` / `nvtop` → 识别显卡
2. `gpu-burn 10分钟` → 散热 + 功耗
3. 显存压力测试 → 内存健康状况
4. LLM 推理 → 实际 AI 稳定性

FurMark/3DMark 更适合玩家；AI 用户更关注**显存正确性 + CUDA/ROCm 在长张量工作负载下的稳定性**。
