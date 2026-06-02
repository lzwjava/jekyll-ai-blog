---
audio: false
generated: true
lang: en
layout: post
title: Python Script to Double Row
translated: false
type: note
---

Here's the updated Python script modified to work with .xlsx files instead of .xls files. It uses `openpyxl` for handling .xlsx files, keeps the same functionality of repeating values in the third row based on the provided parameter, and saves the output to a new .xlsx file with "_plus.xlsx" appended to the original filename. The artifact_id is reused since this is an update to the previous artifact.

```python
import pandas as pd
import argparse
import os

def repeat_value(value, n):
    return str(value) * n

def process_excel(input_file, n):
    df = pd.read_excel(input_file, engine='openpyxl')
    if len(df) < 3:
        raise ValueError("Excel file must have at least 3 rows")
    third_row = df.iloc[2].apply(lambda x: repeat_value(x, n))
    df.iloc[2] = third_row
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_plus.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Processed file saved as: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Double values in the third row of an Excel file")
    parser.add_argument("input_file", help="Path to the input Excel (.xlsx) file")
    parser.add_argument("-n", type=int, default=1, help="Number of times to repeat each value (default: 1)")
    args = parser.parse_args()
    process_excel(args.input_file, args.n)

if __name__ == "__main__":
    main()
```
