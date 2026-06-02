---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 文件创建中的竞态条件
translated: true
type: note
---

观察代码执行路径，锁机制并非根本原因。重复问题的发生是因为当 `slug` 已存在时，`create_filename` 会静默回退到使用计数器后缀。

**用户假设的竞争路径（并发执行 `ww note`）：**

同一台机器上的两次调用可能越过 `check_duplicate_notes()` 产生竞争：
1. 两者都通过 `check_uncommitted_changes()` 和 `git pull --rebase`
2. 两者都调用 `check_duplicate_notes()` — 此时都尚未看到对方创建的文件
3. 两者都调用 `create_filename()` — 其中一个得到 `...-en.md`，另一个则在 `create_note_utils.py:77-79` 处进入回退逻辑：
   ```python
   while os.path.exists(file_path):
       file_path = os.path.join(notes_dir, f"{date_str}-{short_title}-{counter}-en.md")
   ```
4. 两者都提交并推送 — 最终结果：两份几乎完全相同的笔记。

加锁可以防止*这种*竞争，但无法阻止更常见的路径。

**更可能的路径（也是测试输出实际显示的）：**

文件对 `2026-04-20-iphone-daylight-timelapse-en.md` 和 `...-timelapse-1-en.md` 是计数器后缀分支的典型特征。即使*顺序执行*（而不仅是并发），也可能进入该分支，当：

- `check_duplicate_notes` 未能识别重复，因为 `_are_notes_quick_similar` 要求前250个字符完全相同且字符匹配数≥450/500 — 任何空白字符/清理差异都可能绕过它（`check_duplicate_notes.py:12-30`）
- LLM 为相似但不完全相同的剪贴板内容重新生成了相同的 `slug`
- `create_filename` 将已存在的 `slug` 视为需要消歧的信号，而非危险标志

**实际的修复方案：**

1. 在 `create_filename` 中将 `slug` 冲突设为致命错误 — 如果 `{date}-{slug}-en.md` 已存在，则中止（或要求提供标志）。计数器后缀回退是真正的漏洞。
2. 加强 `check_duplicate_notes`，使其在写入前也能标记相同日期相同 `slug` 的情况。
3. 可选地，为笔记目录添加 `flock` 作为额外保障，防止进程内竞争。

修复（1）是最有效的手段 — 它能同时关闭竞争路径和顺序重复路径。需要我实施这个修改吗？
