---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 按条件加载环境变量
translated: true
type: note
---

已修复。以下是我在 ~/.hermes/plugins/note/init.py 中的更改：

    python
    加载 ww 的 .env 文件，使 LLM 调用无需 shell 级环境变量也能正常工作
    try:
        from dotenv import load_dotenv
        load_dotenv(Path.home() / "projects" / "ww" / ".env", override=False)
    except ImportError:
        pass


    关键细节：override=False —— 如果你已经在 shell 中设置了 MODEL 变量，它不会被覆盖。它只从 ww 的 .env 中补充缺失的变量。

    try/except ImportError 处理了 python-dotenv 未安装的边界情况（几乎肯定已安装，但防御性处理）。

    再次尝试 /note —— 现在应该可以正常工作。