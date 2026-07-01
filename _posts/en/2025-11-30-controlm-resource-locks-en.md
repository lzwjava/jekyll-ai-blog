---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Control-M Resource Locks Explained
translated: false
type: note
---

In Control-M (the workload automation tool by BMC), a **lock** typically refers to a **resource lock** or more commonly to **Control-M Resources** of type **Control Resource** (also called **Quantitative Resources** or simply **Locks** in some contexts).

### What is a "Lock" in Control-M?

A **Control Resource** (often used as a lock) is a mechanism to **limit concurrency** or **serialize access** to a shared resource (e.g., a file, a database connection pool, a license seat, a server, etc.).

- It behaves like a semaphore or a mutex.
- You define a Control Resource with a certain quantity (e.g., quantity = 1 means only one job can use it at a time; quantity = 5 means up to 5 jobs can use it concurrently).
- Jobs that need the resource will **wait** in the queue if the required number of units is not available.
- When the job ends (OK or NOT OK), the resource is automatically released.

### Common Use Cases for Locks in Control-M

| Use Case | Typical Quantity | Purpose |
| ----------------------------------- | ------------------ | ------- |
| Only one job processes a file at a time | 1 | Prevent file corruption |
| Limit concurrent connections to a database | e.g., 10 | Avoid overloading the DB |
| Serialize jobs that update the same table | 1 | Ensure data consistency |
| Limit how many jobs run on a single server/agent | e.g., 3 | Prevent resource exhaustion |
| Software license management | Number of seats | Stay within license limits |

### How to Set It Up

1. In Control-M/EM (Enterprise Manager) or Control-M Self Service:
   - Go to **Resources** → **Control Resources**
   - Create a new Control Resource, e.g., name = `FILE_PROCESSING_LOCK`, quantity = 1
2. In the job definition (SMART folder or regular job):
   - Under **Resources** tab → add a **Control** resource
   - Specify the name (`FILE_PROCESSING_LOCK`) and how many units the job needs (usually 1)

### Example

If three jobs all require the Control Resource `DB_UPDATE_LOCK` with quantity = 1:

- First job starts → acquires the lock → runs
- Second and third jobs go into **Waiting for Resource** status
- When the first job ends, the lock is released → next job in line grabs it and runs

### Terminology Note

- In older versions of Control-M, these were sometimes explicitly called “Locks.”
- In modern versions (Control-M 9 and 10), the official name is **Control Resource**, but many long-time users and administrators still refer to them simply as “locks.”

So when someone in the Control-M world says “lock,” 99% of the time they mean a **Control Resource** used to control concurrency.
