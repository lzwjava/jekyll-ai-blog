---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DB2 UNION vs. UNION ALL Explained
translated: false
type: note
---

**Question:** What do UNION ALL and UNION mean in DB2?

**Answer:**

In DB2 (and in SQL in general), both **UNION** and **UNION ALL** are set operators used to **combine the result sets** of two or more SELECT statements into a single result set. They stack rows vertically (append rows from one query below the rows of another).

### Key Differences

- **UNION**
  Combines the result sets and **automatically removes duplicate rows** (performs deduplication).
  This is the default behavior when you write just `UNION`.

- **UNION ALL**
  Combines the result sets and **keeps all rows**, including duplicates.
  No deduplication is performed.

### Comparison Table

| Feature              | UNION                        | UNION ALL                    |
|----------------------|------------------------------|------------------------------|
| Removes duplicates?  | Yes                          | No                           |
| Performance          | Slower (needs to sort/dedup) | Faster (no deduplication)    |
| Use when...          | You want distinct rows only  | You want all rows (even duplicates) |
| Typical use case     | Combining similar data without repetition | Aggregating logs, history + current data, recursive CTEs |

### Rules that apply to both

- The number of columns must be the same in all SELECT statements.
- The corresponding columns must have compatible data types.
- Column names are taken from the first SELECT statement.
- An `ORDER BY` clause (if needed) must appear only once at the very end.

### Simple Example

```sql
-- Assume these two tables have some overlapping CITY values

SELECT CITY FROM CUSTOMERS
UNION
SELECT CITY FROM SUPPLIERS;
-- Returns only unique cities

SELECT CITY FROM CUSTOMERS
UNION ALL
SELECT CITY FROM SUPPLIERS;
-- Returns all cities, including duplicates if the same city appears in both tables
```

### Performance Note

`UNION ALL` is almost always faster than `UNION` because DB2 does not have to compare rows for duplicates (which usually involves sorting or hashing).
Use `UNION ALL` by default unless you explicitly need to remove duplicates.

### Special Case

In **recursive Common Table Expressions (CTE)** in DB2, you **must** use `UNION ALL` between the anchor and recursive members — `UNION` is not allowed.

**References:**

- [IBM Db2 Support - Difference between UNION and UNION ALL](https://www.ibm.com/support/pages/difference-between-union-and-union-all-db2)
- [IBM Db2 for i - Specifying the UNION ALL keyword](https://www.ibm.com/docs/en/i/7.4.0?topic=subselects-specifying-union-all-keyword)
- [Db2Tutorial - Db2 UNION Operator](https://www.db2tutorial.com/db2-basics/db2-union)
