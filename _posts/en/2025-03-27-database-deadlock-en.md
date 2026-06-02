---
audio: false
generated: true
lang: en
layout: post
title: Database Deadlock
translated: false
type: note
---

A **database deadlock** occurs when two or more transactions are waiting for each other to release locks on resources, creating a circular dependency that prevents any of them from proceeding. The database management system (DBMS) typically detects this situation and resolves it by rolling back one of the transactions. Below is a detailed example of a deadlock scenario:

---

### Example: Deadlock Between Two Transactions

- **Scenario**:
  - Transaction T1 updates a row in the `Orders` table and then needs to update a row in the `Customers` table.
  - Transaction T2 updates a row in the `Customers` table and then needs to update a row in the `Orders` table.
  - Both transactions lock resources in a different order, leading to a deadlock.

- **Step-by-Step**:
  1. T1 locks a row in `Orders`.
  2. T2 locks a row in `Customers`.
  3. T1 tries to lock the row in `Customers` (blocked by T2).
  4. T2 tries to lock the row in `Orders` (blocked by T1).
  - Result: Neither transaction can proceed, creating a deadlock.

- **SQL Example**:

  ```sql
  -- Transaction T1
  BEGIN TRANSACTION;
  UPDATE Orders SET Status = 'Shipped' WHERE OrderID = 100;  -- Locks OrderID 100
  -- (some delay or processing)
  UPDATE Customers SET LastOrderDate = '2025-03-27' WHERE CustomerID = 1;  -- Blocked by T2

  -- Transaction T2
  BEGIN TRANSACTION;
  UPDATE Customers SET Balance = Balance - 50 WHERE CustomerID = 1;  -- Locks CustomerID 1
  -- (some delay or processing)
  UPDATE Orders SET PaymentStatus = 'Paid' WHERE OrderID = 100;  -- Blocked by T1
  ```

- **What Happens**:
  - T1 holds an exclusive lock on `OrderID = 100` and waits for `CustomerID = 1`.
  - T2 holds an exclusive lock on `CustomerID = 1` and waits for `OrderID = 100`.
  - This circular wait condition is a deadlock.
  - The DBMS detects this (e.g., via a timeout or deadlock detection algorithm) and rolls back one transaction (e.g., T2), allowing T1 to complete.

---

### Visual Representation of the Deadlock

```
T1: Locks Orders(100) --> Wants Customers(1)
   |                        ↑
   |                        |
T2: Wants Orders(100)  <-- Locks Customers(1)
```

- **Resolution**: The DBMS might output an error like:

  ```
  Transaction T2 was deadlocked on lock resources with another process and has been chosen as the deadlock victim. Rerun the transaction.
  ```

---

### Why It Happens

- **Locking Order**: T1 and T2 acquire locks in a different sequence (T1: Orders → Customers; T2: Customers → Orders).
- **Concurrency**: Both transactions run simultaneously and need overlapping resources.
- **Exclusive Locks**: Updates require exclusive locks, which prevent other transactions from accessing the same data.

---

### How to Avoid Deadlocks

1. **Consistent Lock Order**: Ensure all transactions acquire locks in the same order (e.g., always lock `Orders` before `Customers`).

   ```sql
   -- Both T1 and T2 should lock Orders first, then Customers
   ```

2. **Reduce Transaction Time**: Minimize delays within transactions to reduce the chance of overlap.
3. **Use Lower Isolation Levels**: If appropriate, use a less strict isolation level (e.g., Read Committed) to reduce locking duration.
4. **Timeouts**: Set shorter lock timeouts to fail fast and retry.

---

Let me know if you'd like a more specific example (e.g., with a particular DBMS like PostgreSQL or SQL Server) or further clarification!
