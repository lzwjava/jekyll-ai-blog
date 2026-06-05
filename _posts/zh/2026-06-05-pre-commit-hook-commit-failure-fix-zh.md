---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预提交钩子提交失败修复
translated: true
type: note
---

以下是完整情况：

## 问题

当 `ww note watch`（或 `ww note process`）创建笔记并尝试提交时，如果 pre-commit hooks 修改了文件，提交可能会失败。失败后，重试会被未提交更改检查阻塞，导致不可恢复的状态。

## 根本原因 —— 逐步分析

1. `process_queue()` 创建笔记文件，然后调用 `_git_commit_push(files=created_paths)`
2. 在 `gitmessageai()` 内部，文件通过 `git add <file>` 暂存（gitmessageai.py 第87行）
3. 暂存的差异被发送给 LLM 以生成提交信息
4. `git commit -m <message>` 运行 —— pre-commit hooks 触发
5. `end-of-file-fixer` hook 检测到缺少尾部换行符，并静默修复了磁盘上的文件
6. 现在工作树（已修复）与索引（原始暂存）不同。Git 拒绝提交：
   ```
   error: Your local changes to the following files would be overwritten by merge
   ```
7. `_git_commit_push()` 抛出 `CalledProcessError`，该异常向上传递到 `process_queue()` 中的 `except` 块（第105-108行）—— 它会打印错误并提示你重试
8. 队列条目已被标记为完成并清理（第115行），但文件被卡住：**已暂存 + 脏工作树**
9. 重试时，`_check_uncommitted()`（第51-55行）检测到脏状态并调用 `sys.exit(1)` —— 死胡同

核心问题：`gitmessageai` 在开始时执行一次 `git add`，但如果 hooks 在 `git commit` 期间修改了文件，这些修改不会被重新暂存。索引变得过时。

## 修复方案

在 `_git_commit_push()` 中（`note_queue_process.py` 第31行），将 `gitmessageai()` 调用包裹在 try/except 中：

```python
try:
    gitmessageai(...)
except subprocess.CalledProcessError:
    # Re-stage files so hook modifications are picked up
    subprocess.run([*git, "add", *files], check=True)
    # Retry once
    gitmessageai(...)
```

当第一次尝试因 hooks 修改文件而失败时：
- `except` 块对同一文件重新运行 `git add`，暂存 hook 修复后的版本
- 第二次 `gitmessageai()` 调用看到干净的差异（如果 hooks 是唯一的更改，则没有差异），生成提交信息，并成功提交

这样做是安全的，因为：
- 仅重试一次（无无限循环）
- 如果第二次尝试也失败，异常正常传播
- 涵盖所有 pre-commit hooks，而不仅仅是 `end-of-file-fixer`
- 同时适用于 `ww note process` 和 `ww note watch`（观察者调用 `process_queue()`）

## 即时修复

手动重新暂存被卡住的笔记并提交：
```
9478ec3f3  docs(notes): add Qwen3.6 unpacked vs hype analysis
```

该文件已在磁盘上被 hook 修复，因此第二次提交顺利通过了所有 hooks。