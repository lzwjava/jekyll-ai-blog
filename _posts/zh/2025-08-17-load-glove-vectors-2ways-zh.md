---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 加载GloVe向量的两种方法
translated: true
type: note
---

获取像 `the`、`to`、`U.S.` 这类词的 GloVe 向量，以及处理自定义文本，你有两种简便方法：

---

## 方案 A — 下载 Stanford GloVe 并用 `gensim` 查询

这是最常用的方式，下载后即可完全离线使用。

```python
# 1) 下载和解压（首次运行）
import os, zipfile, urllib.request
url = "https://nlp.stanford.edu/data/glove.6B.zip"
zip_path = "glove.6B.zip"
if not os.path.exists(zip_path):
    urllib.request.urlretrieve(url, zip_path)
with zipfile.ZipFile(zip_path) as zf:
    zf.extract("glove.6B.300d.txt")  # 300维版本

# 2) 转换 GloVe 格式 -> word2vec 文本格式并加载
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

glove_path = "glove.6B.300d.txt"
w2v_path   = "glove.6B.300d.w2v.txt"
if not os.path.exists(w2v_path):
    glove2word2vec(glove_path, w2v_path)

vectors = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
print(vectors.vector_size)  # 300

# 3) 单词查询
print(vectors['the'][:5])   # 前5个维度
print(vectors['to'][:5])

# 注意：glove.6B 词表已转为小写
# 'U.S.' -> 'u.s.'（如果存在）。更安全做法：将标记转为小写
print(vectors['u.s.'][:5])
```

现在嵌入你的自定义文本：

```python
import re, numpy as np

# 保留 u.s. 等标记中句点的简单分词器
TOKEN_RE = re.compile(r"[A-Za-z0-9\.\-']+")

def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())

def embed_tokens(tokens, kv: KeyedVectors):
    vecs = [kv[w] for w in tokens if w in kv.key_to_index]
    return np.stack(vecs) if vecs else np.zeros((0, kv.vector_size))

def embed_sentence_avg(text: str, kv: KeyedVectors):
    V = embed_tokens(tokenize(text), kv)
    return V.mean(axis=0) if V.size else np.zeros(kv.vector_size)

# 示例
print(embed_sentence_avg("The quick brown fox jumps over the lazy dog.", vectors)[:10])
print(embed_tokens(tokenize("U.S. interest rates rose today."), vectors).shape)  # (标记数, 300)
```

**提示**

* `glove.6B.300d.txt` 内存占用约 1.1 GB。如果负担过重，可改用 `100d` 版本
* 6B 数据集为**小写格式**；请始终将文本转为小写，若需更广覆盖范围可使用更大的 **840B** 数据集（实际仍主要为小写）
* 未登录词（OOV）将返回空值；可跳过此类词或采用子词回退策略

---

## 方案 B — 使用 `torchtext` 自动下载并提供 GloVe

此方案无需手动下载和转换。

```python
import torch
from torchtext.vocab import GloVe
import re

glove = GloVe(name="6B", dim=300)  # 自动下载到 ~/.vector_cache
stoi = glove.stoi    # 单词 -> 索引
vecs = glove.vectors # 张量 [词表大小, 300]

def get_word_vec(word: str):
    idx = stoi.get(word.lower())
    return vecs[idx] if idx is not None else None

print(get_word_vec("the")[:5])
print(get_word_vec("to")[:5])
print(get_word_vec("U.S.")[:5])     # 多数构建中返回 None；尝试 "u.s."：
print(get_word_vec("u.s.")[:5])

# 句子嵌入（平均法）
TOKEN_RE = re.compile(r"[A-Za-z0-9\.\-']+")
def embed_sentence_avg(text: str):
    toks = TOKEN_RE.findall(text.lower())
    xs = [get_word_vec(t) for t in toks]
    xs = [x for x in xs if x is not None]
    return torch.stack(xs, dim=0).mean(0) if xs else torch.zeros(glove.dim)

print(embed_sentence_avg("The quick brown fox...")[:10])
```

---

## 关于特定行的说明

你提到的那些行：

```
the  0.418 0.24968 -0.41242 0.1217 ... 0.34527  # 共300个浮点数
to   0.68047 -0.039263 -0.67412 0.056051 ... -0.067549
U.S. 0.3459  0.21513  -0.09982 0.25344 ... 0.024118
```

正是纯文本 `.txt` 文件中的格式：每行包含一个`标记`及后续的`300个浮点数`。使用 `gensim` 或 `torchtext` 时无需手动解析——它们会直接处理并提供向量查询接口。

---

## 常见问题（及解决方案）

* **“KeyError: ‘U.S.’”** → 使用 `u.s.`（针对6B数据集），或选择覆盖更广的大数据集，查询前务必转为小写
* **内存/时间占用过高** → 使用 `100d` 或 `200d` 替代 `300d`，或通过扫描文件构建精简词表
* **句子/文档向量** → 对词向量取平均或求和；加权平均可尝试 TF-IDF 权重

如需进一步协助，请告知你的具体文本处理目标（分类、相似度计算、聚类等），我将为你绘制基于 GloVe 的端到端最小化流程草图。
