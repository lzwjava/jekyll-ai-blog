---
audio: false
generated: true
lang: zh
layout: post
title: 使用Gensim的Word2Vec脚本
translated: true
type: note
---

为您提供关于 Word2Vec 的 Python 脚本，我需要先做一些假设，因为"关于 Word2Vec 的脚本"这个范围很广。我将提供两种常见场景：

1. **使用 `gensim` 进行训练和基础用法的简单脚本**：这是在 Python 中使用 Word2Vec 最常见且最实用的方式。
2. **从零开始的基本概念性实现**：这更多是为了理解核心算法，但由于复杂性和优化问题，在实际应用中不太实用。

根据您的要求，我将优先介绍 `gensim` 方法，因为这是大多数人会使用的方式。

-----

### 使用 `gensim` 的 Word2Vec Python 脚本

此脚本将演示：

* 准备示例文本数据。
* 训练 Word2Vec 模型。
* 查找最相似的词。
* 执行词汇类比。
* 保存和加载模型。

**前提条件：**

您需要安装 `gensim` 库：

```bash
pip install gensim
```

**Python 脚本 (`word2vec_gensim_example.py`):**

```python
import gensim
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import logging

# 配置日志记录以查看训练进度
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# --- 1. 准备示例文本数据 ---
# 在实际场景中，您需要从文件加载文本数据。
# 这里，我们使用一个简单的句子列表。
raw_sentences = [
    "I love natural language processing.",
    "Word embeddings are a fascinating topic.",
    "Machine learning revolutionizes many industries.",
    "Deep learning is a subset of machine learning.",
    "Natural language processing uses various techniques.",
    "Computers understand human language better with word vectors.",
    "The quick brown fox jumps over the lazy dog.",
    "Dog and cat are common pets.",
    "King is to Queen as Man is to Woman."
]

# 预处理句子：分词并转换为小写
# gensim 的 simple_preprocess 对此非常方便
tokenized_sentences = [simple_preprocess(sentence) for sentence in raw_sentences]

print("\n--- 分词后的句子 ---")
for sentence in tokenized_sentences:
    print(sentence)

# --- 2. 训练 Word2Vec 模型 ---
# 参数解释：
#   vector_size: 词向量的维度。
#   window: 当前词与预测词在一个句子中的最大距离。
#   min_count: 忽略总频率低于此值的所有单词。
#   sg: 训练算法：0 表示 CBOW，1 表示 Skip-gram。对于罕见词，Skip-gram 通常效果更好。
#   workers: 使用这些数量的工作线程来训练模型（=训练更快）。
#   epochs: 对语料库的迭代次数。
model = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=100,      # 示例：100 维向量
    window=5,             # 上下文窗口为两侧各 5 个词
    min_count=1,          # 包含所有单词（针对此小示例）
    sg=1,                 # 使用 Skip-gram (sg=1)
    workers=4,            # 使用 4 个 CPU 核心进行训练
    epochs=10             # 训练 10 个周期
)

print("\n--- 模型训练完成 ---")

# --- 3. 探索模型 ---

# 获取特定词的向量
try:
    word_vector = model.wv['machine']
    print(f"\n'machine' 的向量（前 10 维）: {word_vector[:10]}")
    print(f"'machine' 的向量形状: {word_vector.shape}")
except KeyError:
    print("\n词汇表中未找到 'machine'。")

# 查找最相似的词
print("\n--- 与 'machine' 最相似的词 ---")
try:
    similar_words = model.wv.most_similar('machine')
    for word, similarity in similar_words:
        print(f"{word}: {similarity:.4f}")
except KeyError:
    print("\n词汇表中未找到 'machine'。")

print("\n--- 与 'dog' 最相似的词 ---")
try:
    similar_words_dog = model.wv.most_similar('dog')
    for word, similarity in similar_words_dog:
        print(f"{word}: {similarity:.4f}")
except KeyError:
    print("\n词汇表中未找到 'dog'。")


# 执行词汇类比（例如，King - Man + Woman = Queen）
# 对于非常小的数据集，这可能无法完美工作，但演示了这个概念。
print("\n--- 词汇类比 (King - Man + Woman = ?) ---")
try:
    result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)
    if result:
        print(f"King - Man + Woman 类似于: {result[0][0]} (相似度: {result[0][1]:.4f})")
    else:
        print("类比无结果。词汇量可能太小。")
except KeyError as e:
    print(f"类比所需的一个或多个词未在词汇表中找到: {e}")
except Exception as e:
    print(f"执行类比时发生错误: {e}")

# 检查两个词之间的相似度
print("\n--- 'machine' 和 'learning' 之间的相似度 ---")
try:
    similarity = model.wv.similarity('machine', 'learning')
    print(f"相似度: {similarity:.4f}")
except KeyError:
    print("一个或两个词未在词汇表中找到。")

print("\n--- 'dog' 和 'cat' 之间的相似度 ---")
try:
    similarity_pets = model.wv.similarity('dog', 'cat')
    print(f"相似度: {similarity_pets:.4f}")
except KeyError:
    print("一个或两个词未在词汇表中找到。")

print("\n--- 'dog' 和 'computer' 之间的相似度 ---")
try:
    similarity_diff = model.wv.similarity('dog', 'computer')
    print(f"相似度: {similarity_diff:.4f}")
except KeyError:
    print("一个或两个词未在词汇表中找到。")

# --- 4. 保存和加载模型 ---
model_path = "word2vec_model.bin"
model.save(model_path)
print(f"\n模型已保存至 {model_path}")

# 加载回模型
loaded_model = Word2Vec.load(model_path)
print(f"模型已从 {model_path} 加载")

# 验证加载的模型
print("\n--- 验证加载的模型（使用加载模型查找与 'machine' 最相似的词） ---")
try:
    similar_words_loaded = loaded_model.wv.most_similar('machine')
    for word, similarity in similar_words_loaded:
        print(f"{word}: {similarity:.4f}")
except KeyError:
    print("\n在加载模型的词汇表中未找到 'machine'。")

print("\n脚本执行完成。")
```

**如何运行脚本：**

1. 将上面的代码保存为 Python 文件（例如，`word2vec_gensim_example.py`）。
2. 打开您的终端或命令提示符。
3. 导航到保存文件的目录。
4. 使用以下命令运行脚本：`python word2vec_gensim_example.py`

-----

### Word2Vec (`gensim` 实现) 中的关键概念

* **`gensim.models.Word2Vec`**：用于训练的主类。
* **`sentences`**：一个可迭代对象的可迭代对象，外层可迭代对象是语料库，内层可迭代对象是词列表（分词后的句子）。
* **`vector_size`**：词向量的维度数。更高的维度可以捕捉更多细微差别，但需要更多数据和计算。
* **`window`**：当前词与其在句子中周围词之间的最大距离。
* **`min_count`**：出现次数少于 `min_count` 的词将被忽略。这有助于过滤掉可能没有有意义嵌入的非常罕见的词。
* **`sg` (Skip-gram vs. CBOW)**：
  * `sg=0` (CBOW - 连续词袋模型)：根据上下文预测当前词。训练速度更快。
  * `sg=1` (Skip-gram)：给定当前词预测周围的词。通常对罕见词表现更好。
* **`workers`**：用于训练的 CPU 核心数，可加速过程。
* **`epochs`**：算法在整个数据集上迭代的次数。更多的周期可以带来更高质量的嵌入，但也需要更长时间。
* **`model.wv`**："词向量"对象 (`KeyedVectors`)，包含训练好的词嵌入以及 `most_similar`、`similarity` 等方法。您也可以像 `model.wv['word']` 这样直接访问向量。

-----

这个 `gensim` 脚本为使用 Word2Vec 提供了坚实的基础。对于实际应用，您通常会使用更大的语料库（例如，维基百科、Common Crawl）并调整超参数以获得最佳性能。
