---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Tesla M40: 大显存，旧技术'
translated: true
type: note
---

Tesla M40 是一张独特的显卡：**大显存（24GB），但是老旧的 Maxwell 架构**——没有 tensor cores，没有快速 FP16/INT8，计算能力 5.2 已被现代框架放弃。所以实际情况是：

## ⚡ 现实检查

| M40 规格 | 数值 | 影响 |
|---|---|---|
| VRAM | 24 GB | 可以容纳大模型 ✅ |
| FP32 | ~7 TFLOPS | 还可以 |
| FP16 | ~7 TFLOPS（无加速） | LLM 数学运算很慢 ❌ |
| Tensor cores | ❌ 无 | 没有快速矩阵核心 ❌ |
| 内存带宽 | 288 GB/s | Token 生成瓶颈 |
| 软件支持 | 已在 PyTorch 2.x、TF 2.x、CUDA 13 中被移除 | 必须使用 CUDA 12.x / llama.cpp |

## 🎯 最佳应用（按排名）

**1. 通过 llama.cpp 系列进行 LLM 推理——最合适的选择**
llama.cpp 仍在积极维护，并且仍在为 Maxwell（CC 5.2）构建。24GB 显存让你可以运行在较小显卡上无法容纳的大型量化模型。预期速度**慢但可用**：

| 模型 | 量化 | VRAM | 预估速度（M40） |
|---|---|---|---|
| Llama 3.1 / Qwen 8B | Q4/Q5/Q6 | 4–6 GB | ~6–12 tok/s |
| Qwen 14B / Mistral 衍生模型 | Q4/Q5 | 8–9 GB | ~4–7 tok/s |
| Qwen 32B / 34B | Q4_K_M | ~20 GB | ~1.5–3 tok/s |
| 70B | Q4（约 40GB） | ❌ 装不下 | 需要 CPU offload |

也可使用的前端/分支：**KoboldCpp**、**text-generation-webui（使用旧版 CUDA 构建）**、**Ollama**（旧版本 / 强制 CUDA 12 arch）。

**2. 语音转文字——whisper.cpp** ✅
Whisper 模型很小（0.24–1.5 GB），在 Maxwell 上运行得很好。这是一个好用且真正实用的工作负载。

**3. 经典 / 科学计算 CUDA** ✅
GROMACS/LAMMPS/OpenMM（旧版本，FP32）仍支持 sm_52。还有渲染：旧版 **Blender 2.8x/3.0 Cycles**、**OctaneRender 4/2018**。

**4. 视频转码（NVENC/NVDEC）**——如果显卡暴露了 NVENC（我们可以检查），就可以使用。H.264/H.265 固定功能编码可减轻 CPU 负担。

## ❌ 在 M40 上不值得做的事
- **vLLM / 现代 PyTorch 2.x / TensorFlow 2.x**——需要 Turing+（sm_70/75+），无法运行。
- **Stable Diffusion / 图像生成**——可以运行但慢得痛苦（生成一张 512px 图像需要数分钟），并且需要古老的 PyTorch。
- **微调 LLM**——没有 tensor cores 太慢。

---

## 我的建议

既然 **`llama.cpp` 是明显的赢家**，我可以现在就完整地设置好：

1. 安装 `nvidia-cuda-toolkit`（CUDA 12.x——最后一个支持 Maxwell 的版本）。
2. 构建针对你的显卡优化的 **llama.cpp**（`-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=52`，再加上量化 MMU "MMQ" 路径，因为 Maxwell 没有 `dp4a`）。
3. 构建 **whisper.cpp** 用于语音转文字。
4. 下载一个好的启动模型（例如 **Qwen2.5-14B-Instruct Q5_K_M**，约 10GB），并实测 tokens/秒。

要我继续并设置好吗？如果是的话，告诉我你的首选使用场景（聊天助手、代码、翻译、转录），我会挑选匹配的模型。