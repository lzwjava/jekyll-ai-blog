---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在H200或MI300X上运行DeepSeek-V3
translated: true
type: note
---

**问题：** 如果我们有 H200 或 AMD MI300X，能否在其上运行完整的 DeepSeek-V3/V4（671B）模型？

**回答：**

## 在 H200 或 AMD MI300X 上运行 DeepSeek-V3/V4

先算清楚内存需求，再讨论部署方案。

---

## 内存计算

### DeepSeek-V3（671B 参数，最新开源权重模型）

| 精度 | 所需显存 | 备注 |
|-----------|------------|-------|
| FP8 | ~380 GB | 推理推荐 |
| BF16 | ~1.34 TB | 单节点显存远超 |
| INT4（GPTQ/AWQ） | ~190 GB | 有损但可行 |

### 你的硬件

| GPU | 显存 | 备注 |
|-----|------|-------|
| H200 SXM（单卡） | 141 GB HBM3e | 单卡不够 |
| H200 SXM（2 卡） | 282 GB | FP8 勉强够，需 offload |
| **AMD MI300X（单卡）** | **192 GB HBM3** | **单 GPU 最佳选择——FP8 勉强能装** |
| MI300X（2 卡） | 384 GB | FP8 充裕，BF16 可能可行 |

**MI300X 192GB 实际上是单卡 FP8 运行 DeepSeek-V3 的最佳选择。**

---

## 选项 1：AMD MI300X —— 完整 DeepSeek-V3 模型（FP8）

DeepSeek 官方支持此配置，其仓库正是针对此场景。

### 部署（ROCm 路径）

```bash
# 在你的 AMD Dev Cloud 实例上（$2/小时 — MI300X 节点约 $3-4/小时）
# 检查硬件
rocm-smi
rocminfo | grep "gfx"  # MI300X 应为 gfx942

# 克隆 DeepSeek-V3 推理仓库
git clone https://github.com/deepseek-ai/DeepSeek-V3.git
cd DeepSeek-V3/inference

# 安装依赖（ROCm 兼容）
pip install torch --index-url https://download.pytorch.org/whl/rocm6.1
pip install transformers accelerate safetensors
pip install flashinfer  # 可能需要 ROCm 版本

# 下载模型（FP8 检查点 ~380GB）
# 从 HuggingFace —— 需要 HF_TOKEN
pip install huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='deepseek-ai/DeepSeek-V3',
    local_dir='/mnt/data/deepseek-v3',
    ignore_patterns=['*.pt'],  # 优先使用 safetensors
)
"
```

### 运行推理（单 MI300X，FP8）

```bash
# 使用官方推理脚本
cd DeepSeek-V3/inference

python generate.py \
    --ckpt-path /mnt/data/deepseek-v3 \
    --config configs/config_671B.json \
    --interactive \
    --max-new-tokens 512 \
    --temperature 0.7
```

### vLLM 路径（推荐用于服务）

```bash
# vLLM 从 v0.4+ 开始原生支持 MI300X
pip install vllm

vllm serve deepseek-ai/DeepSeek-V3 \
    --dtype fp8 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.92 \
    --tensor-parallel-size 1  # 单 MI300X
```

---

## 选项 2：H200 —— 多 GPU 部署

单张 H200（141GB）无法装下 FP8 的 V3（需要 ~380GB），需要张量并行。

### 2 卡 H200 = 282GB —— 勉强可行

```bash
# 使用 vLLM 并启用张量并行
vllm serve deepseek-ai/DeepSeek-V3 \
    --dtype fp8 \
    --tensor-parallel-size 2 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.90

# 或使用原生推理（fp8, tp=2）
python generate.py \
    --ckpt-path /mnt/data/deepseek-v3 \
    --tp 2 \
    --dtype fp8 \
    --interactive
```

### 4 卡 H200 = 564GB —— 充裕，可运行 BF16 MoE 层

```bash
vllm serve deepseek-ai/DeepSeek-V3 \
    --dtype bfloat16 \
    --tensor-parallel-size 4 \
    --max-model-len 32768  # 完整上下文可用
```

---

## 选项 3：SGLang（DeepSeek MLA 架构最佳选择）

SGLang 针对 DeepSeek 的 **MLA（多头潜在注意力）** 进行了专门优化——这种 KV 缓存压缩技巧使 V3/V4 内存效率极高。对于此架构，SGLang 优于 vLLM。

```bash
pip install sglang[all]

# 单 MI300X
python -m sglang.launch_server \
    --model-path deepseek-ai/DeepSeek-V3 \
    --tp 1 \
    --dtype fp8 \
    --port 30000 \
    --mem-fraction-static 0.88 \
    --enable-mla  # MLA 专用 KV 缓存优化

# 客户端
python -c "
import sglang as sgl

@sgl.function
def pipeline(s, prompt):
    s += sgl.user(prompt)
    s += sgl.assistant(sgl.gen('response', max_new_tokens=512))

sgl.set_default_backend(sgl.RuntimeEndpoint('http://localhost:30000'))
state = pipeline.run(prompt='Explain transformer attention from scratch')
print(state['response'])
"
```

---

## 架构提醒：为何 MLA 在这些 GPU 上很重要

DeepSeek-V3 使用 **多头潜在注意力**——它将 key/value 投影到低秩潜在空间，从而压缩 KV 缓存：

```
标准 MHA KV 缓存：2 × n_heads × d_head × seq_len × 字节
MLA KV 缓存：      d_c × seq_len × 字节   # d_c << n_heads × d_head
```

对于 V3：`d_c = 512` 对比 `n_heads × d_head = 128 × 128 = 16384` —— 即 **32 倍 KV 缓存缩减**。这就是为什么 V3 能在 MI300X 上服务长上下文，而在同等显存的标准 MHA 模型上会 OOM。

---

## 针对你配置的建议

| 目标 | 最佳选择 |
|------|------------|
| 快速实验，单 GPU | **MI300X + SGLang + FP8** |
| 生产服务 | **2 卡 MI300X + SGLang TP=2** |
| 有 H200 可用 | **4 卡 H200 + vLLM TP=4 + FP8** |
| 预算敏感 | **1 卡 MI300X，$2-4/小时，仅 FP8** |

**你的 AMD Dev Cloud MI300X 正是合适的机器。** 单节点、单 GPU、FP8——DeepSeek-V3 能装下（勉强，~92% 利用率），而 SGLang 的 MLA 优化可提供不错的吞吐量。从这里开始。

---

## 参考资料

- [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/DeepSeek-V3)
- [SGLang MLA 优化](https://github.com/sgl-project/sglang)
- [vLLM AMD ROCm 支持](https://docs.vllm.ai/en/latest/getting_started/amd-installation.html)
- [DeepSeek-V3 技术报告](https://arxiv.org/abs/2412.19437)
