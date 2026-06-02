---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Memcached In-Memory Caching System Overview
translated: false
type: note
---

### What is Memcached?

Memcached is an open-source, high-performance, distributed memory object caching system. It's primarily used to speed up dynamic web applications (like those built with PHP frameworks such as CodeIgniter) by caching database query results, API responses, or other computationally expensive data in RAM. This reduces the load on databases and improves application response times. It's not a full-fledged database but a simple key-value store designed for temporary data storage.

### How Does Memcached Work?

Memcached operates as a daemon (background process) that runs on one or more servers, typically started with commands like `memcached -p 11211 -m 64` (specifying port and memory limit). Here's a simplified overview:

1. **In-Memory Storage**: It stores data as key-value pairs entirely in RAM for fast access. Each value can be up to 1 MB, and keys are strings up to 250 characters. Data is volatile—if the server restarts, cached data is lost.

2. **Client-Server Model**: Applications (clients) connect to Memcached via TCP or UDP protocols. The provided CodeIgniter configuration snippet shows a PHP setup connecting to a local Memcached instance:
   - **Hostname**: '127.0.0.1' (localhost, meaning the same server as your app).
   - **Port**: '11211' (Memcached's default port).
   - **Weight**: '1' (defines server priority in a cluster; higher values mean more load).

3. **Operations**:
   - Set: Store a key-value pair with an optional expiration time (e.g., `set app_name 0 3600 13\n"cached_data"` via telnet).
   - Get: Retrieve a value by key.
   - Delete: Remove by key.
   It uses a simple hashing algorithm to distribute keys across servers in a clustered setup (e.g., consistent hashing to handle server additions/removals).

4. **Eviction and Scaling**: If memory fills up, it uses an LRU (Least Recently Used) policy to evict old data. Scaling involves multiple server instances, often auto-discovered via tools like moxi or external sharding.

Performance peaks at millions of operations per second, but it's optimized for read-heavy workloads. Monitoring tools like memcached-top can track usage.

### Comparison to Redis

While both Memcached and Redis are in-memory, key-value data stores used for caching and high-speed data access, they differ in features, architecture, and use cases:

| Aspect          | Memcached                              | Redis                                                  |
|-----------------|----------------------------------------|--------------------------------------------------------|
| **Data Types** | Simple strings (just keys/values).     | Supports strings, hashes, lists, sets, sorted sets, bitmaps, hyperloglogs, and more. Allows complex data structures (e.g., JSON objects or counters). |
| **Persistence**| None—data is pure RAM; lost on restart.| Optional persistence (AOF or RDB snapshots) to disk, enabling data recovery. |
| **Eviction**   | LRU only.                             | LRU, LFU (Least Frequently Used), or volatile TTL-based evictions. |
| **Operations** | Basic set/get/delete/multiget.         | Thousands of commands (e.g., pub/sub, transactions, Lua scripting, geospatial queries). Supports atomic operations like increment. |
| **Performance**| Slightly faster for simple read/write (multigets help). | Excellent overall, but slightly overhead for complex structures. Benchmarks show Memcached edging out for pure caching in low- complexity scenarios. |
| **Scaling & Clustering** | Built-in via consistent hashing; no native clustering (use external partitioning). | Supports native clustering, replication (master-slave), and Redis Cluster for automatic partitioning. |
| **Use Cases** | Ideal for web app caching (e.g., session or query caches), like in CodeIgniter setups. Simple and lightweight. | Broader: caching, session storage, message queues, real-time analytics, or even as a full database alternative. |
| **Memory Efficiency** | Efficient for fixed-size data; no compression. | Better for large datasets with compression options (Redis 5+). |
| **Protocol**   | Custom binary/text protocols.         | RESP (Redis Serialization Protocol) with better error handling. |
| **Licensing & Ecosystem** | Open-source (BSD), widely used in LAMP stacks. | Open-source (BSD), larger community with tools like RedisInsight. |

In summary, choose Memcached for simplicity and speed in basic caching (as shown in your CodeIgniter config). Opt for Redis if you need persistence, advanced data types, or features like pub/sub messaging. If migrating from Memcached, projects like redis-memcached offer compatibility layers, but Redis often replaces Memcached due to its versatility. For CodeIgniter specifically, the config allows seamless swapping between drivers.
