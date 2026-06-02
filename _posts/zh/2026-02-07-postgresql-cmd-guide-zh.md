---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: PostgreSQL 服务器命令指南
translated: true
type: note
---

你遇到了 `postgres` 服务器进程不知道其数据目录（data directory）位置的问题。让我为你解释一下直接使用 `postgres` 命令以及更常用的 `pg_ctl` 封装工具。

## postgres (Database Server Process)

`postgres` 命令用于启动实际的 PostgreSQL 服务器。它需要知道数据目录的位置。

**指定数据目录（必填）：**
- `-D DATADIR` - 指定数据目录路径
- 或者设置 `PGDATA` 环境变量

**连接选项：**
- `-p PORT` - TCP port（默认：5432）
- `-h HOSTNAME` - 监听的 hostnames/IPs（默认：localhost）
- `-k DIRECTORY` - Unix socket 目录
- `-i` - 启用 TCP/IP 连接（已弃用，请使用 `-h`）

**配置：**
- `-c NAME=VALUE` - 设置配置参数
- `--config-file=FILE` - 使用指定的配置文件
- `--hba-file=FILE` - 使用指定的 pg_hba.conf 文件
- `--ident-file=FILE` - 使用指定的 pg_ident.conf 文件

**日志：**
- `-d LEVEL` - debug 级别 (1-5)
- `-F` - 关闭 fsync（危险，仅用于测试）
- `-N MAX-CONNECT` - 最大并发连接数

**示例：**
```bash
# 使用数据目录启动服务器
postgres -D /var/lib/postgresql/data

# 或使用环境变量
export PGDATA=/var/lib/postgresql/data
postgres

# 在不同端口启动
postgres -D /var/lib/postgresql/data -p 5433

# 覆盖配置参数
postgres -D /var/lib/postgresql/data -c shared_buffers=256MB
```

## pg_ctl (Server Control Utility)

`pg_ctl` 是推荐的启动、停止和管理 PostgreSQL 服务器的方式。它是 `postgres` 的一个封装工具，提供了更好的控制能力。

**基本命令：**
- `pg_ctl start` - 启动服务器
- `pg_ctl stop` - 停止服务器
- `pg_ctl restart` - 重启服务器
- `pg_ctl reload` - 重新加载配置文件
- `pg_ctl status` - 显示服务器状态
- `pg_ctl promote` - 将 standby 提升为主节点

**常用选项：**
- `-D DATADIR` - 数据目录位置
- `-l FILENAME` - 日志文件位置
- `-o OPTIONS` - 传递给 postgres 的选项
- `-m MODE` - 停机模式 (smart, fast, immediate)
- `-w` - 等待操作完成
- `-W` - 不等待操作完成
- `-t SECONDS` - 等待的超时时间（秒）

**停机模式：**
- `smart` - 等待所有客户端断开连接
- `fast` - 断开客户端连接，中止事务
- `immediate` - 立即停机（重启时可能需要 recovery）

**示例：**

```bash
# 启动服务器
pg_ctl -D /var/lib/postgresql/data start

# 使用自定义选项启动
pg_ctl -D /var/lib/postgresql/data -o "-p 5433" start

# 指定日志文件启动
pg_ctl -D /var/lib/postgresql/data -l /var/log/postgresql/server.log start

# 优雅地停止服务器
pg_ctl -D /var/lib/postgresql/data stop -m smart

# 快速停机
pg_ctl -D /var/lib/postgresql/data stop -m fast

# 重启服务器
pg_ctl -D /var/lib/postgresql/data restart

# 不重启加载配置
pg_ctl -D /var/lib/postgresql/data reload

# 检查状态
pg_ctl -D /var/lib/postgresql/data status
```

## initdb (Initialize Data Directory)

在启动 PostgreSQL 之前，你需要使用 `initdb` 初始化一个数据目录。

**选项：**
- `-D DATADIR` - 数据目录位置
- `-U USERNAME` - 数据库超级用户名称
- `-W` - 提示输入超级用户密码
- `--pwfile=FILE` - 从文件读取超级用户密码
- `-E ENCODING` - 默认编码（默认：UTF8）
- `--locale=LOCALE` - 默认 locale
- `--data-checksums` - 启用数据校验（data checksums）
- `-A METHOD` - 默认身份验证方法

**示例：**
```bash
# 初始化新的数据库集群
initdb -D /var/lib/postgresql/data -U postgres -W

# 使用特定的 locale 和编码
initdb -D /var/lib/postgresql/data -E UTF8 --locale=en_US.UTF-8
```

## 解决你的具体错误

当你看到 "postgres does not know where to find the server configuration file" 时，你需要采取以下行动之一：

**方案 1：设置 PGDATA 环境变量**
```bash
export PGDATA=/var/lib/postgresql/data
postgres
```

**方案 2：使用 -D 标志**
```bash
postgres -D /var/lib/postgresql/data
```

**方案 3：使用 pg_ctl（推荐）**
```bash
pg_ctl -D /var/lib/postgresql/data start
```

## 常见工作流程

**首次设置：**
```bash
# 1. 初始化数据库集群
initdb -D /var/lib/postgresql/data

# 2. 启动服务器
pg_ctl -D /var/lib/postgresql/data -l logfile start

# 3. 创建数据库
createdb mydb

# 4. 连接
psql mydb
```

**日常操作：**
```bash
# 启动
pg_ctl -D /var/lib/postgresql/data start

# 检查是否运行中
pg_ctl -D /var/lib/postgresql/data status

# 编辑 postgresql.conf 后重载配置
pg_ctl -D /var/lib/postgresql/data reload

# 停止
pg_ctl -D /var/lib/postgresql/data stop
```

## 配置文件

初始化后，数据目录包含：
- `postgresql.conf` - 主配置文件
- `pg_hba.conf` - 客户端身份验证配置
- `pg_ident.conf` - 用户名映射

你可以编辑这些文件并使用 `pg_ctl reload` 重新加载，而无需重启服务器（对于大多数设置生效）。

核心要点是：PostgreSQL 始终需要知道其数据目录的位置，而管理服务器最用户友好的方式是通过 `pg_ctl` 而不是直接调用 `postgres`。
