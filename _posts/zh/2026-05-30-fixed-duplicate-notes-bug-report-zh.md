---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复重复笔记的缺陷报告
translated: true
type: note
---

完成。以下是总结：

**根本原因：**

1. `create_note_from_content()` 没有重复检查——只有 `create_note()` 做了检查
2. Hermes `/note` 插件和研究代理直接调用 `create_note_from_content()`
3. `check_duplicate_notes.py` 中的 bug：`note_files[:-1]` 删除了最旧的文件而不是最新的

**已应用的修复：**

1. **ww 仓库** (`/Users/lzwjava/projects/ww`):
   - 向 `create_note_from_content()` 添加了重复检查——针对最新的 200 条笔记进行检查
   - 修复了 `check_duplicate_notes.py` 第 84 行：`note_files[:-1]` → `note_files[1:]`
   - 已提交并推送

2. **jekyll-ai-blog 仓库** (`/Users/lzwjava/projects/jekyll-ai-blog`):
   - 删除了重复文件：`2026-05-30-cost-saving-gpt-3-training-on-amd-cloud-en.md`
   - 保留：`2026-05-30-reduce-gpt-3-training-costs-amd-cloud-en.md`
   - 已提交并推送

**CI 状态：** 下一次 GitHub Actions 运行应通过重复检查测试。
