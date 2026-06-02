---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DB2 中使用 UR 实现未提交读
translated: true
type: note
---

**Question:** 在 DB2 中 "WITH UR" 是什么意思？

**Answer:**

在 DB2 (IBM Db2) 中，`WITH UR` 是一个可以添加到 `SELECT` 语句中的子句，用于为该特定查询指定 **Uncommitted Read**（未提交读）隔离级别。

### 它的作用：

```sql
SELECT * FROM employee WHERE dept = 'A00' WITH UR;
```

- **UR** = **Uncommitted Read**（也称为 **dirty read**，脏读）
- 它允许查询读取已被其他事务修改但**尚未提交（not yet committed）**的数据行。
- 读取数据时不获取 **shared locks** (S-locks) → 极高的并发性，极少的阻塞。
- 在大多数情况下拥有最快的读取性能。
- DB2 中最低的隔离级别。

### 常见 DB2 隔离级别对比：

| Isolation level | Clause       | Locks taken          | Can read uncommitted data? | Typical use case                          |
|-----------------|--------------|----------------------|-----------------------------|--------------------------------------------|
| UR             | WITH UR      | 几乎没有             | 是 (dirty read)            | 报表、监控、非关键性读取                   |
| CS             | WITH CS      | 短期读取锁           | 否                          | 许多应用程序的默认设置                     |
| RS             | WITH RS      | Read stability locks | 否                          | 查询期间需要一致的视图                     |
| RR             | WITH RR      | 强 Repeatable read   | 否                          | 最高的一致性，重度锁定                     |

### 使用 `WITH UR` 的优点：

- 避免锁冲突（你的查询几乎从不等待其他事务）。
- 在只需要近似值或当前数据时，极大提升高频率更新表的性能。
- 在监控工具、仪表盘、运营报表和临时查询（ad-hoc queries）中非常常见。

### 缺点与风险：

- 你可能会读取到**脏数据（dirty data）**（随后被回滚的修改）。
- 你可能会遇到 **non-repeatable reads**（不可重复读）和 **phantom rows**（幻读）。
- 在以下情况中**不要**使用：
  - 你需要 100% 准确或可审计的数据。
  - 数据用于财务决策、计费等。
  - 结果集内部的一致性至关重要。

### 总结：

`WITH UR` = “我接受脏数据/未提交数据，以换取最高的速度和零阻塞。”

它是生产环境下（尤其是在 Db2 for z/OS 上）最常用的 DB2 特定指令之一。

**References:**

- [IBM Db2 Documentation - ISOLATION (UR) option](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=option-isolation-ur)
- [IBM Db2 Documentation - Specifying isolation levels in SQL statements](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=concurrency-specifying-isolation-levels-in-sql-statements)
