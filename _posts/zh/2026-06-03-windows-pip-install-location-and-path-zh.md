---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows pip安装位置与PATH
translated: true
type: note
---

**问题：** 在 Windows 上，`pip install` 将包放置在何处？如何配置 PATH 以便直接运行安装的命令，而不是使用 `python -m`？

**答案：**

## pip 安装包的位置

在 Windows 上，`pip install` 将包放置在：

```
C:\Users\<用户名>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages\
```

或者如果你在虚拟环境中：

```
<venv-path>\Lib\site-packages\
```

## 可执行脚本的位置

当一个包安装了 CLI 工具（如 `black`、`pytest`、`numpy`），**可执行文件**会放在：

```
C:\Users\<用户名>\AppData\Local\Programs\Python\Python3xx\Scripts\
```

或者在虚拟环境中：

```
<venv-path>\Scripts\
```

## 为什么需要 PATH

默认情况下，Windows 不知道 `Scripts\` 在哪里。你有两个选择：

### 选项 1：将 Python Scripts 添加到系统 PATH（永久生效）

1. 找到你的 Python Scripts 路径：

```python
import site
import os
print(os.path.dirname(site.PREFIXES[0]))  # 显示 Python 根目录
# 然后 Scripts 位于：<root>\Scripts
```

2. 添加到系统 PATH：
   - Win+X → 系统 → 高级系统设置
   - 环境变量 → 编辑系统 PATH
   - 添加：`C:\Users\<用户名>\AppData\Local\Programs\Python\Python3xx\Scripts`
   - 重启终端

3. 现在可以直接运行命令：

```bash
black myfile.py
pytest
```

### 选项 2：使用 python -m（始终有效，无需设置）

```bash
python -m pip install black
python -m black myfile.py
python -m pytest
```

这之所以有效，是因为 `python.exe` 已经在 PATH 中，Python 会在内部找到模块。

## 验证是否生效

```bash
where pytest   # 显示 pytest 可执行文件的路径
pip show -f black  # 显示包及其脚本的安装位置
```

## 专业提示：使用虚拟环境

不要再与系统 PATH 较劲了。改用 venv：

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS/Linux
pip install black pytest
black .   # 现在在 venv 上下文中可以直接运行
```

当你激活一个 venv 时，它的 `Scripts\` 文件夹会自动添加到当前终端会话的 PATH 最前面。

---

**TL;DR：** `pip` 将包安装到 `site-packages\`（库存储），脚本安装到 `Scripts\`。将 `Scripts\` 添加到系统 PATH，或者使用虚拟环境，以免污染系统 Python。
