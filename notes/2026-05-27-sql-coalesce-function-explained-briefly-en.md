---
audio: false
generated: true
image: false
lang: en
layout: post
title: SQL COALESCE Function Explained Briefly
translated: false
type: note
---

**Question:** What is `COALESCE` in SQL — if value is not null use that value, if null then use `''`?

**Answer:**

`COALESCE(expr, fallback)` returns the **first non-NULL argument** in its argument list.

```sql
SELECT COALESCE(some_column, '') AS safe_value
FROM my_table;
```

- If `some_column` is `'hello'` → returns `'hello'`
- If `some_column` is `NULL` → returns `''`

It short-circuits — stops at the first non-NULL. You can chain multiple fallbacks:

```sql
SELECT COALESCE(nickname, full_name, email, 'Unknown') AS display_name
FROM users;
```

Works across PostgreSQL, MySQL, SQLite, SQL Server, Oracle — it's ANSI SQL standard.

**Alternative (MySQL-specific):** `IFNULL(expr, '')` — same behavior but only takes 2 args.

**Alternative (SQL Server):** `ISNULL(expr, '')` — same, 2 args only.

`COALESCE` is the portable one to default to.
