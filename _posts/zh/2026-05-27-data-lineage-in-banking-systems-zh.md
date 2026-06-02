---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 银行系统中的数据血缘
translated: true
type: note
---

**问题：** 什么是数据血缘？如何在不同银行系统中构建数据血缘？

**回答：**

## 数据血缘

数据血缘是数据的**全生命周期追踪**——它从何而来，如何转换，最终流向何处。可以将其视为一个有向无环图（DAG），其中：

- **节点** = 数据集、表、列或字段
- **边** = 转换（SQL、ETL作业、API调用、模型推理）
- **边上的元数据** = 谁执行的，何时执行，哪个版本，使用什么参数

```
[源系统] → [ETL作业] → [原始表] → [转换] → [集市表] → [报表/模型]
     Oracle CRM     Informatica   data_lake      dbt model     dim_customer   PowerBI
```

其核心回答了：

1. **这个数字从哪来？**（上游血缘）
2. **如果我更改这个字段，什么会出问题？**（下游影响）
3. **该数据在使用时是否合规？**（审计追踪）

---

## 为什么银行对数据血缘如此执着

银行做血缘不是为了好奇——而是因为监管机构要求：

| 法规 | 要求 |
|---|---|
| **BCBS 239** | 风险数据必须端到端可追溯；银行必须证明数据准确性 |
| **GDPR / PDPA** | 必须知道个人身份信息（PII）流向，谁曾访问，何时访问 |
| **SOX** | 财务报告必须有可审计的数据轨迹 |
| **MAS TRM（新加坡）** | 关键系统的数据治理和血缘 |
| **DORA（欧盟2025）** | 运营韧性——了解你的数据依赖关系 |

BCBS 239 是最大的驱动力。它明确要求“银行应能够及时汇总风险数据”，并追溯到源头。

---

## 血缘的三个层级

### 1. 表级（粗略）

```
raw.transactions → mart.daily_pnl → report.risk_dashboard
```

易于构建，但不足以满足监管要求。

### 2. 列级（中等）

```
raw.transactions.amount
  → [sum, group by trade_date]
  → mart.daily_pnl.gross_amount
  → [*fx_rate]
  → report.risk_dashboard.usd_equivalent
```

这是 BCBS 239 的最低可行血缘。

### 3. 值级 / 记录级（精细）

```
trade_id=T12345, amount=1,000,000 CNY
  → fx_rate=7.24（来源：Reuters 2024-01-15 09:00 UTC）
  → usd_equivalent=138,122.17
  → 出现在2024-01-16提交的RWA报表第47行
```

特定审计请求需要，但存储成本极高。

---

## 如何构建：架构模式

### 模式1：被动/元数据采集

不改变管道。**解析现有工件**以提取血缘。

```python
# 解析SQL以提取表/列依赖关系
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

# 遍历AST以获取列级血缘
for col in ast.find_all(sqlglot.exp.Column):
    print(col.table, col.name)
```

工具：**sqlglot**、**sqlparse**、**OpenLineage解析器**

优点：无需更改管道，适用于遗留SQL。
缺点：无法跟踪运行时转换（Python Pandas操作、动态SQL的存储过程）。

---

### 模式2：主动检测——OpenLineage

**OpenLineage** 是开放标准。在ETL/管道运行时发出血缘事件。

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

client = OpenLineageClient.from_environment()  # 指向Marquez或你的后端

run_id = str(uuid.uuid4())
job_name = "etl.daily_pnl_aggregation"

# 发出START事件
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

# ... 运行实际的ETL作业 ...

# 发出COMPLETE事件
client.emit(RunEvent(
    eventType=RunState.COMPLETE,
    eventTime=datetime.utcnow().isoformat() + "Z",
    run=Run(runId=run_id),
    job=Job(namespace="banking.risk", name=job_name),
    inputs=[...], outputs=[...]
))
```

**Marquez** 是OpenLineage的参考后端——它存储DAG并暴露REST API。

---

### 模式3：dbt血缘（现代银行数据平台中最常见）

dbt通过`ref()`宏原生生成血缘：

{% raw %}

```sql
-- models/mart/daily_pnl.sql
{{ config(materialized='table') }}

SELECT
    t.trade_date,
    SUM(t.amount * fx.rate) AS usd_gross
FROM {{ ref('raw_transactions') }} t   -- ← 此处声明血缘边
JOIN {{ ref('fx_rates') }} fx
  ON t.currency = fx.currency
  AND t.trade_date = fx.rate_date
GROUP BY t.trade_date
```

{% endraw %}

dbt将其编译为完整的血缘图：

```bash
dbt docs generate
dbt docs serve  # → 浏览器中的可视化DAG

# 或以编程方式提取：
cat target/manifest.json | python3 -c "
import json, sys
m = json.load(sys.stdin)
for node, meta in m['nodes'].items():
    print(node, '←', meta.get('depends_on', {}).get('nodes', []))
"
```

`manifest.json` 是机器可读的血缘。将其输入到元数据目录中。

---

### 模式4：目录层血缘（DataHub / Apache Atlas）

对于企业级多系统血缘，你需要一个**元数据目录**，从所有源聚合。

**DataHub**（开源，源自LinkedIn，广泛应用于银行）：

```python
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    DataFlowInfoClass, DataJobInfoClass, DataJobInputOutputClass,
    DatasetLineageTypeClass, UpstreamClass, UpstreamLineageClass
)
import datahub.metadata.schema_classes as models

emitter = DatahubRestEmitter("http://datahub-gms:8080")

# 声明数据集的上游血缘
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

## 银行系统地图：血缘变得复杂的地方

```
┌─────────────────────────────────────────────────────────────────┐
│                 典型的银行数据流                               │
│                                                                 │
│  [核心银行系统]    [交易系统]      [CRM/运营]                   │
│   Finacle/T24       Murex / Summit    Siebel                    │
│       │                  │                  │                   │
│       └──────────────────┴──────────────────┘                  │
│                          │                                      │
│                    [EDW / 数据湖]                              │
│               Oracle / Teradata / Snowflake                     │
│                          │                                      │
│            ┌─────────────┼────────────────┐                    │
│            │             │                │                     │
│      [风险引擎]    [财务/总账]      [监管报告]                  │
│       RWA / VaR     SAP / Oracle    COREP / MAS 610            │
│            │             │                │                     │
│            └─────────────┴────────────────┘                    │
│                          │                                      │
│                   [报表 / 仪表板]                               │
│               PowerBI / Tableau / Custom                        │
└─────────────────────────────────────────────────────────────────┘
```

### 各系统血缘策略

| 系统 | 技术 | 血缘方法 |
|---|---|---|
| **Murex**（交易） | 专有 | 解析MxML数据市场导出；检测ETL层 |
| **Finacle / T24**（核心银行） | 专有COBOL/Java | 解析报表定义；ETL元数据采集 |
| **Oracle EDW** | SQL + PL/SQL | sqlglot解析 + 存储过程分析 |
| **Informatica** | ETL | 通过Informatica CLAIRE API原生血缘导出 |
| **Snowflake** | SQL | `INFORMATION_SCHEMA.ACCESS_HISTORY` + `QUERY_HISTORY` |
| **dbt** | SQL | `manifest.json` —— 最佳原生血缘 |
| **Spark** | Python/Scala | OpenLineage Spark集成（自动，无需代码更改） |
| **Kafka** | 流式 | Schema Registry + 每个主题的自定义血缘事件 |

### 特别是Snowflake（现代银行平台中常见）

```sql
-- Snowflake的access_history显示列级血缘
SELECT
    query_start_time,
    query_text,
    direct_objects_accessed,     -- 读取的表/列
    base_objects_accessed,       -- 底层基础表
    objects_modified             -- 写入的表/列
FROM snowflake.account_usage.access_history
WHERE query_start_time > dateadd('day', -1, current_timestamp())
ORDER BY query_start_time DESC;
```

### Spark OpenLineage（零代码检测）

```bash
# 添加到spark-submit — 所有Spark作业的自动血缘
spark-submit \
  --conf spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener \
  --conf spark.openlineage.transport.type=http \
  --conf spark.openlineage.transport.url=http://marquez:5000 \
  --conf spark.openlineage.namespace=banking.risk \
  my_etl_job.py
```

每个DataFrame读/写操作都会自动发出血缘事件。现有作业无需更改代码。

---

## 你现在可以构建的最小端到端栈

```
数据源（Oracle, Snowflake, dbt, Spark）
    ↓  [OpenLineage事件]
Marquez（血缘后端，REST API）
    ↓  [REST / Kafka]
DataHub（目录，搜索，治理UI）
    ↓
血缘API → 你的合规报告 / BCBS 239证据
```

本地搭建：

```bash
# Marquez（OpenLineage后端）
git clone https://github.com/MarquezProject/marquez
cd marquez && ./docker/up.sh

# DataHub
pip install acryl-datahub
datahub docker quickstart

# 测试：发出一个血缘事件
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

## 列级血缘：最难的部分

列级血缘是大多数解决方案的瓶颈。当前的最新技术：

```python
# sqlglot可以从SQL中进行列级血缘分析
import sqlglot
from sqlglot.lineage import lineage

sql = """
SELECT
    t.amount * fx.rate AS usd_amount,
    t.trade_date
FROM raw.transactions t
JOIN ref.fx_rates fx ON t.currency = fx.currency
"""

# 追踪输出中 'usd_amount' 的来源
result = lineage("usd_amount", sql)
result.walk()  # → 回溯到 raw.transactions.amount 和 ref.fx_rates.rate
```

对于包含动态SQL的存储过程——你无法静态解析。你的选项：

1. 运行时追踪（检测数据库引擎）
2. 大模型辅助解析——将过程输入Claude，提取JSON格式的血缘图

{% raw %}

```python
# 针对复杂存储过程的AI辅助血缘提取
import anthropic

proc_code = open("complex_stored_proc.sql").read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": f"""从该存储过程中提取列级数据血缘。
仅返回JSON：
{{
  "inputs": [{{"table": "...", "column": "..."}}],
  "outputs": [{{"table": "...", "column": "..."}}],
  "transformations": [{{"output_col": "...", "expression": "...", "input_cols": [...]}}]
}}

存储过程：
{proc_code}"""
    }]
)
lineage_json = response.content[0].text
```

{% endraw %}

对于静态解析器难以处理的复杂PL/SQL和T-SQL过程，这种方法效果出奇地好。

---

## 参考资料

- [OpenLineage规范](https://openlineage.io/docs/spec/api)
- [Marquez — OpenLineage后端](https://marquezproject.ai/)
- [DataHub血缘文档](https://datahubproject.io/docs/lineage/lineage-feature-guide)
- [sqlglot血缘](https://github.com/tobymao/sqlglot/blob/main/sqlglot/lineage.py)
- [BCBS 239全文](https://www.bis.org/publ/bcbs239.htm)
- [Snowflake ACCESS_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/access_history)
- [OpenLineage Spark集成](https://openlineage.io/docs/integrations/spark/)
