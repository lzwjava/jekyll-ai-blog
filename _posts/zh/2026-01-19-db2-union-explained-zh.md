---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DB2 UNION 与 UNION ALL 详解
translated: true
type: note
---

**Question:** 在 DB2 中，UNION ALL 和 UNION 代表什么意思？

**Answer:**

在 DB2（以及通用的 SQL）中，**UNION** 和 **UNION ALL** 都是集合操作符（set operators），用于将两个或多个 SELECT 语句的**结果集组合**为一个单一的结果集。它们将行垂直堆叠（将一个查询的行追加到另一个查询的行下方）。

### 核心区别

- **UNION**
  组合结果集并**自动移除重复行**（执行去重操作）。
  当你只写 `UNION` 时，这是默认行为。

- **UNION ALL**
  组合结果集并**保留所有行**，包括重复行。
  不执行去重操作。

### 对比表

| 特性 | UNION | UNION ALL |
| :--- | :--- | :--- |
| 是否移除重复项？ | 是 | 否 |
| Performance | 较慢（需要排序/去重） | 较快（无需去重） |
| 适用场景 | 只需要不重复的行时 | 需要所有行（即使重复）时 |
| 典型用例 | 合并相似数据且不重复 | 汇总 logs、历史数据 + 当前数据、递归 CTE |

### 共同规则

- 所有 SELECT 语句中的列数必须相同。
- 对应的列必须具有兼容的 data types。
- 列名取自第一个 SELECT 语句。
- 如果需要 `ORDER BY` 子句，只能在最后出现一次。

### 简单示例

```sql
-- 假设这两个表中有一些重叠的 CITY 值

SELECT CITY FROM CUSTOMERS
UNION
SELECT CITY FROM SUPPLIERS;
-- 仅返回唯一的城市

SELECT CITY FROM CUSTOMERS
UNION ALL
SELECT CITY FROM SUPPLIERS;
-- 返回所有城市，如果同一个城市在两个表中都出现，则包含重复项
```

### Performance 提示

`UNION ALL` 几乎总是比 `UNION` 快，因为 DB2 不需要为了去重而比较行（这通常涉及排序或哈希操作）。
除非你明确需要移除重复项，否则请默认使用 `UNION ALL`。

### 特殊情况

在 DB2 的**递归 Common Table Expressions (CTE)** 中，你**必须**在 anchor member 和 recursive member 之间使用 `UNION ALL` —— 不允许使用 `UNION`。

**References:**

- [IBM Db2 Support - Difference between UNION and UNION ALL](https://www.ibm.com/support/pages/difference-between-union-and-union-all-db2)
- [IBM Db2 for i - Specifying the UNION ALL keyword](https://www.ibm.com/docs/en/i/7.4.0?topic=subselects-specifying-union-all-keyword)
- [Db2Tutorial - Db2 UNION Operator](https://www.db2tutorial.com/db2-basics/db2-union)
