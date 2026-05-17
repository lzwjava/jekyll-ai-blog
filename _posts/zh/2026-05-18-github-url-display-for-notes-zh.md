---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 笔记的GitHub URL显示
translated: true
type: note
---

所有导入均通过。远程 URL 检测会将 `git@github.com:lzwjava/blog-source.git` 转换为 `https://github.com/lzwjava/blog-source`，这是正确的行为。

以下是 4 个文件中所做更改的摘要：

1. `/Users/lzwjava/projects/.../gitmessageai.py` - 添加了 `_get_github_repo_url(git)` 和 `_print_note_urls(git, file_changes)` 辅助函数。推送后，如果类型为"file"类型且存在文件变更时，针对每个新增的 `.md` 文件打印 `[info] Note created at <github_url>`。

2. `/Users/lzw/.../screenshot_log.py` - 添加了 `import subprocess`、`_get_github_repo_url()` 和 `_print_note_url(file_path)`。创建笔记后打印 GitHub URL。

3. `/Users/lzw/.../interact_note.py` - 从 `screenshot_log` 导入 `_print_note_url`，并在创建笔记后调用它。

4. `/Users/lzw/.../note_workflow.py` - 将最终的 `[info] Note created at` 消息改为显示 GitHub URL（出错时回退到本地文件路径）。

现在所有笔记创建路径（`ww note`、`ww screenshot note`、`ww screenshot interact-note`）以及 git 推送路径（`ww git gpa`）都会以如下格式输出 GitHub URL：

```
[info] Note created at https://github.com/lzwjava/blog-source/blob/main/notes/2026-05-18-amd-digitalocean-cloud-partnership-en.md
```