---
audio: false
generated: true
lang: en
layout: post
title: Redis Guide
translated: false
type: note
---

Here’s a comprehensive guide to Redis, an open-source, in-memory data structure store widely used as a database, cache, and message broker. This guide will cover its fundamentals, features, use cases, installation, basic operations, and advanced concepts.

---

### What is Redis?

Redis (Remote Dictionary Server) is a high-performance, key-value store that operates primarily in memory, making it exceptionally fast. It supports various data structures such as strings, hashes, lists, sets, sorted sets, bitmaps, hyperloglogs, and geospatial indexes. Created by Salvatore Sanfilippo in 2009, Redis is now maintained by a community and sponsored by Redis Inc.

Key characteristics:

- **In-memory**: Data is stored in RAM for low-latency access.
- **Persistent**: Offers optional disk persistence for durability.
- **Versatile**: Supports complex data structures beyond simple key-value pairs.
- **Scalable**: Provides clustering and replication for high availability.

---

### Why Use Redis?

Redis is popular for its speed and flexibility. Common use cases include:

1. **Caching**: Speeds up applications by storing frequently accessed data (e.g., API responses, web pages).
2. **Session Management**: Stores user session data in web applications.
3. **Real-time Analytics**: Tracks metrics, leaderboards, or event counters.
4. **Pub/Sub Messaging**: Enables real-time messaging between processes or services.
5. **Task Queues**: Manages background jobs (e.g., with tools like Celery).
6. **Geospatial Applications**: Handles location-based queries (e.g., finding nearby points of interest).

---

### Key Features

1. **Data Structures**:
   - **Strings**: Simple key-value pairs (e.g., `SET key "value"`).
   - **Lists**: Ordered collections (e.g., `LPUSH mylist "item"`).
   - **Sets**: Unordered, unique collections (e.g., `SADD myset "item"`).
   - **Sorted Sets**: Sets with scores for ranking (e.g., `ZADD leaderboard 100 "player1"`).
   - **Hashes**: Key-value mappings (e.g., `HSET user:1 name "Alice"`).
   - **Bitmaps, HyperLogLogs, Streams**: For specialized use cases like counting unique users or event streaming.

2. **Persistence**:
   - **RDB (Snapshotting)**: Periodically saves data to disk as a point-in-time snapshot.
   - **AOF (Append-Only File)**: Logs every write operation for durability; can be replayed to rebuild the dataset.

3. **Replication**: Master-slave replication for high availability and read scalability.
4. **Clustering**: Distributes data across multiple nodes for horizontal scaling.
5. **Atomic Operations**: Ensures safe concurrent access with commands like `INCR` or `MULTI`.
6. **Lua Scripting**: Allows custom server-side logic.
7. **Pub/Sub**: Lightweight messaging system for real-time communication.

---

### Installation

Redis is available on Linux, macOS, and Windows (via WSL or unofficial builds). Here’s how to install it on a Linux system:

1. **Via Package Manager** (Ubuntu/Debian):

   ```bash
   sudo apt update
   sudo apt install redis-server
   ```

2. **From Source**:

   ```bash
   wget http://download.redis.io/releases/redis-7.0.15.tar.gz
   tar xzf redis-7.0.15.tar.gz
   cd redis-7.0.15
   make
   sudo make install
   ```

3. **Start Redis**:

   ```bash
   redis-server
   ```

4. **Verify Installation**:

   ```bash
   redis-cli ping
   ```

   Output: `PONG`

5. **Configuration**: Edit `/etc/redis/redis.conf` (or equivalent) to tweak settings like persistence, memory limits, or binding to specific IPs.

---

### Basic Operations

Redis uses a simple command-based interface via `redis-cli` or client libraries. Here are some examples:

#### Strings

- Set a value: `SET name "Alice"`
- Get a value: `GET name` → `"Alice"`
- Increment: `INCR counter` → `1` (increments to 2, 3, etc.)

#### Lists

- Add to left: `LPUSH mylist "item1"`
- Add to right: `RPUSH mylist "item2"`
- Pop from left: `LPOP mylist` → `"item1"`

#### Sets

- Add items: `SADD myset "apple" "banana"`
- List members: `SMEMBERS myset` → `"apple" "banana"`
- Check membership: `SISMEMBER myset "apple"` → `1` (true)

#### Hashes

- Set fields: `HSET user:1 name "Bob" age "30"`
- Get field: `HGET user:1 name` → `"Bob"`
- Get all fields: `HGETALL user:1`

#### Sorted Sets

- Add with score: `ZADD leaderboard 100 "player1" 200 "player2"`
- Get top scores: `ZRANGE leaderboard 0 1 WITHSCORES` → `"player1" "100" "player2" "200"`

---

### Advanced Concepts

1. **Persistence Configuration**:
   - Enable RDB: Set `save 60 1000` in `redis.conf` (save every 60s if 1000 keys change).
   - Enable AOF: Set `appendonly yes` for write logging.

2. **Replication**:
   - Configure a slave: `SLAVEOF master_ip master_port`.
   - Check status: `INFO REPLICATION`.

3. **Clustering**:
   - Enable with `cluster-enabled yes` in `redis.conf`.
   - Use `redis-cli --cluster create` to set up nodes.

4. **Eviction Policies**:
   - Control memory usage with `maxmemory` and policies like `LRU` (least recently used) or `LFU` (least frequently used).
   - Example: `maxmemory-policy allkeys-lru`.

5. **Transactions**:
   - Group commands: `MULTI`, followed by commands, then `EXEC`.
   - Example:

     ```
     MULTI
     SET key1 "value1"
     SET key2 "value2"
     EXEC
     ```

6. **Pub/Sub**:
   - Subscribe: `SUBSCRIBE channel1`
   - Publish: `PUBLISH channel1 "Hello"`

---

### Client Libraries

Redis supports many programming languages. Examples:

- **Python**: `redis-py` (`pip install redis`)

  ```python
  import redis
  r = redis.Redis(host='localhost', port=6379, db=0)
  r.set('key', 'value')
  print(r.get('key'))  # b'value'
  ```

- **Node.js**: `ioredis`

  ```javascript
  const Redis = require('ioredis');
  const redis = new Redis();
  redis.set('key', 'value');
  redis.get('key').then(console.log); // 'value'
  ```

---

### Performance Tips

1. **Use Pipelining**: Batch commands to reduce round-trip latency.
2. **Optimize Data Structures**: Choose the right structure (e.g., use hashes for small objects instead of multiple keys).
3. **Monitor Memory**: Use `INFO MEMORY` to track usage.
4. **Tune Persistence**: Balance speed (RDB) and durability (AOF).

---

### Security

- **Bind to localhost**: Set `bind 127.0.0.1` in `redis.conf` to restrict access.
- **Set a Password**: Use `requirepass yourpassword`.
- **Disable Dangerous Commands**: Use `rename-command` (e.g., `rename-command FLUSHALL ""`).

---

### Limitations

- **Memory-bound**: Data size is limited by available RAM.
- **Single-threaded**: Core operations run on one thread (though I/O and persistence can use multiple threads in newer versions).
- **No Complex Queries**: Lacks SQL-like querying; relies on key-based access.

---

### Redis vs. Other Databases

- **Redis vs. Memcached**: Redis offers richer data structures and persistence; Memcached is simpler and purely in-memory.
- **Redis vs. MongoDB**: Redis is faster for caching but less suited for complex, persistent document storage.
- **Redis vs. PostgreSQL**: Redis excels at real-time, low-latency tasks; PostgreSQL is better for relational data and ACID compliance.

---

### Resources

- **Official Docs**: [redis.io](https://redis.io)
- **Try Redis**: [try.redis.io](https://try.redis.io) (interactive tutorial)
- **GitHub**: [github.com/redis/redis](https://github.com/redis/redis)

---

This guide provides a solid foundation for understanding and using Redis. Let me know if you’d like a deeper dive into any specific aspect!
