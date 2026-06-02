---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GloVe格式与加载指南
translated: true
type: note
---

GloVe向量是纯文本文件。每行包含一个标记及其嵌入值，所有内容以空格分隔。**没有文件头**（与许多word2vec文本文件不同）。

示例（300维GloVe）：

```
the 0.418 0.24968 -0.41242 0.1217 ... 0.34527   # 共300个浮点数
to   0.68047 -0.039263 -0.67412 0.056051 ... -0.067549
U.S. 0.3459  0.21513  -0.09982  0.25344 ... 0.024118
```

若干实用说明：

* 常见发布版本：
  * `glove.6B.{50,100,200,300}d.txt`（维基百科+Gigaword语料；约40万词表，小写形式）
  * `glove.840B.300d.txt`（Common Crawl语料；约220万词表）
  * `glove.twitter.27B.{25,50,100,200}d.txt`（推特数据；含大量标签/表情符号）
* 标记从不包含空格（短语使用下划线连接），因此简单使用`line.split()`即可
* 浮点数为ASCII格式；可见常规小数表示法，有时会出现科学计数法
* 没有特殊的`<unk>`行；未登录词处理需自行实现

您的加载器

```python
def read_glove_vecs(glove_file):
    with open(glove_file, 'r', encoding='utf-8') as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
    return words, word_to_vec_map
```

符合该格式。建议进行两项小优化：

1. 使用float32节省一半内存：

```python
vec = np.asarray(line[1:], dtype=np.float32)
```

2. 跳过意外出现的“文件头”或异常行（某些重新打包的文件会添加）：

```python
parts = line.rstrip().split(' ')
if len(parts) < 2:
    continue
if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
    # 疑似word2vec风格文件头："<词表大小> <维度>"
    continue
word, *vals = parts
```

### 构建词表嵌入矩阵

创建`dictionary: 单词 -> ID`后，将GloVe行映射到`nn.Embedding`的权重矩阵：

```python
def build_embedding_matrix(dictionary, glove_path, dim=300, dtype=np.float32):
    _, glove = read_glove_vecs(glove_path)  # 使用前述方法，但dtype设为float32
    V = len(dictionary)
    W = np.random.uniform(-0.05, 0.05, (V, dim)).astype(dtype)
    for w, idx in dictionary.items():
        vec = glove.get(w)
        if vec is not None and vec.shape[0] == dim:
            W[idx] = vec
    return torch.tensor(W)

# 使用示例
# emb_weight = build_embedding_matrix(dictionary, "glove.6B.300d.txt", dim=300)
# model.in_embeddings.weight.data.copy_(emb_weight)
```

### 与word2vec文本/二进制格式快速对比

* **GloVe文本**：无文件头，格式为`单词 浮点数 浮点数 ...`
* **word2vec文本**：通常以`"<词表大小> <维度>"`文件头开始
* **word2vec二进制**：文件头 + 二进制浮点数

如需使用需要word2vec格式的工具，可通过`gensim.scripts.glove2word2vec`进行转换。
