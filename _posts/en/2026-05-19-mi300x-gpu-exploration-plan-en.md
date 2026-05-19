---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X GPU Exploration Plan
translated: false
type: note
---

**Question:** I now have access to an AMD MI300X GPU. I want to get familiar with it — training, inference, easy and hard tasks, Whisper, multi-hour and multi-day jobs. Give me a battle-tested exploration plan.

**Answer:**

MI300X is a beast — 192 GB HBM3 means you can fit models that choke even A100 80GB. The ROCm stack is the main friction point vs CUDA. Here's a progressive plan from "verify it works" to "train something real."

---

## Phase 0 — Verify ROCm Stack (30 min)

```bash
# Confirm ROCm sees the GPU
rocminfo | grep -E "Name|gfx"
rocm-smi

# Python sanity check
python3 -c "import torch; print(torch.version.hip); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
# On ROCm, torch.cuda.* maps to ROCm — this is correct behavior

# Quick compute test
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

## Phase 1 — Inference Warm-Up (2–4 hours)

### 1a. Whisper on ROCm

```bash
pip install openai-whisper
python3 -c "
import whisper, torch
model = whisper.load_model('large-v3', device='cuda')
result = model.transcribe('your_audio.mp3')
print(result['text'])
"
```

If Whisper's CUDA kernels have issues, fall back to `faster-whisper` with ROCm-patched builds or just run on CPU first to verify correctness, then GPU.

### 1b. LLM inference via vLLM (ROCm build)

```bash
# vLLM has ROCm support — install from source or use their Docker
docker pull rocm/vllm:latest  # check hub.docker.com/r/rocm/vllm

# Or pip install (ROCm wheel)
pip install vllm  # verify it picks up ROCm

# Run Llama 3 70B — fits easily in 192GB
python3 -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-70B-Instruct \
  --dtype bfloat16 \
  --max-model-len 8192
```

MI300X can run **Llama 3 70B in bf16 comfortably** (~140 GB). You could even try 405B with quantization.

### 1c. Transformers pipeline

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

## Phase 2 — Training Warm-Up (half day)

### 2a. nanoGPT on ROCm (your comfort zone)

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
# prepare data
python data/shakespeare_char/prepare.py

# train — ROCm torch just works here
python train.py config/train_shakespeare_char.py \
  --device=cuda \
  --dtype=bfloat16 \
  --compile=False  # disable torch.compile initially, add later

# with compile (ROCm supports it via HIP):
# --compile=True
```

Watch `rocm-smi` in another terminal — confirm utilization hits >90%.

### 2b. GPT-2 scale (your H200 experience applies)

```bash
# train_gpt2.py from llm.c or nanoGPT
# MI300X has ~5.3 TB/s HBM bandwidth vs H100's ~3.35 TB/s
# You should see better memory-bound throughput
python train.py config/train_gpt2.py \
  --device=cuda \
  --dtype=bfloat16 \
  --batch_size=32 \
  --gradient_accumulation_steps=8
```

---

## Phase 3 — Real Multi-Hour Jobs (1–3 days)

### 3a. Fine-tune with Unsloth or TRL (LoRA)

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

### 3b. Benchmark vs your H100/H200 numbers

Key metrics to log:
- tokens/sec for training (MFU — model FLOP utilization)
- tokens/sec for inference (throughput at batch sizes 1, 8, 32)
- memory bandwidth utilization (`rocm-smi -d 0 --showrascount` + compute)

```bash
# simple MFU tracker
rocm-smi --showuse --showmemuse -d 0 --json
```

---

## ROCm-Specific Gotchas

| Issue | Fix |
|---|---|
| `torch.compile` slow first run | Add `TORCH_COMPILE_DEBUG=1`, cache in `/tmp/torchinductor_*` |
| Missing CUDA kernels | Many libs auto-map; for manual: `HIP_VISIBLE_DEVICES=0` |
| Flash Attention | Use `flash-attn` ROCm fork or `xformers` with ROCm |
| Triton kernels | ROCm Triton is upstream now — `pip install triton` works |
| `bitsandbytes` quantization | Use `bitsandbytes-rocm` fork |

```bash
# Flash attention for ROCm
pip install flash-attn  # check if ROCm wheel available, else:
# use --attn_implementation eager in HF models as fallback
```

---

## Suggested Progression Timeline

```
Day 1 AM  — ROCm verify, Whisper large-v3, Mistral 7B inference
Day 1 PM  — nanoGPT Shakespeare, GPT-2 training run, watch utilization
Day 2     — vLLM serving Llama 70B, benchmark throughput
Day 3     — LoRA fine-tune on a dataset you care about (code, finance)
Day 4+    — Multi-day training run, checkpoint/resume, wandb logging
```

With 192 GB you have headroom nobody else has at this scale on a single card. The unlock is running 70B+ models without quantization — that's your unique advantage over H100 80GB setups.