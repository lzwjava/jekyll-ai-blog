---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据库断电后幸存
translated: true
type: note
---

**Phase 2 已交付——数据库现在能在断电后存活。** 已作为 `june` 提交（新增 804 行）。

## 构建内容

**Write-ahead log（`wal.c`）具备真正的 LSN 语义：**

- 每次变更在确认之前都会记录一个**带 `seq` 编号的 JSON 效果**，并将该记录 `fsync` 到磁盘——`insert` 记录*最终*行（保留自增），`update` 记录后像，`delete` 记录前像，DDL 记录 schema 操作
- 快照文件携带所覆盖的 `"seq"`；检查点**先**写入快照，然后截断日志——因此两者之间发生崩溃时，重放会重复执行，但会作为 no-op 处理。这与 SQLite/PostgreSQL 用于 LSN 记账的思路相同
- **原子批量操作**：`{"ops":[...]}` 会缓冲其日志行，并在提交时刷新——失败的操作或崩溃不会在磁盘上留下任何部分数据
- REPL 中的 **`BEGIN` / `COMMIT` / `ROLLBACK`** 运行在同一套机制上——回滚会丢弃缓冲的条目，即使事务中途被 SIGKILL 杀死，在重启时也会干净地回滚

## 证明（tests/crash_recovery.sh — 真实的 SIGKILL，非模拟）

```
wal entries before crash: 4
SIGKILL while idle → recover → all 3 committed inserts survived
next auto-increment id is 4          ← PK continuity across the crash
clean exit → checkpoint → wal truncated to 0 lines
BEGIN; insert; SIGKILL → recover → 0 rows  ← uncommitted txn correctly lost
```

引擎测试套件从 49 增至 **66 项检查**（崩溃恢复、回滚可见性、检查点幂等性），零警告，全部通过。

## 当前状况与后续计划

| | |
| --- | --- |
| ✅ | SQL 功能：JOIN、聚合、ALTER、运算符、DISTINCT |
| ✅ | 原子批量操作 + 交互式事务 |
| ✅ | WAL 持久性 + 崩溃恢复 + 检查点 |
| ⏳ | **pk B-tree 索引**（Phase 2 剩余项——全表扫描仍是唯一的访问路径） |
| → | **Phase 3**：streaming completions、`explain` 计划打印、schema-hallucination validator |

如果你想要一个真正的索引结构，B-tree 是自然的下一步；否则 Phase 3 会让 AI 交互达到最先进水平。要我继续做其中一项吗？
