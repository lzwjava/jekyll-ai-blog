---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 推送后GitHub链接可点击
translated: true
type: note
---

看起来不错——语法检查通过。以下是我所做的修改：

**`ww/note/note_queue_process.py`** — 在成功提交并推送后，watch/process 命令现在会为每个推送的笔记打印一个可点击的 GitHub 链接：

```python
# 在 "[ok] All notes committed and pushed" 之后，会打印：
#   https://github.com/lzwjava/jekyll-ai-blog/blob/main/notes/2026-07-23-nanochat-evaluation-built-in-and-external-en.md
```

新增的 `_print_note_links()` 函数：
1. 读取 git 远程仓库 URL 以获取 `owner/repo`
2. 查找 git 工作树根目录以生成相对路径
3. 为每个文件打印 `https://github.com/<owner>/<repo>/blob/main/<relative-path>` 链接

现在你的 watch 输出会显示为：

```
[ok] All notes committed and pushed
  https://github.com/lzwjava/jekyll-ai-blog/blob/main/notes/2026-07-23-nanochat-evaluation-built-in-and-external-en.md
[ok] Cleaned 1 processed entry/entries from queue
```