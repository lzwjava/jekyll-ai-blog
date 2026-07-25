---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决48GB显存中的FLUX模型问题
translated: true
type: note
---

问得好。以下是我们遇到的具体问题及解决方式：

---

## 🔧 出了什么问题 & 我们如何修复

### 1. ❌ `pipe.to('cuda')` — 显存溢出崩溃

**问题：** 整个模型在 bfloat16 精度下约 **54 GB**。一次性将所有参数移到 GPU（`pipe.to('cuda')`）会试图塞进 **48 GB 显存** → 立即 OOM。

```
HIP out of memory. Tried to allocate 18.00 MiB.
GPU 0 has a total capacity of 47.98 GiB of which 0 bytes is free.
```

**修复：** 使用 `pipe.enable_sequential_cpu_offload()` — 将大部分权重保留在 CPU 内存中，仅在计算前将所需子模块移到 GPU，计算结束后再卸载。

### 2. ❌ `pipe.enable_model_cpu_offload()` — 依然 OOM

**问题：** 即使按模块卸载，**仅 Transformer 部分**（约 20 GB）加上其 **中间激活值**（注意力状态、前馈隐藏层）在 1024×1024 前向传播时会超过 48 GB 总容量。

**修复：** 同时将分辨率从 **1024×1024** 降至 **512×512**。这大幅降低了激活内存：

- 注意力：序列长度为 O(n²) — 1024² → 512² 内存减少 4 倍
- 潜在通道：成比例缩小

### 3. ⚠️ APEX JIT 编译（每次运行 20 秒）

**问题：** 每次运行都会重新编译 `fused_layer_norm_cuda`，因为 `.so` 文件在运行之间未缓存。

**修复：** 仅首次编译（第一次运行耗时 20 秒），之后缓存（第二次运行显示 `ninja: no work to do.` → 0.7 秒）。

### 4. 🔌 网络：HuggingFace 无法访问

**问题：** 服务器位于中国，`huggingface.co` 被屏蔽。直接连接超时。

**修复：** 使用 `hf-mirror.com`（HF 镜像）作为 `HF_ENDPOINT`。否则连模型元数据都无法检查。

### 5. 🔐 模型需授权访问

**问题：** FLUX 模型需要接受许可协议并提供 HF token。

**修复：** 用户提供了有效 token。我们将其保存到 `~/.cache/huggingface/token`。

---

## 🤯 为什么 FLUX 难以运行

### A. 模型体积巨大

| 组件 | 大小（bf16） |
| ----------- | ------------ |
| Transformer（DoubleStreamBlock） | ~20 GB |
| T5 文本编码器 | ~9 GB |
| CLIP 文本编码器 | ~2 GB |
| VAE + AE | ~1 GB |
| **总计** | **~54 GB** |

不能直接加载并运行——需要 **CPU 卸载** 或 **量化**（8-bit/4-bit）。即使是 48 GB 显存也不够。

### B. FLUX 架构极其消耗内存

FLUX 采用 **DoubleStreamBlock** 架构，文本和图像特征在整个 Transformer 中持续交互。这意味着：

- 每个去噪步骤都必须加载完整的 Transformer
- 对 4096+ token 序列的注意力计算是 O(n²) 内存
- 没有像 Stable Diffusion 那样的交叉注意力分离（后者可以交换文本编码器）

### C. ROCm 仍有一些粗糙边缘

- `flash_attn` 在 ROCm 上不工作 → 回退到 PyTorch 原生 SDPA（更慢）
- APEX 操作在首次运行需要 JIT 编译
- `aiter` 后端关于 NUMA 平衡的警告
- `amdgpu-coerce-illegal-types=1` 标志与新版 clang 不兼容

### D. CPU 卸载导致速度变慢

使用顺序卸载时，每一步都需要：

1. 将 Transformer 权重 **CPU → GPU**（PCIe 瓶颈）
2. 运行前向传播
3. 将结果 **GPU → CPU**
4. 重复下一步

这就是为什么 4 步花了 **60 秒**，而在单块 H100 且全部数据在显存中时只需约 2 秒。

---

## 🏆 最终结果：克服所有困难成功运行

```
提示词: "A cute cat sitting on a desk, digital art style"
4步，512×512 → 60.3 秒 ✅
```

如果你希望 **更快生成**，我们可以：

1. 安装 `bitsandbytes` 进行 8-bit/4-bit 量化（腾出更多显存）
2. 使用 `torch.compile` 融合操作
3. 禁用 APEX aiter 后端（`USE_ROCM_AITER_ROPE_BACKEND=0`）以避免慢路径
