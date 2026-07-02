---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在环境变量中扩展用户路径
translated: true
type: note
---

已推送。提交 `cb60fb4` 至 `main` → `origin/main`。

上传内容摘要：

- **`ww/env/__init__.py`** — `load_env()` 现在会展开 `BASE_PATH` 中的 `~`，并将解析后的路径写回 `os.environ`
- **`ww/note/create_note_utils.py`** — `get_base_path()` 调用 `os.path.expanduser()` 实现深度防御
- **`ww/db.py`** — 在构造 `ww.db` 路径前进行展开
- **`ww/llm/update_env.py`** — 在查找 `.env` 前进行展开
- **`ww/main.py` + `completions/_ww` + `ww/env/github_desktop.py`** — 还包括了工作目录中的 github-desktop 命令
