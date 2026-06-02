---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: PGVector：PostgreSQL中的向量嵌入
translated: true
type: note
---

PGVector 是一个 **PostgreSQL 扩展**，支持在 Postgres 数据库中存储和查询*向量嵌入*（数值数组，通常为 128-4096 维）。

它常用于 **AI 和机器学习应用**场景，需要存储和检索由 OpenAI、Hugging Face 或其他嵌入提供商生成的嵌入向量。例如，您可以将文档、代码片段或产品描述转换为向量，然后使用 PGVector 快速找到与用户查询最相似的内容。

### 核心特性

* **向量数据类型**：为 Postgres 表新增 `vector` 列类型
* **相似性搜索**：支持余弦相似度、欧氏距离或内积等向量比较操作
* **高效索引**：提供 `ivfflat` 和 `hnsw` 索引类型，支持高效的*近似最近邻（ANN）*搜索，即使处理数百万条嵌入数据也能快速检索
* **SQL 集成**：由于在 Postgres 内部运行，可将向量搜索与标准 SQL 查询、联接和过滤器结合使用

### 使用示例

```sql
-- 创建包含向量列的表
CREATE TABLE items (
  id bigserial PRIMARY KEY,
  embedding vector(1536)  -- 维度需与模型匹配
);

-- 插入数据
INSERT INTO items (embedding) VALUES ('[0.25, 0.1, ...]');

-- 搜索最相似的嵌入向量
SELECT id, embedding
FROM items
ORDER BY embedding <-> '[0.24, 0.11, ...]'
LIMIT 5;
```

其中 `<-> 为相似性运算符`。

### 重要意义

PGVector 让您能够 **直接在 Postgres 中构建完整的向量数据库**，而无需使用独立的专用向量数据库（如 Pinecone、Weaviate 或 Milvus）。如果您已在使用 Postgres 并希望将所有数据和查询集中管理，这个特性将极具吸引力。

---

是否需要我进一步对比 **PGVector 与专用向量数据库**（如 Pinecone 或 Weaviate）的差异，帮助您了解各自的适用场景？
