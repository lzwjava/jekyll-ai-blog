---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding ACID Database Properties
translated: false
type: note
---

Question: How to understand the ACID properties (Atomicity, Consistency, Isolation, Durability) in databases?

Answer: 

ACID is an acronym that stands for **Atomicity**, **Consistency**, **Isolation**, and **Durability**. These four properties are fundamental guarantees provided by transactional database management systems (DBMS) to ensure that database transactions are processed reliably and correctly, even in the presence of errors, power failures, or concurrent access.

### 1. **Atomicity**
   - **Definition**: Atomicity ensures that a transaction is treated as a single, indivisible unit of work. Either **all** operations in the transaction are completed successfully, or **none** of them are applied.
   - **Key idea**: "All or nothing."
   - **How it's achieved**: Using **commit** (make changes permanent) and **rollback** (undo changes if something fails) mechanisms.
   - **Example**: In a bank transfer of $100 from Account A to Account B:
     - Debit $100 from A.
     - Credit $100 to B.
     - If the debit succeeds but the credit fails (e.g., due to a crash), atomicity guarantees the debit is rolled back. The database returns to its original state.

### 2. **Consistency**
   - **Definition**: Consistency ensures that a transaction brings the database from one **valid state** to another valid state. All defined rules, constraints, and data integrity conditions (e.g., primary keys, foreign keys, check constraints) must be satisfied before and after the transaction.
   - **Key idea**: The database never sees invalid or intermediate data that violates its rules.
   - **Example**: If a table has a constraint that account balances must never be negative:
     - A withdrawal transaction of $200 from an account with $150 must fail or be rolled back.
     - After any transaction, all balances remain ≥ 0.

### 3. **Isolation**
   - **Definition**: Isolation ensures that transactions are executed in isolation from one another. Even if multiple transactions run concurrently, the intermediate state of one transaction is not visible to others until it is committed.
   - **Key idea**: Concurrent transactions behave as if they were executed serially (one after another).
   - **How it's achieved**: Through **locking**, **multiversion concurrency control (MVCC)**, or other concurrency control mechanisms.
   - **Common isolation levels** (from weakest to strongest): Read Uncommitted, Read Committed, Repeatable Read, Serializable.
   - **Example**: Two users trying to book the last seat on a flight simultaneously:
     - Isolation prevents both from seeing the seat as available at the same time, avoiding double-booking.

### 4. **Durability**
   - **Definition**: Durability guarantees that once a transaction is committed, its changes are permanently saved to the database, even in the event of a system crash or power failure.
   - **Key idea**: Committed data is never lost.
   - **How it's achieved**: By writing changes to **non-volatile storage** (e.g., disk) using **write-ahead logging (WAL)** or transaction logs before acknowledging commit.
   - **Example**: After a successful bank transfer commit, even if the server crashes immediately afterward, the transfer remains recorded when the system restarts.

### Why ACID Matters
ACID properties are crucial for applications requiring high reliability, such as banking, e-commerce, and inventory systems. Databases that fully support ACID (e.g., PostgreSQL, Oracle, traditional SQL Server) are often called "ACID-compliant." In contrast, many NoSQL databases prioritize availability and performance over strict ACID compliance, sometimes offering "eventual consistency" instead.

In summary, ACID ensures **reliability**, **correctness**, and **robustness** of database transactions in the face of failures and concurrency.