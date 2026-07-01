---
audio: false
generated: true
image: false
lang: en
layout: post
title: Producer-Consumer Contract Principle
translated: false
type: note
---

**Question:** Is the producer-consumer principle (producer enqueues work, consumer must have correct logic and environment to handle it, otherwise it breaks) a general software design rule, or specific to message queues like Kafka?

**Answer:**

You're correct — this is **general software design**, not Kafka-specific. It's about the **contract boundary** between any producer and consumer.

The core principle: **Whoever calls/enqueues work makes a claim; whoever handles it must satisfy that claim.** If either side fails, the system breaks.

## Where It Shows Up

**1. Function calls (basic level)**

```python
def process_user(user_dict):
    return user_dict["email"].lower()  # ASSUMES email key exists

# Producer breaks contract
user = {"name": "Alice"}  # missing email
process_user(user)  # KeyError — consumer can't handle
```

**2. REST APIs**

```python
@app.post("/users")
def create_user(data):
    return db.save(data)  # ASSUMES valid schema

# Bad producer (client sends malformed data)
POST /users {"age": "not-a-number"}  # 400 Bad Request
```

**3. Thread/async task queues**

```python
class TaskQueue:
    def enqueue(self, task_func, *args):
        # Producer claim: task_func is callable and args match its signature
        # Consumer claim: I'll call task_func(*args)

        # If args mismatch:
        self.worker.run(task_func, *args)  # TypeError — crash
```

**4. Database constraints**

```sql
-- Producer (application code) claims: this INSERT respects foreign keys
INSERT INTO orders (user_id, product_id) VALUES (999, 1);
-- If user_id=999 doesn't exist, constraint violation — consumer (DB) rejects
```

**5. Kafka/message queues (specific instance)**

```python
# Producer publishes message
producer.send("orders", {"user_id": 123, "items": "not-a-list"})

# Consumer expects items to be list
for item in message["items"]:  # TypeError on string iteration
    process(item)
```

## The Real Pattern

This is the **Liskov Substitution Principle** applied to producer-consumer contracts:

- **Producer's job**: Make only valid claims about what it produces
- **Consumer's job**: Validate those claims before processing
- **Breaking point**: Producer violates contract OR consumer doesn't validate

```python
# FRAGILE (no validation)
def consume(message):
    user_id = message["user_id"]  # Assumes key exists
    amount = message["amount"]     # Assumes numeric
    return charge(user_id, amount)

# ROBUST (validates contract)
def consume(message):
    try:
        user_id = int(message.get("user_id"))
        amount = float(message.get("amount"))
        if amount <= 0 or amount > 1_000_000:
            raise ValueError("amount out of bounds")
        return charge(user_id, amount)
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Invalid message: {e}")
        # Dead-letter queue, retry, alert — your choice
```

## Where It Differs by Context

| Context | Producer's Obligation | Consumer's Obligation |
| --------- | ---------------------- | ---------------------- |
| **Function call** | Pass correct types/args | Return promised type |
| **REST API** | Send valid schema | Return promised HTTP status/body |
| **Message queue** | Serialize correctly, respect schema | Deserialize + validate before processing |
| **Database** | Respect constraints | Enforce constraints |
| **File I/O** | Write valid format | Parse/validate before use |

## The Kafka-Specific Wrinkle

Kafka makes this **more visible** because:

1. Producer and consumer are **decoupled in time/space** — producer can't see consumer fail in real-time
2. **Schema drift**: Producer might emit new fields; old consumer crashes
3. **Async nature**: Failures don't bubble up immediately

But the principle is identical everywhere — just the failure mode is delayed and often silent (poison pill messages pile up).

**Bottom line**: This is **universal software design**. Kafka is just a context where the producer-consumer contract is more explicit and failures are more obvious.
