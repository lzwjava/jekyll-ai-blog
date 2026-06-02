---
audio: false
generated: true
lang: zh
layout: post
title: 数据库阻塞
translated: true
type: note
---

我理解您想了解数据库管理系统（DBMS）中的阻塞场景。当某个事务因并发访问或修改相同数据而阻碍另一事务执行时，就会发生阻塞，这通常通过锁机制来确保数据一致性和完整性。以下是几种典型的数据库阻塞场景：

---

### 示例1：读写阻塞

- **场景**：事务T1正在更新表中某行数据（如修改客户余额），事务T2尝试读取同一行
- **运行机制**：T1获取该行的排他锁，阻止其他事务在更新完成前读取或修改数据。T2被阻塞，必须等待T1提交或回滚
- **SQL示例**：

  ```sql
  -- 事务T1
  BEGIN TRANSACTION;
  UPDATE Accounts SET Balance = Balance - 100 WHERE AccountID = 1;

  -- 事务T2（被阻塞）
  SELECT Balance FROM Accounts WHERE AccountID = 1;
  ```

  由于行级排他锁的存在，T2需等待T1执行完毕

---

### 示例2：写写阻塞

- **场景**：事务T1正在更新产品库存数量，同时事务T2尝试更新同一产品库存
- **运行机制**：T1持有该行的排他锁，T2在T1完成前被阻塞。这能避免导致数据不一致的冲突更新
- **SQL示例**：

  ```sql
  -- 事务T1
  BEGIN TRANSACTION;
  UPDATE Products SET Stock = Stock - 5 WHERE ProductID = 100;

  -- 事务T2（被阻塞）
  UPDATE Products SET Stock = Stock + 10 WHERE ProductID = 100;
  ```

  T2在T1提交或回滚前将持续被阻塞

---

### 示例3：死锁（阻塞导致的僵局）

- **场景**：事务T1锁定行A后需更新行B，而事务T2锁定行B后需更新行A
- **运行机制**：T1被T2对行B的锁阻塞，T2被T1对行A的锁阻塞，形成死锁。此时需要DBMS介入处理（如回滚其中一个事务）
- **SQL示例**：

  ```sql
  -- 事务T1
  BEGIN TRANSACTION;
  UPDATE Table1 SET Value = 10 WHERE ID = 1;  -- 锁定行A
  UPDATE Table2 SET Value = 20 WHERE ID = 2;  -- 被T2阻塞

  -- 事务T2
  BEGIN TRANSACTION;
  UPDATE Table2 SET Value = 30 WHERE ID = 2;  -- 锁定行B
  UPDATE Table1 SET Value = 40 WHERE ID = 1;  -- 被T1阻塞
  ```

  两个事务均无法继续执行，直到DBMS解除死锁

---

### 示例4：表级阻塞

- **场景**：事务T1在没有合适索引的情况下对整个表进行大规模更新，事务T2尝试从同一表读取单行数据
- **运行机制**：T1可能将行级锁升级为表级锁，导致T2即使读取不相关行也会被阻塞
- **SQL示例**：

  ```sql
  -- 事务T1
  BEGIN TRANSACTION;
  UPDATE Employees SET Salary = Salary * 1.1;  -- 锁定整张数据表

  -- 事务T2（被阻塞）
  SELECT Name FROM Employees WHERE EmployeeID = 5;
  ```

  由于T1持有表级排他锁，T2操作被阻塞

---

### 阻塞管理机制

- **锁机制**：数据库通过共享锁（用于读操作）和排他锁（用于写操作）控制访问权限
- **隔离级别**：较高隔离级别（如可序列化）会增强阻塞以确保一致性，较低级别（如读未提交）则减少阻塞但可能产生脏读
- **超时机制**：事务被阻塞过久时会触发超时强制回滚
- **死锁检测**：DBMS通过终止其中一个事务来检测和解除死锁

如果您需要针对特定数据库系统（如MySQL、PostgreSQL、SQL Server）的更多细节或示例，欢迎随时告知！
