---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复GPT-2填充词汇不匹配
translated: true
type: note
---

问题：为什么我在加载 GPT-2 124M GGUF 模型时，llama.cpp 会报错“Shape mismatch! Model tensors are 50304 (padded) but vocab is 50257”？如何修复？

回答：

这是经典的 nanoGPT 填充词表问题。你的训练代码为了 GPU 效率将词表从 50257 扩充到 50304，但你的 GGUF 元数据声明的 `vocab_size` 却是 50257（真正的 GPT-2 BPE 分词器计数）。llama.cpp 会交叉检查 `output.weight` / `token_embd.weight` 的行数与分词器词表，发现不匹配后终止。

为什么会出现 50304：GPT-2 的真实词表是 50257。nanoGPT 将其向上取整到最近的 64 的倍数（50304 = 50257 + 47），因为维度能被 64/128 整除的矩阵乘法能完美对齐 Tensor Core 的 tile 边界——这就是 Karpathy 那个“最漂亮的 30% 加速”提交。多出来的 47 行永远不会被分词器产生；它们是死 logits，训练时被压制到近似负无穷（梯度只流经真实 token）。

```python
# nanoGPT model.py —— 这就是 50304 的来源
vocab_size: int = 50304  # GPT-2 的 vocab_size 是 50257，填充到最接近的 64 的倍数
```

携带填充的两个嵌入张量：

- `transformer.wte.weight` → 导出为 `token_embd.weight`，形状 `[50304, 768]`
- `lm_head.weight` → 导出为 `output.weight`，形状 `[50304, 768]`

（如果启用权重绑定，这两个张量是同一个，但你在导出时会将它们分别导出。）

修复方法：在导出时，调用 `write_tensors_to_file()` 之前，将两个张量裁剪为 50257 行。被裁掉的行就是填充——丢弃它们不会造成任何影响。

```python
REAL_VOCAB = 50257

def maybe_truncate_vocab(name, tensor):
    # token_embd / output 的形状是 [vocab, n_embd]；裁剪行维度
    if name in ("token_embd.weight", "output.weight") and tensor.shape[0] > REAL_VOCAB:
        tensor = tensor[:REAL_VOCAB, :].contiguous()
    return tensor

# 在你的 add() 辅助函数中：
def add(name, tensor):
    tensor = maybe_truncate_vocab(name, tensor)
    gw.add_tensor(name, tensor.to(torch.float16).numpy())  # 或者你正在使用的任何数据类型
```

同时确保 GGUF 头部信息一致：

```python
gw.add_uint32("gpt2.vocab_size", REAL_VOCAB)  # 50257，必须与张量行数匹配
# （键前缀与传递给 GGUFWriter 的架构字符串一致）
```

具体到你的代码片段中，需要保护的行是：

```python
add("token_embd.weight", sd["transformer.wte.weight"])  # 在此处裁剪
...
add("output.weight",     sd["lm_head.weight"])           # 以及此处
```

你展示的偏置/归一化张量（如 `output_norm.bias` 等）都是 `[768]` 维——不是词表维度的——所以保持不动。

重新导出后快速验证：

```bash
python -c "from gguf import GGUFReader; r=GGUFReader('sec-edgar-gpt-124m.gguf'); \
print([(t.name, t.shape) for t in r.tensors if 'embd' in t.name or t.name=='output.weight'])"
# 预期结果：[('token_embd.weight', [768, 50257]), ('output.weight', [768, 50257])]
```

注意 GGUFReader 打印的形状是反转的（`[n_embd, vocab]`），与 PyTorch 不同——这只是 ggml 的列优先约定，并非另一个 bug。

如果你不想重新导出，另一种方案是：将 GGUF 元数据中的词表大小改为 50304，并让分词器携带 47 个未使用的 token。这样做可以加载，但并非正确的修复——你的 `tokenizer.json` 只知道 50257 个合并规则，因此 token ID 50257–50303 是不可达的，并且你多输出了 36K 个死参数（50304−50257 × 768 × 2 个张量）。裁剪的方式更干净。
