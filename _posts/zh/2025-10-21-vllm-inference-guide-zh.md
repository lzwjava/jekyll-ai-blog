---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: vLLM：高速大语言模型推理指南
translated: true
type: note
---

vLLM 是一个专为快速、内存高效的大型语言模型推理与服务而设计的开源库。最初由加州大学伯克利分校 Sky Computing 实验室开发，现已发展成为由学术界和工业界共同贡献的社区驱动项目。vLLM 解决了 LLM 部署中的关键挑战，如高延迟、内存碎片化和低吞吐量，使其成为生产环境的理想选择。它支持与 Hugging Face 模型的无缝集成，并提供兼容 OpenAI 的 API 以便快速采用。

## 核心特性

vLLM 以其卓越性能和灵活性脱颖而出：

- **PagedAttention**：高效管理键值缓存内存，减少浪费并实现更高吞吐量
- **连续批处理**：动态批处理传入请求，无需等待完整批次，提升资源利用率
- **优化内核**：集成 FlashAttention、FlashInfer 和自定义 CUDA/HIP 图以实现更快执行
- **量化支持**：支持 GPTQ、AWQ、INT4/INT8/FP8 量化以降低内存占用
- **解码算法**：支持并行采样、束搜索、推测解码和分块预填充
- **分布式推理**：支持张量、流水线、数据和专家并行的多 GPU 配置
- **硬件兼容性**：支持 NVIDIA GPU、AMD/Intel CPU/GPU、PowerPC CPU、TPU，以及 Intel Gaudi、IBM Spyre、华为昇腾的插件
- **附加工具**：流式输出、前缀缓存、多 LoRA 支持和兼容 OpenAI 的服务器

这些特性使 vLLM 在保持易用性的同时，能够实现最先进的服务吞吐量。

## 环境要求

- **操作系统**：Linux（主要支持平台，部分功能支持其他平台）
- **Python**：3.9 至 3.13
- **硬件**：推荐使用 NVIDIA GPU 以获得完整功能；支持 CPU 专用模式但速度较慢
- **依赖项**：PyTorch（通过 CUDA 版本自动检测）、Hugging Face Transformers

## 安装指南

可通过 pip 安装 vLLM。推荐使用 `uv`（快速 Python 环境管理器）进行最优配置：

1. 按照 [uv 文档](https://docs.astral.sh/uv/getting_started/installation/) 安装 `uv`
2. 创建虚拟环境并安装 vLLM：

   ```
   uv venv --python 3.12 --seed
   source .venv/bin/activate
   uv pip install vllm --torch-backend=auto
   ```

   - `--torch-backend=auto` 根据 CUDA 驱动自动选择 PyTorch
   - 特定后端（如 CUDA 12.6）：`--torch-backend=cu126`

也可使用 `uv run` 执行单次命令而无需永久环境：

   ```
   uv run --with vllm vllm --help
   ```

Conda 用户可使用：

   ```
   conda create -n myenv python=3.12 -y
   conda activate myenv
   pip install --upgrade uv
   uv pip install vllm --torch-backend=auto
   ```

非 NVIDIA 环境（如 AMD/Intel）请参考[官方安装指南](https://docs.vllm.ai/en/stable/getting_started/installation.html)获取平台特定说明，包括 CPU 专用构建。

注意力后端会自动选择；如需覆盖可使用 `VLLM_ATTENTION_BACKEND` 环境变量。注意：FlashInfer 需要手动安装，因其未包含在预构建轮中。

## 快速开始

### 离线批量推理

使用 vLLM 从提示词列表生成文本。示例脚本：

```python
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm = LLM(model="facebook/opt-125m")  # 默认从 Hugging Face 下载
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

- **注意事项**：
  - 默认使用模型的 `generation_config.json` 作为采样参数；可通过 `generation_config="vllm"` 覆盖
  - 对于聊天/指令模型，需手动应用聊天模板或使用 `llm.chat(messages_list, sampling_params)`
  - 设置 `VLLM_USE_MODELSCOPE=True` 以使用 ModelScope 模型

### 在线服务（兼容 OpenAI API）

启动服务：

```
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

服务默认运行在 `http://localhost:8000`。可通过 `--host` 和 `--port` 自定义。

通过 curl 查询（补全端点）：

```
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0
    }'
```

或使用聊天补全：

```
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'
```

使用 Python（OpenAI 客户端）：

```python
from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)

completion = client.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct",
    prompt="San Francisco is a"
)
print("Completion result:", completion)
```

通过 `--api-key <key>` 或 `VLLM_API_KEY` 启用 API 密钥认证。

## 支持模型

vLLM 通过原生实现或 Hugging Face Transformers 后端支持大量生成式和池化模型，主要类别包括：

- **因果语言模型**：Llama、Mistral、Gemma、Qwen、Phi、Mixtral、Falcon、BLOOM、GPT 系列、DeepSeek、InternLM、GLM、Command-R、DBRX、Yi 等
- **专家混合模型**：Mixtral、DeepSeek-V2/V3 MoE 变体、Granite MoE
- **多模态模型**：LLaVA、Phi-3-Vision、Qwen2-VL、InternVL2、CogVLM、Llama-3.2-Vision
- **视觉语言模型**：CLIP、SigLIP
- **其他模型**：编码器-解码器架构、扩散模型以及自定义架构

完整支持包括 LoRA 适配器、流水线并行和 V1 引擎兼容性。完整支持列表请参阅[支持模型文档](https://docs.vllm.ai/en/stable/models/supported_models.html)。自定义模型可通过最小改动集成。

## 部署方案

### Docker 部署

使用官方镜像快速部署服务：

```
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HF_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model Qwen/Qwen2.5-1.5B-Instruct
```

- 多 GPU 设置需使用 `--ipc=host` 或 `--shm-size=8g`
- 同样支持 Podman
- 自定义镜像：使用 BuildKit 从源码构建

其他部署选项包括 Kubernetes、AWS SageMaker 或直接与 Ray Serve 等框架集成。

## 性能调优

优化吞吐量和延迟的建议：

- **GPU 选择**：使用 A100/H100 获得高吞吐量；通过张量并行扩展
- **批处理大小**：基于 KV 缓存设置参数，目标 GPU 利用率达 80-90%
- **量化**：启用 AWQ/GPTQ 以运行更大模型
- **注意力后端**：新款 GPU 优先使用 FlashInfer
- **预填充/解码平衡**：长输入使用分块预填充
- **基准测试**：运行性能基准测试测量关键指标
- **最佳实践**：
  - 使用监控工具实时观测
  - 避免过度并行化
  - 参考硬件特定调优指南

## 进阶使用

- **分布式服务**：多 GPU 张量并行与集群部署
- **LoRA 适配器**：动态加载微调模块
- **推测解码**：集成加速方案提升推理速度
- **自定义内核**：通过插件扩展新硬件支持
- **监控指标**：启用高级功能并记录运行数据

详细使用指南请参阅[用户文档](https://docs.vllm.ai/en/stable/usage/)。

## 参考资源

- [vLLM 官方文档](https://docs.vllm.ai/)
- [快速入门指南](https://docs.vllm.ai/en/stable/getting_started/quickstart.html)
- [支持模型列表](https://docs.vllm.ai/en/stable/models/supported_models.html)
- [Docker 部署指南](https://docs.vllm.ai/en/stable/serving/deploying_with_docker.html)
- [性能调优终极指南](https://cloud.google.com/blog/topics/developers-practitioners/vllm-performance-tuning-the-ultimate-guide-to-xpu-inference-configuration)
- [vLLM 完整指南](https://www.newline.co/@zaoyang/ultimate-guide-to-vllm--aad8b65d)
- [vLLM 初学者教程](https://www.designveloper.com/blog/vllm-tutorial/)
