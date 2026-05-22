---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 映射AI堆栈定位
translated: true
type: note
---

**问题：** 我该如何系统地探索 AI 价值链——从 NVIDIA 到 AMD、开源模型、本地推理、芯片和工具链——然后在 3-6 个月后重新审视，以发现哪些细分领域正在发展以及我该在何处定位自己？将 AI 作为兼顾深度与广度的工具——是这样吗？

**回答：**

是的，完全正确。这正是正确的元策略：*审视全栈，进行实验，让时间揭示哪些投入能产生复利效应。* 以下是一份结构化的 AI 价值链地图，包含了你可以实际运行和衡量的具体内容。

---

## AI 价值链，逐层解析

```
┌─────────────────────────────────────────┐
│           应用层 / 智能体                │  ← 你现在在此构建
├─────────────────────────────────────────┤
│           模型（开放权重）               │  ← Llama, Qwen, Mistral, DeepSeek
├─────────────────────────────────────────┤
│        推理运行时与框架                  │  ← vLLM, llama.cpp, MLX, ROCm
├─────────────────────────────────────────┤
│           训练框架                       │  ← PyTorch, FSDP, Megatron
├─────────────────────────────────────────┤
│           硬件（GPU/NPU）                │  ← NVIDIA H100, AMD MI300X, Apple M2
├─────────────────────────────────────────┤
│         芯片设计与编译器                 │  ← CUDA, ROCm/HIP, Metal, Triton
└─────────────────────────────────────────┘
```

---

## 逐层解析：要运行的内容 + 要关注的内容

### 1. 硬件 —— NVIDIA vs AMD vs Apple

**你三者兼备。** 这很罕见且珍贵。

| 平台 | 你的硬件 | 关键栈 |
|----------|--------------|-----------|
| NVIDIA | AMD Dev Cloud MI300X | ROCm + HIP |
| AMD | RTX 4070（工作站） | CUDA 12.x |
| Apple | M2 Air | Metal + MLX |

**本周运行：**

```bash
# 在 M2 上 —— MLX 是 Apple 对 CUDA 的回应
pip install mlx mlx-lm
python -m mlx_lm.generate --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --prompt "用一段话解释 KV 缓存"

# 在 RTX 4070 上 —— llama.cpp 配合 CUDA
git clone https://github.com/ggml-org/llama.cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j8
./build/bin/llama-cli -m qwen2.5-7b-q4_k_m.gguf -p "KV 缓存解释"

# 在 MI300X 上 —— ROCm 基线
rocm-smi  # 检查设备
pip install torch --index-url https://download.pytorch.org/whl/rocm6.2
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

**需要基准测试的内容：** 每瓦特 tokens/秒，不同量化级别下的 VRAM 余量，首 token 生成时间。

**需要追踪的洞察：** AMD MI300X 拥有 192GB HBM3——这是目前大型模型推理中最大的单一优势。观察 ROCm 软件能否在 6 个月内赶上 CUDA。

---

### 2. 开放模型 —— 真正的颠覆

开放权重生态系统正在将商业模型的领先时间从数年压缩到数月再到数周。

**当前值得运行的模型：**

```
Qwen3-235B (MoE)     —— 阿里巴巴，在许多基准测试中击败 GPT-4o
DeepSeek-R1          —— 推理能力，MIT 许可，可本地运行
Llama-3.3-70B        —— Meta，70B 级别最好的开放密集模型
Gemma-3-27B          —— Google，编码能力强
Mistral Small 3.1    —— 24B，速度快，Apache 2.0 许可
```

**需要运行的实验 —— 模型质量与大小权衡：**

```python
import subprocess, time

models = [
    "qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b"  # 通过 ollama
]
prompt = "使用 numpy 从头实现注意力机制，并添加注释。"

for m in models:
    t0 = time.time()
    result = subprocess.run(
        ["ollama", "run", m, prompt],
        capture_output=True, text=True
    )
    elapsed = time.time() - t0
    print(f"{m}: {elapsed:.1f}s, {len(result.stdout)} chars")
```

**6 个月内关注内容：** Qwen4 / Llama-4 能否在智能体任务上缩小与 Claude/GPT-4.5 的差距？模型大小能否在同等能力下继续缩小？

---

### 3. 推理运行时 —— 不起眼的护城河

这一层被低估了。谁赢得了推理运行时，谁就赢得了开发者市场份额。

| 运行时 | 目标平台 | 关键特性 |
|---------|--------|-------------|
| `llama.cpp` | CPU/GPU 本地 | GGUF 量化，通用 |
| `vLLM` | GPU 服务器 | PagedAttention，高吞吐量 |
| `MLX` | Apple Silicon | 统一内存，M 系列上速度快 |
| `ollama` | 本地开发者体验 | 类似 Docker 的模型用户体验 |
| `SGLang` | 服务化 | 结构化生成，速度快 |
| `TensorRT-LLM` | NVIDIA 生产环境 | 最大性能，仅限 NVIDIA |

**在你的工作站上运行 vLLM：**

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --gpu-memory-utilization 0.85 \
  --max-model-len 8192

# 然后像调用 OpenAI API 一样调用它
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen2.5-7B-Instruct","messages":[{"role":"user","content":"hello"}]}'
```

**要关注的内容：** SGLang 会超越 vLLM 吗？llama.cpp 能否在 Vulkan/Metal 性能上与 CUDA 持平？是否存在能干净地抽象 CUDA 和 ROCm 的运行时？

---

### 4. 训练与微调 —— 你现有的优势

你已经从零开始训练过 GPT-2。下一步：

```bash
# 在你的 RTX 4070 上进行 LoRA 微调（12GB 对于 7B 模型足够了）
pip install unsloth
# Unsloth 使 LoRA 速度快 2 倍，节省 60% 的 VRAM

from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen2.5-7B-Instruct",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16)
```

**要关注的内容：** GRPO（DeepSeek 的 RL 方法）会成为 PPO/DPO 在推理场景下的新标准吗？你能微调一个小模型使其在你特定的银行领域任务上超越大模型吗？

---

### 5. 芯片层 —— 理解而非制造

你不需要设计芯片。但理解计算原语会让你成为更好的机器学习工程师。

**需要内化的关键概念：**

```
FLOPS        → 原始计算能力 (H100: 989 TFLOPS BF16)
内存带宽     → 权重移动速度 (H100: 3.35 TB/s HBM3)
算术强度     → FLOPs / 字节 = 你的操作瓶颈在哪里
Roofline 模型 → 可视化计算受限 vs 内存受限
```

**代码中的快速 roofline 直觉：**

```python
# 你的操作是计算受限还是内存受限？
# 矩阵乘法 A(M,K) @ B(K,N)
M, K, N = 4096, 4096, 4096

flops = 2 * M * K * N          # 乘加操作
bytes = (M*K + K*N + M*N) * 2  # fp16，读取输入 + 写入输出
arithmetic_intensity = flops / bytes

# H100 峰值：计算能力 989 TFLOPS，内存带宽 3350 GB/s
ridge_point = 989e12 / 3350e9  # ~295 FLOPs/字节

print(f"算术强度: {arithmetic_intensity:.1f} FLOPs/字节")
print(f"H100 脊点: {ridge_point:.1f} FLOPs/字节")
print("计算受限" if arithmetic_intensity > ridge_point else "内存受限")
```

**要关注的内容：** Cerebras, Groq (LPU), Tenstorrent——它们中任何一个能大规模解决推理延迟问题吗？AMD 的 MI400 能缩小与 H100 继任者的差距吗？

---

## 你的 3/6 个月复盘框架

设置一个提醒。回来回答这些问题：

```markdown
## AI 价值链快照 — [日期]

### 硬件
- [ ] NVIDIA 在推理与训练中的市场份额：有变化吗？
- [ ] AMD ROCm：现在使用起来没有痛苦了吗？
- [ ] Apple MLX：它是否达到了严肃的模型规模（70B+）？

### 开放模型
- [ ] 现在最好的开放 7B / 70B 模型是什么？
- [ ] 开源模型是否缩小了与 GPT-5/Claude 4 的差距？
- [ ] 是否存在超越 Transformer 的新架构？

### 推理
- [ ] vLLM vs SGLang vs llama.cpp：谁赢得了市场份额？
- [ ] 是否已经存在统一的 CUDA/ROCm/Metal 运行时？

### 训练
- [ ] GRPO 成为新的标准训练方法了吗？
- [ ] 我能微调一个 7B 模型在我的领域击败 GPT-4 吗？

### 芯片
- [ ] Groq / Cerebras：有实际生产部署了吗？
- [ ] TSMC 2nm 良率：谁获得了产能分配？

### 要押注的生态系统细分领域
- [ ] 不起眼的基础设施缺口在哪里？
- [ ] 哪家公司开始购买大家都没想到的东西？
```

---

## 如何定位 —— 战略建议

鉴于你的背景（银行 AI 工程师、智能体构建者、模型训练者）：

**短期（现在–3个月）：** 掌握推理和智能体层。你已经可以构建。重点在于：模型间的路由、为特定任务微调小模型、构建评估体系。

**中期（3–6个月）：** 深入研究 ROCm。如果 AMD MI300X + ROCm 变得可行（一个巨大的"如果"），成为少数几个能同时驾驭 CUDA 和 ROCm 的工程师之一将是一个真正的护城河。目前几乎没人能做到。

**需要关注的长期信号：** 谁赢得了*智能体基础设施*层——任务记忆、多智能体编排、大规模工具使用——下一个平台将在这里出现。你已经通过你的 CLI 智能体在那里构建了。

---

**是的，AI 让你同时具备深入（deep）和博识（broadly knowledgeable）的能力**——这就是复利效应。每一层都为其他层提供信息。理解 roofline 模型让你写出更好的内核，进而让你理解为什么 vLLM 的 PagedAttention 很重要，而这又让你构建出更好的智能体。这是一个良性循环。运行实验，做好笔记，让 6 个月的证据告诉你真正的杠杆作用在哪里。