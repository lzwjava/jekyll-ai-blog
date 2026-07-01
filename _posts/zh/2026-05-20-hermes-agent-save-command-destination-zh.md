---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes 代理保存命令目标
translated: true
type: note
---

**问题：** Hermes 代理（你的 `ww`/`zz` CLI 代理）中，`/save` 命令将数据持久化到何处？

**答案：**

我缺乏关于你具体 Hermes 代理实现的足够上下文，无法给出确切答案。`/save` 命令的行为完全取决于你的配置方式。

快速定位方法：

```bash
# 如果是 Python CLI 代理，用 grep 搜索保存逻辑
grep -rn "save\|/save\|checkpoint\|persist" ~/path/to/hermes/ --include="*.py" | grep -v ".pyc"

# 检查可能写入的配置文件/状态文件
lsof -p $(pgrep -f hermes) 2>/dev/null | grep REG

# 在可能的目录中查找最近写入的文件
ls -lt ~/.config/hermes/ ~/.local/share/hermes/ ~/.hermes/ 2>/dev/null | head -20

# 或者直接用 strace 跟踪 save 命令（macOS 使用 dtruss 或 dtrace）
# 在 macOS 上：
sudo dtrace -n 'syscall::open*:entry /pid == $target/ { printf("%s\n", copyinstr(arg0)); }' -p $(pgrep -f hermes)
```

常见的代理状态持久化模式：

| 模式 | 位置 |
| --- | --- |
| SQLite | `~/.local/share/<agent>/db.sqlite` |
| JSON/JSONL | `~/.config/<agent>/sessions/` |
| Pickle | `/tmp/<agent>_state.pkl` |
| Markdown/笔记 | `~/notes/` 或当前工作目录 |
| 向量存储 | `~/.cache/<agent>/embeddings/` |

如果你能粘贴 Hermes 代理代码中与 `/save` 处理器或状态类相关的部分，我可以准确告诉你它写入的位置，并提出改进建议——例如，改用带 FTS 的 SQLite 以实现可搜索的对话历史。
