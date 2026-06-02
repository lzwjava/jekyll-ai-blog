---
audio: false
generated: true
lang: zh
layout: post
title: 单行CSV数据对比
translated: true
type: note
---

以下是一个 Python 脚本，用于比较两个包含字符串（例如 "P0001"）的单行 CSV 文件，并识别：
- 共有项（同时存在于两个文件中）
- 第一个文件独有的项
- 第二个文件独有的项

该脚本使用 `argparse` 来接收两个 CSV 文件路径，读取每个文件的第一行，执行基于集合的比较，并将结果写入 `comparison.txt`。

```python
#!/usr/bin/env python3
import argparse
import csv
import os

def main():
    # 设置参数解析器
    parser = argparse.ArgumentParser(description='比较两个单行CSV文件的共有项和独有项')
    parser.add_argument('file1_path', help='第一个CSV文件的路径')
    parser.add_argument('file2_path', help='第二个CSV文件的路径')

    # 解析参数
    args = parser.parse_args()

    try:
        # 读取第一个CSV文件的第一行
        with open(args.file1_path, 'r') as file1:
            reader1 = csv.reader(file1)
            for row in reader1:
                values1 = row
                break

        # 读取第二个CSV文件的第一行
        with open(args.file2_path, 'r') as file2:
            reader2 = csv.reader(file2)
            for row in reader2:
                values2 = row
                break

        # 转换为集合进行比较
        set1 = set(values1)
        set2 = set(values2)

        # 查找共有项和独有项
        common_items = set1.intersection(set2)
        unique_to_file1 = set1.difference(set2)
        unique_to_file2 = set2.difference(set1)

        # 确定输出目录（使用第一个文件的目录）
        output_dir = os.path.dirname(args.file1_path) or '.'
        output_file = os.path.join(output_dir, 'comparison.txt')

        # 将结果写入输出文件
        with open(output_file, 'w') as file:
            file.write("比较结果：\n\n")

            file.write("共有项（同时存在于两个文件）：\n")
            if common_items:
                for item in sorted(common_items):
                    file.write(f"{item}\n")
            else:
                file.write("无\n")

            file.write("\n仅存在于第一个文件的项：\n")
            if unique_to_file1:
                for item in sorted(unique_to_file1):
                    file.write(f"{item}\n")
            else:
                file.write("无\n")

            file.write("\n仅存在于第二个文件的项：\n")
            if unique_to_file2:
                for item in sorted(unique_to_file2):
                    file.write(f"{item}\n")
            else:
                file.write("无\n")

        print(f"比较完成。结果已保存至 {output_file}")

    except FileNotFoundError as e:
        print(f"错误：文件未找到 - {e}")
    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()
```

### 工作原理：
1. **输入**：通过命令行参数接收两个 CSV 文件路径。
2. **读取**：仅读取每个 CSV 文件的第一行。
3. **比较**：
   - 将行转换为集合以进行高效比较。
   - 查找：
     - **共有项**：同时存在于两行的项（集合交集）。
     - **第一个文件独有项**：仅存在于第一行的项（集合差集：文件1 - 文件2）。
     - **第二个文件独有项**：仅存在于第二行的项（集合差集：文件2 - 文件1）。
4. **输出**：将结果写入第一个文件所在目录的 `comparison.txt`，列出：
   - 共有项
   - 仅存在于第一个文件的项
   - 仅存在于第二个文件的项
   - 每个部分按字母顺序排序；如果某部分为空，则写入"无"。
5. **错误处理**：捕获文件未找到错误和其他异常。

### 使用示例：
将脚本保存为 `compare_csv.py`。创建两个 CSV 文件，例如：
- `file1.csv`：`P0001,P0002,P0003`
- `file2.csv`：`P0001,P0004,P0003`

运行脚本：
```
python compare_csv.py file1.csv file2.csv
```

**输出**（`comparison.txt`）：
```
比较结果：

共有项（同时存在于两个文件）：
P0001
P0003

仅存在于第一个文件的项：
P0002

仅存在于第二个文件的项：
P0004
```

### 注意事项：
- 该脚本忽略项的位置，仅关注存在/不存在。
- 自动处理行中的重复项（集合会移除重复项）。
- 输出写入到第一个输入文件所在目录的 `comparison.txt`。
- 如果文件为空或没有行，脚本将视其为空集合。

您是否需要我修改脚本（例如更改输出格式或添加更多细节）？
