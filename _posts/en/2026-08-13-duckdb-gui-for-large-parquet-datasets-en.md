---
audio: false
generated: true
image: false
lang: en
layout: post
title: DuckDB GUI for Large Parquet Datasets
translated: false
type: note
---

Question: What GUI tools can I use on Ubuntu/Linux to inspect a huge Parquet dataset like your 4.8 GB FineWeb-2 shard?

Answer: For your use case, I'd pick **DuckDB + a GUI frontend** rather than loading the Parquet file into a traditional spreadsheet/database GUI.

### 1. Best fit: DBeaver + DuckDB

![Image](https://images.openai.com/static-rsc-4/s3KATBsdQRUniVJxal5IfQPBNqy-Ak-47N-6S9Zu6vR_jzJECFxn-Tlvgg3QsG6DUCDEeWnbKfez3Jqls01UbVM7UpRcJVBwCvNtPIhb_yKfbT7wZvZ5KFNAkU2_cz38PQxOOTyfNpN_OWcigXoyY1wrdMLhEBrXWzNBFuYnu1YhUBz07PyDxoYK2XI5f0XQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/8AArbpearnsRvjeH2oXlWpVlYnNcoYfFwwdNx7pqgpttJswCzeSbI87bdrd3EwCJ5tzEFoHe4Tl4aSz5oKLI9f0aTy78NIk2lpZl8fWv7FqoLf3L2x48cBS2Z4EXR4bLtS9R4FevsgcLWM94c-8EPn-v_uhZMtykmXfeUKpw1IWtHA52LR1ZQdgGtCCIMHqd?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LPgxDIFVIK88C3swlzAbmFRuOAes29RFOnFDfRVJ3m25RcBtEpWovbkaCoEZ2Rw9K-6bzXqjRKxSGnVo9L4N5iVZfV8__jHkM_nGSlu0fQQ-gKdeicM7nOXU9QPfspK6n99D2xRmNwrFQei40mDELRTFwQsK4BQabhHdCIVWHNbt3_tunozWi4dlYtsoDKvy?purpose=fullsize)

Install DuckDB:

```bash
curl -fsSL https://install.duckdb.org | sh
```

Then:

```bash
duckdb
```

You can inspect the 4.8 GB file **without converting it to JSONL**:

```sql
SELECT *
FROM '000_00000.parquet'
LIMIT 20;
```

Schema:

```sql
DESCRIBE
SELECT *
FROM '000_00000.parquet';
```

Count:

```sql
SELECT count(*)
FROM '000_00000.parquet';
```

Search:

```sql
SELECT *
FROM '000_00000.parquet'
WHERE text LIKE '%transformer%'
LIMIT 100;
```

DBeaver can connect to DuckDB and gives you a proper table/grid UI.

This is probably what I'd use for FineWeb because **Parquet is already columnar**, and DuckDB can query it directly.

---

### 2. MotherDuck

![Image](https://images.openai.com/static-rsc-4/ZFZvaDGQYBEjYxj-IJkc3FL6x2H9MiiS7x_FclxfeWJegxw8WsRDBlMolKOKlwDXSh6R-mKJ0dbV783_ORnWhqEiANIVS6wUUZc5vgaRzj62sy753yrrIEPmOPs2vHTaCM2itq3EsENatLd68cmHFMskJ55xKhiPjKYLo1gxWf_NQ6NhBe9tA_jPzHzmMnWh?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Rk2F43M2UxiU9aTd9KFLnqz0-dfAZJlrDwxbnKd9wuZ5s1URUQP1JDGIvXTlplMRA1_m1YOhZymEGbYGO9DhvIj_gGSs30GXqiyzFbJefLaHdoUeILz6XjR7pmFxXS--AqGAGeDqoc9f1B-ZMRpv6BAyeksv-Ld0lGsv-1ydyLmYMc8IqDKBv2_NlIbF8g-p?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4EiusSMt6Qm6_daaMSjMhr5zBi1MDwk4s-d_hLCyjVJxSljlRNTZATBvlt3bkZQKuMc_GHCiJz6NrvMgoQ3tCPyDdNySRGtDeRwzFqRkU0aazuzEc9aIJqldqFnH0h0xLr9MC8ON9eUjq-jQ4kwoeJRErczfDm0Avsp0anLUlVCajIOwYpNuQAQ4P-14gRro?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/gPZCK5koPZmPaXEzXskfTtI61XLck_FsZmUx2Yuh_KFGPSttQmAp6hGqfHlQFqOTf__J48cngk_s-qBzA5GIuJWGJMCJOGWupt3wNlneIzLk0IzhszEPnm7q7fQrlEM8myrH4RR1DaKw2aCPhARx52abiCrDuG585WQjJhZw00VgpJSy6npKSsVnzjPCoSgm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/F0Gk1kJAShi9XyDTGDNOfl99QyLwNbyVfrCY6mm2ED1meJsE-6Eazi8787iqgejddj8aWl42VhxYmys6H7I1r27rBynjiAoVAzt1j6bL9a3sxiDwL6fqviExDa9rVQu08NlHSirJqCYYClxQoa89zPdKX2yYqqR8Rge8l32nAgOzUb0l8B2AFhOWcQye34G9?purpose=fullsize)

MotherDuck is essentially a web UI around DuckDB.

You can do things like:

```sql
SELECT *
FROM '000_00000.parquet'
LIMIT 100;
```

It's particularly nice if you want to explore datasets interactively rather than build a local application.

---

### 3. VS Code + DuckDB extension

If you live in the terminal/VS Code, this is probably the **lowest-friction option**.

You can keep your dataset at:

```text
/mnt/data/.../000_00000.parquet
```

and query it with DuckDB from VS Code.

This is much more practical than trying to open a 4.8 GB Parquet file with a generic CSV/Excel viewer.

---

### 4. Apache Arrow / Polars + a tiny local web UI

If you want something more dataset-browser-like, you can build a tiny viewer with Python:

```python
import duckdb

con = duckdb.connect()

df = con.sql("""
    SELECT *
    FROM '/mnt/data/xxx/000_00000.parquet'
    LIMIT 100
""").df()

print(df)
```

Then put Streamlit/Gradio on top.

But honestly, **don't build this unless you need custom functionality**. DuckDB already solves the hard part.

---

### What I'd use for your FineWeb-2 workflow

Your file is:

```text
4.84 GB
1,973,000 rows
```

and presumably contains something like:

```text
text
id
language
...
```

I would keep the original Parquet and inspect it directly:

```bash
duckdb /mnt/data/fineweb/xxx.parquet
```

Then:

```sql
-- See columns
DESCRIBE SELECT * FROM 'xxx.parquet';

-- Random examples
SELECT *
FROM 'xxx.parquet'
USING SAMPLE 50;

-- Longest documents
SELECT length(text), text
FROM 'xxx.parquet'
ORDER BY length(text) DESC
LIMIT 20;

-- Distribution
SELECT count(*), avg(length(text))
FROM 'xxx.parquet';

-- Search
SELECT text
FROM 'xxx.parquet'
WHERE text ILIKE '%machine learning%'
LIMIT 50;
```

**Key point:** don't convert the 4.8 GB Parquet into JSONL merely to inspect it. Your current conversion:

```text
Parquet
   ↓
1,973,000 rows
   ↓
JSONL
```

throws away a lot of the advantages of Parquet. DuckDB can operate directly on:

```text
Parquet
   ↓
DuckDB SQL
   ↓
GUI table
```

For ML datasets specifically, **DuckDB + DBeaver** is the combination I'd recommend first.