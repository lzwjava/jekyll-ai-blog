---
audio: false
generated: true
image: false
lang: en
layout: post
title: Managing Deadlocks in Shared Databases
translated: false
type: note
---

Question:
In a shared database used by multiple downstream systems, we can’t control other teams’ application logic. So is it realistic to ensure consistent lock ordering across all transactions, and are we limited to only controlling our own application behavior?

Answer:

You’re right about the core constraint: in a shared database, you **do not control global behavior**. Each team owns its own transactions, query patterns, and update order. So the “perfect world rule” (global consistent lock ordering) is usually **not enforceable end-to-end**.

But the conclusion is not “there’s nothing we can do”—it becomes:

> You cannot control everyone, but you can still **shape the system so deadlocks become rare and survivable**.

---

## 1. What is actually realistic in shared DB environments

In systems like MySQL or IBM Db2 used by multiple services:

### You *can’t control*:

* Other teams’ SQL order
* Their transaction boundaries
* Their isolation levels
* Their retry logic

### You *can control*:

* Your own lock ordering discipline
* Your transaction length
* Your indexing strategy
* Your query patterns
* Your concurrency level
* Your retry behavior

So yes: **local control only, not global coordination**

---

## 2. So does “consistent lock ordering” still matter?

Yes—but only **within your own application boundary**.

Think of it like this:

* Each service is a “mini universe”
* You ensure internal consistency
* The database is the shared battlefield

Even if other teams are chaotic, your own consistency:

* reduces your *contribution* to deadlocks
* prevents self-inflicted cycles
* avoids amplification effects

In practice, a large portion of deadlocks in production systems are actually **self-caused within one service**, not cross-service chaos.

---

## 3. Why batching vs single SQL is not the real answer

Your earlier framing:

> 200ms lock vs 20ms lock → batching is better

This is not the key dimension.

A better model:

### Deadlock probability depends on:

* overlap of transactions
* conflicting row access
* lock order mismatch

### NOT just:

* total lock duration

So batching can actually go either way:

| Approach                    | Effect                                      |
| --------------------------- | ------------------------------------------- |
| Many small auto-commit SQLs | shorter locks, but many interleavings       |
| Batch transaction           | fewer interleavings, but longer lock window |

So there is no universal “better”—only tradeoffs.

---

## 4. In shared DB systems, the real strategy is different

Instead of trying to eliminate deadlocks globally, production systems do this:

### (1) Accept deadlocks as normal

Both MySQL and DB2 explicitly assume:

* deadlocks will happen
* systems must retry

So production-grade systems rely on:

> **retry + idempotency**

---

### (2) Minimize your “deadlock footprint”

You can reduce your chance of participating:

* Always access tables in consistent order *within your service*
* Keep transactions tight (not necessarily split into many SQLs)
* Avoid mixing read-modify-write patterns unnecessarily
* Use proper indexes to avoid lock escalation
* Avoid long business logic inside transactions

---

### (3) Design for retry safety

If a deadlock happens:

* transaction is rolled back
* you retry automatically

So architecture assumes:

> “conflicts are inevitable, failure is transient”

---

## 5. The key mental correction

Your intuition:

> “We should reduce lock time to reduce deadlocks”

More accurate model:

> “We should reduce *conflict probability per transaction*, and assume retries will happen”

Because:

* even a 5ms transaction can deadlock under heavy concurrency
* even a 500ms transaction can be safe if access patterns don’t conflict

---

## 6. What “good engineering” looks like in shared DB environments

A mature approach usually includes:

### At application level (your control)

* consistent ordering inside your service
* short transactions
* retry on deadlock
* idempotent writes

### At system level (shared reality)

* accept cross-service contention
* avoid tight coupling through DB
* sometimes introduce queues or partitioning if contention grows

---

## 7. Final answer

Yes—you are correct that:

> In a shared database, you cannot enforce global lock ordering.

But the correct conclusion is not to focus on global control. Instead:

* You optimize **your own transaction discipline**
* You reduce your **conflict surface area**
* You design for **deadlock tolerance, not deadlock elimination**

In real-world large systems, stability comes less from “avoiding all deadlocks” and more from:

> “making deadlocks rare + making retries safe + keeping impact small”

---

If you want, I can break down a real production pattern like:
**how high-scale banking systems or payment systems design DB access to survive constant deadlocks without user-visible failure**.
