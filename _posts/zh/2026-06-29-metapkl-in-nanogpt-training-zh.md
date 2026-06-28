---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanoGPT训练中的meta.pkl
translated: true
type: note
---

**问题：** 在 nanoGPT 训练中，`meta.pkl` 是什么？

**答案：**

`meta.pkl` 是由字符级预处理脚本（例如 `data/shakespeare_char/prepare.py`）生成的词汇表元数据文件。它序列化保存了分词器的映射关系，确保训练和采样使用相同的编码方式。

它包含以下三个部分：

```python
meta = {
    'vocab_size': vocab_size,   # 唯一字符数
    'itos': itos,               # int -> str  (解码)
    'stoi': stoi,               # str -> int  (编码)
}
with open('meta.pkl', 'wb') as f:
    pickle.dump(meta, f)
```

之所以存在这个文件：

1. **`train.py`** 会在数据目录中查找 `meta.pkl`，自动设置 `meta_vocab_size`，以便模型的嵌入层/输出层大小正确：

```python
meta_path = os.path.join(data_dir, 'meta.pkl')
if os.path.exists(meta_path):
    with open(meta_path, 'rb') as f:
        meta = pickle.load(f)
    meta_vocab_size = meta['vocab_size']  # 否则默认使用 GPT-2 的 50304
```

2. **`sample.py`** 会加载该文件，将生成的 token id 解码回文本：

```python
stoi, itos = meta['stoi'], meta['itos']
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])
```

关键点：它**仅针对字符级数据集生成**。GPT-2/BPE 数据集（`openwebtext`、`shakespeare` 词级）会跳过此文件，因为它们使用固定的 tiktoken `gpt2` 编码——此时 `train.py` 回退到 `vocab_size=50304`，`sample.py` 使用 `tiktoken.get_encoding("gpt2")`。

所以：没有 `meta.pkl` = “使用 GPT-2 BPE”；存在 `meta.pkl` = “使用这个自定义字符词汇表”。

**参考：**

- [karpathy/nanoGPT — data/shakespeare_char/prepare.py](https://github.com/karpathy/nanoGPT/blob/master/data/shakespeare_char/prepare.py)
- [karpathy/nanoGPT — train.py](https://github.com/karpathy/nanoGPT/blob/master/train.py)