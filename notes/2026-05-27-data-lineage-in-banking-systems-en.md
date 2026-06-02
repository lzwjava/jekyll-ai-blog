---
audio: false
generated: true
image: false
lang: en
layout: post
title: Data Lineage in Banking Systems
translated: false
type: note
---

**Question:** What is data lineage? How do you build data lineage in different banking systems?

**Answer:**

## Data Lineage

Data lineage is the **full lifecycle tracking of data** — where it originates, how it transforms, and where it ends up. Think of it as a DAG (directed acyclic graph) where:

- **Nodes** = datasets, tables, columns, or fields
- **Edges** = transformations (SQL, ETL jobs, API calls, model inference)
- **Metadata on edges** = who ran it, when, which version, with what parameters

```
[Source System] → [ETL Job] → [Raw Table] → [Transform] → [Mart Table] → [Report/Model]
     Oracle CRM     Informatica   data_lake      dbt model     dim_customer   PowerBI
```

At its core it answers:
1. **Where did this number come from?** (upstream lineage)
2. **What breaks if I change this field?** (downstream impact)
3. **Was this data compliant when it was used?** (audit trail)

---

## Why Banks Obsess Over Data Lineage

Banks aren't doing lineage for curiosity — they're doing it because regulators require it:

| Regulation | Requirement |
|---|---|
| **BCBS 239** | Risk data must be traceable end-to-end; banks must prove data accuracy |
| **GDPR / PDPA** | Must know where PII flows, who accessed it, when |
| **SOX** | Financial reports must have auditable data trails |
| **MAS TRM (Singapore)** | Data governance and lineage for critical systems |
| **DORA (EU 2025)** | Operational resilience — know your data dependencies |

BCBS 239 is the biggest driver. It explicitly requires that "a bank should be able to aggregate risk data in a timely manner" and trace it back to source.

---

## The Three Levels of Lineage

### 1. Table-level (coarse)
```
raw.transactions → mart.daily_pnl → report.risk_dashboard
```
Easy to build. Not enough for regulators.

### 2. Column-level (medium)
```
raw.transactions.amount
  → [sum, group by trade_date]
  → mart.daily_pnl.gross_amount
  → [*fx_rate]
  → report.risk_dashboard.usd_equivalent
```
This is the minimum viable lineage for BCBS 239.

### 3. Value-level / Record-level (fine)
```
trade_id=T12345, amount=1,000,000 CNY
  → fx_rate=7.24 (sourced from Reuters 2024-01-15 09:00 UTC)
  → usd_equivalent=138,122.17
  → appears in row 47 of RWA report filed 2024-01-16
```
Required for specific audit requests. Very expensive to store.

---

## How to Build It: Architecture Patterns

### Pattern 1: Passive / Metadata Harvesting
Don't change pipelines. **Parse existing artifacts** to extract lineage.

```python
# Parse SQL to extract table/column dependencies
import sqlglot

sql = """
INSERT INTO mart.daily_pnl (gross_amount, trade_date)
SELECT SUM(t.amount), t.trade_date
FROM raw.transactions t
JOIN ref.fx_rates fx ON t.currency = fx.currency
WHERE t.status = 'SETTLED'
GROUP BY t.trade_date
"""

ast = sqlglot.parse_one(sql)
sources = {t.name for t in ast.find_all(sqlglot.exp.Table)}
# → {'transactions', 'fx_rates'}

# Walk the AST for column-level lineage
for col in ast.find_all(sqlglot.exp.Column):
    print(col.table, col.name)
```

Tools: **sqlglot**, **sqlparse**, **OpenLineage parsers**

Pros: Zero pipeline changes. Works on legacy SQL.
Cons: Can't track runtime transformations (Python Pandas ops, stored procs with dynamic SQL).

---

### Pattern 2: Active Instrumentation — OpenLineage

**OpenLineage** is the open standard. Emit lineage events at runtime from your ETL/pipelines.

```python
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client.facet import (
    SchemaDatasetFacet, SchemaField,
    DataSourceDatasetFacet
)
from openlineage.client.dataset import Dataset
import uuid
from datetime import datetime

client = OpenLineageClient.from_environment()  # points to Marquez or your backend

run_id = str(uuid.uuid4())
job_name = "etl.daily_pnl_aggregation"

# Emit START event
client.emit(RunEvent(
    eventType=RunState.START,
    eventTime=datetime.utcnow().isoformat() + "Z",
    run=Run(runId=run_id),
    job=Job(namespace="banking.risk", name=job_name),
    inputs=[Dataset(
        namespace="oracle://prod-db:1521",
        name="RAW.TRANSACTIONS",
        facets={"schema": SchemaDatasetFacet(fields=[
            SchemaField("amount", "DECIMAL"),
            SchemaField("currency", "VARCHAR"),
            SchemaField("trade_date", "DATE"),
        ])}
    )],
    outputs=[Dataset(
        namespace="hive://datalake",
        name="MART.DAILY_PNL",
    )]
))

# ... run the actual ETL job ...

# Emit COMPLETE event
client.emit(RunEvent(
    eventType=RunState.COMPLETE,
    eventTime=datetime.utcnow().isoformat() + "Z",
    run=Run(runId=run_id),
    job=Job(namespace="banking.risk", name=job_name),
    inputs=[...], outputs=[...]
))
```

**Marquez** is the reference backend for OpenLineage — it stores the DAG and exposes a REST API.

---

### Pattern 3: dbt Lineage (most common in modern bank data platforms)

dbt natively generates lineage via `ref()` macros:

{% raw %}
```sql
-- models/mart/daily_pnl.sql
{{ config(materialized='table') }}

SELECT
    t.trade_date,
    SUM(t.amount * fx.rate) AS usd_gross
FROM {{ ref('raw_transactions') }} t   -- ← lineage edge declared here
JOIN {{ ref('fx_rates') }} fx
  ON t.currency = fx.currency
  AND t.trade_date = fx.rate_date
GROUP BY t.trade_date
```
{% endraw %}

dbt compiles this into a full lineage graph:

```bash
dbt docs generate
dbt docs serve  # → visual DAG in browser

# Or extract programmatically:
cat target/manifest.json | python3 -c "
import json, sys
m = json.load(sys.stdin)
for node, meta in m['nodes'].items():
    print(node, '←', meta.get('depends_on', {}).get('nodes', []))
"
```

The `manifest.json` is machine-readable lineage. Feed it to your metadata catalog.

---

### Pattern 4: Catalog-Layer Lineage (DataHub / Apache Atlas)

For enterprise multi-system lineage, you need a **metadata catalog** that aggregates from all sources.

**DataHub** (open source, LinkedIn origin, widely used in banks):

```python
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    DataFlowInfoClass, DataJobInfoClass, DataJobInputOutputClass,
    DatasetLineageTypeClass, UpstreamClass, UpstreamLineageClass
)
import datahub.metadata.schema_classes as models

emitter = DatahubRestEmitter("http://datahub-gms:8080")

# Declare upstream lineage for a dataset
upstream_lineage = models.MetadataChangeProposalWrapper(
    entityType="dataset",
    changeType=models.ChangeTypeClass.UPSERT,
    entityUrn="urn:li:dataset:(urn:li:dataPlatform:hive,mart.daily_pnl,PROD)",
    aspect=UpstreamLineageClass(
        upstreams=[
            UpstreamClass(
                dataset="urn:li:dataset:(urn:li:dataPlatform:oracle,raw.transactions,PROD)",
                type=DatasetLineageTypeClass.TRANSFORMED,
            ),
            UpstreamClass(
                dataset="urn:li:dataset:(urn:li:dataPlatform:oracle,ref.fx_rates,PROD)",
                type=DatasetLineageTypeClass.TRANSFORMED,
            ),
        ]
    ),
)
emitter.emit(upstream_lineage)
```

---

## Banking System Map: Where Lineage Gets Complicated

```
┌─────────────────────────────────────────────────────────────────┐
│                    TYPICAL BANK DATA FLOW                       │
│                                                                 │
│  [Core Banking]    [Trading Systems]    [CRM/Ops]              │
│   Finacle/T24       Murex / Summit       Siebel                │
│       │                  │                  │                   │
│       └──────────────────┴──────────────────┘                  │
│                          │                                      │
│                    [EDW / Data Lake]                            │
│               Oracle / Teradata / Snowflake                     │
│                          │                                      │
│            ┌─────────────┼────────────────┐                    │
│            │             │                │                     │
│      [Risk Engine]  [Finance/GL]    [Regulatory]               │
│       RWA / VaR     SAP / Oracle    COREP / MAS 610            │
│            │             │                │                     │
│            └─────────────┴────────────────┘                    │
│                          │                                      │
│                   [Reports / Dashboards]                        │
│               PowerBI / Tableau / Custom                        │
└─────────────────────────────────────────────────────────────────┘
```

### Per-System Lineage Strategy

| System | Tech | Lineage Approach |
|---|---|---|
| **Murex** (trading) | Proprietary | Parse MxML datamart exports; instrument ETL layer |
| **Finacle / T24** (core banking) | Proprietary COBOL/Java | Parse report definitions; ETL metadata harvesting |
| **Oracle EDW** | SQL + PL/SQL | sqlglot parsing + stored proc analysis |
| **Informatica** | ETL | Native lineage export via Informatica CLAIRE API |
| **Snowflake** | SQL | `INFORMATION_SCHEMA.ACCESS_HISTORY` + `QUERY_HISTORY` |
| **dbt** | SQL | `manifest.json` — best native lineage |
| **Spark** | Python/Scala | OpenLineage Spark integration (automatic, no code changes) |
| **Kafka** | Streaming | Schema Registry + custom lineage events per topic |

### Snowflake specifically (common in modern bank platforms):

```sql
-- Snowflake has access_history showing column-level lineage
SELECT
    query_start_time,
    query_text,
    direct_objects_accessed,     -- tables/columns read
    base_objects_accessed,       -- underlying base tables
    objects_modified             -- tables/columns written
FROM snowflake.account_usage.access_history
WHERE query_start_time > dateadd('day', -1, current_timestamp())
ORDER BY query_start_time DESC;
```

### Spark OpenLineage (zero-code instrumentation):

```bash
# Add to spark-submit — automatic lineage for all Spark jobs
spark-submit \
  --conf spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener \
  --conf spark.openlineage.transport.type=http \
  --conf spark.openlineage.transport.url=http://marquez:5000 \
  --conf spark.openlineage.namespace=banking.risk \
  my_etl_job.py
```

Every DataFrame read/write automatically emits lineage events. No code changes to existing jobs.

---

## Minimal End-to-End Stack You Can Build Now

```
Data Sources (Oracle, Snowflake, dbt, Spark)
    ↓  [OpenLineage events]
Marquez (lineage backend, REST API)
    ↓  [REST / Kafka]
DataHub (catalog, search, governance UI)
    ↓
Lineage API → your compliance reports / BCBS 239 evidence
```

Stand it up locally:

```bash
# Marquez (OpenLineage backend)
git clone https://github.com/MarquezProject/marquez
cd marquez && ./docker/up.sh

# DataHub
pip install acryl-datahub
datahub docker quickstart

# Test: emit a lineage event
pip install openlineage-python
python3 -c "
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client.dataset import Dataset
import uuid
from datetime import datetime

client = OpenLineageClient(url='http://localhost:5000')
client.emit(RunEvent(
    eventType=RunState.COMPLETE,
    eventTime=datetime.utcnow().isoformat()+'Z',
    run=Run(runId=str(uuid.uuid4())),
    job=Job(namespace='test', name='test_job'),
    inputs=[Dataset(namespace='postgres://localhost', name='raw.trades')],
    outputs=[Dataset(namespace='postgres://localhost', name='mart.pnl')],
))
print('Lineage emitted')
"
```

---

## Column-Level Lineage: The Hard Part

Column-level is where most solutions break. The state of the art:

```python
# sqlglot does column-level lineage from SQL
import sqlglot
from sqlglot.lineage import lineage

sql = """
SELECT
    t.amount * fx.rate AS usd_amount,
    t.trade_date
FROM raw.transactions t
JOIN ref.fx_rates fx ON t.currency = fx.currency
"""

# Trace where 'usd_amount' in the output comes from
result = lineage("usd_amount", sql)
result.walk()  # → traces back to raw.transactions.amount and ref.fx_rates.rate
```

For stored procedures with dynamic SQL — you can't parse statically. Your options:
1. Runtime tracing (instrument the DB engine)
2. LLM-assisted parsing — feed the proc to Claude, extract the lineage graph as JSON

{% raw %}
```python
# AI-assisted lineage extraction for complex stored procs
import anthropic

proc_code = open("complex_stored_proc.sql").read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": f"""Extract column-level data lineage from this stored procedure.
Return JSON only:
{{
  "inputs": [{{"table": "...", "column": "..."}}],
  "outputs": [{{"table": "...", "column": "..."}}],
  "transformations": [{{"output_col": "...", "expression": "...", "input_cols": [...]}}]
}}

Stored procedure:
{proc_code}"""
    }]
)
lineage_json = response.content[0].text
```
{% endraw %}

This works surprisingly well for complex PL/SQL and T-SQL procs that static parsers choke on.

---

## References

- [OpenLineage Spec](https://openlineage.io/docs/spec/api)
- [Marquez — OpenLineage Backend](https://marquezproject.ai/)
- [DataHub Lineage Docs](https://datahubproject.io/docs/lineage/lineage-feature-guide)
- [sqlglot Lineage](https://github.com/tobymao/sqlglot/blob/main/sqlglot/lineage.py)
- [BCBS 239 Full Text](https://www.bis.org/publ/bcbs239.htm)
- [Snowflake ACCESS_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/access_history)
- [OpenLineage Spark Integration](https://openlineage.io/docs/integrations/spark/)
