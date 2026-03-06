---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Black 缺少打包依赖
translated: true
type: note
---

**问题：** 为什么运行 `python -m black scripts` 会失败，报错 "ModuleNotFoundError: No module named 'packaging'"，尽管 black 已安装？

**答案：**

错误是因为 **black** 包已安装，但其 **dependencies** 之一——`packaging` 库——在当前 Python 环境中缺失。

这种情况最常见于：

- black 使用 `--no-deps` 安装（有意或由某些工具/脚本导致）
- 环境部分损坏 / 被清理
- black 通过某种不寻常的方法安装（例如 `python -m pip install --no-deps black`）
- 使用非常新的 Python 版本（例如您的 Python 3.14），某些 system/site-packages 状态变得不一致
- 存在多个 Python 安装，black 在其中一个中，但依赖项在您实际使用的解释器中缺失

### 快速修复（推荐）

```bash
# 重新安装 black + 所有其依赖项
python -m pip install --force-reinstall black

# 或者更干净的版本：
python -m pip uninstall black -y
python -m pip install black
```

大多数人使用这两个命令之一即可解决问题。

### 替代修复方法

1. 手动安装缺失的包（快速但粗糙）

```bash
python -m pip install packaging
```

→ 然后再次尝试 `python -m black scripts`

2. 如果怀疑环境混乱 / 使用了错误的 python

```bash
# 检查实际使用的 python 和 pip
which python
which pip
python --version
pip --version

# 确保它们匹配，否则使用完整路径：
python3.14 -m pip install --force-reinstall black
```

3. 如果您在虚拟环境中但忘记激活它

```bash
source .venv/bin/activate          # macOS/Linux
# or
.\.venv\Scripts\activate           # Windows
```

然后再次运行 `python -m pip install black`。

### 总结 – 最可能的原因及解决方案

| 情况                                   | 最可能的修复方法                               |
|----------------------------------------|--------------------------------------------------|
| 缺失依赖                               | `pip install packaging` 或重新安装 black        |
| 损坏 / 不完整的安装                    | `pip install --force-reinstall black`           |
| 错误的 Python 解释器                   | 使用 `python3.14 -m pip install black`          |
| 未激活 Virtualenv                      | 先激活 venv                                     |
| 使用 `--no-deps` 安装                  | 不带该标志重新安装                              |

在 macOS/homebrew + 近期 Python 的 95% 情况下，仅运行

```bash
python -m pip install --force-reinstall black
```

即可解决问题。

请先尝试这个，如果仍然失败请告诉我。