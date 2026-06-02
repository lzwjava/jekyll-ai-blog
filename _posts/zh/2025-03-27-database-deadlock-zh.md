---
audio: false
generated: true
lang: zh
layout: post
title: 数据库死锁
translated: true
type: note
---

**数据库死锁**是指两个或多个事务相互等待对方释放资源锁，形成循环依赖，导致所有事务都无法继续执行的情况。数据库管理系统（DBMS）通常会检测到这种状况，并通过回滚其中一个事务来解决死锁。以下是一个详细的死锁场景示例：

---

### 示例：两个事务间的死锁

- **场景**：
  - 事务 T1 更新 `Orders` 表中的一行，随后需要更新 `Customers` 表中的一行。
  - 事务 T2 更新 `Customers` 表中的一行，随后需要更新 `Orders` 表中的一行。
  - 两个事务以不同的顺序锁定资源，导致死锁。

- **步骤分解**：
  1. T1 锁定 `Orders` 表中的某一行。
  2. T2 锁定 `Customers` 表中的某一行。
  3. T1 尝试锁定 `Customers` 表中的行（被 T2 阻塞）。
  4. T2 尝试锁定 `Orders` 表中的行（被 T1 阻塞）。
  - 结果：两个事务均无法继续，形成死锁。

- **SQL 示例**：

  ```sql
  -- 事务 T1
  BEGIN TRANSACTION;
  UPDATE Orders SET Status = '已发货' WHERE OrderID = 100;  -- 锁定 OrderID 100
  -- （某些延迟或处理）
  UPDATE Customers SET LastOrderDate = '2025-03-27' WHERE CustomerID = 1;  -- 被 T2 阻塞

  -- 事务 T2
  BEGIN TRANSACTION;
  UPDATE Customers SET Balance = Balance - 50 WHERE CustomerID = 1;  -- 锁定 CustomerID 1
  -- （某些延迟或处理）
  UPDATE Orders SET PaymentStatus = '已支付' WHERE OrderID = 100;  -- 被 T1 阻塞
  ```

- **发生过程**：
  - T1 持有 `OrderID = 100` 的排他锁，并等待 `CustomerID = 1`。
  - T2 持有 `CustomerID = 1` 的排他锁，并等待 `OrderID = 100`。
  - 这种循环等待条件即构成死锁。
  - DBMS 检测到死锁（例如通过超时或死锁检测算法）并回滚其中一个事务（例如 T2），使 T1 得以完成。

---

### 死锁的直观表示

```
T1: 锁定 Orders(100) --> 请求 Customers(1)
   |                             ↑
   |                             |
T2: 请求 Orders(100)  <-- 锁定 Customers(1)
```

- **解决方案**：DBMS 可能输出如下错误：

  ```
  事务 T2 在锁资源上与另一个进程发生死锁，并已被选为死锁牺牲者。请重新运行该事务。
  ```

---

### 死锁成因

- **锁定顺序**：T1 和 T2 以不同顺序获取锁（T1：Orders → Customers；T2：Customers → Orders）。
- **并发性**：两个事务同时运行且需要重叠的资源。
- **排他锁**：更新操作需要排他锁，这会阻止其他事务访问相同数据。

---

### 如何避免死锁

1. **一致的锁定顺序**：确保所有事务按相同顺序获取锁（例如总是先锁定 `Orders` 再锁定 `Customers`）。

   ```sql
   -- T1 和 T2 都应先锁定 Orders，再锁定 Customers
   ```

2. **缩短事务时间**：减少事务内的延迟以降低资源重叠概率。
3. **使用较低隔离级别**：在适用情况下使用限制较少的隔离级别（如读已提交）以缩短锁定时长。
4. **设置超时**：配置较短的锁超时时间以实现快速失败重试。

---

如果您需要更具体的示例（例如针对 PostgreSQL 或 SQL Server 等特定 DBMS）或进一步说明，请随时告知！
