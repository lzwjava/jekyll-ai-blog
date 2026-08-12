---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DuckDB大型Parquet数据集图形界面
translated: true
type: note
---

问题：在 Ubuntu/Linux 上，我可以使用哪些 GUI 工具来检查像你提供的 4.8 GB FineWeb-2 分片这样的大型 Parquet 数据集？

答案：针对你的使用场景，我建议选择 **DuckDB + GUI 前端**，而不是将 Parquet 文件加载到传统的电子表格/数据库 GUI 中。

### 1. 最佳选择：DBeaver + DuckDB

安装 DuckDB：

```bash
curl -fsSL https://install.duckdb.org | sh
```

然后：

```bash
duckdb
```

你可以检查这个 4.8 GB 的文件，**无需将其转换为 JSONL**：

```sql
SELECT *
FROM '000_00000.parquet'
LIMIT 20;
```

查看模式：

```sql
DESCRIBE
SELECT *
FROM '000_00000.parquet';
```

统计行数：

```sql
SELECT count(*)
FROM '000_00000.parquet';
```

搜索：

```sql
SELECT *
FROM '000_00000.parquet'
WHERE text LIKE '%transformer%'
LIMIT 100;
```

DBeaver 可以连接到 DuckDB，并提供合适的表格/网格界面。

这可能是我在 FineWeb 上会使用的方案，因为 **Parquet 已经是列式存储**，而 DuckDB 可以直接查询它。

---

### 2. MotherDuck

MotherDuck 本质上是围绕 DuckDB 构建的 Web UI。

你可以执行如下操作：

```sql
SELECT *
FROM '000_00000.parquet'
LIMIT 100;
```

如果你希望以交互方式探索数据集，而不是构建本地应用程序，这个方案特别方便。

---

### 3. VS Code + DuckDB 扩展

如果你习惯在终端/VS Code 中工作，这可能是**摩擦最小的选项**。

你可以将数据集保存在：

```text
/mnt/data/.../000_00000.parquet
```

并从 VS Code 中使用 DuckDB 查询它。

这比尝试用通用的 CSV/Excel 查看器打开 4.8 GB 的 Parquet 文件要实用得多。

---

### 4. Apache Arrow / Polars + 小型本地 Web UI

如果你想要更像数据集浏览器的工具，可以用 Python 构建一个小型查看器：

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

然后在其上添加 Streamlit/Gradio。

但说实话，**除非你需要自定义功能，否则不要自己构建**。DuckDB 已经解决了最困难的部分。

---

### 我会为你的 FineWeb-2 工作流使用的方案

你的文件是：

```text
4.84 GB
1,973,000 行
```

并且可能包含类似这样的内容：

```text
text
id
language
...
```

我会保留原始 Parquet 并直接检查它：

```bash
duckdb /mnt/data/fineweb/xxx.parquet
```

然后：

```sql
-- 查看列
DESCRIBE SELECT * FROM 'xxx.parquet';

-- 随机样本
SELECT *
FROM 'xxx.parquet'
USING SAMPLE 50;

-- 最长文档
SELECT length(text), text
FROM 'xxx.parquet'
ORDER BY length(text) DESC
LIMIT 20;

-- 分布情况
SELECT count(*), avg(length(text))
FROM 'xxx.parquet';

-- 搜索
SELECT text
FROM 'xxx.parquet'
WHERE text ILIKE '%machine learning%'
LIMIT 50;
```

**关键点：** 不要仅仅为了检查而将 4.8 GB 的 Parquet 转换为 JSONL。你当前的转换：

```text
Parquet
   ↓
1,973,000 行
   ↓
JSONL
```

浪费了 Parquet 的许多优势。DuckDB 可以直接操作：

```text
Parquet
   ↓
DuckDB SQL
   ↓
GUI 表格
```

专门针对机器学习数据集，**DuckDB + DBeaver** 是我首先推荐的组合。