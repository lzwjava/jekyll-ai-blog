---
audio: false
generated: true
lang: en
layout: post
title: Database Blocking
translated: false
type: note
---

I assume you're asking for examples of database blocking in the context of database management systems (DBMS). Blocking occurs when one transaction in a database prevents another transaction from proceeding because they are trying to access or modify the same data concurrently. This is typically managed using locks to ensure data consistency and integrity. Below are some examples of database blocking scenarios:

---

### Example 1: Read-Write Blocking

- **Scenario**: Transaction T1 is updating a row in a table (e.g., changing a customer's balance), and Transaction T2 tries to read that same row.
- **What Happens**: T1 acquires an exclusive lock on the row to prevent other transactions from reading or modifying it until the update is complete. T2 is blocked and must wait until T1 commits or rolls back.
- **SQL Example**:

  ```sql
  -- Transaction T1
  BEGIN TRANSACTION;
  UPDATE Accounts SET Balance = Balance - 100 WHERE AccountID = 1;

  -- Transaction T2 (blocked)
  SELECT Balance FROM Accounts WHERE AccountID = 1;
  ```

  T2 waits until T1 finishes because of the exclusive lock on the row.

---

### Example 2: Write-Write Blocking

- **Scenario**: Transaction T1 is updating a product’s stock quantity, and Transaction T2 tries to update the same product’s stock at the same time.
- **What Happens**: T1 holds an exclusive lock on the row, and T2 is blocked until T1 completes. This prevents conflicting updates that could lead to data inconsistency.
- **SQL Example**:

  ```sql
  -- Transaction T1
  BEGIN TRANSACTION;
  UPDATE Products SET Stock = Stock - 5 WHERE ProductID = 100;

  -- Transaction T2 (blocked)
  UPDATE Products SET Stock = Stock + 10 WHERE ProductID = 100;
  ```

  T2 is blocked until T1 commits or rolls back.

---

### Example 3: Deadlock (Blocking Leading to Stalemate)

- **Scenario**: Transaction T1 locks Row A and needs to update Row B, while Transaction T2 locks Row B and needs to update Row A.
- **What Happens**: T1 is blocked by T2’s lock on Row B, and T2 is blocked by T1’s lock on Row A. This creates a deadlock, and the DBMS must intervene (e.g., by rolling back one transaction).
- **SQL Example**:

  ```sql
  -- Transaction T1
  BEGIN TRANSACTION;
  UPDATE Table1 SET Value = 10 WHERE ID = 1;  -- Locks Row A
  UPDATE Table2 SET Value = 20 WHERE ID = 2;  -- Blocked by T2

  -- Transaction T2
  BEGIN TRANSACTION;
  UPDATE Table2 SET Value = 30 WHERE ID = 2;  -- Locks Row B
  UPDATE Table1 SET Value = 40 WHERE ID = 1;  -- Blocked by T1
  ```

  Neither transaction can proceed until the DBMS resolves the deadlock.

---

### Example 4: Table-Level Blocking

- **Scenario**: Transaction T1 is performing a large update on an entire table without proper indexing, and Transaction T2 tries to read a single row from the same table.
- **What Happens**: T1 might escalate its row-level locks to a table-level lock, blocking T2 from even reading unrelated rows until T1 completes.
- **SQL Example**:

  ```sql
  -- Transaction T1
  BEGIN TRANSACTION;
  UPDATE Employees SET Salary = Salary * 1.1;  -- Locks the entire table

  -- Transaction T2 (blocked)
  SELECT Name FROM Employees WHERE EmployeeID = 5;
  ```

  T2 is blocked because T1 has a table-level exclusive lock.

---

### How Blocking is Managed

- **Locks**: Databases use shared locks (for reading) and exclusive locks (for writing) to control access.
- **Isolation Levels**: Higher isolation levels (e.g., Serializable) increase blocking to ensure consistency, while lower levels (e.g., Read Uncommitted) reduce blocking but risk dirty reads.
- **Timeouts**: Transactions can time out if blocked for too long, forcing a rollback.
- **Deadlock Detection**: DBMS detects and resolves deadlocks by terminating one transaction.

Let me know if you'd like more details or examples specific to a particular database system (e.g., MySQL, PostgreSQL, SQL Server)!
