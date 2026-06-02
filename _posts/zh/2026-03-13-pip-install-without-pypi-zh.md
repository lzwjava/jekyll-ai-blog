---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么 pip install 无需 PyPI 也能工作
translated: true
type: note
---

有几个原因可以解释为什么 `pip install mini-copilot` 在本地可能即使没有发布到 PyPI 也能工作：

1. **Already published to PyPI** — 有人（可能是你）可能已经发布了它。你可以在 `https://pypi.org/project/mini-copilot/` 检查。

2. **Installed in editable mode** — 如果你在项目目录内运行了 `pip install -e .`，pip 会直接从你的本地源安装它。之后运行 `pip install mini-copilot` 只会发现它已经安装并报告成功。

3. **Local package index or cache** — pip 有本地缓存 (`~/.cache/pip`)。如果你之前从本地 wheel 或源安装了它，缓存版本可能会被重用。

4. **Different package with same name** — PyPI 上可能有一个不相关的 `mini-copilot` 包，刚好共享同一个名称。

要诊断，请运行：

```bash
pip show mini-copilot
```

它将显示 **Location** 和 **Home-page** 字段，精确告诉你 pip 从哪里获取的。如果位置指向你的本地项目目录，则是通过 `-e .` 安装的。
