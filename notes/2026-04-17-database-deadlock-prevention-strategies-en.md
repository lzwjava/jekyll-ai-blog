---
audio: false
generated: true
image: false
lang: en
layout: post
title: Database Deadlock Prevention Strategies
translated: false
type: note
---

Question:
How does deadlock happen in a database like MySQL or DB2, and is it better to execute SQL statements one by one or batch them into a transaction to reduce deadlock probability?

Answer:

### 1. How deadlocks happen in databases

A **deadlock** occurs when two (or more) transactions are waiting on each other’s locks in a cycle.

Classic example:

* Transaction A:

  ```sql
  UPDATE table SET ... WHERE id = 1;  -- locks row 1
  UPDATE table SET ... WHERE id = 2;  -- waits for row 2
  ```

* Transaction B:

  ```sql
  UPDATE table SET ... WHERE id = 2;  -- locks row 2
  UPDATE table SET ... WHERE id = 1;  -- waits for row 1
  ```

Now:

* A waits for B (row 2)
* B waits for A (row 1)

→ **Deadlock formed**

Both MySQL (InnoDB) and IBM Db2 detect this and **kill one transaction** to break the cycle.

---

### 2. What actually causes deadlocks (important mental model)

Deadlocks are not about *time alone*, but about:

* **Lock order inconsistency**
* **Lock overlap**
* **Concurrency**

Key factors:

| Factor                    | Effect                |
| ------------------------- | --------------------- |
| Different access order    | 🚨 Main cause         |
| Long transaction duration | Increases probability |
| High concurrency          | Increases contention  |
| Range locks / index gaps  | Makes it worse        |

---

### 3. Your idea: “execute SQL one by one vs batch in transaction”

You are thinking:

> many small SQL calls → lock/unlock repeatedly → more contention
> batch SQLs → shorter total lock time → better

This is **partially correct but incomplete**.

Let’s analyze both:

---

### Case A: Execute SQL one-by-one (auto-commit mode)

Each SQL:

* starts a transaction
* acquires lock
* commits immediately
* releases lock

**Pros:**

* Locks are held **very briefly**
* Lower chance of long blocking

**Cons:**

* More round trips
* No atomicity
* Still can deadlock if overlapping happens at the same time

---

### Case B: Batch SQLs in a transaction

```sql
BEGIN;
UPDATE ...;
UPDATE ...;
COMMIT;
```

**Pros:**

* Fewer round trips
* Better consistency (atomic)
* Can enforce consistent lock order

**Cons:**

* Locks are held **longer**
* If badly designed → **more deadlock risk**

---

### 4. Your key assumption: “200ms vs 20ms lock time”

This is where you need correction.

👉 **Deadlocks are NOT proportional to total lock time alone**

Even a **20ms transaction can deadlock** if:

* lock order is inconsistent
* two transactions overlap in the wrong pattern

And a **200ms transaction may NOT deadlock** if:

* all transactions use the same lock order

---

### 5. What actually reduces deadlocks (important)

#### ✅ 1. Consistent lock ordering (MOST IMPORTANT)

Always access rows/tables in the same order:

```sql
-- Always do id=1 then id=2 (never reverse)
```

This alone eliminates most deadlocks.

---

#### ✅ 2. Keep transactions short (but not fragmented)

* Short ≠ many tiny auto-commit SQLs
* Short = minimal time between `BEGIN` and `COMMIT`

---

#### ✅ 3. Proper indexing

Without index:

```sql
UPDATE table WHERE non_index_column = ...
```

→ may lock **many rows or even full table**

---

#### ✅ 4. Avoid unnecessary locks

* Use `SELECT ... FOR UPDATE` only when needed
* Choose correct isolation level (e.g., avoid SERIALIZABLE unless needed)

---

#### ✅ 5. Retry logic

Deadlocks are **normal in high concurrency systems**

Both MySQL and DB2 expect:

```pseudo
try:
    run transaction
catch deadlock:
    retry
```

---

### 6. Final answer to your question

> Is batching SQLs into a transaction better than executing one-by-one?

👉 **Answer: It depends, but generally YES—with conditions**

* ✅ Better for correctness and performance
* ✅ Can reduce contention if designed well
* ❌ Can increase deadlocks if lock order is inconsistent

---

### 7. Correct mental model (important takeaway)

Instead of thinking:

> “reduce total lock time from 200ms → 20ms”

Think:

> “ensure all transactions acquire locks in the SAME ORDER and finish QUICKLY”

That’s what really prevents deadlocks.

---

### 8. Simple intuition

* Deadlock = **circular dependency**, not just “slow locks”
* Time increases probability, but **order creates the problem**

---

If you want, I can show you **real InnoDB deadlock logs** and how to analyze them line-by-line—that’s where understanding becomes very concrete.