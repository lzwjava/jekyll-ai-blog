---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Python Subprocess 模块指南
translated: true
type: note
---

问题：如何在 Python 中使用 `subprocess` 模块运行命令？

回答：

Python 中的 `subprocess` 模块允许您生成新进程、连接到它们的输入/输出/错误管道，并获取它们的返回码。推荐的高级函数（在 Python 3.5 中引入）是 `subprocess.run()`，它运行一个命令并等待其完成。

### 基本用法

导入模块并调用 `subprocess.run()`，将命令作为字符串列表（出于安全考虑首选）或单个字符串。

```python
import subprocess

# 简单命令：列出文件（类 Unix 系统）
result = subprocess.run(["ls", "-l"])

# 在 Windows 上：等同于 dir
# result = subprocess.run(["dir"])
```

默认情况下，这将运行命令并将输出打印到控制台。该函数返回一个 `CompletedProcess` 对象，其中包含 `returncode` 等属性（0 通常表示成功）。

### 捕获输出

要捕获标准输出（以及可选的标准错误）：

```python
import subprocess

result = subprocess.run(["ls", "-l"], capture_output=True, text=True)

print(result.stdout)  # 以字符串形式输出
print(result.stderr)  # 错误输出（如果有）
print(result.returncode)  # 退出状态
```

- `capture_output=True`：捕获标准输出和标准错误。
- `text=True`：将输出作为字符串返回（而不是字节）。

### 处理错误

使用 `check=True` 以在命令失败（非零返回码）时引发异常：

```python
try:
    subprocess.run(["ls", "nonexistent_file"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with code {e.returncode}")
```

### 提供输入

将数据传递给命令的标准输入：

```python
result = subprocess.run(["grep", "search_term"], input="line1\nsearch_term here\nline3", text=True, capture_output=True)
print(result.stdout)
```

### 使用 Shell 功能

对于 shell 内置命令、管道或通配符，设置 `shell=True`（但请谨慎处理不受信任的输入，因为存在安全风险）：

```python
result = subprocess.run("ls -l | grep .py", shell=True, capture_output=True, text=True)
```

在可能的情况下，为了安全起见，优先使用不带 `shell=True` 的列表形式。

对于更高级的控制（例如，流式传输或超时），请使用 `subprocess.Popen()`，但 `run()` 涵盖了大多数常见情况。

参考：

- [Python 官方文档：subprocess — Subprocess management](https://docs.python.org/3/library/subprocess.html)
- [An Introduction to Python Subprocess: Basics and Examples | DataCamp](https://www.datacamp.com/tutorial/python-subprocess)
- [The subprocess Module: Wrapping Programs With Python – Real Python](https://realpython.com/python-subprocess/)
