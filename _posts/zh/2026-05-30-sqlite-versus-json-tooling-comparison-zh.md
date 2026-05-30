---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SQLite 与 JSON 工具比较
translated: true
type: note
---

**问题：** SQLite 有 GUI/CLI 数据库客户端来查看和检查数据——这是否比 JSON 更有优势？

**回答：** 是的，这是 SQLite 的一个实际优势。但针对你的情况，JSON 仍然更胜一筹，因为你的工具链已经足够完善了。

## SQLite 客户端生态系统

- **TablePlus**、**DBeaver**、**DB Browser for SQLite** —— 图形界面，可浏览行、过滤、排序
- `sqlite3` 命令行界面 —— 内置于 macOS/Linux，无需安装
- VS Code 扩展 —— SQLite Viewer，内联表格浏览

```bash
sqlite3 data/tt.db "SELECT * FROM punch_days WHERE status='missed_punch'"
```

## 但 JSON 也有等效的工具

```bash
# jq —— 已在你的 README 中
cat data/contractor_a.json | jq '.punch_days[] | select(.status=="missed_punch")'

# fx —— 交互式 JSON 浏览器（类似 GUI）
fx data/contractor_a.json

# gron —— 使 JSON 可被 grep 搜索
gron data/contractor_a.json | grep missed_punch
```

说实话，对于这种数据形状的只读检查，`jq` 与 SQL 一样强大。你已经在使用它了。

## 真正的权衡

|          | SQLite                        | JSON                          |
|----------|-------------------------------|-------------------------------|
| GUI 客户端 | ✅ TablePlus 等                | ❌                             |
| CLI 检查  | ✅ `sqlite3`                  | ✅ `jq`, `fx`                  |
| `grep` / `cat` | ❌ 二进制文件              | ✅                             |
| 编辑单个值 | ❌ 需要客户端/SQL               | ✅ `vim data/x.json`           |
| 非技术用户查看 | ✅ GUI                     | ❌                             |

## 对 `tt` 的结论

你是唯一用户，以终端为主，且已经在使用 `jq`。GUI 客户端的优势并不适用于你。如果你需要将这个交给一个需要浏览记录的非技术 HR 人员——那么 SQLite + TablePlus 会立即胜出。这才是该优势的真正用例。