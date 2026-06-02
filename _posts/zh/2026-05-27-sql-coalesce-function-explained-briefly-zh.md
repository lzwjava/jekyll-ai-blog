---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SQL COALESCE 函数简要解释
translated: true
type: note
---

**问题：** SQL 中的 `COALESCE` 是什么——如果值不为 null 则使用该值，如果为 null 则使用 `''`？

**答案：**

`COALESCE(expr, fallback)` 返回其参数列表中**第一个非 NULL 的参数**。

```sql
SELECT COALESCE(some_column, '') AS safe_value
FROM my_table;
```

- 如果 `some_column` 是 `'hello'` → 返回 `'hello'`
- 如果 `some_column` 是 `NULL` → 返回 `''`

它是短路求值的——遇到第一个非 NULL 即停止。你可以链式添加多个回退值：

```sql
SELECT COALESCE(nickname, full_name, email, 'Unknown') AS display_name
FROM users;
```

该函数在 PostgreSQL、MySQL、SQLite、SQL Server、Oracle 中均可使用——它是 ANSI SQL 标准。

**替代方案（MySQL 专用）：** `IFNULL(expr, '')` — 行为相同，但只接受两个参数。

**替代方案（SQL Server 专用）：** `ISNULL(expr, '')` — 同上，仅接受两个参数。

`COALESCE` 是通用性更好的默认选择。
