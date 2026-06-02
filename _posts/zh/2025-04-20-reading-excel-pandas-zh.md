---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用Pandas读取Excel文件
translated: true
type: note
---

### 前置准备
要在 Python 中读取 Excel 文件，你需要安装 `pandas` 库及相应的 Excel 引擎。若未安装 pandas，请执行：
```
pip install pandas
```
对于新版 Excel 格式 (.xlsx)，请安装 `openpyxl`：
```
pip install openpyxl
```
对于 .xls 格式文件，请使用 `xlrd`：
```
pip install xlrd
```

### 基础用法
Pandas 提供 `pd.read_excel()` 函数将 Excel 数据加载至 DataFrame。

1. 导入 pandas：
   ```python
   import pandas as pd
   ```

2. 读取 Excel 文件（需指定文件路径）：
   ```python
   df = pd.read_excel('路径/至/你的/文件.xlsx')
   ```
   - 默认加载第一个工作表
   - 返回结果为包含 Excel 数据的 DataFrame

3. 查看数据：
   ```python
   print(df.head())  # 查看前5行数据
   print(df.info())  # 获取列信息与数据类型概览
   ```

### 高级选项
- **指定工作表**：使用 `sheet_name` 参数（默认为0即首个工作表）：
  ```python
  df = pd.read_excel('文件.xlsx', sheet_name='Sheet2')  # 按名称指定
  df = pd.read_excel('文件.xlsx', sheet_name=1)         # 按索引指定（从0开始）
  ```
- **读取多工作表**：传入列表或 `None` 可加载所有工作表为字典：
  ```python
  all_sheets = pd.read_excel('文件.xlsx', sheet_name=None)  # 返回以工作表名称为键的字典
  ```
- **指定数据范围**：使用 `usecols` 选择列（如 `'A:C'` 表示 A 到 C 列），`skiprows` 跳过起始行：
  ```python
  df = pd.read_excel('文件.xlsx', usecols='A,C,E', skiprows=2)
  ```
- **处理表头**：若表头不在首行，可通过 `header` 参数指定：
  ```python
  df = pd.read_excel('文件.xlsx', header=1)  # 表头位于第1行（基于0的索引）
  ```
- **设置索引**：使用 `index_col` 将指定列设为索引：
  ```python
  df = pd.read_excel('文件.xlsx', index_col='列名称')
  ```

### 示例
假设存在名为 `sales.xlsx` 的 Excel 文件，其中包含名为 "Data" 的销售数据工作表。

```python
import pandas as pd

# 读取指定工作表
df = pd.read_excel('sales.xlsx', sheet_name='Data')

# 显示 DataFrame
print(df)

# 如需保存为 CSV 文件
df.to_csv('sales.csv', index=False)
```

更多详细信息请参阅 [pandas 官方文档关于 read_excel 的说明](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)。若遇到错误，请检查 Excel 文件格式并确保已安装所需依赖包。
