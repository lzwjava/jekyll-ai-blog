---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA、注意力与Autograd修复
translated: true
type: note
---

以下是我遇到的错误和障碍，以及各自的修复方法：

---

## 障碍与修复

### 1. `flash-attn` 无法安装（CUDA 版本不匹配）

**障碍：** 系统 CUDA 版本为 13.2，但 PyTorch (2.10.0) 编译时使用的是 CUDA 12.8。从源码构建 `flash-attn` 失败，错误信息如下：

```
RuntimeError: The detected CUDA version (13.2) mismatches the version that was used to compile PyTorch (12.8)
```

**修复：** 将 `flash_attn_varlen_func` 和 `flash_attn_with_kvcache` 替换为 PyTorch 原生的 `torch.nn.functional.scaled_dot_product_attention` (SDPA)，该函数在可用时会内部调用 FlashAttention。同时，在 `pyproject.toml` 中将 `flash-attn` 设为可选依赖。

### 2. Triton 段错误（CUDA 版本不匹配）

**障碍：** `store_kvcache` 内核使用了 Triton 3.6.0，同样因驱动/运行时版本不匹配导致 CUDA 兼容性问题，引发了硬段错误（core dump），且没有 Python 回溯信息。

**修复：** 使用纯 PyTorch 索引重写了 `store_kvcache`，不再依赖 Triton：

```python
# 之前：在 CUDA 上启动 Triton 内核
store_kvcache_kernel[(N,)](key, key.stride(0), value, value.stride(0), 
                           k_cache, v_cache, slot_mapping, D)

# 之后：纯 PyTorch，可在任何地方运行
k_cache_flat[slot_mapping[valid]] = key_flat[valid]
v_cache_flat[slot_mapping[valid]] = value_flat[valid]
```

### 3. `@torch.compile` 段错误（原地操作 + inductor）

**障碍：** 有 4 个文件使用了 `@torch.compile` 并指定 `inductor` 后端。编译后的 RMSNorm 包含原地操作（`x.mul_()`、`x.add_()`），触发了以下错误：

```
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation
```

在 `torch.inference_mode()` 下，这导致硬段错误而非正确的错误提示。

**修复：** 移除了所有 `@torch.compile` 装饰器，涉及文件：
- `layernorm.py` (RMSNorm)
- `activation.py` (SiluAndMul)
- `sampler.py` (Sampler)
- `rotary_embedding.py` (RotaryEmbedding)

### 4. KV 缓存写入中的 Autograd 冲突

**障碍：** `store_kvcache` 使用了原地赋值（`k_cache_flat[...] = key_flat[valid]`），而 `key_flat[valid]` 是计算图的一部分，导致：

```
RuntimeError: a leaf Variable that requires grad is being used in an in-place operation
```

**修复：** 将缓存写入操作包裹在 `torch.no_grad()` 中：

```python
with torch.no_grad():
    k_cache_flat[slot_mapping[valid]] = key_flat[valid]
    v_cache_flat[slot_mapping[valid]] = value_flat[valid]
```

### 5. 错误的解码注意力掩码（关键逻辑错误）

**障碍：** 在解码路径中，使用了 `is_causal=True`，但 `q_len=1`、`k_len=N`（N > 1）。PyTorch 的 SDPA 会生成一个因果掩码，其中 **查询位置 0 只能关注到键位置 0**，而非所有 N 个缓存位置。这意味着模型只能看到第一个缓存的 token，导致输出乱码。

```
q: (1 个 token，位于位置 5)
k: (5 个缓存的 token，位于位置 0-4)

is_causal=True 掩码：  # 错误
  查询 0 -> 仅键 0，键 1-4 被遮蔽

预期掩码：            # 正确
  查询 0 -> 键 0-4（所有之前的 token）
```

**修复：** 改为 `is_causal=False` 且不提供注意力掩码，这样单个查询 token 可以关注所有缓存的键位置：

```python
# 之前（错误）：
o = F.scaled_dot_product_attention(q, k, v, is_causal=True)

# 之后（正确）：
o = F.scaled_dot_product_attention(q, k, v, is_causal=False)
```

这种做法是安全的，因为在解码模式下，只有一个查询 token，而所有缓存的 KV 位置都是之前的 token。

---

## 验证

所有修复完成后，模型能够生成连贯的输出：

```
输入:  "introduce yourself"
输出: "Hello! I'm a language model trained on a diverse range of languages..."
```