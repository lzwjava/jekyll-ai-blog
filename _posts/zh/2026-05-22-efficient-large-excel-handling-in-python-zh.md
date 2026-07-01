---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python中高效处理大型Excel
translated: true
type: note
---

**问题：** 如何使用 `polars`、`pyexcel`、`openpyxl` 等库让 Python 处理大型 Excel 文件？

**答案：**

大型 Excel 文件的核心问题在于内存和速度。`openpyxl` 默认会将所有内容加载到 RAM 中——一个 50 万行的 xlsx 文件就足以让 16GB 内存的机器内存耗尽。以下是按性能排序的方案概览：

---

## 库对比

| 库 | 最适合场景 | 内存 | 速度 |
| --- | --- | --- | --- |
| `polars` | 大型数据分析 | 低（惰性） | 最快 |
| `pandas` 分块读取 | 中等文件，熟悉的 API | 中等 | 中等 |
| `openpyxl` read_only 模式 | 只读流式处理 | 低 | 慢（纯 Python） |
| `calamine` / `fastexcel` | 快速读取为 arrow/polars 格式 | 极低 | 读取最快 |
| `xlrd` | 旧版 `.xls` 文件 | 低 | 快 |
| `pyexcel` | 多格式抽象 | 高 | 慢 |

`pyexcel` 是高级封装器——处理大文件时应避免使用，因为它不支持流式处理。

---

## 1. 最快方案：`fastexcel` + `polars`（推荐）

`fastexcel` 是一个基于 Rust 的读取器，原生输出 Apache Arrow 格式——近乎零拷贝地直接输入到 polars：

```python
pip install fastexcel polars
```

```python
import fastexcel
import polars as pl

# 将整个工作表读为 polars LazyFrame
reader = fastexcel.read_excel("large.xlsx")
print(reader.sheet_names)

df = reader.load_sheet(0).to_polars()  # 原生 Arrow，非常快
print(df.shape, df.dtypes)

# 在物化前进行过滤（下推优化）
result = (
    df.lazy()
    .filter(pl.col("amount") > 1000)
    .select(["id", "amount", "date"])
    .collect()
)
```

对于 100 万行的文件，这通常比 pandas **快 5-10 倍**，且 RAM 使用量减少约 3 倍。

---

## 2. `openpyxl` 流式处理（read_only 模式）

当必须使用 openpyxl 时（例如需要公式级别的访问），可以逐行流式读取：

```python
from openpyxl import load_workbook

wb = load_workbook("large.xlsx", read_only=True, data_only=True)
ws = wb.active

for i, row in enumerate(ws.iter_rows(values_only=True)):
    # 处理行元组——不会加载整个工作表
    if i % 100_000 == 0:
        print(f"Row {i}: {row[:3]}")

wb.close()  # 在 read_only 模式下必须显式关闭
```

**注意：** `read_only=True` 加上 `data_only=True` 会返回缓存的公式计算结果，而非重新计算的值。如果文件从未在 Excel 中打开过，公式单元格将返回 `None`。

---

## 3. pandas 分块读取

pandas 本身不支持对 xlsx 进行分块读取（与 CSV 不同），但可以通过模拟实现：

```python
import pandas as pd

# 通过 skiprows/nrows 分块读取
CHUNK = 50_000
df_iter = pd.read_excel(
    "large.xlsx",
    engine="calamine",   # 比 openpyxl 引擎更快
    chunksize=CHUNK      # 仅对 CSV 有效；xlsx 请使用 skiprows
)

# 手动分块处理 xlsx：
def read_excel_chunks(path, chunksize=50_000):
    nrows_total = pd.read_excel(path, usecols=[0], engine="calamine").shape[0]
    for start in range(0, nrows_total, chunksize):
        yield pd.read_excel(
            path,
            skiprows=range(1, start + 1),  # 跳过 header=0，然后是数据行
            nrows=chunksize,
            header=0 if start == 0 else None,
            engine="calamine"
        )

for chunk in read_excel_chunks("large.xlsx"):
    print(chunk.shape)
```

对于 CSV 文件，这很简单——直接使用 `pd.read_csv(..., chunksize=N)` 即可。

---

## 4. 用于 pandas 的 `python-calamine` 引擎

`calamine` 是另一个基于 Rust 的读取器，可作为 pandas 引擎使用：

```bash
pip install python-calamine
```

```python
import pandas as pd

df = pd.read_excel("large.xlsx", engine="calamine")
# 比默认的 openpyxl 引擎快约 3-5 倍
```

---

## 5. 写入大型文件：`xlsxwriter` > `openpyxl`

对于写入操作，`xlsxwriter` 支持常量内存模式：

```python
import xlsxwriter

wb = xlsxwriter.Workbook("output.xlsx", {"constant_memory": True})
ws = wb.add_worksheet()

for i in range(1_000_000):
    ws.write_row(i, 0, [i, i * 2, f"row_{i}"])

wb.close()
# 逐行流式写入磁盘——O(1) 内存占用
```

`openpyxl` 的 write_only 模式也能实现同样的效果：

```python
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()

for i in range(1_000_000):
    ws.append([i, i * 2, f"row_{i}"])  # 流式写入磁盘

wb.save("output.xlsx")
```

---

## 决策树

```
大型 xlsx 文件（>10 万行）？
├── 仅读取数据 → fastexcel + polars  ← 最佳默认选择
├── 需要 pandas API → pd.read_excel(engine="calamine")
├── 需要公式值/样式 → openpyxl read_only=True, iter_rows
├── 写入大型文件 → xlsxwriter constant_memory 或 openpyxl write_only
└── 旧版 .xls 格式 → xlrd（openpyxl 不支持 .xls）
```

---

## 快速基准测试参考

对于 100 万行 × 10 列：

- `fastexcel` → 约 2 秒，约 200MB RAM
- 通过 pandas 使用 `calamine` → 约 5 秒，约 400MB RAM
- `openpyxl` 默认模式 → 约 60 秒，约 2GB RAM
- `openpyxl` read_only 流式模式 → 约 30 秒，约 50MB RAM

您的 M2 Air（16GB）使用 calamine/fastexcel 可轻松处理约 50 万行。对于更大的文件，请使用 `read_only` 流式处理或先转存为 parquet 格式。

---

## 参考

- [fastexcel GitHub](https://github.com/ToucanToco/fastexcel)
- [python-calamine GitHub](https://github.com/dimastbk/python-calamine)
- [openpyxl 优化模式文档](https://openpyxl.readthedocs.io/en/stable/optimised.html)
- [xlsxwriter 常量内存](https://xlsxwriter.readthedocs.io/working_with_memory.html)
- [polars Excel 读取](https://docs.pola.rs/api/python/stable/reference/api/polars.read_excel.html)
