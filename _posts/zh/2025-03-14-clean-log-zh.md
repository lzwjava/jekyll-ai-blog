---
audio: false
generated: true
lang: zh
layout: post
title: 清理日志信息
translated: true
type: note
---

```python
import sys
import argparse
from difflib import SequenceMatcher

def clean_log(input_path=None, output_path=None, similarity_threshold=1.0, lines_to_compare=1):
    """
    读取日志文件，基于相似度移除重复的连续标准日志行，
    并将清理后的日志写入指定文件，默认覆盖输入文件。

    参数:
        input_path (str, 可选): 输入日志文件路径。如果为None，则从stdin读取。
        output_path (str, 可选): 输出日志文件路径。如果为None，则覆盖输入文件。
        similarity_threshold (float, 可选): 判定行重复的相似度比率(0.0到1.0)。默认为1.0(精确匹配)。
        lines_to_compare (int, 可选): 要比较的连续行数。默认为1。
    """

    if not isinstance(lines_to_compare, int) or lines_to_compare < 1:
        raise ValueError("lines_to_compare必须为大于等于1的整数。")

    # 确定输入源
    if input_path:
        try:
            with open(input_path, 'r') as infile:
                lines = infile.readlines()
        except FileNotFoundError:
            print(f"错误: 在路径未找到文件: {input_path}", file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()  # 从stdin读取所有行

    # 确定输出目标
    if output_path:
        try:
            outfile = open(output_path, 'w')
        except IOError:
            print(f"错误: 无法打开文件进行写入: {output_path}", file=sys.stderr)
            sys.exit(1)
    elif input_path:
        try:
            outfile = open(input_path, 'w')  # 覆盖输入文件
        except IOError:
            print(f"错误: 无法打开文件进行写入: {input_path}", file=sys.stderr)
            sys.exit(1)
    else:
        outfile = sys.stdout  # 如果没有input_path，默认输出到stdout

    num_lines = len(lines)
    i = 0
    removed_lines = 0
    while i < num_lines:
        # 收集'lines_to_compare'行，如果剩余行数不足则收集剩余行
        current_lines = lines[i:min(i + lines_to_compare, num_lines)]

        # 只有在有足够行数进行比较时才处理
        if len(current_lines) == lines_to_compare:
            # 从第一组行中提取标准信息
            current_standards = []
            all_standard = True
            for line in current_lines:
                parts = line.split(" | ", 3)
                if len(parts) == 4:
                    level, _, thread, message = parts
                    current_standards.append((thread, message))
                else:
                    print(f"非标准行: {line.strip()}")
                    print(line, end='', file=outfile)
                    all_standard = False
                    break  # 如果找到非标准行，停止处理该组

            if all_standard:
                # 从第二组行中提取标准信息(如果可用)
                next_lines_start_index = i + lines_to_compare
                next_lines_end_index = min(next_lines_start_index + lines_to_compare, num_lines)
                next_lines = lines[next_lines_start_index:next_lines_end_index]

                if len(next_lines) == lines_to_compare:
                    next_standards = []
                    for line in next_lines:
                        parts = line.split(" | ", 3)
                        if len(parts) == 4:
                            level, _, thread, message = parts
                            next_standards.append((thread, message))
                        else:
                            # 如果任何下一行是非标准的，则将下一组行视为非标准
                            next_standards = None
                            break

                    if next_standards:
                        similarity = SequenceMatcher(None, ' '.join([' '.join(x) for x in current_standards]), ' '.join([' '.join(x) for x in next_standards])).ratio()
                        print(f"相似度: {similarity:.4f}, 阈值: {similarity_threshold:.4f}")

                        if similarity < similarity_threshold:
                            for line in current_lines:
                                print(line, end='', file=outfile)
                        else:
                            print(f"跳过重复行: { ''.join([line.strip() for line in current_lines])}")
                            removed_lines += len(current_lines)
                    else:
                        for line in current_lines:
                            print(line, end='', file=outfile)
                else:
                    for line in current_lines:
                        print(line, end='', file=outfile)
            i += lines_to_compare  # 移动到下一组行
        else:
            # 处理剩余行(少于'lines_to_compare'行)
            for line in current_lines:
                parts = line.split(" | ", 3)
                if len(parts) == 4:
                    print(line, end='', file=outfile)
                else:
                    print(f"非标准行: {line.strip()}")
                    print(line, end='', file=outfile)
            i += len(current_lines)

    if output_path or input_path:
        outfile.close()

    print(f"移除了{removed_lines}个重复行。")


def is_valid_similarity_threshold(value):
    """
    检查给定值是否为有效的相似度阈值。
    """
    try:
        value = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("相似度阈值必须为浮点数。")
    if 0.0 <= value <= 1.0:
        return value
    else:
        raise argparse.ArgumentTypeError("相似度阈值必须在0.0到1.0之间。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从文件或stdin中清理重复日志行并写入文件，默认覆盖输入文件。")
    parser.add_argument("input_path", nargs="?", type=str, help="输入日志文件路径(可选，默认为stdin)")
    parser.add_argument("-o", "--output_path", type=str, help="输出日志文件路径(可选，默认为覆盖输入文件)")
    parser.add_argument("-s", "--similarity", type=is_valid_similarity_threshold, default=1.0, help="判定行重复的相似度阈值(0.0-1.0)(默认: 1.0)")
    parser.add_argument("-l", "--lines", type=int, default=1, help="要比较的连续行数(默认: 1)")

    args = parser.parse_args()

    clean_log(args.input_path, args.output_path, args.similarity, args.lines)
```

这个Python脚本`clean_log.py`旨在从文件或标准输入中移除重复的日志行。它使用相似度阈值来确定连续的日志行是否足够相似以被视为重复。

以下是代码的详细说明：

**1. 导入模块:**

- `sys`: 用于与Python解释器交互，例如从stdin读取和向stderr写入。
- `argparse`: 用于创建命令行界面。
- `difflib.SequenceMatcher`: 用于比较字符串序列之间的相似度。

**2. `clean_log`函数:**

- 接受`input_path`、`output_path`、`similarity_threshold`和`lines_to_compare`作为参数。
- `input_path`: 指定输入日志文件。如果为`None`，则从stdin读取。
- `output_path`: 指定输出文件。如果为`None`且给出了`input_path`，则覆盖输入文件。如果两者都为`None`，则写入stdout。
- `similarity_threshold`: 介于0.0和1.0之间的浮点数，确定将行视为重复的最小相似度比率。值为1.0表示仅移除完全相同的行。
- `lines_to_compare`: 指定要比较相似度的连续行数的整数。

- **输入处理:**
    - 从输入文件或stdin读取行。
    - 如果输入文件不存在，处理`FileNotFoundError`。

- **输出处理:**
    - 打开输出文件进行写入或使用stdout。
    - 如果无法打开输出文件，处理`IOError`。

- **重复移除逻辑:**
    - 以`lines_to_compare`为块大小迭代日志文件的行。
    - 对于每个块:
        - 基于" | "分隔符将每行拆分为部分，期望四个部分：级别、时间戳、线程和消息。
        - 如果一行没有四个部分，则被视为"非标准"行，并在不比较的情况下打印到输出。
        - 如果当前块中的所有行都是标准的，则将其与下一个`lines_to_compare`行进行比较。
        - 使用`SequenceMatcher`计算当前块和下一个块的线程和消息部分的连接字符串之间的相似度比率。
        - 如果相似度比率小于`similarity_threshold`，则将当前块的行打印到输出。
        - 如果相似度比率大于或等于`similarity_threshold`，则将当前块的行视为重复并跳过。
    - 处理文件末尾的剩余行(少于`lines_to_compare`行)。

- **统计信息:**
    - 跟踪已移除的行数。
    - 将已移除的行数打印到控制台。

- **文件关闭:**
    - 如果打开了输出文件，则关闭它。

**3. `is_valid_similarity_threshold`函数:**

- 由`argparse`使用的辅助函数，用于验证相似度阈值参数。
- 检查输入值是否为介于0.0和1.0之间的浮点数。

**4. `if __name__ == "__main__":`块:**

- 当脚本从命令行运行时执行此块。
- 使用`argparse`创建命令行参数解析器。
- 定义以下参数:
    - `input_path`: 输入日志文件路径(可选)。
    - `-o`或`--output_path`: 输出日志文件路径(可选)。
    - `-s`或`--similarity`: 相似度阈值(默认: 1.0)。
    - `-l`或`--lines`: 要比较的行数(默认: 1)。
- 使用`parser.parse_args()`解析命令行参数。
- 使用解析后的参数调用`clean_log`函数。

**总之，该脚本提供了一种灵活的方式来清理日志文件，通过基于可配置的相似度阈值和要比较的行数来移除重复行。它支持从stdin读取、写入stdout以及覆盖输入文件。**
