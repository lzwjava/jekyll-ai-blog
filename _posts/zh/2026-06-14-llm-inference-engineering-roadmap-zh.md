---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM推理工程路线图
translated: true
type: note
---

**问题：** 大语言模型推理工程的学习路线图是什么？

**回答：**

## 先建立心智模型

LLM 推理包含两个具有完全不同瓶颈的阶段：

```
预填充：提示词 tokens → 计算 KV 缓存   → 计算密集型（矩阵乘法）
解码：  每次生成一个 token，读取 KV 缓存 → 内存带宽密集型
```

推理优化的所有内容都源于这一洞察。请将其作为你的指引原则。

---

## 第一阶段：从头实现 Transformer 前向传播（第 1-2 周）

你已经训练过 GPT-2 —— 但你能用纯 NumPy 编写推理前向传播吗？这才是考验。

```python
import numpy as np

def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / np.sqrt(d_k)  # [B, H, S, S]
    if mask is not None:
        scores += mask * -1e9
    weights = softmax(scores, axis=-1)
    return weights @ V  # [B, H, S, D]

def transformer_block(x, W_qkv, W_o, W_ff1, W_ff2, W_ln1, W_ln2):
    # LayerNorm → Attention → Residual → LayerNorm → FFN → Residual
    x_norm = layer_norm(x, W_ln1)
    qkv = x_norm @ W_qkv          # [B, S, 3*H*D]
    Q, K, V = np.split(qkv, 3, axis=-1)
    attn_out = attention(Q, K, V) @ W_o
    x = x + attn_out              # residual
    x = x + ffn(layer_norm(x, W_ln2), W_ff1, W_ff2)
    return x
```

**需要牢记的关键形状：**

```
输入:        [B, S, D]          B=批量大小, S=序列长度, D=模型维度
Q/K/V:        [B, H, S, D//H]   H=注意力头数
KV 缓存:     [L, 2, B, H, S, D//H]   L=层数, 2=(K,V)
```

**资源：**

- `nanoGPT/model.py` — Karpathy 最简洁的参考
- Annotated Transformer (Harvard NLP)

---

## 第二阶段：KV 缓存与内存计算（第 2-3 周）

这是推理系统的核心。

```python
# KV 缓存内存计算
def kv_cache_size(model, batch_size, seq_len, dtype_bytes=2):
    layers = model.n_layers          # 例如 32 层 (7B 模型)
    heads = model.n_kv_heads         # GQA: 少于 n_heads
    head_dim = model.d_model // model.n_heads

    # 每个 token: 2 (K+V) * 层数 * 头数 * 头维度 * 数据类型大小
    per_token = 2 * layers * heads * head_dim * dtype_bytes
    total = per_token * batch_size * seq_len
    return total

# Llama-3 8B 示例:
# layers=32, kv_heads=8 (GQA), head_dim=128, bf16
per_token = 2 * 32 * 8 * 128 * 2  # = 131072 bytes = 每个 token 128 KB
# 序列长度 4096, 批量大小=1: 仅 KV 缓存就需要 512 MB
```

**需要深入理解的内容：**

- 为什么解码是内存带宽密集型：每个 token 需要读取整个 KV 缓存一次
- GQA（分组查询注意力）— Llama 2/3 使用，将 KV 缓存减少为 `n_heads/n_kv_heads`
- MLA（多头潜在注意力）— DeepSeek 的方法，将 KV 压缩为潜在向量

---

## 第三阶段：量化（第 3-4 周）

```
FP32 → FP16/BF16 → INT8 → INT4 → 2-bit
        免费        SmoothQuant  GPTQ/AWQ  极致优化
```

```python
# 简单的 INT8 量化
def quantize_weight(W, bits=8):
    scale = W.abs().max() / (2**(bits-1) - 1)
    W_int = (W / scale).round().clamp(-128, 127).to(torch.int8)
    return W_int, scale

def dequantize(W_int, scale):
    return W_int.float() * scale

# GPTQ 核心思想：逐层最小化 ||WX - W_q X||²
# 使用激活的 Hessian 矩阵寻找最优量化顺序
```

**学习路径阶梯：**

1. **GGUF/llama.cpp** — 从这里开始，k-quants (Q4_K_M, Q5_K_S)，易于实验
2. **GPTQ** — 使用校准数据进行逐层量化
3. **AWQ**（激活感知权重量化）— 保护重要的权重
4. **SmoothQuant** — 将量化难度从激活迁移到权重

```bash
# 实践：量化一个模型并测量困惑度
pip install llama-cpp-python
# Q4_K_M vs Q8_0 — 在 wikitext-2 上测量困惑度
python -c "
from llama_cpp import Llama
model = Llama('model-Q4_K_M.gguf', n_ctx=512)
# 基准测试 tokens/sec
"
```

---

## 第四阶段：批处理与调度（第 4-5 周）

```
静态批处理：    等待批处理填满 → GPU 利用率低
动态批处理：    按长度分组 → 较好
连续批处理：    中途添加/移除序列 → vLLM 的核心洞察
```

```python
# 概念性：连续批处理调度器
class Scheduler:
    def __init__(self, max_tokens_in_flight):
        self.running = []   # 正在解码的序列
        self.waiting = []   # 等待预填充的序列
        self.max_tokens = max_tokens_in_flight

    def step(self):
        # 如果 KV 缓存已满则抢占（交换到 CPU 或重新计算）
        self._preempt_if_needed()
        # 如果预算允许则添加新序列
        self._admit_from_waiting()
        # 返回此次前向传播的批次
        return self._build_batch()
```

**阅读以下代码：**

```bash
git clone https://github.com/vllm-project/vllm
cat vllm/core/scheduler.py     # 连续批处理
cat vllm/core/block_manager.py # PagedAttention 内存管理
```

**一句话总结 PagedAttention：** KV 缓存存储在不连续的块中（类似操作系统内存页），通过块表映射——消除碎片，支持跨请求共享提示词的 KV。

---

## 第五阶段：FlashAttention（第 5-6 周）

这是最重要的内核，没有之一。

```
朴素注意力：    O(N²) HBM 读写  (慢)
FlashAttention:     O(N²) FLOPs, O(N) HBM  (快)
```

```
关键技巧：将 QK^T 计算分块为 SRAM 大小的块
           增量计算 softmax（在线 softmax）
           永远不要在 HBM 中实例化完整的 N×N 注意力矩阵
```

```python
# 在线 softmax — FlashAttention 的数学核心
def online_softmax(scores_block, running_max, running_sum):
    new_max = max(running_max, scores_block.max())
    # 重新缩放旧的和
    running_sum = running_sum * exp(running_max - new_max)
    # 添加新块
    running_sum += exp(scores_block - new_max).sum()
    running_max = new_max
    return running_max, running_sum
```

**阅读：** FlashAttention-2 论文 (Dao et al.)，然后看 `flash_attn/flash_attn_triton.py`

---

## 第六阶段：推测解码（第 6-7 周）

```
问题：  解码是顺序的，每次前向传播一个 token → 速度慢
洞察：  小型草稿模型提议 k 个 token，大型模型并行验证

加速比：  如果接受率 α，加速比 ≈ k·α / (1 + 草稿模型成本)
典型值：  在代码/重复文本上加速 2-3 倍
```

```python
def speculative_decode(draft_model, target_model, prompt, k=4):
    draft_tokens = draft_model.generate(prompt, k)  # k 个 token，计算量小
    # 目标模型在 ONE 次前向传播中为所有 k+1 个位置打分
    target_logits = target_model(prompt + draft_tokens)

    accepted = []
    for i, token in enumerate(draft_tokens):
        p_target = softmax(target_logits[i])[token]
        p_draft  = draft_model.probs[i][token]
        # 以概率 min(1, p_target/p_draft) 接受
        if random() < min(1.0, p_target / p_draft):
            accepted.append(token)
        else:
            # 从修正后的分布中重新采样
            accepted.append(sample_corrected(target_logits[i], p_draft))
            break
    return accepted
```

---

## 第七阶段：张量并行与大规模服务（第 7-8 周）

```
张量并行：    将权重矩阵拆分到多个 GPU (Megatron 风格)
流水线并行：  将层拆分到多个 GPU
序列并行：    拆分序列维度 (用于长上下文)
```

```python
# 张量并行：列并行线性层
# W 形状 [D_in, D_out] 拆分为 N 个 GPU → 每个持有 [D_in, D_out/N]
# 每个 GPU 计算部分结果，然后 AllReduce

# 在 vLLM 中：通过 tensor_parallel_size 参数控制
from vllm import LLM
llm = LLM("meta-llama/Llama-3-70b", tensor_parallel_size=4)
```

---

## 你的具体路线图

```
第 1-2 周:   从头编写 GPT-2 前向传播 (不使用 PyTorch)
            逐行阅读 nanoGPT model.py
            手动实现 KV 缓存，验证输出匹配

第 3 周:     llama.cpp 深入探索
            从源码构建，使用不同量化运行
            阅读 ggml-cuda.cu — 理解手写 CUDA 矩阵乘法

第 4 周:     vLLM 内部机制
            scheduler.py + block_manager.py
            在你的 4070 上运行 vLLM，与 llama.cpp 进行吞吐量基准测试

第 5 周:     FlashAttention
            阅读 FA2 论文
            运行 flash_attn Triton 内核，与朴素注意力比较

第 6 周:     SGLang + RadixAttention
            sglang/srt/managers/radix_cache.py
            在重复系统提示词上基准测试前缀缓存效果

第 7 周:     量化实验
            GGUF Q4_K_M vs Q8_0 在 wikitext-2 上的困惑度
            在你的 MI300X 上尝试对 7B 模型使用 AWQ

第 8 周:     推测解码
            从头实现简化版本
            分析时间消耗：预填充 vs 解码
```

---

## 关键论文（按顺序）

| 论文 | 原因 |
|---|---|
| Attention Is All You Need | 基线 |
| FlashAttention-2 (Dao 2023) | 最重要的内核 |
| PagedAttention / vLLM (Kwon 2023) | 内存管理 |
| Continuous Batching (Yu 2022) | 调度 |
| GQA (Ainslie 2023) | 现代 KV 缩减 |
| AWQ (Lin 2023) | 最佳实用量化 |
| Speculative Decoding (Leviathan 2023) | 降低延迟 |
| DeepSeek-V2 MLA | KV 压缩的未来方向 |

---

## 你的独特优势

你拥有 192GB HBM3 的 MI300X。大多数推理研究人员都没有这个条件。利用它来：

- 运行未量化的 70B 模型并分析内存带宽利用率
- 基准测试 ROCm 与 CUDA 内核（vLLM 都支持）
- 实验在消费级 GPU 上放不下的批量大小

这是一个真正的优势。大多数学习推理的人都受限于 GPU 内存——而你却没有。
