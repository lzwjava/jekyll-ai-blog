---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Redis CLI and Server Options
translated: false
type: note
---

**Question:** Provide a comprehensive introduction to Redis command line options.

**Answer:** 

Redis has two main command-line programs people usually refer to when talking about "command line options":

- **`redis-server`** — starts the Redis server (most common when people ask about "Redis command line options")
- **`redis-cli`** — the interactive client / command-line interface to send commands to a running server

### 1. redis-server command line options (starting & configuring the server)

**Basic usage patterns**

```bash
redis-server                           # uses default redis.conf or built-in defaults
redis-server /path/to/redis.conf       # read config from file
redis-server --port 6380 --loglevel warning
redis-server /etc/redis.conf --daemonize yes --port 7777
redis-server -                         # read config from stdin
redis-server --help                    # shows usage + very short list
redis-server --version                 # shows version
```

**Important rule (since Redis ~2.8 onward)**

Almost every setting that exists in `redis.conf` can be overridden via command line using `--key value` syntax.

The command-line argument `--key` corresponds directly to a `key` directive in the config file.

Examples:

```bash
--port 6381
--bind 127.0.0.1 10.20.30.40
--protected-mode yes
--daemonize yes
--pidfile /var/run/redis_6380.pid
--logfile /var/log/redis_6380.log
--loglevel notice|verbose|debug|warning
--dbfilename dump-6380.rdb
--dir /var/redis-data/
--requirepass supersecret123
--maxmemory 4gb
--maxmemory-policy allkeys-lru
--save 900 1               # <seconds> <changes>
--save 300 10
--appendonly yes
--replicaof 10.55.1.20 6379
--masterauth somepass
--cluster-enabled yes
--tls-port 6379
--tls-cert-file ...
```

**Most frequently used overrides in production / dev**

- Connection & security
  - `--port 6379..6399`
  - `--bind 127.0.0.1` or `--bind 0.0.0.0` (careful!)
  - `--protected-mode yes/no`
  - `--requirepass yourpassword`
  - `--tls-port 6380 --tls-cert-file ...` (Redis 6+)

- Persistence
  - `--save ""`                     → disable RDB
  - `--appendonly yes`
  - `--appendfsync everysec`

- Memory & eviction
  - `--maxmemory 6gb`
  - `--maxmemory-policy volatile-lru | allkeys-lru | noeviction | ...`

- Replication & cluster
  - `--replicaof <masterip> <masterport>`
  - `--cluster-enabled yes`

- Background / paths
  - `--daemonize yes`
  - `--pidfile /var/run/redis.pid`
  - `--logfile stdout` or real path
  - `--dir /data/redis/`

**Tip:** `redis-server --help` shows only a very short list. For the real full possibilities run:

```bash
redis-server --help | less
# or just look at your redis.conf – almost every non-comment line can become --key
```

### 2. redis-cli command line options (client)

**Basic connection flags**

```bash
redis-cli                               # localhost:6379, db 0
redis-cli -h redis-15.example.com
redis-cli -h 10.20.30.40 -p 6381
redis-cli -u redis://:password@host:port/db   # URL style (Redis 6+)
redis-cli --pass supersecret123
redis-cli -a supersecret123                   # same as --pass
redis-cli -n 5                                # select db 5
redis-cli --tls --cacert ca.crt               # TLS options (Redis 6+)
```

**Useful modes & helpers**

| Flag / Style                  | Purpose                                          | Example                                      |
|-------------------------------|--------------------------------------------------|----------------------------------------------|
| `-r N` / `--repeat N`         | Repeat command N times                           | `redis-cli -r 1000 INCR counter`             |
| `-i 0.1`                      | Interval between repeats (seconds)               | `-r 100 -i 0.05`                             |
| `-x`                          | Read last argument from stdin                    | `echo value | redis-cli SET mykey -x`      |
| `-raw`                        | Raw output (no quotes, no type prefixes)         | good for scripting                           |
| `--scan`                      | Scan mode (very large keys)                      | `redis-cli --scan --pattern user:*`          |
| `-c`                          | Enable cluster mode (follow -MOVED redirection)  | Important on Redis Cluster                   |
| `--pipe`                      | Redis protocol bulk mode (very fast bulk load)   | `cat commands.txt | redis-cli --pipe`     |
| `--bigkeys`                   | Report biggest keys by type                      | Useful for memory investigation              |
| `--stat`                      | Continuous stats like redis-cli monitor          |                                              |
| `--latency` / `--latency-mode`| Latency testing tools                            | `--latency -h host`                          |
| `redis-cli --rdb /tmp/dump.rdb` | Ask server to generate RDB to a file           | Remote backup trick                          |

**One-liner command execution**

```bash
redis-cli KEYS "*"                  # dangerous on big instances
redis-cli -h prod-redis INFO        # get server info
redis-cli --raw GET user:1234:json  # no quotes in output
redis-cli EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey value
```

**Quick reference table – most common redis-cli flags**

| Flag          | Long version       | Typical usage                              |
|---------------|--------------------|--------------------------------------------|
| `-h`          | `--host`           | Hostname / IP                              |
| `-p`          | `--port`           | Port (default 6379)                        |
| `-a`          | `--pass`           | Password (legacy)                          |
| `--user`      | `--user`           | ACL username (Redis 6+)                    |
| `-n`          | `--db`             | Database number                            |
| `-c`          | `--cluster`        | Enable cluster support                     |
| `--tls`       | `--tls`            | Enable TLS                                 |
| `-raw`        | `--raw`            | Raw output format                          |
| `--pipe`      | `--pipe`           | Bulk protocol mode                         |
| `--scan`      | `--scan`           | Safer than KEYS *                          |

**References:**  

- https://redis.io/docs/latest/operate/oss_and_stack/management/config
- https://redis.io/docs/latest/develop/tools/cli
- https://redis.io/docs/latest/commands
- https://stackoverflow.com/questions/55078246/docs-for-redis-server-command-line-options