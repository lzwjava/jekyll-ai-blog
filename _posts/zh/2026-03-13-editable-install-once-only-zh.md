---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可编辑仅安装一次
translated: true
type: note
---

`pip install -e .` 只需要运行 **一次**。之后，代码更改会立即生效 — 只需再次运行 `mini-copilot`，无需重新安装（editable installs 会 symlink 到你的源代码）。

或者，完全跳过安装，直接运行：

```bash
python -m mini_copilot.main
```

这可以在项目目录下工作，无需任何安装步骤。