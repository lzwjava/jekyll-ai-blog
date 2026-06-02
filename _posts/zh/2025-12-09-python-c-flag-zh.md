---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Python -c 命令行标志
translated: true
type: note
---

问题：如何使用 `python -c` 从命令行直接执行 Python 代码？

回答：

`-c` 标志允许你传递一个包含 Python 代码的字符串，该字符串将立即执行，而无需创建脚本文件。

### 基本语法

```bash
python -c "code_here"
# 或者明确使用 python3
python3 -c "code_here"
```

### 简单示例

```bash
# 打印内容
python -c "print('Hello, world!')"

# 进行数学运算
python -c "print(2 + 2 * 10)"

# 导入和使用模块
python -c "import math; print(math.sqrt(16))"

# 多条语句（使用分号或显式换行符）
python -c "import sys; print(sys.version); print('Platform:', sys.platform)"
```

### 处理引号和复杂代码

当你的代码包含引号或跨越多行时，你需要根据你的 shell 正确转义。

#### 单行内部包含单引号

```bash
python -c "print('Single quotes are fine inside double-quoted string')"
python -c 'import os; print("User home:", os.path.expanduser("~"))'
```

#### 多行代码（推荐方式）

使用 heredoc 或引用整个代码块：

```bash
python -c "
import json
data = {'name': 'Alice', 'age': 30}
print(json.dumps(data, indent=2))
"
```

或者使用单引号和转义的换行符：

```bash
python -c 'import antigravity
print("Flying to xkcd...")
'
```

#### 替代方法：使用 `\` 进行行连接 (bash/zsh)

```bash
python -c 'import sys, json; \
data = [line.strip() for line in sys.stdin]; \
print(json.dumps(data))'
```

### 你会实际使用的常用单行命令

```bash
# 列出当前目录中的所有文件（ls 的替代方法）
python -c "import os; print('\n'.join(os.listdir('.')))"

# 获取你的公共 IP
python -c "import urllib.request; print(urllib.request.urlopen('https://api.ipify.org').read().decode())"

# 快速 HTTP 服务器 (Python 3)
python -c "import http.server, socketserver; http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, Port=8000)"

# 生成一个范围并求和
python -c "print(sum(range(1, 101)))"  # 打印 5050
```

### 提示

- 始终将代码用引号括起来，以防止 shell 解释。
- 在 `python` 指向 Python 2 的系统上，使用 `python3` 而不是 `python`。
- 对于非常长的脚本，请考虑编写一个适当的 `.py` 文件。

就是这样！ `python -c` 非常适合快速计算、测试代码片段或在 shell 脚本中进行自动化。
