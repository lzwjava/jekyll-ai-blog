---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最简单的Qwen推理代码库
translated: true
type: note
---

**问题：** llama.cpp 太大，学起来费劲。对于像 Qwen 这样的真实模型，进行*推理/服务*的最简 nanoGPT/nanochat 风格代码库是什么？

**回答：**

根据你选择 Python/GPU 路线还是 C/CPU 路线，有两个明显的赢家：

### 1. nano-vllm ——“推理界的 nanoGPT”（Python，约 1,200 行）

这是与服务场景最接近的 nanoGPT 类比。它由 DeepSeek（名字出现在 DeepSeek-V3/R1 技术报告中）的一位贡献者创建，约 1,200 行 Python 代码，尽管代码量极小，却实现了前缀缓存、张量并行、CUDA graphs 和 torch.compile——吞吐量可与完整的 vLLM 媲美甚至略高。在搭载 Qwen3-0.6B 的 RTX 4070 笔记本电脑 GPU 上的基准测试显示，它在离线推理中与 vLLM 持平或更优——也就是说，它能在你的 192.168.1.36 工作站上完美运行。

```bash
pip install git+https://github.com/GeeeekExplorer/nano-vllm.git
huggingface-cli download Qwen/Qwen3-0.6B --local-dir ./Qwen3-0.6B
```

```python
from nanovllm import LLM, SamplingParams
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("./Qwen3-0.6B")
llm = LLM("./Qwen3-0.6B", enforce_eager=True, tensor_parallel_size=1)

prompts = [tok.apply_chat_template(
    [{"role": "user", "content": "用三句话解释 KV cache"}],
    tokenize=False, add_generation_prompt=True)]
out = llm.generate(prompts, SamplingParams(temperature=0.6, max_tokens=256))
print(out[0]["text"])
```

为什么它是你正确的学习目标：它本质上是 vLLM 架构的简化版。调度器约 150 行，而 vLLM 有数千行；nano-vllm 与 vLLM 之间的 98,800 行差异主要是生产级别的管道（超时、OOM 恢复、指标监控），而 `models/qwen3.py` 中的模型代码是一个纯粹的仅解码器 transformer，你可以将其扩展到其他架构。按此顺序阅读：`sequence.py` → `scheduler.py` → `block_manager.py`（分页 KV 缓存） → `model_runner.py` → `models/qwen3.py`。这就是一个下午理解 vLLM 整个心智模型的路径。

它设计为离线/批量处理——没有 HTTP 服务。将其包装成 OpenAI 兼容端点只需约 30 行 FastAPI 代码，这本身就是一个很好的练习（社区已有 fork 实现，例如 HF Inference Endpoints 集成）。

### 2. qwen3.c ——llama2.c 的继任者（单文件 C，约 1,000 行，CPU）

如果你想要直接的 Karpathy 血统：adriancable/qwen3.c 始于 Karpathy 的 llama2.c，在一个无依赖的 C 文件（约 1,000 行）中运行 Qwen3 架构的模型，支持多核 CPU、Unicode、量化检查点，甚至推理模式——明确构建为最新的学习资源，因为 LLaMA 2 架构已经过时。

```bash
git clone https://github.com/adriancable/qwen3.c && cd qwen3.c
python export.py Qwen3-4B.bin   # 从 Hugging Face 下载并转换，约 10 分钟
make
./run Qwen3-4B.bin -r 1          # -r 1 启用思考模式
```

这可以在你的 M2 Air 上顺畅运行（无需 GPU）。还有一个并行项目 gigit0000/qwen3.c，它直接加载 GGUF 格式而无需转换，并增加了多轮前缀缓存；此外还有 qwen3.cu——与上面类似，但为一个纯 CUDA-C 单文件，通过 CUDA 内核进行分词，无依赖——如果你希望了解 PyTorch 层之下内核的工作原理，这是在 4070 上的自然进阶步骤。

### 鉴于你的目标，我会这样安排学习顺序

1. **在 4070 上学习 nano-vllm**——学习连续批处理、分页 KV 缓存、调度。这是服务系统的知识（可直接迁移至理解 vLLM/SGLang 内部机制）。
2. **在 Air 上学习 qwen3.c**——学习原始前向传播：RMSNorm、RoPE、GQA、SwiGLU 在纯 C 中的实现，没有任何框架隐藏细节。
3. **qwen3.cu**——衔接两者：手写注意力/矩阵乘法内核，这是 CUDA/HIP 层的工作所在。对于在 MI300X 上编写内核也很有帮助（将内核移植到 HIP——主要是机械性工作）。

注意 nanochat 本身提供带有 KV 缓存的最小化 `Engine`，但它仅服务于 nanochat 训练的检查点——不能加载 Qwen 权重，这就是 nano-vllm/qwen3.c 填补这一空白的原因。

**参考文献：**

- [nano-vllm (GitHub, GeeeekExplorer)](https://github.com/GeeeekExplorer/nano-vllm)
- [理解 LLM 推理引擎：深入 Nano-vLLM — Neutree](https://neutree.ai/blog/nano-vllm-part-1)
- [nano-vLLM 架构深度解析 — morphllm](https://www.morphllm.com/nano-vllm)
- [qwen3.c (adriancable)](https://github.com/adriancable/qwen3.c)
- [qwen3.c GGUF 变体 (gigit0000)](https://github.com/gigit0000/qwen3.c)
- [qwen3.cu — 单文件 CUDA C](https://github.com/gigit0000/qwen3.cu)
