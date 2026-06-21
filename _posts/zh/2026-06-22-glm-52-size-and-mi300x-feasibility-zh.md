---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GLM-5.2规模与MI300X可行性分析
translated: true
type: note
---

**问题：** GLM-5.2 有多大？如何运行？AMD MI300X 足够吗？

**回答：**

## 模型大小

**753B 参数**，BF16/F32 张量。以 BF16（2 字节/参数）计算，原始权重约为 **~1.5 TB**。不过它是 MoE 模型（类似 DeepSeek），所以每个 token 的激活参数要小得多——但你仍然需要加载所有专家权重。

对于实际部署：

- **BF16 全精度**：~1.5 TB 显存——单张 MI300X 不可行
- **FP8 / INT8 量化**：~750 GB——仍需要多张 GPU
- **INT4 量化（GGUF）**：~380 GB——勉强可用 2× MI300X 或单个节点

## AMD MI300X 可行性

MI300X 拥有 192 GB HBM3。**单卡：对于 BF16 甚至 FP8 都不够。** 你的选择：

| 配置 | 所需显存 | MI300X 是否可行？ |
|---|---|---|
| BF16 全精度 | ~1.5 TB | 需要 8× MI300X |
| FP8 | ~750 GB | 需要 4× MI300X |
| INT4（GGUF） | ~380 GB | 需要 2× MI300X |
| INT4 + 卸载 | ~100–150 GB 活跃 | 单张 MI300X（慢） |

AMD Dev Cloud 通常提供 **1 节点 = 1× MI300X**，除非你申请多 GPU。请检查你是否能获得 4-GPU 或 8-GPU 节点。

## 如何运行

### 选项 1：vLLM（推荐用于 MI300X / ROCm）

```bash
pip install vllm

# 多 GPU 上的 BF16
vllm serve "zai-org/GLM-5.2" \
  --tensor-parallel-size 8 \
  --dtype bfloat16 \
  --max-model-len 32768

# 或者在更少 GPU 上使用 FP8 量化
vllm serve "zai-org/GLM-5.2" \
  --tensor-parallel-size 4 \
  --quantization fp8
```

针对 ROCm 的特定命令：

```bash
pip install vllm --extra-index-url https://download.pytorch.org/whl/rocm6.1
```

### 选项 2：SGLang（同样支持 ROCm）

```bash
pip install sglang

python3 -m sglang.launch_server \
  --model-path "zai-org/GLM-5.2" \
  --tp 4 \
  --host 0.0.0.0 \
  --port 30000
```

SGLang 提供了 [GLM-5.2 cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2)——请参考该文档。

### 选项 3：通过 llama.cpp / KTransformers 进行 INT4 量化（单张 MI300X）

KTransformers v0.5.12+ 支持 GLM-5.2。对于单张 192 GB 显卡并进行卸载：

```bash
# 首先获取 GGUF 量化版本
huggingface-cli download \
  <some-user>/GLM-5.2-GGUF \
  --local-dir ./glm52-gguf

# 或者从源码权重构建
python convert_hf_to_gguf.py zai-org/GLM-5.2 --outtype q4_k_m
```

查看[量化模型](https://huggingface.co/models?other=base_model:quantized:zai-org/GLM-5.2)——有 24 种量化变体可用。

### 通过 API 进行推理

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")

response = client.chat.completions.create(
    model="zai-org/GLM-5.2",
    messages=[{"role": "user", "content": "解释 MoE 路由"}],
    max_tokens=1000,
)
print(response.choices[0].message.content)
```

## 关键架构说明

GLM-5.2 使用了 **IndexShare**——每 4 层稀疏注意力层复用相同的索引器，在 1M 上下文下将每个 token 的 FLOPs 降低了 2.9 倍。它还改进了 MTP（多 token 预测）层以支持推测解码，将接受长度提升了最多 20%。这使得它在长上下文场景下比简单的 MoE 更高效。

## 总结

你的 **单张 MI300X（192 GB）只能通过 KTransformers 进行激进的 CPU 卸载来运行 INT4 量化的 GLM-5.2（~380 GB）**，这会很慢（1–5 tok/s）。要获得实际吞吐量，你需要 **2–4 个 MI300X 节点**——如果你想认真进行基准测试，建议在 AMD Dev Cloud 上申请多 GPU 分配。

**参考资料：**

- [GLM-5.2 HuggingFace](https://huggingface.co/zai-org/GLM-5.2)
- [GLM-5 Technical Report (arxiv 2602.15763)](https://arxiv.org/abs/2602.15763)
- [IndexShare paper (arxiv 2603.12201)](https://arxiv.org/abs/2603.12201)
- [SGLang GLM-5.2 Cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2)
- [KTransformers GLM-5.2 Tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.2-Tutorial.md)
