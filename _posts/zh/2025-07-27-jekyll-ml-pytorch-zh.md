---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用PyTorch增强Jekyll博客
translated: true
type: note
---

### 使用 PyTorch 为 Jekyll 博客添加机器学习/人工智能功能

由于您正在运行 Jekyll 博客（静态站点生成器），集成推荐或分类等 ML/AI 功能需要一些创意。Jekyll 生成静态 HTML，因此动态元素（例如实时推荐）可能需要客户端 JavaScript 或在构建过程中通过 Jekyll 插件或脚本进行预计算。您提到要避免使用 LLM API 并专注于使用 PyTorch 构建自己的神经网络——这很好，因为这样可以保持所有内容的本地化和可定制性。我将概述一些实用的想法，重点介绍 PyTorch 实现。这些方法假设您可以访问 NumPy 等基本库（用于数据处理），并且能够手动处理文本预处理或使用简单的分词（因为您的设置中没有提到高级 NLP 库如 Hugging Face，但如有需要可以本地添加）。

您可能会创建 Python 脚本（例如在 `scripts/` 目录中），这些脚本在 Jekyll 的构建过程中运行（通过 Makefile 钩子或部署时的 GitHub Actions）。例如，处理 `_posts/` 中的 Markdown 文章，生成 JSON 数据，并通过 Liquid 模板将其注入到您的站点中。

#### 1. 使用 PyTorch 分类器进行文章分类
通过训练一个简单的神经网络分类器，自动对文章进行分类（例如分为“ML”、“笔记”、“Latex”等主题）。这是监督学习：您需要手动标记一部分文章作为训练数据。如果没有标签，可以从无监督聚类开始（见下文）。

**步骤：**
- **数据准备：** 解析 `_posts/` 中的 Markdown 文件。提取文本内容（跳过 frontmatter）。创建数据集：（文本, 标签）对的列表。最初使用 CSV 或列表，包含约 50-100 个带标签的示例。
- **预处理：** 对文本进行分词（基于空格/空白简单分割），构建词汇表，转换为数字索引。使用 one-hot 编码或基本嵌入。
- **模型：** 在 PyTorch 中构建一个基本的全连接神经网络，用于多类分类。
- **训练：** 在本地机器上训练。使用交叉熵损失和 Adam 优化器。
- **集成：** 在构建过程中运行脚本，对所有文章进行分类，生成 `categories.json` 文件，并在 Jekyll 中使用它来标记页面或创建分类索引。

**PyTorch 代码示例（在 `scripts/categorize_posts.py` 等脚本中）：**
```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from collections import Counter

# 步骤 1：加载和预处理数据（简化版）
def load_posts(posts_dir='_posts'):
    texts = []
    labels = []  # 假设手动标签：0=ML, 1=笔记等
    for file in os.listdir(posts_dir):
        if file.endswith('.md'):
            with open(os.path.join(posts_dir, file), 'r') as f:
                content = f.read().split('---')[2].strip()  # 跳过 frontmatter
                texts.append(content)
                # 占位符：从字典或 CSV 加载标签
                labels.append(0)  # 替换为实际标签
    return texts, labels

texts, labels = load_posts()
# 构建词汇表（前 1000 个单词）
all_words = ' '.join(texts).lower().split()
vocab = {word: idx for idx, word in enumerate(Counter(all_words).most_common(1000))}
vocab_size = len(vocab)

# 将文本转换为向量（词袋模型）
def text_to_vec(text):
    vec = np.zeros(vocab_size)
    for word in text.lower().split():
        if word in vocab:
            vec[vocab[word]] += 1
    return vec

X = np.array([text_to_vec(t) for t in texts])
y = torch.tensor(labels, dtype=torch.long)

# 步骤 2：定义模型
class Classifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = Classifier(vocab_size, num_classes=3)  # 调整 num_classes

# 步骤 3：训练
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()
X_tensor = torch.tensor(X, dtype=torch.float32)

for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_tensor)
    loss = loss_fn(outputs, y)
    loss.backward()
    optimizer.step()
    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')

# 步骤 4：对新文章进行分类
def classify_post(text):
    vec = torch.tensor(text_to_vec(text), dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        pred = model(vec).argmax(1).item()
    return pred  # 映射回分类名称

# 保存模型：torch.save(model.state_dict(), 'classifier.pth')
# 在构建脚本中：对所有文章进行分类并写入 JSON
```

**改进：** 为了获得更好的准确性，可以使用词嵌入（在 PyTorch 中训练一个简单的 Embedding 层）或添加更多层。如果未标记，可以切换到聚类（例如，在嵌入上使用 KMeans——见下一节）。在 Makefile 中运行此脚本：`jekyll build && python scripts/categorize_posts.py`。

#### 2. 使用 PyTorch 嵌入构建推荐系统
向读者推荐相似文章（例如，“您可能还喜欢...”）。使用基于内容的推荐：学习每篇文章的嵌入，然后计算相似度（余弦距离）。不需要用户数据——只需文章内容。

**步骤：**
- **数据：** 同上——从文章中提取文本。
- **模型：** 在 PyTorch 中训练一个自编码器，将文本压缩为低维嵌入（例如 64 维向量）。
- **训练：** 最小化重构损失，以学习有意义的表示。
- **推荐：** 对于给定文章，在嵌入空间中找到最近邻。
- **集成：** 在构建过程中预计算嵌入，存储在 JSON 中。在站点上使用 JS 显示推荐（或使用 Liquid 生成静态列表）。

**PyTorch 代码示例（在 `scripts/recommend_posts.py` 中）：**
```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# 复用上面的 load_posts 和 text_to_vec

texts, _ = load_posts()  # 忽略标签
X = np.array([text_to_vec(t) for t in texts])
X_tensor = torch.tensor(X, dtype=torch.float32)

# 自编码器模型
class Autoencoder(nn.Module):
    def __init__(self, input_size, embedding_size=64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, embedding_size)
        )
        self.decoder = nn.Sequential(
            nn.Linear(embedding_size, 256),
            nn.ReLU(),
            nn.Linear(256, input_size)
        )

    def forward(self, x):
        emb = self.encoder(x)
        return self.decoder(emb)

model = Autoencoder(vocab_size)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

for epoch in range(200):
    optimizer.zero_grad()
    reconstructed = model(X_tensor)
    loss = loss_fn(reconstructed, X_tensor)
    loss.backward()
    optimizer.step()
    if epoch % 20 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')

# 获取嵌入
with torch.no_grad():
    embeddings = model.encoder(X_tensor).numpy()

# 推荐：对于文章 i，找到前 3 个相似文章
similarities = cosine_similarity(embeddings)
for i in range(len(texts)):
    rec_indices = similarities[i].argsort()[-4:-1][::-1]  # 前 3 个（排除自身）
    print(f'文章 {i} 的推荐：{rec_indices}')

# 将嵌入保存为 JSON 供 Jekyll 使用
import json
with open('embeddings.json', 'w') as f:
    json.dump({'embeddings': embeddings.tolist(), 'posts': [f'post_{i}' for i in range(len(texts))]}, f)
```

**改进：** 使用变分自编码器以获得更好的嵌入。如果您有用户浏览数据（通过分析），可以在 PyTorch 中添加带有矩阵分解模型的协同过滤。客户端：在 JS 中加载 JSON 并动态计算相似度以实现个性化。

#### 3. 其他 PyTorch 应用思路
- **无监督聚类自动打标签：** 如果标记繁琐，使用嵌入（来自上述自编码器）+ KMeans 聚类将文章分组到主题中。PyTorch 用于嵌入，NumPy/SciPy 用于聚类。
  ```python
  from sklearn.cluster import KMeans
  kmeans = KMeans(n_clusters=5)
  clusters = kmeans.fit_predict(embeddings)
  # 基于聚类分配标签
  ```
  集成：通过脚本在 frontmatter 中生成标签。

- **语义搜索增强：** 类似地嵌入查询和文章，然后使用余弦相似度实现搜索栏。预计算文章嵌入；使用 JS 进行查询嵌入（但由于 PyTorch 是 Python，可以将模型导出为 ONNX，通过 ONNX.js 在 JS 中进行推理，或保持搜索静态）。

- **文章摘要：** 在配对数据（全文, 手动摘要）上训练 seq2seq 模型（PyTorch 中的 RNN/LSTM）。没有大型数据集的情况下具有挑战性，但可以从您的文章开始小规模尝试。用于生成摘要。

**通用提示：**
- **可扩展性：** 对于小型博客，在 CPU 上训练；PyTorch 可以很好地处理。使用 `torch.save` 保存模型并加载进行推理。
- **构建集成：** 添加到 Makefile：`train: python scripts/train_models.py` 然后 `build: jekyll build && python scripts/generate_features.py`。
- **局限性：** 没有高级 NLP（例如 transformers），结果可能较基础——考虑在本地添加 `torchtext` 或手动 GloVe 嵌入。在您的 `ml/` 或 `notes/` 目录上进行测试。
- **部署：** 如果在 GitHub Pages 上，在 CI 中运行脚本。对于动态功能，可以考虑添加轻量级 Flask 后端，但这会偏离静态 Jekyll。

如果您分享更多细节（例如文章数量、主题），我可以进一步优化这些方案！
