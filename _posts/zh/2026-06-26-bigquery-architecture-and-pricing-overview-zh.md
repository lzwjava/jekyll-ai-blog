---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BigQuery架构与定价概述
translated: true
type: note
---

Question: 介绍一下 Google BigQuery 的简介。

Answer:

BigQuery 是 Google 的无服务器列式数据仓库。核心思维模型：你不需要配置集群——你提交 SQL，Dremel（底层执行引擎）将你的查询分布在数千个节点上，并行扫描列式存储（Capacitor 格式）。你按扫描的字节数付费，而不是按节点小时付费。

## 深入一层的架构

由三个解耦的组件构成，通过 Google 的 Jupiter 网络（每秒千万亿位级的二分带宽，这是计算与存储分离在此能运作的关键）连接：

- **Colossus** — 分布式存储。表以列式 Capacitor 文件形式存在。列式意味着只涉及 50 列中 2 列的查询大约扫描 4% 的数据，而不是全部数据。
- **Dremel** — 查询引擎。构建一个多级服务树：根节点分片查询，混洗器聚合，叶子节点（槽位）扫描 Colossus。“槽位”是计算单位（≈ 一个 CPU 线程）。
- **Borg** — Google 的集群管理器，负责调度 Dremel 的槽位。

解耦是核心要点：存储与计算独立扩展，并且你分别支付存储和计算的费用。

## 定价模型——真正让人头疼的地方

两个维度：

- **存储**：活跃数据约 $0.02/GB/月；90 天未触动的数据价格减半。
- **查询**：按需查询约 $6.25/扫描 TB。这是个大坑——对宽表执行 `SELECT *` 很贵；`SELECT col1, col2` 则很便宜，因为列式存储。没有索引来拯救你；分区和聚类是用来减少扫描数据量的手段。

替代方案：**容量/版本定价**——为高负载工作负载购买槽位（近似于固定费用），实现可预测的成本。

## 最重要的两个优化

```sql
-- 分区：按某列（通常是日期）物理拆分表。
-- 使用包含该列的过滤条件查询 → BQ 跳过整个分区。
CREATE TABLE ds.events
PARTITION BY DATE(event_ts)
CLUSTER BY user_id, event_type
AS SELECT * FROM ds.raw;

-- 以下查询只扫描一天的分区，然后利用聚类
-- 跳过不包含该 user_id 的数据块：
SELECT event_type, COUNT(*)
FROM ds.events
WHERE DATE(event_ts) = '2026-06-25'   -- 分区剪枝
  AND user_id = '<UUID>'              -- 聚类剪枝
GROUP BY event_type;
```

分区以分区粒度进行剪枝；聚类在分区内对数据进行排序，使 BQ 能跳过数据块。两者结合可将 1 TB 的扫描量降至 1 GB——成本降低约 1000 倍。

## CLI / 优先构建

`bq` 工具随 `gcloud` 一起提供：

```bash
# 预估——在执行前告诉你将扫描多少字节
bq query --use_legacy_sql=false --dry_run \
  'SELECT name, SUM(number) AS total
   FROM `bigquery-public-data.usa_names.usa_1910_2013`
   WHERE state = "CA" GROUP BY name'

# 执行
bq query --use_legacy_sql=false \
  'SELECT name, SUM(number) total
   FROM `bigquery-public-data.usa_names.usa_1910_2013`
   GROUP BY name ORDER BY total DESC LIMIT 10'

# 将本地文件加载到表中
bq load --autodetect --source_format=CSV \
  mydataset.mytable ./data.csv
```

Python（实际集成到数据管道中的方式）：

```python
from google.cloud import bigquery

client = bigquery.Client(project="<PROJECT_ID>")

# 带参数 + 预估成本检查
job_config = bigquery.QueryJobConfig(
    dry_run=True,
    query_parameters=[bigquery.ScalarQueryParameter("st", "STRING", "CA")],
)
q = """SELECT name, SUM(number) AS total
       FROM `bigquery-public-data.usa_names.usa_1910_2013`
       WHERE state = @st GROUP BY name"""
job = client.query(q, job_config=job_config)
print(f"Will scan {job.total_bytes_processed / 1e9:.2f} GB")

# 直接输出 DataFrame —— 适用于快速迭代
df = client.query(q.replace("@st", "'CA'")).to_dataframe()
```

## 为什么与你的技术方向相关

两个角度对于 AI 工作有叠加效应：

- **BigQuery ML** 允许你用 SQL 训练模型（`CREATE MODEL ... OPTIONS(model_type='...')`），包括对表行调用 Vertex/Gemini 端点——即 LLM 推理作为 SQL 函数应用于整列。这是 AI 原生数据仓库模式：无需编写服务循环，即可批量嵌入或批量分类数百万行。
- **向量搜索** — BQ 现在原生支持 `VECTOR_SEARCH` 和嵌入生成，因此它可作为一个廉价的无服务器嵌入存储，用于基于结构化数据的 RAG。

```sql
-- 对某列生成嵌入，然后进行 ANN 搜索 —— 无需独立的向量数据库
SELECT * FROM VECTOR_SEARCH(
  TABLE my_dataset.doc_embeddings, 'embedding',
  (SELECT embedding FROM my_dataset.query_emb),
  top_k => 10);
```

几个值得尽早了解的坑：它针对追加进行了优化（点更新/删除虽然可行，但属于反模式——应将其视为不可变分析场景，而非 OLTP）；流式插入需要额外付费，且去重窗口很短；标准 SQL 是默认设置（`--use_legacy_sql=false` 处处适用——旧版 SQL 已废弃，忽略它）。

如果你愿意，我可以深入探讨任何一个分支——Capacitor/Dremel 的内部原理、适用于密集型 token 工作负载的 BQML + Gemini 批量推理，或针对特定模式的成本优化策略。

参考资料：

- [BigQuery 概述](https://cloud.google.com/bigquery/docs/introduction)
- [Dremel: Interactive Analysis of Web-Scale Datasets（论文）](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets/)
- [查询定价](https://cloud.google.com/bigquery/pricing)
- [分区与聚类表](https://cloud.google.com/bigquery/docs/partitioned-tables)
- [BigQuery ML + 生成式 AI](https://cloud.google.com/bigquery/docs/generate-text)