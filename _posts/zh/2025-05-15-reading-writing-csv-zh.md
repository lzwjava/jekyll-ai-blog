---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 读写CSV文件
translated: true
type: note
---

### Python `csv` 模块简介

`csv` 模块是 Python 标准库的一部分，用于读写 CSV（逗号分隔值）文件。它能高效解析行和列数据。使用时需先导入模块：`import csv`。通常需要配合文件对象进行操作，一般以读取模式（`'r'`）或写入模式（`'w'`）打开文件。

核心组件：
- **读取器**：解析 CSV 文件数据（例如 `csv.reader()` 实现按行访问）
- **写入器**：将数据输出到 CSV 文件（例如 `csv.writer()`）
- CSV 文件被视为行序列，每行是由字符串组成的列表（列）

为确保安全性和便捷性，建议始终使用 `with` 语句处理文件，以保证正确关闭。

### 基础 CSV 文件读取

读取 CSV 文件的方法：
```python
import csv

with open('file.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)  # 每个 'row' 是包含列数据的列表
```
- 逐行读取文件，可通过索引访问特定列（例如 `row[0]` 获取第一列）
- 处理表头时，可单独读取首行：`headers = next(reader)`

### 双 CSV 文件行列对比

比较两个 CSV 文件（如 `file1.csv` 和 `file2.csv`）时，可将其加载为列表结构（行列表），然后进行对比。前提条件：两个 CSV 结构相同（列数/行数一致）。比较时可检查完全匹配、差异或特定逻辑（例如按关键列匹配）。

#### 示例1：整行对比
使用字典存储行数据（若存在唯一标识列），或直接使用列表进行对比。

```python
import csv

def compare_rows(file1, file2, key_column=0):
    # 将 file1 读取到字典（以 key_column 为键，整行数据为值）
    data1 = {}
    with open(file1, 'r') as f1:
        reader1 = csv.reader(f1)
        headers1 = next(reader1, None)  # 跳过表头（如果存在）
        for row in reader1:
            data1[row[key_column]] = row  # 例如以首列作为键

    # 同理读取 file2
    data2 = {}
    with open(file2, 'r') as f2:
        reader2 = csv.reader(f2)
        headers2 = next(reader2, None)
        for row in reader2:
            data2[row[key_column]] = row

    # 执行对比
    common_keys = set(data1.keys()) & set(data2.keys())
    differing_rows = []
    for key in common_keys:
        if data1[key] != data2[key]:
            differing_rows.append((key, data1[key], data2[key]))

    return differing_rows  # 返回（键, file1行数据, file2行数据）元组列表

# 使用示例
differences = compare_rows('file1.csv', 'file2.csv', key_column=0)  # 以第0列为键
print("差异行：", differences)
```

- **实现原理**：将 CSV 转换为按指定列（如 ID 列）键控的字典，直接对比匹配行。通过调整 `key_column` 参数指定键控列。
- **变体方案**：若需无键逐行对比，可同步遍历两个读取器（需确保顺序和长度一致）。

#### 示例2：列数据对比
对比两个文件中特定列的全量数据（例如检查两个文件第1列值是否完全一致）。

```python
import csv

def compare_columns(file1, file2, col_index=0):
    # 提取列数据到列表
    col1 = []
    with open(file1, 'r') as f1:
        reader1 = csv.reader(f1)
        next(reader1, None)  # 跳过表头（如需）
        for row in reader1:
            if len(row) > col_index:
                col1.append(row[col_index])

    col2 = []
    with open(file2, 'r') as f2:
        reader2 = csv.reader(f2)
        next(reader2, None)
        for row in reader2:
            if len(row) > col_index:
                col2.append(row[col_index])

    # 执行列对比
    are_equal = col1 == col2
    differences = []
    for i, (val1, val2) in enumerate(zip(col1, col2)):
        if val1 != val2:
            differences.append((i, val1, val2))

    return are_equal, differences  # 返回匹配状态和（行索引, 值1, 值2）元组列表

# 使用示例
equal, diffs = compare_columns('file1.csv', 'file2.csv', col_index=1)  # 对比第1列
print("列数据是否一致？", equal)
print("差异详情（行号, 值1, 值2）：", diffs)
```

- **实现原理**：将指定列数据提取至列表后进行逐元素对比。假设两个 CSV 行数相同，如存在行数差异需额外处理。
- **变体方案**：需进行高级列操作时可使用 `pandas`（例如 `df1['column'] == df2['column']`），但纯标准库方案建议坚持使用 `csv` 模块。

#### 技巧与边界情况
- **表头处理**：若 CSV 含表头，使用 `next(reader)` 跳过
- **数据类型**：CSV 默认以字符串格式读取，需要时可转换类型（例如 `int(row[0])`）
- **大文件处理**：处理大型 CSV 时建议使用 DictReader 进行键控访问：`csv.DictReader(file)` 返回 OrderedDict 格式的行数据
- **分隔符**：非逗号分隔文件需在 reader/writer 中指定 `delimiter=';'`
- **异常处理**：使用 try-except 处理文件问题，验证列长度避免索引错误
- **替代方案**：复杂对比场景可考虑 `pandas` 库（例如通过 `df1.equals(df2)` 对比数据框）

完整文档请参阅 [Python 官方 csv 模块指南](https://docs.python.org/3/library/csv.html)。如有具体 CSV 文件或对比逻辑需求，提供更多细节可获取定制化代码方案！
