---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已添加命令日志记录和数据库功能
translated: true
type: note
---

已完成。以下是构建的内容：

**新文件：**
- `ww/db.py` — SQLite 模块：`get_db_path()`、`init_db()`、`log_command()`、`parse_command()`
- `ww/db_stats.py` — `ww db` 命令，包含 5 个子命令：`stats`、`recent`、`top`、`errors`、`search`

**修改的文件：**
- `ww/main.py` — `main()` 现在会捕获原始参数并通过 try/finally 记录每次调用（成功或错误）。分发逻辑移至 `_main_dispatch()`。
- `.env.example` — 添加了 `DB_PATH` 文档说明
- `.env` — 设置 `DB_PATH=/Users/lzwjava/projects/jekyll-ai-blog/ww.db`
- `~/.zsh/completions/_ww` — 添加了 `db` 命令及其所有子命令和 `--limit` 标志

**数据库模式：**
```sql
command_log (
    id, timestamp, raw_command, group_name, subcmd, exit_code, cwd
)
```

**使用方法：**
```
ww db stats      -- 总体统计、热门分组、错误率、最繁忙日期
ww db recent     -- 最近 20 条命令（使用 --limit N）
ww db top        -- 最常用命令（使用 --limit N）
ww db errors     -- 最近失败的命令
ww db search <pattern>  -- 在历史记录中搜索
```

现在每次 `ww` 调用都会被记录——即使是错误的命令（如 `ww nonexistent`）也会连同其退出码一并捕获。`raw_command` 列存储完整的命令字符串，以便后续解析/分析。