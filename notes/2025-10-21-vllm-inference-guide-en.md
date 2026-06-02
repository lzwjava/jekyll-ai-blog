---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: 'vLLM: Fast LLM Inference Guide'
translated: false
type: note
---

vLLM is an open-source library designed for fast and memory-efficient inference and serving of large language models (LLMs). Developed initially at the Sky Computing Lab at UC Berkeley, it has grown into a community-driven project with contributions from academia and industry. vLLM addresses key challenges in LLM deployment, such as high latency, memory fragmentation, and low throughput, making it ideal for production environments. It supports seamless integration with Hugging Face models and provides an OpenAI-compatible API for easy adoption.

## Key Features

vLLM stands out for its performance and flexibility:
- **PagedAttention**: Efficiently manages key-value (KV) cache memory to reduce waste and enable higher throughput.
- **Continuous Batching**: Dynamically batches incoming requests without waiting for full batches, improving resource utilization.
- **Optimized Kernels**: Integrates FlashAttention, FlashInfer, and custom CUDA/HIP graphs for faster execution.
- **Quantization Support**: Includes GPTQ, AWQ, INT4/INT8/FP8 for reduced memory footprint.
- **Decoding Algorithms**: Supports parallel sampling, beam search, speculative decoding, and chunked prefill.
- **Distributed Inference**: Tensor, pipeline, data, and expert parallelism for multi-GPU setups.
- **Hardware Compatibility**: NVIDIA GPUs, AMD/Intel CPUs/GPUs, PowerPC CPUs, TPUs, and plugins for Intel Gaudi, IBM Spyre, Huawei Ascend.
- **Additional Tools**: Streaming outputs, prefix caching, multi-LoRA support, and an OpenAI-compatible server.

These features enable vLLM to achieve state-of-the-art serving throughput while being easy to use.

## Prerequisites

- **OS**: Linux (primary support; some features on other platforms).
- **Python**: 3.9 to 3.13.
- **Hardware**: NVIDIA GPUs recommended for full features; CPU-only mode available but slower.
- **Dependencies**: PyTorch (auto-detected via CUDA version), Hugging Face Transformers.

## Installation

vLLM can be installed via pip. Use `uv` (a fast Python environment manager) for optimal setup:

1. Install `uv` following its [documentation](https://docs.astral.sh/uv/getting-started/installation/).
2. Create a virtual environment and install vLLM:

   ```
   uv venv --python 3.12 --seed
   source .venv/bin/activate
   uv pip install vllm --torch-backend=auto
   ```

   - `--torch-backend=auto` auto-selects PyTorch based on your CUDA driver.
   - For specific backends (e.g., CUDA 12.6): `--torch-backend=cu126`.

Alternatively, use `uv run` for one-off commands without a permanent environment:

   ```
   uv run --with vllm vllm --help
   ```

For Conda users:

   ```
   conda create -n myenv python=3.12 -y
   conda activate myenv
   pip install --upgrade uv
   uv pip install vllm --torch-backend=auto
   ```

For non-NVIDIA setups (e.g., AMD/Intel), refer to the [official installation guide](https://docs.vllm.ai/en/stable/getting_started/installation.html) for platform-specific instructions, including CPU-only builds.

Attention backends (FLASH_ATTN, FLASHINFER, XFORMERS) are auto-selected; override with `VLLM_ATTENTION_BACKEND` environment variable if needed. Note: FlashInfer requires manual installation as it's not in pre-built wheels.

## Quick Start

### Offline Batched Inference

Use vLLM for generating text from a list of prompts. Example script (`basic.py`):

```python
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm = LLM(model="facebook/opt-125m")  # Downloads from Hugging Face by default
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

- **Notes**:
  - By default, uses model's `generation_config.json` for sampling params; override with `generation_config="vllm"`.
  - For chat/instruct models, apply chat templates manually or use `llm.chat(messages_list, sampling_params)`.
  - Set `VLLM_USE_MODELSCOPE=True` for ModelScope models.

### Online Serving (OpenAI-Compatible API)

Launch a server with:

```
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

This starts at `http://localhost:8000`. Customize with `--host` and `--port`.

Query via curl (completions endpoint):

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

Or chat completions:

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

Using Python (OpenAI client):

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

Enable API key auth with `--api-key <key>` or `VLLM_API_KEY`.

## Supported Models

vLLM supports a vast array of generative and pooling models via native implementations or Hugging Face Transformers backend. Key categories include:

- **Causal Language Models**: Llama (3.1/3/2), Mistral, Gemma (2/3), Qwen, Phi (3/3.5), Mixtral, Falcon, BLOOM, GPT-NeoX/J/2, DeepSeek (V2/V3), InternLM (2/3), GLM (4/4.5), Command-R, DBRX, Yi, and more.
- **Mixture-of-Experts (MoE)**: Mixtral, DeepSeek-V2/V3 MoE variants, Granite MoE.
- **Multimodal**: LLaVA (1.5/1.6/Next), Phi-3-Vision, Qwen2-VL, InternVL2, CogVLM, Llama-3.2-Vision.
- **Vision-Language**: CLIP, SigLIP (pooling/embedding).
- **Other**: Encoder-decoder (T5, BART), diffusion models (Stable Diffusion), and custom architectures like Jamba, GritLM.

Full support includes LoRA adapters, pipeline parallelism (PP), and V1 engine compatibility for most. For the complete list (over 100 architectures), see the [supported models documentation](https://docs.vllm.ai/en/stable/models/supported_models.html). Custom models can be integrated with minimal changes.

## Deployment Options

### Docker Deployment

Use the official `vllm/vllm-openai` image for easy serving:

```
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HF_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model Qwen/Qwen2.5-1.5B-Instruct
```

- `--ipc=host` or `--shm-size=8g` for shared memory in multi-GPU setups.
- Supports Podman similarly.
- For custom images: Build from source using `docker/Dockerfile` with BuildKit:

  ```
  DOCKER_BUILDKIT=1 docker build . --target vllm-openai --tag vllm/custom --file docker/Dockerfile
  ```

- Arm64/aarch64 builds: Use `--platform linux/arm64` (experimental; requires PyTorch Nightly).
- Add optional deps (e.g., audio) or Transformers from source in a custom Dockerfile.

Other options include Kubernetes, AWS SageMaker, or direct integration with frameworks like Ray Serve.

## Performance Tuning

To optimize throughput and latency:

- **GPU Selection**: Use A100/H100 for high throughput; scale with tensor parallelism (`--tensor-parallel-size`).
- **Batch Size**: Set `--max-num-seqs` and `--max-model-len` based on KV cache; aim for 80-90% GPU utilization.
- **Quantization**: Enable AWQ/GPTQ (`--quantization awq`) to fit larger models.
- **Attention Backend**: Prefer FlashInfer for newer GPUs; test with `VLLM_ATTENTION_BACKEND=FLASHINFER`.
- **Prefill/Decode Balance**: Use `--chunked-prefill-size` for long inputs.
- **Benchmarking**: Run `vllm benchmark` or ShareGPT datasets to measure TTFT (time-to-first-token) and TPOT (time-per-output-token).
- **Best Practices**:
  - Monitor with Prometheus/Grafana.
  - For TPUs: Use JAX backend; tune sharding.
  - Avoid over-parallelism; start with single GPU and scale.

For detailed xPU configs, refer to hardware-specific guides.

## Advanced Usage

- **Distributed Serving**: `--tensor-parallel-size N` for multi-GPU; combine with Ray for clusters.
- **LoRA**: Load adapters with `--lora-modules`.
- **Speculative Decoding**: Integrate with Medusa for 2x speedups.
- **Custom Kernels**: Extend via plugins for new hardware.
- **Monitoring**: Enable `--enable-chunked-prefill` and log metrics.

Explore the [user guide](https://docs.vllm.ai/en/stable/usage/) for engines, engines, and integrations.

## References

- [vLLM Official Documentation](https://docs.vllm.ai/)
- [Quickstart Guide](https://docs.vllm.ai/en/stable/getting_started/quickstart.html)
- [Supported Models](https://docs.vllm.ai/en/stable/models/supported_models.html)
- [Docker Deployment](https://docs.vllm.ai/en/stable/serving/deploying_with_docker.html)
- [vLLM Performance Tuning Guide (Google Cloud)](https://cloud.google.com/blog/topics/developers-practitioners/vllm-performance-tuning-the-ultimate-guide-to-xpu-inference-configuration)
- [Ultimate Guide to vLLM (newline)](https://www.newline.co/@zaoyang/ultimate-guide-to-vllm--aad8b65d)
- [vLLM Tutorial for Beginners](https://www.designveloper.com/blog/vllm-tutorial/)
