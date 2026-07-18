---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM驱动的ww帮助
translated: true
type: note
---

完成。以下是实现的内容：

**新命令：`ww help <文件路径>`**

它使用 LLM（`deepseek/deepseek-v4-flash`）读取模块文件，查找其在 `main.py` 中的连接方式，并告诉你应该使用的具体 `ww` 命令。

```
ww help ww/gcp_speech/transcribe.py
ww help ww/ffmpeg/merge.py
ww help ~/projects/ww/ww/display/appearance.py
```

**修改的文件：**

- **`ww/help_llm/help.py`**（新增）——帮助模块：读取目标文件 + 扫描 `main.py` 中对应的导入/连接方式，将两者发送给 LLM，打印解释说明
- **`ww/help_llm/__init__.py`**（新增）——空包初始化文件
- **`ww/main.py`**——将 `help` 添加为独立命令组（`ww help <路径>` → LLM 帮助，`ww help` → 原有帮助；`--help`/`-h` 仍显示原有帮助页面不变）
- **`~/.zsh/completions/_ww`**——在命令列表和分发处理中添加了 `help`（Tab 键可补全文件路径）
