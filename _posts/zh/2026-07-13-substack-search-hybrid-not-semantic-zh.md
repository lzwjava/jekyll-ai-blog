---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Substack搜索：混合式，非语义
translated: true
type: note
---

问题：Substack 的搜索功能好吗？例如，我能搜索王垠的 Substack 中关于「时间」的内容，并获得语义匹配的结果，而不仅仅是精确的关键词匹配吗？

答案：

是的，Substack 的搜索远不止简单的 `grep "时间"` 这种风格，但它也不是像现代 AI 搜索那样的完整语义搜索引擎。

对于像王垠 Substack 这样的出版物，Substack 通过其搜索栏提供对文章/出版物/主题的搜索。（[Substack 支持][1]）

你的观察基本正确：

* 它并不只做精确字符串匹配。
* 搜索 `时间` 可能会返回以下文章：

  * 包含「时间」这个词
  * 讨论相关概念
  * 标题/内容与时间、存在、生命、思维等在语义上相关

这更接近于 **hybrid search**：

```
query = "时间"

score =
    keyword_match_score
  + title_similarity
  + content_similarity
  + popularity/relevance signals
```

而不是：

```bash
grep -r "时间" posts/
```

纯关键词引擎会漏掉：

```
「人生为什么有限」
「不要浪费生命」
「过去与未来」
「意识和存在」
```

因为它们可能不包含「时间」这两个字，但在语义上与时间相关。

然而，Substack 搜索的威力不如自己构建一个 RAG 系统：

```
王垠文章
        |
        v
爬取 markdown/html
        |
        v
文档分块
        |
        v
embedding model
        |
        v
vector database
        |
        v
查询："王垠关于时间的观点"
        |
        v
semantic retrieval
```

然后你可以问：

```
「找到所有王垠讨论时间的地方，
包括与之相关的想法，如生命、存在、变化和意识。」
```

一个本地实现很简单：

```python
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("BAAI/bge-large-en-v1.5")

docs = load_yinwang_articles()

embeddings = model.encode(docs)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

query = "王垠关于时间是什么的思考"

q = model.encode([query])

scores, ids = index.search(q, 10)

for i in ids[0]:
    print(docs[i])
```

对于深度哲学研究，这很可能超越 Substack 搜索。

对于像你这样已经拥有以下资源的人：

* 8000+ AI 笔记
* Jekyll 博客
* LLM 基础设施经验

一个非常自然的项目是：

```
个人知识引擎

Markdown
   |
   v
chunking
   |
   v
embedding
   |
   v
FAISS / Qdrant
   |
   v
带有引用的 LLM 回答
```

基本上就是一个个人「AI 第二大脑」。

参考资料：

* （[Substack 支持][1]）
* （[Substack 支持][2]）

[1]: https://support.substack.com/hc/en-us/articles/4406018060692-How-do-I-find-a-Substack-publication?utm_source=chatgpt.com "如何找到Substack出版物？– Substack, Inc"
[2]: https://support.substack.com/hc/en-us/articles/15853567274772-Guide-to-your-Substack-Posts-page?utm_source=chatgpt.com "Substack文章页面指南 – Substack, Inc"