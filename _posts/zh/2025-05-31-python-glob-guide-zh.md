---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python Glob模块文件匹配指南
translated: true
type: note
---

### 导入 Glob 模块

要在 Python 中使用 glob，需从标准库中导入该模块：

```python
import glob
```

### 基础功能

`glob.glob()` 函数接收模式字符串，返回匹配的文件或目录路径列表。它使用 Unix shell 风格的通配符：

- `*`：匹配任意字符序列（路径分隔符除外）
- `?`：匹配任意单个字符
- `[seq]`：匹配 seq 中的任意字符（如 `[0-9]` 匹配数字）
- `**`：递归匹配目录（需设置 `recursive=True`）

除非指定绝对路径，否则模式将相对于当前目录进行匹配。

### 使用示例

#### 1. 查找当前目录下所有 .txt 文件

```python
import glob

files = glob.glob("*.txt")
print(files)  # 输出: ['file1.txt', 'file2.txt', ...]
```

#### 2. 在子目录中查找特定扩展名的文件

```python
files = glob.glob("documents/*.pdf")
print(files)  # 输出: ['documents/doc1.pdf', ...]
```

#### 3. 匹配特定模式（如以 'log' 开头且以数字结尾的文件）

```python
files = glob.glob("log[0-9].txt")
print(files)  # 输出: ['log1.txt', 'log2.txt', ...]（若存在此类文件）
```

#### 4. 在子目录中递归搜索

使用 `**` 并设置 `recursive=True` 可搜索目录及其子目录：

```python
files = glob.glob("**/*.py", recursive=True)
print(files)  # 输出: ['script1.py', 'subdir/script2.py', ...]
```

### 重要注意事项

- 默认返回结果未排序，如需排序可使用：`sorted(glob.glob("*.txt"))`
- 在区分大小写的文件系统中进行不区分大小写匹配时，建议结合 `fnmatch` 或在代码中处理，因为 glob 默认区分大小写
- 除非显式处理，否则 glob 不会跟踪符号链接；如需复杂遍历请使用 `os.walk()`
- 需要逐个匹配时，可使用返回迭代器的 `glob.iglob()` 以节省内存：`for file in glob.iglob("*.txt"): print(file)`

以上是核心功能概述，更多细节请参阅 [Python 官方文档](https://docs.python.org/3/library/glob.html)。
