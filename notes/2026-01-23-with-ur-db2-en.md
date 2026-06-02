---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: WITH UR for Uncommitted Reads in DB2
translated: false
type: note
---

**Question:** What does "WITH UR" mean in DB2?

**Answer:**

In DB2 (IBM Db2), `WITH UR` is a clause you can add to a `SELECT` statement to specify the **Uncommitted Read** isolation level for that particular query.

### What it does:
```sql
SELECT * FROM employee WHERE dept = 'A00' WITH UR;
```

- **UR** = **Uncommitted Read** (also known as **dirty read**)
- It allows the query to read rows that have been modified by other transactions but **not yet committed**.
- No **shared locks** (S-locks) are taken when reading data → very high concurrency, minimal blocking
- Fastest possible read performance in most cases
- Lowest isolation level in DB2

### Comparison of common DB2 isolation levels:

| Isolation level | Clause       | Locks taken          | Can read uncommitted data? | Typical use case                          |
|-----------------|--------------|----------------------|-----------------------------|--------------------------------------------|
| UR             | WITH UR      | Almost none          | Yes (dirty read)           | Reporting, monitoring, non-critical reads |
| CS             | WITH CS      | Short read locks     | No                          | Default for many applications             |
| RS             | WITH RS      | Read stability locks | No                          | Need consistent view during query         |
| RR             | WITH RR      | Strong repeatable read | No                        | Highest consistency, heavy locking        |

### Advantages of USING `WITH UR`
- Avoids lock contention (your query almost never waits for other transactions)
- Greatly improves performance on high-update tables when you only need approximate/current data
- Very common in monitoring tools, dashboards, operational reports, and ad-hoc queries

### Disadvantages / Risks
- You might read **dirty data** (changes that later get rolled back)
- You might see **non-repeatable reads** and **phantom rows**
- Do **not** use it when:
  - You need 100% accurate / auditable numbers
  - The data is used for financial decisions, billing, etc.
  - Consistency within the result set is critical

### Summary
`WITH UR` = "I accept dirty / uncommitted data in exchange for maximum speed and zero blocking."

It's one of the most frequently used DB2-specific hints in production environments, especially on Db2 for z/OS.

**References:**

- [IBM Db2 Documentation - ISOLATION (UR) option](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=option-isolation-ur)
- [IBM Db2 Documentation - Specifying isolation levels in SQL statements](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=concurrency-specifying-isolation-levels-in-sql-statements)
