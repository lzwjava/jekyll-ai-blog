---
audio: false
generated: true
image: false
lang: en
layout: post
title: Efficient Large Excel Handling in Python
translated: false
type: note
---

**Question:** How can Python handle large Excel files using libraries like `polars`, `pyexcel`, `openpyxl`, etc.?

**Answer:**

The core problem with large Excel files is memory and speed. `openpyxl` loads everything into RAM by default — a 500k-row xlsx will OOM a 16GB machine. Here's the landscape ranked by performance:

---

## Library Comparison

| Library | Best For | Memory | Speed |
| --- | --- | --- | --- |
| `polars` | Large data analysis | Low (lazy) | Fastest |
| `pandas` chunked | Medium files, familiar API | Medium | Medium |
| `openpyxl` read_only | Read-only streaming | Low | Slow (pure Python) |
| `calamine` / `fastexcel` | Fast read into arrow/polars | Very Low | Fastest reads |
| `xlrd` | Old `.xls` | Low | Fast |
| `pyexcel` | Multi-format abstraction | High | Slow |

`pyexcel` is a high-level wrapper — avoid it for large files, it has no streaming.

---

## 1. Fastest: `fastexcel` + `polars` (recommended)

`fastexcel` is a Rust-backed reader that outputs Apache Arrow natively — feeding directly into polars with near-zero copy:

```python
pip install fastexcel polars
```

```python
import fastexcel
import polars as pl

# Read entire sheet as polars LazyFrame
reader = fastexcel.read_excel("large.xlsx")
print(reader.sheet_names)

df = reader.load_sheet(0).to_polars()  # Arrow-native, very fast
print(df.shape, df.dtypes)

# Filter before materializing (push-down)
result = (
    df.lazy()
    .filter(pl.col("amount") > 1000)
    .select(["id", "amount", "date"])
    .collect()
)
```

For a 1M-row file this is typically **5-10x faster** than pandas and uses ~3x less RAM.

---

## 2. `openpyxl` Streaming (read_only mode)

When you must use openpyxl (e.g. need formula-level access), stream rows:

```python
from openpyxl import load_workbook

wb = load_workbook("large.xlsx", read_only=True, data_only=True)
ws = wb.active

for i, row in enumerate(ws.iter_rows(values_only=True)):
    # Process row tuple — never loads full sheet
    if i % 100_000 == 0:
        print(f"Row {i}: {row[:3]}")

wb.close()  # MUST close explicitly in read_only mode
```

**Gotcha:** `read_only=True` + `data_only=True` returns cached formula values, not recalculated ones. If the file was never opened in Excel, formula cells return `None`.

---

## 3. pandas chunked reading

pandas doesn't natively chunk xlsx (unlike CSV), but you can simulate it:

```python
import pandas as pd

# Read in chunks via skiprows/nrows
CHUNK = 50_000
df_iter = pd.read_excel(
    "large.xlsx",
    engine="calamine",   # faster than openpyxl engine
    chunksize=CHUNK      # only works for CSV; for xlsx use skiprows
)

# Manual chunking for xlsx:
def read_excel_chunks(path, chunksize=50_000):
    nrows_total = pd.read_excel(path, usecols=[0], engine="calamine").shape[0]
    for start in range(0, nrows_total, chunksize):
        yield pd.read_excel(
            path,
            skiprows=range(1, start + 1),  # skip header=0, then data rows
            nrows=chunksize,
            header=0 if start == 0 else None,
            engine="calamine"
        )

for chunk in read_excel_chunks("large.xlsx"):
    print(chunk.shape)
```

For CSV this is trivial — just use `pd.read_csv(..., chunksize=N)`.

---

## 4. `python-calamine` engine for pandas

`calamine` is another Rust-backed reader, pluggable as a pandas engine:

```bash
pip install python-calamine
```

```python
import pandas as pd

df = pd.read_excel("large.xlsx", engine="calamine")
# ~3-5x faster than default openpyxl engine
```

---

## 5. Writing large files: `xlsxwriter` > `openpyxl`

For writing, `xlsxwriter` has a constant-memory mode:

```python
import xlsxwriter

wb = xlsxwriter.Workbook("output.xlsx", {"constant_memory": True})
ws = wb.add_worksheet()

for i in range(1_000_000):
    ws.write_row(i, 0, [i, i * 2, f"row_{i}"])

wb.close()
# Streams to disk row by row — O(1) memory
```

`openpyxl` write_only mode does the same:

```python
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()

for i in range(1_000_000):
    ws.append([i, i * 2, f"row_{i}"])  # streams to disk

wb.save("output.xlsx")
```

---

## Decision Tree

```
Large xlsx (>100k rows)?
├── Just reading data → fastexcel + polars  ← best default
├── Need pandas API → pd.read_excel(engine="calamine")
├── Need formula values/styles → openpyxl read_only=True, iter_rows
├── Writing large file → xlsxwriter constant_memory or openpyxl write_only
└── Old .xls format → xlrd (openpyxl doesn't support .xls)
```

---

## Quick benchmark mental model

For 1M rows × 10 cols:

- `fastexcel` → ~2s, ~200MB RAM
- `calamine` via pandas → ~5s, ~400MB RAM
- `openpyxl` default → ~60s, ~2GB RAM
- `openpyxl` read_only streaming → ~30s, ~50MB RAM

Your M2 Air (16GB) will handle up to ~500k rows fine with calamine/fastexcel. For anything bigger, stream with `read_only` or dump to parquet first.

---

## References

- [fastexcel GitHub](https://github.com/ToucanToco/fastexcel)
- [python-calamine GitHub](https://github.com/dimastbk/python-calamine)
- [openpyxl optimised modes docs](https://openpyxl.readthedocs.io/en/stable/optimised.html)
- [xlsxwriter constant memory](https://xlsxwriter.readthedocs.io/working_with_memory.html)
- [polars Excel reading](https://docs.pola.rs/api/python/stable/reference/api/polars.read_excel.html)
