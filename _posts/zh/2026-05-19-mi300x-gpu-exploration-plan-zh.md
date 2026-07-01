---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X GPU探索计划
translated: true
type: note
---

**问题：** 我现在可以使用一块 AMD MI300X GPU。我想熟悉它——训练、推理、简单和困难的任务、Whisper、几个小时和几天的作业。给我一个经过实战验证的探索计划。

**回答：**

MI300X 是一头猛兽——192 GB HBM3 意味着你可以运行那些连 A100 80GB 都吃不消的模型。与 CUDA 相比，ROCm 栈是主要的摩擦点。下面是一个渐进式计划，从“验证它能否工作”到“训练真正的东西”。

---

## 阶段 0 — 验证 ROCm 栈（30 分钟）

```bash
# 确认 ROCm 识别到 GPU
rocminfo | grep -E "Name|gfx"
rocm-smi

# Python 基础检查
python3 -c "import torch; print(torch.version.hip); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
# 在 ROCm 上，torch.cuda.* 映射到 ROCm — 这是正常行为

# 快速计算测试
python3 -c "
import torch
x = torch.randn(4096, 4096, device='cuda')
y = torch.randn(4096, 4096, device='cuda')
import time; t = time.time()
for _ in range(100): z = x @ y
torch.cuda.synchronize()
print(f'matmul 4096x4096 x100: {time.time()-t:.2f}s')
"
```

---

## 阶段 1 — 推理预热（2–4 小时）

### 1a. Whisper 在 ROCm 上的 Whisper

```bash
pip install openai-whisper
python3 -c "
import whisper, torch
model = whisper.load_model('large-v3', device='cuda')
result = model.transcribe('your_audio.mp3')
print(result['text'])
"
```

如果 Whisper 的 CUDA 内核有问题，可以改用 `faster-whisper` 配合 ROCm 补丁版本，或者先只在 CPU 上运行以验证正确性，再切换到 GPU。

### 1b. 通过 vLLM（ROCm 构建）进行 LLM 推理

```bash
# vLLM 支持 ROCm — 从源码安装或使用它们的 Docker
docker pull rocm/vllm:latest  # 查看 hub.docker.com/r/rocm/vllm

# 或者 pip 安装（ROCm wheel）
pip install vllm  # 确认它识别到 ROCm

# 运行 Llama 3 70B — 192GB 轻松容纳
python3 -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-70B-Instruct \
  --dtype bfloat16 \
  --max-model-len 8192
```

MI300X 可以**舒适地运行 Llama 3 70B bf16**（约 140 GB）。你甚至可以尝试量化后的 405B。

### 1c. Transformers 流水线

```bash
pip install transformers accelerate

python3 -c "
from transformers import pipeline
import torch
pipe = pipeline('text-generation', model='mistralai/Mistral-7B-Instruct-v0.2',
                device='cuda', torch_dtype=torch.bfloat16)
print(pipe('Explain attention mechanism in one paragraph')[0]['generated_text'])
"
```

---

## 阶段 2 — 训练热身（半天）

### 2a. ROCm 上的 nanoGPT（你的舒适区）

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
# 准备数据
python data/shakespeare_char/prepare.py

# 训练 — ROCm torch 在这里直接可用
python train.py config/train_shakespeare_char.py \
  --device=cuda \
  --dtype=bfloat16 \
  --compile=False  # 先禁用 torch.compile，之后再启用

# 启用编译（ROCm 通过 HIP 支持）：
# --compile=True
```

在另一个终端监控 `rocm-smi`——确认利用率达到 >90%。

### 2b. GPT-2 规模（你的 H200 经验适用）

```bash
# 来自 llm.c 或 nanoGPT 的 train_gpt2.py
# MI300X 的 HBM 带宽约为 5.3 TB/s，而 H100 约为 3.35 TB/s
# 你应该会看到更好的内存受限吞吐量
python train.py config/train_gpt2.py \
  --device=cuda \
  --dtype=bfloat16 \
  --batch_size=32 \
  --gradient_accumulation_steps=8
```

---

## 阶段 3 — 真正的多小时作业（1–3 天）

### 3a. 使用 Unsloth 或 TRL 微调（LoRA）

```bash
pip install trl peft datasets

python3 << 'EOF'
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from peft import LoraConfig
import torch

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    torch_dtype=torch.bfloat16,
    device_map="cuda"
)

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj","v_proj"])

args = TrainingArguments(
    output_dir="./lora-output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    bf16=True,
    logging_steps=10,
)

# trainer = SFTTrainer(model=model, args=args, ...)
# trainer.train()
EOF
```

### 3b. 与你的 H100/H200 数据对比

需要记录的关键指标：

- 训练 tokens/sec（MFU — 模型 FLOP 利用率）
- 推理 tokens/秒的推理吞吐量（batch size 为 1、8、32 时）
- 内存带宽利用率（`rocm-smi -d 0 --showrascount` + compute）

```bash
# 简单的 MFU 跟踪器
rocm-smi --showuse --showmemuse -d 0 --json
```

---

## ROCm 特定注意事项

| 问题 | 解决方法 |
| --- | --- |
| `torch.compile` 首次运行慢 | 添加 `TORCH_COMPILE_DEBUG=1`，缓存位于 `/tmp/torchinductor_*` |
| 缺少 CUDA 内核 | 许多库会自动映射；手动：`HIP_VISIBLE_DEVICES=0` |
| Flash Attention | 使用 `flash-attn` 的 ROCm 分支或带 ROCm 的 `xformers` |
| Triton 内核 | ROCm Triton 现已上游——`pip install triton` 即可 |
| `bitsandbytes` 量化 | 使用 `bitsandbytes-rocm` 分支 |

```bash
# ROCm 的 Flash attention
pip install flash-attn  # 检查是否有 ROCm wheel，否则：
# 在 HF 模型中使用 --attn_implementation eager 作为回退
```

---

## 建议的进度时间线

```
第1天上午 — ROCm 验证，Whisper large-v3，Mistral 7B 推理
第1天下午 — nanoGPT Shakespeare，GPT-2 训练GPT-2，监控利用率
第2天     — 用 vLLM 服务 Llama 70B，基准测试吞吐量
第3天     — 在你关心的数据集（代码、金融）上做 LoRA 微调
第4天+    — 多天训练运行、检查点/恢复、wandb 日志记录
```

凭借 192 GB 的容量，你拥有其他单卡在这个规模上无法匹敌的余量。关键在于无需量化即可运行 70B+ 模型——这是你相对于 H100 80GB 配置的独特优势。
