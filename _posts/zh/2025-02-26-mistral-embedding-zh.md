---
audio: false
generated: true
lang: zh
layout: post
title: Mistral AI嵌入技术
translated: true
type: note
---

要使用 Mistral AI 提供嵌入示例，您可以利用其嵌入 API 生成能捕捉语义的文本数值表示（嵌入）。这些嵌入可用于相似性检测、聚类、分类或搜索等任务。下面我将演示如何为一组句子生成嵌入，并使用 Mistral AI 嵌入端点计算它们的相似度。本示例基于所提供代码的结构，但根据文档专门针对嵌入功能进行了调整：[Mistral AI 嵌入](https://docs.mistral.ai/capabilities/embeddings/)。

### 准备工作

运行示例前请确保：

1. **API 密钥**：有效的 Mistral AI API 密钥已存储在 `MISTRAL_API_KEY` 环境变量中
2. **依赖项**：已安装所需的 Python 包。可通过以下命令安装：

   ```bash
   pip install requests numpy
   ```

### 示例代码

以下是完整的 Python 脚本，可为三个句子生成嵌入并计算它们的成对相似度：

```python
import os
import requests
import numpy as np

def call_mistral_embeddings_api(texts, model="mistral-embed"):
    """
    调用 Mistral AI 嵌入 API 为文本列表生成嵌入向量

    参数：
        texts (list): 要嵌入的字符串列表
        model (str): 使用的嵌入模型（默认为 "mistral-embed"）

    返回：
        list: 嵌入向量列表，如果请求失败则返回 None
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("错误：未设置 MISTRAL_API_KEY 环境变量")
        return None

    url = "https://api.mistral.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "input": texts
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if response_json and "data" in response_json:
            embeddings = [item["embedding"] for item in response_json["data"]]
            return embeddings
        else:
            print(f"Mistral 嵌入 API 错误：无效的响应格式：{response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral 嵌入 API 错误：{e}")
        if e.response:
            print(f"响应状态码：{e.response.status_code}")
            print(f"响应内容：{e.response.text}")
        return None

def calculate_similarity(emb1, emb2):
    """
    使用点积计算两个嵌入向量之间的相似度

    参数：
        emb1 (list): 第一个嵌入向量
        emb2 (list): 第二个嵌入向量

    返回：
        float: 相似度得分（点积，对于归一化向量等同于余弦相似度）
    """
    return np.dot(emb1, emb2)

if __name__ == "__main__":
    # 要嵌入的示例文本
    texts = [
        "I love programming in Python.",
        "Python is a great programming language.",
        "The weather is sunny today."
    ]

    # 生成嵌入向量
    embeddings = call_mistral_embeddings_api(texts)
    if embeddings:
        # 打印嵌入维度
        print(f"嵌入维度：{len(embeddings[0])}")

        # 计算成对相似度
        sim_12 = calculate_similarity(embeddings[0], embeddings[1])
        sim_13 = calculate_similarity(embeddings[0], embeddings[2])
        sim_23 = calculate_similarity(embeddings[1], embeddings[2])

        # 显示结果
        print(f"\n相似度结果：")
        print(f"文本 1：'{texts[0]}'")
        print(f"文本 2：'{texts[1]}'")
        print(f"文本 3：'{texts[2]}'")
        print(f"\n文本 1 与文本 2 的相似度：{sim_12:.4f}")
        print(f"文本 1 与文本 3 的相似度：{sim_13:.4f}")
        print(f"文本 2 与文本 3 的相似度：{sim_23:.4f}")
```

### 运行方法

1. **设置 API 密钥**：

   ```bash
   export MISTRAL_API_KEY="your_api_key_here"
   ```

2. **保存并执行**：
   将脚本保存（如保存为 `embedding_example.py`）并运行：

   ```bash
   python embedding_example.py
   ```

### 预期输出

假设 API 调用成功，您将看到类似以下的输出（具体值取决于返回的嵌入向量）：

```
嵌入维度：1024

相似度结果：
文本 1：'I love programming in Python.'
文本 2：'Python is a great programming language.'
文本 3：'The weather is sunny today.'

文本 1 与文本 2 的相似度：0.9200
文本 1 与文本 3 的相似度：0.6500
文本 2 与文本 3 的相似度：0.6700
```

### 说明

- **API 端点**：`call_mistral_embeddings_api` 函数向 `https://api.mistral.ai/v1/embeddings` 发送 POST 请求，传递文本列表和 `"mistral-embed"` 模型。API 返回包含在 `"data"` 键下的嵌入向量的 JSON 响应。

- **嵌入向量**：每个嵌入向量是一个 1024 维向量（根据 Mistral 文档），表示输入文本的语义内容。嵌入向量被归一化为模长为 1。

- **相似度计算**：由于嵌入向量已归一化，两个嵌入向量之间的点积（`np.dot`）等于它们的余弦相似度。较高的值表示更大的语义相似度：
  - **文本 1 和文本 2**：两者都关于 Python 编程，因此相似度应较高（例如约 0.92）
  - **文本 1 和文本 3**：一个关于编程，另一个关于天气，因此相似度应较低（例如约 0.65）
  - **文本 2 和文本 3**：类似模式，由于主题不同相似度较低

### 其他应用场景

Mistral AI 的嵌入向量除了相似度检测外，还可应用于：

- **聚类**：使用 K-means 等算法对相似文本进行分组（需要 `scikit-learn`）

  ```python
  from sklearn.cluster import KMeans
  kmeans = KMeans(n_clusters=2).fit(np.array(embeddings))
  print(kmeans.labels_)
  ```

- **搜索**：嵌入查询并找到最相似的文本：

  ```python
  query = "Tell me about Python."
  query_emb = call_mistral_embeddings_api([query])[0]
  similarities = [calculate_similarity(query_emb, emb) for emb in embeddings]
  most_similar = texts[np.argmax(similarities)]
  print(f"最相似的文本：'{most_similar}'")
  ```

- **分类**：在机器学习模型中使用嵌入向量作为特征

### 注意事项

- **模型**：`"mistral-embed"` 模型针对嵌入任务进行了优化。请查看[文档](https://docs.mistral.ai/capabilities/embeddings/)了解更新或其他模型
- **批处理**：API 可在一次调用中处理多个文本，提高效率
- **高级应用**：对于大规模相似度搜索，可与 Faiss 或 Milvus 等向量数据库集成

本示例提供了使用 Mistral AI 嵌入向量的实用介绍，通过更改端点和数据格式，可适应所提供的聊天补全代码结构。
