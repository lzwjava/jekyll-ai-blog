---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Python 3.14 命令行基础导论
translated: true
type: note
---

这是来自 Python 3.14 的帮助输出，显示了运行 Python 时所有可用的命令行选项。以下是其中最常用部分的解析：

## Common Usage Patterns

**运行 Python：**

- `python file.py` - 执行脚本
- `python -m module` - 将 module 作为脚本运行（例如 `python -m pip install package`）
- `python -c "code"` - 执行单条命令
- `python` - 启动 interactive mode

## Key Options You'll Actually Use

**`-m mod`** - 将库 module 作为脚本运行。这是运行 pip、venv 或 http.server 等工具的方式：

```bash
python -m pip install requests
python -m venv myenv
python -m http.server 8000
```

**`-i`** - 脚本运行后进入 interactive 模式。非常适合 debugging —— 脚本运行结束后，你会进入到一个保留了所有变量的 interactive prompt。

**`-c cmd`** - 执行单行脚本：

```bash
python -c "print('Hello')"
```

**`-u`** - Unbuffered output。在对 Python 输出进行重定向或在 Docker 中运行时非常有用，可以让你立即看到 print 的内容。

**`-B`** - 不写入 `.pyc` 文件。在开发过程中保持目录整洁。

**`-I`** - Isolation mode。忽略环境变量和 user site-packages —— 适用于需要 reproducible environments 的场景。

## Optimization Options

**`-O`** - 移除 assert 语句和 `__debug__` 检查
**`-OO`** - 在此基础上进一步移除 docstrings 以节省内存

## The Proxy Notice

顶部的 `🚀 Proxy Settings Detected` 并非来自 Python 本身 —— 它来自你的 shell environment，显示 HTTP/HTTPS 流量正通过 `127.0.0.1:7890`（通常是 VPN 或代理工具）进行路由。

大多数开发者平时只会用到其中的 3-4 个选项。在日常使用中，`-m` flag 可能是最常用的。
