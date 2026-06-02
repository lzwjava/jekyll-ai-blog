---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重复预防修复调用路径
translated: true
type: note
---

你质疑得对。让我追溯一下确切的调用路径：

**调用路径 1：Hermes `/note` 插件** (`ww/config/hermes/plugins/note/__init__.py`)
```python
# 第143-152行
try:
    file_path = create_note_from_content(text, custom_title=title, directory=note_dir)
except ValueError as e:
    return f"Note rejected: {e}"  # ← 捕获 ValueError
```
✅ 有错误处理 - 会捕获重复内容的 ValueError

**调用路径 2：Research agent** (`ww/agent/research_agent.py`)
```python
# 第108-114行
try:
    file_path = create_note_from_content(content, custom_title=topic)
except Exception as e:
    print(f"Error using create_note_from_content: {str(e)}")  # ← 捕获 Exception
```
✅ 有错误处理 - 会捕获重复内容的 ValueError

**调用路径 3：`create_note()`** (`create_note_from_clipboard.py` 第101-105行)
```python
def create_note(date=None):
    if check_duplicate_notes():  # ← 第一层检查（剪贴板内容 vs 现有笔记）
        raise ValueError(...)
    content = get_clipboard_content()
    return create_note_from_content(content, date=date)  # ← 第二层检查（我的修复）
```
✅ 现在有双重保护

**总结：**
- 两个调用方（Hermes 插件、research agent）都有适当的异常处理
- 它们**直接**调用 `create_note_from_content()`，没有事先进行重复检查
- 我的修复在中心函数 `create_note_from_content()` 内部增加了重复检查
- ValueError 会被它们现有的 `except` 块捕获

修复是正确的——它正好堵住了之前会创建重复内容的漏洞。
