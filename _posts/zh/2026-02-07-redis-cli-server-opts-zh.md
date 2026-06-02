---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Redis CLI 与服务器选项
translated: true
type: note
---

**Question:** 请提供 Redis 命令行选项的全面介绍。

**Answer:**

当提到 “Redis 命令行选项” 时，通常指的是两个主要的命令行程序：

- **`redis-server`** — 启动 Redis server（人们询问 “Redis 命令行选项” 时最常指代的对象）
- **`redis-cli`** — 用于向运行中的服务器发送命令的交互式 client / 命令行界面

### 1. redis-server 命令行选项（启动与配置服务器）

**基本使用模式**

```bash
redis-server                           # 使用默认的 redis.conf 或内置默认值
redis-server /path/to/redis.conf       # 从文件读取配置
redis-server --port 6380 --loglevel warning
redis-server /etc/redis.conf --daemonize yes --port 7777
redis-server -                         # 从 stdin 读取配置
redis-server --help                    # 显示用法及简短列表
redis-server --version                 # 显示版本
```

**重要规则（自 Redis 2.8 及以上版本起）**

几乎所有存在于 `redis.conf` 中的设置都可以通过命令行使用 `--key value` 语法进行覆盖。

命令行参数 `--key` 直接对应配置文件中的 `key` 指令。

示例：

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

**在生产 / 开发环境中最常用的覆盖选项**

- 连接与安全
  - `--port 6379..6399`
  - `--bind 127.0.0.1` 或 `--bind 0.0.0.0`（需谨慎！）
  - `--protected-mode yes/no`
  - `--requirepass yourpassword`
  - `--tls-port 6380 --tls-cert-file ...` (Redis 6+)

- 持久化 (Persistence)
  - `--save ""`                     → 禁用 RDB
  - `--appendonly yes`
  - `--appendfsync everysec`

- 内存与逐出 (Memory & eviction)
  - `--maxmemory 6gb`
  - `--maxmemory-policy volatile-lru | allkeys-lru | noeviction | ...`

- 复制与集群 (Replication & cluster)
  - `--replicaof <masterip> <masterport>`
  - `--cluster-enabled yes`

- 后台运行与路径
  - `--daemonize yes`
  - `--pidfile /var/run/redis.pid`
  - `--logfile stdout` 或实际路径
  - `--dir /data/redis/`

**提示：** `redis-server --help` 仅显示非常简短的列表。要查看完整的可能性，请运行：

```bash
redis-server --help | less
# 或者直接查看你的 redis.conf —— 几乎每一行非注释行都可以变成 --key
```

### 2. redis-cli 命令行选项 (client)

**基本连接标志 (Flags)**

```bash
redis-cli                               # localhost:6379, db 0
redis-cli -h redis-15.example.com
redis-cli -h 10.20.30.40 -p 6381
redis-cli -u redis://:password@host:port/db   # URL 风格 (Redis 6+)
redis-cli --pass supersecret123
redis-cli -a supersecret123                   # 与 --pass 相同
redis-cli -n 5                                # 选择 db 5
redis-cli --tls --cacert ca.crt               # TLS 选项 (Redis 6+)
```

**实用的模式与辅助工具**

| Flag / 风格                    | 用途                                             | 示例                                         |
|-------------------------------|--------------------------------------------------|----------------------------------------------|
| `-r N` / `--repeat N`         | 重复执行命令 N 次                                | `redis-cli -r 1000 INCR counter`             |
| `-i 0.1`                      | 重复执行的间隔时间（秒）                         | `-r 100 -i 0.05`                             |
| `-x`                          | 从 stdin 读取最后一个参数                         | `echo value | redis-cli SET mykey -x`      |
| `-raw`                        | 原始输出（无引号，无类型前缀）                    | 适用于脚本编写                               |
| `--scan`                      | Scan 模式（处理大量 key）                        | `redis-cli --scan --pattern user:*`          |
| `-c`                          | 启用集群模式（遵循 -MOVED 重定向）               | 在 Redis Cluster 上非常重要                  |
| `--pipe`                      | Redis protocol 批量模式（极速批量加载）           | `cat commands.txt | redis-cli --pipe`     |
| `--bigkeys`                   | 按类型报告最大的 key                             | 用于内存排查非常有用                         |
| `--stat`                      | 持续统计，类似 redis-cli monitor                 |                                              |
| `--latency` / `--latency-mode`| 延迟测试工具                                     | `--latency -h host`                          |
| `redis-cli --rdb /tmp/dump.rdb` | 请求服务器生成 RDB 并传输至文件                 | 远程备份技巧                                 |

**单行命令执行**

```bash
redis-cli KEYS "*"                  # 在大型实例上很危险
redis-cli -h prod-redis INFO        # 获取服务器信息
redis-cli --raw GET user:1234:json  # 输出中不含引号
redis-cli EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey value
```

**快速参考表 – 最常用的 redis-cli 标志**

| Flag          | 长版本             | 典型用法                                   |
|---------------|--------------------|--------------------------------------------|
| `-h`          | `--host`           | 主机名 / IP                                |
| `-p`          | `--port`           | 端口（默认 6379）                          |
| `-a`          | `--pass`           | 密码（旧版）                               |
| `--user`      | `--user`           | ACL 用户名 (Redis 6+)                      |
| `-n`          | `--db`             | 数据库编号                                 |
| `-c`          | `--cluster`        | 启用集群支持                               |
| `--tls`       | `--tls`            | 启用 TLS                                   |
| `-raw`        | `--raw`            | 原始输出格式                               |
| `--pipe`      | `--pipe`           | 批量协议模式                               |
| `--scan`      | `--scan`           | 比 KEYS * 更安全                           |

**References:**

- https://redis.io/docs/latest/operate/oss_and_stack/management/config
- https://redis.io/docs/latest/develop/tools/cli
- https://redis.io/docs/latest/commands
- https://stackoverflow.com/questions/55078246/docs-for-redis-server-command-line-options
