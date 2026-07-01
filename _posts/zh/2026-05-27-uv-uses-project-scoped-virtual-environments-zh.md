---
audio: false
generated: true
image: false
lang: zh
layout: post
title: uv 使用项目范围的虚拟环境
translated: true
type: note
---

是的 — uv 是**项目级别的**，而非全局。它的工作原理如下：

```
~/projects/ww/          → 拥有自己的 .venv/
~/projects/uv/          → 拥有自己的 .venv/
```

当你在项目内运行 `uv sync` 或 `uv pip install -e .` 时，uv 会在该**项目目录中**创建/使用一个 `.venv/`。所有内容都在那里，不会触及你的全局 Python。

**关于 ww 项目的情况：**

```bash
cd ~/projects/ww
pip install -e .        # 安装到了某个虚拟环境（或全局——到底是哪个？）
```

问题是：那个 `pip install -e .` 指向的是哪个 Python/环境？

- 如果是在未激活虚拟环境的情况下运行 → 它进入了系统 Python（不好，全局污染）
- 如果当时有虚拟环境激活 → 它进入了那个环境

**uv 带来的改变：**

```bash
cd ~/projects/uv
uv sync                 # 在此处创建 .venv/，并从 uv.lock 安装依赖
```

这个 `.venv/` 是完全隔离的。不同项目可以拥有同一库的不同版本，没有冲突。

**理解模型：**

| 工具 | 作用域 | 依赖存放位置 |
| ------ | -------- | -------------- |
| `pip install`（无虚拟环境） | 全局 | 系统 site-packages |
| `pip install`（在虚拟环境中） | 项目 | `.venv/` |
| `uv sync` | 始终为项目 | `.venv/`（自动创建） |
| `uv pip install -e .` | 项目 | `.venv/` |

uv 更严格——它**始终**使用虚拟环境。如果不存在，它会创建一个。不会意外安装到全局。

**对于你的 ww 项目**，你可以迁移：

```bash
cd ~/projects/ww
uv sync    # 读取 pyproject.toml，创建 .venv，安装所有内容
```

之后就不再需要旧的 `pip install -e .` 了。`.venv/` 默认会被 git 忽略（uv 会自动将其添加到 `.gitignore` 中）。
