---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复了 DB_PATH 中的波浪号扩展
translated: true
type: note
---

已全部修复。以下是发生的问题及处理过程：

**根本原因**：`~/.config/ww/.env` 文件中的 `DB_PATH=~/projects/jekyll-ai-blog/ww.db` 包含字面波浪号（`~`）。在 `ww/db.py` 中，`get_db_path()` 直接返回 `DB_PATH` 而未使用 `os.path.expanduser()` 展开，导致 `os.makedirs()` 将 `~` 视为字面目录名——当从 `zz/` 目录运行时，实际创建了 `fineweb-code-sec-gpt/~/projects/jekyll-ai-blog/ww.db`。

**已应用的修复方案**：

1. **`ww/db.py`** —— 在 `DB_PATH` 分支中增加了 `os.path.expanduser()`，确保无论环境变量还是 `.env` 文件中的波浪号都能正确展开。已提交为 `1d283a1`。

2. **`~/.config/ww/.env`** —— 将 `DB_PATH` 从 `~/projects/jekyll-ai-blog/ww.db` 修改为 `~/.config/ww/ww.db`（标准 XDG 配置目录位置）。

3. **`zz` 仓库** —— 通过 `git commit --amend` 从 git 历史中移除了被跟踪的 `~/projects/jekyll-ai-blog/ww.db` 文件，删除了字面 `~` 目录树，并在 `.gitignore` 中添加了 `*.db` 规则，防止未来意外提交 sqlite 数据库文件。

现在 `ww` 写入命令历史数据库时，会正确展开波浪号并存储到 `~/.config/ww/ww.db`，项目目录下不会再出现幽灵目录。
