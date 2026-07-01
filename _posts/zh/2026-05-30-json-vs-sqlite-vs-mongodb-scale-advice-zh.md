---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JSON vs SQLite vs MongoDB 扩展建议
translated: true
type: note
---

**问题：** 对于 `tt` 工时表验证工具，我是否应该使用 MongoDB 或 SQLite（而不是 JSON 文件）？

**回答：**

两者都不需要。**继续使用 JSON 缓存。** 你的 README 已经说得很好："在这种规模下不需要数据库。"

原因如下，特别是针对 `tt`：

## `tt` 实际存储的内容

```
contractors: ~1-20
weeks per contractor: ~4-5
punch days per contractor: ~20-31
```

每月总共约 **500 条记录**，每次运行读取一次，每次提取写入一次。这是配置文件级别，而不是数据库级别。

## 为什么 JSON 在这里胜出

- **无需强制关系** — `client_weeks` 和 `punch_days` 已按每个 contractor 反规范化。永远不会发生跨 contractor 的关联查询。
- **"外键问题"不适用** — 每个 `contractor_a.json` 都是自包含的。你不需要跨文件关联行。
- **人类可编辑** — 你明确使用 `jq` 来检查/修复提取的数据。数据库会破坏这个工作流。
- **LLM 提取输出天然是 JSON** — 你只需序列化到数据库再反序列化回来，零收益。
- **`--force` 重新提取会替换整个记录** — 原子文件替换比 `DELETE + INSERT` 更简单。

## 你真正需要数据库的情况

| 条件 | SQLite | Mongo |
| --- | --- | --- |
| 50+ 个 contractor，查询所有数据 | ✅ | ✅ |
| 跨月的历史趋势分析 | ✅ | ✅ |
| 多用户同时写入 | ✅ | ✅ |
| 每个 contractor 灵活的 schema（嵌套、可变） | — | ✅ |
| 需要在 SQL 中使用 `GROUP BY month, contractor` | ✅ | — |

当前 `tt` 均不满足这些条件。

## 如果确实超出 JSON 范围 → SQLite，而非 MongoDB

MongoDB 会显得大材小用（需要独立的服务器进程、默认无 ACID 4.0 之前版本、运维开销）。如果将来需要跨 contractor 查询或历史运行分析，SQLite 才是正确的下一步：

```python
CREATE TABLE contractor_weeks (
    contractor TEXT,
    week_start DATE,
    total_hours REAL,
    project_hours REAL,
    status TEXT,
    extracted_at TIMESTAMP
);
```

然后执行 `SELECT contractor, AVG(project_hours/total_hours) FROM contractor_weeks GROUP BY contractor` — 对趋势报告确实有用。

## 结论

```
tt 规模：   JSON ✅   SQLite（大材小用）   MongoDB（极大浪费）
```

JSON 设计对这个工具来说是合适的。之前关于 JSON 作为数据库的讨论适用于**具有完整性要求的关联数据** — `tt` 的数据是扁平的、按 contractor 隔离、且由 LLM 生成。JSON 是正确的选择。
