---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python包导入提取器
translated: true
type: note
---

### 提取所有导入包的 Python 脚本

该脚本遍历指定目录及其子目录，查找所有 Python 文件（`.py`），使用 Python 的 `ast` 模块（用于安全、语法感知解析）解析其导入语句，并累积所有唯一的基础模块名称（例如，从 `import os` 中提取 `os`，或从 `from collections import defaultdict` 中提取 `collections`）。它会忽略内置模块，专注于外部模块。

将此脚本保存为 `.py` 文件（例如 `extract_imports.py`），并以目录路径作为参数运行，例如 `python extract_imports.py /path/to/directory`。

```python
import os
import ast
import sys

def extract_imports_from_file(file_path):
    """
    解析 Python 文件并提取导入的模块名称。
    处理 'import mod' 和 'from mod import item' 两种形式。
    """
    modules = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split('.')[0])  # 获取基础模块（例如 'import os.path' -> 'os'）
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split('.')[0])  # 从 'from mod.sub import ...' 中获取基础模块
    except Exception as e:
        print(f"解析 {file_path} 时出错: {e}")

    return modules

def get_all_imported_modules(directory):
    """
    遍历目录和子目录，收集所有唯一的导入模块。
    """
    all_modules = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                modules = extract_imports_from_file(file_path)
                all_modules.update(modules)

    # 排除常见内置模块（可选，因为它们很少是外部包）
    excluded = {'sys', 'os', 're', 'math', 'random', 'json', 'time', 'datetime', 'collections', 'itertools', 'functools'}
    all_modules -= excluded

    return sorted(all_modules)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python extract_imports.py <目录路径>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"错误: {directory} 不是有效目录。")
        sys.exit(1)

    modules = get_all_imported_modules(directory)
    print("所有唯一的导入包:")
    for mod in modules:
        print(mod)
```

### 工作原理
- **目录遍历**：使用 `os.walk` 递归访问所有子目录和文件。
- **文件过滤**：仅处理 `.py` 文件。
- **导入解析**：使用 `ast` 安全解析源代码并识别 `Import` 和 `ImportFrom` 节点。通过 `.` 分割以捕获顶级模块（例如，从 `import numpy.linalg` 中提取 `numpy`）。
- **累积收集**：将模块收集到集合中以确保唯一性，然后排序并打印。
- **边缘情况处理**：跳过内置模块（可自定义 `excluded` 集合），优雅处理语法错误，并支持 Unicode 文件。
- **输出结果**：排序后的唯一包名称列表。如果在您自己的项目目录上运行，它将列出需要安装的包，如 `requests`、`pandas` 等。

这种方法对于代码库分析非常高效，并且避免了执行可能不安全的代码。如果您需要改进（例如，以不同方式处理相对导入或生成 requirements.txt），请提供更多详细信息！
