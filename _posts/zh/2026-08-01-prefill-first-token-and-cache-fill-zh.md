---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 首个令牌与缓存填充
translated: true
type: note
---

是的，你基本说对了——但让我精确一点，因为此文件中的“prefill”指的是**请求处理的一个阶段**，而填充 KV 缓存只是它工作的一部分。

## 这里的 prefill 是什么

在 LLM 服务中，一个请求会经历两个阶段：

**1. Prefill** (`context.is_prefill` → `_prefill_forward`)

- **一次性处理整个提示**（所有 token 并行）
- 为每个提示 token 计算 K/V，并通过 `store_kvcache(k, v, k_cache, v_cache, context.slot_mapping)` **将其存入 KV 缓存**——这就是你提到的“填充缓存”
- 同时**对整个提示运行注意力机制**（`_flash_attention` 且 `causal=True`），以生成**第一个输出 token**

**2. Decode** (`_decode_forward`)

- 每次生成一个 token
- 仅计算*新* token 的 K/V，将其存入缓存
- 然后从缓存中**读取所有之前的 K/V**（`_gather_kv_from_cache`），这样新 token 就能关注提示已经说过的一切——而**无需重新计算**提示的 K/V

## 关键代码行

```python
# forward():
if has_cache and context.slot_mapping is not None:
    store_kvcache(k, v, k_cache, v_cache, context.slot_mapping)  # ← 填充缓存

if context.is_prefill:
    return self._prefill_forward(...)   # 提示一次性处理 → 第一个 token
else:
    return self._decode_forward(...)    # 1 个新 token，关注已缓存的 K/V
```

## 所以，你的直觉修正后如下

- ✅ **是的**：prefill 将提示的 K/V 写入分页 KV 缓存（`store_kvcache`），这样 decode 步骤可以在后续重用它们而无需重新计算。
- ⚠️ **但是**：prefill 不仅仅是填充缓存。它是消耗整个提示并产生第一个 token 的阶段。缓存填充是一个副作用，使得所有后续（decode）步骤变得廉价。

此文件中的一个有趣细节：还支持**前缀缓存**——在 `_prefill_forward` 中，当 `block_tables` 已设置且缓存中已有内容（`_gather_kv_from_cache`）时，新请求可以重用之前见过的前缀的缓存 K/V，而无需重新计算。在这种情况下，prefill 仅计算*新*后缀 token 的 K/V，并对收集到的缓存前缀进行注意力计算。
