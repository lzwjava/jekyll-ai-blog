---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Windows文件重命名错误
translated: true
type: note
---

**修复摘要：**

- **根本原因**：`tmp.rename(qf)` 在底层使用了 `os.rename()`，而该函数在 **Windows** 系统上拒绝覆盖已存在的文件（会抛出 `FileExistsError`）。在 POSIX（macOS/Linux）系统上，`rename()` 会原子性地替换目标文件——但 Windows 系统并非如此。
- **修复方法**：将 `tmp.rename(qf)` 替换为 `os.replace(tmp, qf)`。`os.replace()` 函数被明确设计为跨平台等效方案——它在 POSIX 系统 **和** Windows 系统上都能原子性地替换目标文件。
- 同时补充了缺失的 `import os` 语句。

现在你可以重新运行 `uv run ww note process`——`mark_done` → `_save_queue` 路径在 Windows 系统上将不再抛出 `FileExistsError` 错误。
