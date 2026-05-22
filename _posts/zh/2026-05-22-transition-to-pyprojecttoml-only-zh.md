---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仅过渡到 pyproject.toml
translated: true
type: note
---

是的，完全正确。既然你有 `pyproject.toml`，那么 `requirements.txt` 就是多余的。以下是操作计划：

1. **在 `pyproject.toml` 的 `[project].dependencies` 下添加 `piexif`**
2. **删除 `requirements.txt`**
3. **使用 `pip install .`（或 `pip install -e .` 用于可编辑/开发模式）进行安装**

`pip install -e .` 更适用于活跃开发——对源代码的更改会立即生效，无需重新安装。

如果你有仅用于开发的依赖（例如 `pyright`），则将其添加到以下部分：

```toml
[project.optional-dependencies]
dev = ["pyright"]
```

然后使用 `pip install -e ".[dev]"` 进行安装。

所以是的——删除 `requirements.txt`，将 `piexif` 添加到 `pyproject.toml`，并继续使用 `pip install -e .`。