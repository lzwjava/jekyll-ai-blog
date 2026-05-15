---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 截图目录优先级实现
translated: true
type: note
---

完成。以下是变更摘要：

**截图保存目录优先级：**

1. `.env` 中的 `SCREENSHOT_DIR`（全局配置）——优先检查
2. `[dir]` CLI 参数——若无环境配置则作为后备
3. macOS 下使用 `.`（当前目录），Linux 下使用 `assets/screenshots`——最终默认值

**修改的文件：**

- `/Users/lzwjava/projects/ww/ww/image/screenshot.py` —— 添加了 `load_dotenv()`，优先读取环境变量 `SCREENSHOT_DIR`，然后依次回退到 CLI 参数 `[dir]` 和当前目录。逻辑：`env_dir or cli_dir or "."`
- `/Users/lzwjava/projects/ww/ww/image/screenshot_linux.py` —— 将所有模块级代码移至 `main()` 内部，添加了 `load_dotenv()`，读取 `SCREENSHOT_DIR` 并回退到 `assets/screenshots`。逻辑：`env_dir or "assets/screenshots"`
- `/Users/lzwjava/projects/ww/.env` —— 添加了 `SCREENSHOT_DIR=` 配置项（当前为空，表示使用默认值）
- `/Users/lzwjava/projects/ww/ww/main.py` —— 更新帮助文本以提及 `SCREENSHOT_DIR`
- `/Users/lzwjava/projects/ww/README.md` —— 更新文档

使用方法：在 `.env` 中设置 `SCREENSHOT_DIR`，例如：
```
SCREENSHOT_DIR=/Users/lzwjava/projects/jekyll-ai-blog/assets/screenshots
```

如果为空或未设置，则保留原有行为（macOS 下为当前目录，Linux 下为 `assets/screenshots`，或通过 `[dir]` 参数指定）。