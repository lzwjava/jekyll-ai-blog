---
audio: false
generated: true
image: false
lang: en
layout: post
title: BigQuery Architecture and Pricing Overview
translated: false
type: note
---

Question: Give me an intro to Google BigQuery.

Answer:

BigQuery is Google's serverless, columnar data warehouse. The core mental model: you don't provision clusters — you submit SQL, and Dremel (the underlying execution engine) fans your query out across thousands of nodes, scanning columnar storage (Capacitor format) in parallel. You pay per byte scanned, not per node-hour.

## Architecture in one layer deeper

Three decoupled pieces, connected by Google's Jupiter network (petabit-scale bisection bandwidth, which is *why* compute/storage separation works here):

- **Colossus** — distributed storage. Tables live as columnar Capacitor files. Columnar means a query touching 2 of 50 columns scans ~4% of the data, not all of it.
- **Dremel** — the query engine. Builds a multi-level serving tree: a root node shards the query, mixers aggregate, leaf nodes (slots) scan Colossus. A "slot" is a unit of compute (≈ a CPU thread).
- **Borg** — Google's cluster manager that schedules Dremel's slots.

The decoupling is the whole point: storage scales independently of compute, and you're billed separately for each.

## Pricing model — the thing that actually bites

Two axes:

- **Storage**: ~$0.02/GB/month active, half that for data untouched 90 days.
- **Query**: on-demand is ~$6.25/TB *scanned*. This is the footgun — `SELECT *` on a wide table is expensive; `SELECT col1, col2` is cheap because columnar. There's no index to save you; partitioning and clustering are how you prune bytes.

Alternative: **capacity/editions pricing** — buy slots (flat-rate-ish) for predictable cost on heavy workloads.

## The two optimizations that matter most

```sql
-- Partition: physically splits table by a column (usually date).
-- Query with a filter on it → BQ skips entire partitions.
CREATE TABLE ds.events
PARTITION BY DATE(event_ts)
CLUSTER BY user_id, event_type
AS SELECT * FROM ds.raw;

-- This scans only one day's partition, then uses clustering
-- to skip blocks where user_id doesn't match:
SELECT event_type, COUNT(*)
FROM ds.events
WHERE DATE(event_ts) = '2026-06-25'   -- partition prune
  AND user_id = '<UUID>'              -- cluster prune
GROUP BY event_type;
```

Partitioning prunes at partition granularity; clustering sorts within partitions so BQ skips blocks. Together they can turn a 1 TB scan into a 1 GB scan — a ~1000x cost cut.

## CLI / build-first

The `bq` tool ships with `gcloud`:

```bash
# Dry run — tells you bytes scanned BEFORE you pay
bq query --use_legacy_sql=false --dry_run \
  'SELECT name, SUM(number) AS total
   FROM `bigquery-public-data.usa_names.usa_1910_2013`
   WHERE state = "CA" GROUP BY name'

# Run it
bq query --use_legacy_sql=false \
  'SELECT name, SUM(number) total
   FROM `bigquery-public-data.usa_names.usa_1910_2013`
   GROUP BY name ORDER BY total DESC LIMIT 10'

# Load a local file into a table
bq load --autodetect --source_format=CSV \
  mydataset.mytable ./data.csv
```

Python (the way you'd actually wire it into a pipeline):

```python
from google.cloud import bigquery

client = bigquery.Client(project="<PROJECT_ID>")

# Parameterized + dry-run cost check
job_config = bigquery.QueryJobConfig(
    dry_run=True,
    query_parameters=[bigquery.ScalarQueryParameter("st", "STRING", "CA")],
)
q = """SELECT name, SUM(number) AS total
       FROM `bigquery-public-data.usa_names.usa_1910_2013`
       WHERE state = @st GROUP BY name"""
job = client.query(q, job_config=job_config)
print(f"Will scan {job.total_bytes_processed / 1e9:.2f} GB")

# DataFrame straight out — good for fast iteration
df = client.query(q.replace("@st", "'CA'")).to_dataframe()
```

## Why it's relevant to your trajectory

Two angles that compound for AI work:

- **BigQuery ML** lets you train models in SQL (`CREATE MODEL ... OPTIONS(model_type='...')`), including calling Vertex/Gemini endpoints over table rows — i.e. LLM inference as a SQL function over a whole column. That's the AI-native data-warehouse pattern: batch-embed or batch-classify millions of rows without writing a serving loop.
- **Vector search** — BQ now has native `VECTOR_SEARCH` and embedding generation, so it doubles as a cheap, serverless embedding store for RAG over structured data.

```sql
-- Generate embeddings over a column, then ANN search — no separate vector DB
SELECT * FROM VECTOR_SEARCH(
  TABLE my_dataset.doc_embeddings, 'embedding',
  (SELECT embedding FROM my_dataset.query_emb),
  top_k => 10);
```

A few sharp edges worth knowing early: it's append-optimized (point UPDATEs/DELETEs are possible but anti-pattern — think immutable analytics, not OLTP); streaming inserts cost extra and have a short de-dup window; and standard SQL is the default (`--use_legacy_sql=false` everywhere — legacy SQL is dead, ignore it).

If you want, I can go deeper on any one branch — the Capacitor/Dremel internals, BQML + Gemini batch inference for your token-heavy workflows, or cost-optimization patterns for a specific schema.

References:

- [BigQuery overview](https://cloud.google.com/bigquery/docs/introduction)
- [Dremel: Interactive Analysis of Web-Scale Datasets (paper)](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets/)
- [Query pricing](https://cloud.google.com/bigquery/pricing)
- [Partitioned & clustered tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
- [BigQuery ML + generative AI](https://cloud.google.com/bigquery/docs/generate-text)
