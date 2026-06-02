---
audio: false
generated: true
lang: zh
layout: post
title: Python脚本实现行复制
translated: true
type: note
---

这是更新后的Python脚本，已修改为适用于.xlsx文件而非.xls文件。该脚本使用`openpyxl`处理.xlsx文件，保留基于参数重复第三行数值的原有功能，并将输出保存到新.xlsx文件（在原文件名后追加"_plus.xlsx"）。由于这是对先前成品的更新，因此复用原有工件ID。

```python
import pandas as pd
import argparse
import os

def repeat_value(value, n):
    return str(value) * n

def process_excel(input_file, n):
    df = pd.read_excel(input_file, engine='openpyxl')
    if len(df) < 3:
        raise ValueError("Excel文件必须至少包含3行")
    third_row = df.iloc[2].apply(lambda x: repeat_value(x, n))
    df.iloc[2] = third_row
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_plus.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"处理后的文件已保存为: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="重复Excel文件第三行的数值")
    parser.add_argument("input_file", help="输入Excel文件(.xlsx)路径")
    parser.add_argument("-n", type=int, default=1, help="数值重复次数（默认值: 1）")
    args = parser.parse_args()
    process_excel(args.input_file, args.n)

if __name__ == "__main__":
    main()
```
