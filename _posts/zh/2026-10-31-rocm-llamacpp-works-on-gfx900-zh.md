---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm llama.cpp 在 gfx900 上运行
translated: true
type: note
---

完成——完整流程运行成功。以下是总结：

## 结果

| 阶段   | 状态                                                             |
|--------|------------------------------------------------------------------|
| 克隆   | `~/projects/llama.cpp` @ `eb4e244`                              |
| 构建   | HIP/ROCm 后端，`gfx900`，`GGML_CUDA_FORCE_MMQ=ON`              |
| 模型   | `models/Qwen2.5-7B-Instruct-Q4_K_M.gguf` (4.36 GiB，7.62 B params) |
| 推理   | ✅ 运行在 **AMD Radeon Pro WX 9100** (`gfx900`) 上，无 CPU 回退    |

**基准测试（ROCm，ngl=99）：**
```
pp128: 182.86 t/s
tg32:   45.84 t/s
```
**样本输出** — 提示 *"Explain in one sentence what a GPU is."*：
> A GPU is a specialized electronic circuit that processes graphics and can also be used for general-purpose computing tasks.

## 你需要记住的关键陷阱

ROCm **7.1 从 rocBLAS 中移除了 `gfx900`** — 其 Tensile 内核仅支持 `gfx908/gfx90a`。正常的 HIP 构建会在运行时崩溃：
```
rocBLAS error: Cannot read .../TensileLibrary.dat: Illegal seek for GPU arch : gfx900
```
修复：使用 `-DGGML_CUDA_FORCE_MMQ=ON` 构建，这样 llama.cpp 使用自己的 MMQ 内核而非 hipBLAS。（你还需要安装 `libhipblas-dev` 以满足 CMake 要求，即使在运行时不会用到。）

## 如何运行

```bash
cd ~/projects/llama.cpp
export PATH="$HOME/.local/bin:$PATH"   # 用于 cmake

# 单次补全
./build/bin/llama-completion -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
    -ngl 99 -p "Your prompt" -n 256

# 交互式聊天
./build/bin/llama-cli -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf -ngl 99

# 兼容 OpenAI 的服务器，端口 8080
./build/bin/llama-server -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf -ngl 99 --host 127.0.0.1 --port 8080
```

一切都在 GPU 上运行；使用的 VRAM 约为 16 GiB 中的 4.4 GiB，因此你有充足的空间运行更大的模型或更长的上下文。