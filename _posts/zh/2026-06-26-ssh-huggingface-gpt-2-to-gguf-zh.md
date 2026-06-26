---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH HuggingFace GPT-2 转 GGUF
translated: true
type: note
---

**问题：** 解释这条 SSH 单行命令的作用——它将一个 HuggingFace GPT-2 模型转换为 GGUF 格式。

**回答：**

这条命令通过 SSH 在远端 GPU 机器（`root@<IP_ADDRESS>`）上运行一个 Python 脚本，将你微调后的 `sec-edgar-gpt-124m` GPT-2 模型从 HuggingFace 格式转换为单个 `.gguf` 文件，供 `llama.cpp` / `ollama` 推理使用。

逐层解析如下：

**1. 分词器重建**
```python
vocab = td["model"]["vocab"]          # {token_str: id}
nv = len(vocab)
toks = [""] * nv
for s, i in vocab.items(): toks[i] = s   # 反转得到 id 有序列表
for i, c in added.items():               # 覆盖 added_tokens
    if i < nv: toks[i] = c
tb = [t.encode("utf-8") for t in toks]   # token 字节
mb = ["".join([a,b]).encode("utf-8") for a,b in td["model"]["merges"]]  # BPE merges
```
GGUF 将分词器内嵌存储。脚本将 `{token: id}` 映射反转成 id 索引列表，覆盖特殊/新增 token，然后将 token 列表和 BPE 合并对编码为 UTF-8 字节。合并对（merges）让 llama.cpp 能够精确重建 BPE 编码器。

**2. 配置 → GGUF 元数据（KV 对）**
```python
gw.add_context_length(c.n_positions)     # 1024
gw.add_embedding_length(c.n_embd)        # 768
gw.add_block_count(c.n_layer)            # 12
gw.add_head_count(c.n_head)              # 12
gw.add_feed_forward_length(...n_inner... or 4*n_embd)  # 3072
```
标准 GPT-2 124M 超参数被写入 GGUF KV 元数据，供运行时知晓架构形状。BOS/EOS 均设为 `50256`（`<|endoftext|>`），这对 GPT-2 是正确的。

**3. 权重转置——关键细节**

GPT-2 的 HuggingFace 实现使用 `Conv1D` 而非 `nn.Linear`。`Conv1D` 以 `[in, out]` 存储权重，而 llama.cpp 期望线性权重为 `[out, in]`。因此每个投影层都需要 `.T`：
```python
gw.add_tensor("blk.{i}.attn_qkv.weight",  sd[...c_attn.weight].numpy().T)
gw.add_tensor("blk.{i}.attn_output.weight", sd[...c_proj.weight].numpy().T)
gw.add_tensor("blk.{i}.ffn_up.weight",    sd[...mlp.c_fc.weight].numpy().T)
gw.add_tensor("blk.{i}.ffn_down.weight",  sd[...mlp.c_proj.weight].numpy().T)
```
偏置 **不** 转置（一维）。`.T` 后的 `np.ascontiguousarray(...)` 是必要的，因为转置返回非连续视图，而 GGUF 写入器需要连续内存来转储原始字节。

**4. 张量名称重映射**

HF 名称 → GGUF 规范名称：

| HF | GGUF |
|---|---|
| `transformer.wte.weight` | `token_embd.weight` |
| `transformer.wpe.weight` | `position_embd.weight` |
| `h.{i}.ln_1` | `blk.{i}.attn_norm` |
| `h.{i}.attn.c_attn` | `blk.{i}.attn_qkv` |
| `h.{i}.attn.c_proj` | `blk.{i}.attn_output` |
| `h.{i}.mlp.c_fc` | `blk.{i}.ffn_up` |
| `h.{i}.mlp.c_proj` | `blk.{i}.ffn_down` |
| `transformer.ln_f` | `output_norm` |
| `lm_head` | `output` |

**5. 嵌入/头部裁剪**
```python
wte = sd["transformer.wte.weight"].numpy()[:nv]   # 裁剪到真实词汇表大小
lm  = sd["lm_head.weight"].numpy()[:nv].T
```
`[:nv]` 裁剪掉多余的填充行（GPT-2 常将词汇表填充到 64 的倍数以对齐张量核心——50257 → 50304）。它切回真实分词器大小，使嵌入和分词器一致。

**6. 写入顺序**
```python
gw.write_header_to_file()
gw.write_kv_data_to_file()
gw.write_tensors_to_file()
```
GGUF 的布局顺序为：文件头 → KV 元数据 → 张量数据，按此顺序写入。

**需要注意的点：**

- `gw.add_parallel_residual(True)` 对于 GPT-2 是 **错误** 的。GPT-2 使用顺序残差（attn → add → MLP → add），而非并行（GPT-J/NeoX 风格，attn 和 MLP 在同一归一化输入上运行）。这条元数据可能被 llama.cpp 的 GPT-2 路径忽略，但语义上不正确。
- `add_token_scores([0.0]*nv)` —— 没问题，GPT-2 BPE 不使用 unigram 分数。
- 输出为 `f32`（未量化）。之后运行 `llama-quantize sec-edgar-gpt-124m.gguf out-q8.gguf Q8_0` 来压缩大小。

你可以用 llama.cpp 自带的 `python convert_hf_to_gguf.py hf-model/ --outfile sec-edgar-gpt-124m.gguf` 替换整个脚本，它会自动处理 Conv1D 转置和命名——除非你特别想控制分词器重建，否则值得使用。