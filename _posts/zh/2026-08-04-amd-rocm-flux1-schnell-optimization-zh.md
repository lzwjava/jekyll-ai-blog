---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD ROCm FLUX.1-schnell 优化
translated: true
type: note
---

问题：如何优化在 AMD GPU 上使用 ROCm 的 stable-diffusion.cpp FLUX.1-schnell GGUF 工作流？

回答：

您当前的设置针对 **RTX 4070 CUDA** 进行了优化：

```
sd-cli
 ├── diffusion=cuda
 ├── vae=cuda
 ├── clip=cpu
 └── t5xxl=cpu
```

对于 AMD ROCm，优化路径有所不同。关键在于：

1. 使用 HIP/ROCm 后端构建 `stable-diffusion.cpp`。
2. 如果 VRAM 允许，将更多组件移至 GPU。
3. 调整内存卸载。
4. 使用 ROCm 特定的内核/构建标志。

---

## 1. 使用 ROCm/HIP 构建 stable-diffusion.cpp

`stable-diffusion.cpp` 使用与 llama.cpp 相同的 ggml 后端风格。

克隆：

```bash
git clone https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp
```

使用 HIP 构建：

```bash
cmake -B build \
  -DSD_USE_HIPBLAS=ON \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build -j$(nproc)
```

检查：

```bash
./build/bin/sd-cli --help
```

您应该会看到 HIP 后端支持。

验证：

```bash
rocminfo | grep gfx
```

示例：

```
gfx1100   # RDNA3
gfx1030   # RDNA2
gfx90a    # MI250/MI300
```

---

## 2. 将后端从 CUDA 更改为 HIP

您当前的设置：

```python
self._backend = "diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu"
```

更改为：

```python
self._backend = "diffusion=hip,clip=cpu,vae=hip,t5xxl=cpu"
```

示例：

```bash
--backend diffusion=hip,clip=cpu,vae=hip,t5xxl=cpu
```

---

## 3. VRAM 放置策略

FLUX 模型很重。

您的模型：

```
flux1-schnell-Q4_0.gguf
~8-9GB
```

其他文件：

```
vae.safetensors
~300MB

clip_l
~235MB

t5xxl_fp16
~9.8GB
```

FP16 总计：

```
diffusion     8GB
T5XXL         10GB
VAE           0.3GB
CLIP          0.2GB

≈18-20GB VRAM
```

因此，您当前的设置：

```
diffusion GPU
vae GPU
clip CPU
t5 CPU
```

对于 12GB 来说是合理的。

---

### AMD 16GB GPU

示例：

RX 7900 XT：

```
24GB
```

或 MI50：

```
16GB
```

您可以尝试：

```bash
--backend diffusion=hip,vae=hip,clip=hip,t5xxl=cpu
```

更好的方案：

```
GPU:
 diffusion
 VAE
 CLIP

CPU:
 T5XXL
```

---

### AMD 24GB+

示例 MI300X：

```
192GB HBM
```

将所有内容移至 GPU：

```bash
--backend diffusion=hip,vae=hip,clip=hip,t5xxl=hip
```

速度差异巨大。

---

## 4. 启用 ROCm 环境调优

运行前：

```bash
export HSA_OVERRIDE_GFX_VERSION=<您的 gfx 版本>
export PYTORCH_ROCM_ARCH=<您的 gfx 版本>
```

示例：

RX 7900：

```bash
export HSA_OVERRIDE_GFX_VERSION=11.0.0
```

MI300：

```bash
export HSA_OVERRIDE_GFX_VERSION=9.4.2
```

---

## 5. 使用 rocBLAS 调优

ROCm 有内核选择开销。

运行：

```bash
rocblaslt-bench
```

或启用：

```bash
export ROCBLAS_LAYER=4
```

生产环境：

```bash
export ROCBLAS_TENSILE_LIBPATH=/opt/rocm/lib/rocblas/library
```

---

## 6. 使用激进优化编译

对于 RDNA3：

```bash
cmake -B build \
  -DSD_USE_HIPBLAS=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DAMDGPU_TARGETS=gfx1100
```

对于 MI300：

```bash
cmake -B build \
  -DSD_USE_HIPBLAS=ON \
  -DAMDGPU_TARGETS=gfx942
```

---

## 7. 使用 Vulkan 后端作为替代方案

对于 AMD 消费级 GPU，Vulkan 有时可以胜过 ROCm。

构建：

```bash
cmake -B build \
  -DSD_USE_VULKAN=ON
```

运行：

```bash
--backend diffusion=vulkan
```

优点：

```
ROCm:
+ 更好的计算性能
+ 张量内核
- 驱动复杂性

Vulkan:
+ 随处可用
+ 无需安装 ROCm
- 有时较慢
```

对于 RX 6000/7000 系列显卡，建议对两者进行基准测试。

---

## 8. 您的 Python 代码更改

使后端可配置：

```python
if self._backend is None:
    if os.environ.get("AMD_GPU"):
        self._backend = (
            "diffusion=hip,"
            "clip=cpu,"
            "vae=hip,"
            "t5xxl=cpu"
        )
    else:
        self._backend = (
            "diffusion=cuda,"
            "clip=cpu,"
            "vae=cuda,"
            "t5xxl=cpu"
        )
```

然后：

AMD：

```bash
AMD_GPU=1 python app.py
```

NVIDIA：

```bash
python app.py
```

---

## 9. 最大的性能提升

对于 FLUX.1-schnell：

| 优化项                     |     速度影响 |
| -------------------------- | -----------: |
| GPU VAE                    |       10-20% |
| GPU CLIP                   |        5-10% |
| GPU T5XXL                  |         2-3x |
| 使用 Q8/Q6 扩散替代 Q4     | 质量提升 + 更慢 |
| Vulkan 与 HIP 基准测试     |        ±20% |
| 持久化进程                 |       20-30% |

您当前的架构：

```
spawn sd-cli
load GGUF
generate
exit
```

存在隐藏成本。

持久化服务器会更快：

```
Python
 |
 v
sd-cpp 守护进程
 |
 GPU 常驻模型
```

类似于 vLLM。

对于多张图片：

```
当前：
10 张图片
10 次模型加载

优化后：
10 张图片
1 次模型加载
```

可以轻松节省数分钟。

---

针对您的硬件方向：

* RTX 4070 12GB → 保持 CUDA。
* RX 7900 XTX 24GB → ROCm 值得关注。
* MI300X → 全 GPU FLUX 流水线，巨大速度提升。
* MI50 16GB → 可能可行，但 ROCm 支持较旧且不理想。

对于当今的 AMD 图像生成，我建议对以下方案进行基准测试：

```
stable-diffusion.cpp HIP
        vs
stable-diffusion.cpp Vulkan
        vs
ComfyUI ROCm
```

因为 FLUX 性能高度依赖后端内核。
