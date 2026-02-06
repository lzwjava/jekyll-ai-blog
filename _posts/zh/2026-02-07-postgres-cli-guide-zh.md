---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: PostgreSQL CLI 基础指南
translated: true
type: note
---

PostgreSQL 提供了多种 command-line utilities，每种都有丰富的选项。以下是关于最重要工具的全面指南。

## psql (Interactive Terminal)

`psql` 命令是与 PostgreSQL 数据库交互的主要 interface。

**Connection Options:**

- `-h HOST` 或 `--host=HOST` - 数据库服务器 host（默认：local socket）
- `-p PORT` 或 `--port=PORT` - 服务器 port（默认：5432）
- `-U NAME` 或 `--username=NAME` - 数据库用户名
- `-d DBNAME` 或 `--dbname=DBNAME` - 要连接的数据库
- `-W` 或 `--password` - 强制密码提示

**Output Options:**

- `-c COMMAND` - 运行单个 SQL 命令并退出
- `-f FILE` - 从文件执行命令
- `-o FILE` - 将查询结果发送到文件
- `-t` - 仅打印行（无 headers/footers）
- `-A` - unaligned table 输出模式
- `-H` - HTML 输出格式
- `-x` - 开启 expanded table 输出
- `-q` - quiet 模式（抑制欢迎消息）

**Behavior Options:**

- `-v NAME=VALUE` - 设置 psql 变量
- `-1` - 作为单个 transaction 执行
- `-L FILENAME` - 将 session 记录到文件
- `--no-psqlrc` - 不读取启动文件 (~/.psqlrc)

**Example:**

```bash
psql -h localhost -U postgres -d mydb -c "SELECT * FROM users LIMIT 5"
```

## pg_dump (Backup Utility)

创建数据库的 backup 副本。

**General Options:**

- `-h HOST` - 数据库服务器 host
- `-p PORT` - 数据库服务器 port
- `-U NAME` - 以指定用户连接
- `-d DBNAME` - 要 dump 的数据库
- `-f FILE` - 输出文件名

**Output Format:**

- `-F FORMAT` - 输出格式 (p=plain SQL, c=custom, d=directory, t=tar)
- `-a` - 仅 dump 数据，不包含 schema
- `-s` - 仅 dump schema，不包含数据
- `-c` - 在 CREATE 之前包含 DROP 命令
- `-C` - 包含 CREATE DATABASE 命令

**Selective Dumping:**

- `-t TABLE` - 仅 dump 指定的 table(s)
- `-T TABLE` - 排除指定的 table(s)
- `-n SCHEMA` - 仅 dump 指定的 schema(s)
- `-N SCHEMA` - 排除指定的 schema(s)
- `--data-only` - 仅 dump 数据
- `--schema-only` - 仅 dump schema

**Compression:**

- `-Z 0-9` - custom 格式的 compression 级别

**Example:**

```bash
pg_dump -h localhost -U postgres -d mydb -F c -f mydb_backup.dump
```

## pg_restore (Restore Utility)

从 pg_dump 创建的 backups 中还原数据库。

**Connection Options:**

- `-h HOST`, `-p PORT`, `-U NAME`, `-d DBNAME` - 与其他工具相同

**Restore Options:**

- `-a` - 仅 restore 数据
- `-s` - 仅 restore schema
- `-c` - 在重新创建之前 clean (drop) 数据库对象
- `-C` - 在 restore 之前创建数据库
- `-1` - 作为单个 transaction restore
- `--if-exists` - 在 drop 对象时使用 IF EXISTS

**Selective Restore:**

- `-t TABLE` - 仅 restore 指定的 table(s)
- `-n SCHEMA` - 仅 restore 指定的 schema(s)
- `-I INDEX` - 仅 restore 指定的 index
- `-P FUNCTION` - 仅 restore 指定的 function

**Example:**

```bash
pg_restore -h localhost -U postgres -d mydb -c mydb_backup.dump
```

## createdb / dropdb

快速创建和删除数据库的 utilities。

**createdb Options:**

- `-O OWNER` - 数据库所有者
- `-T TEMPLATE` - 要复制的 template 数据库
- `-E ENCODING` - encoding（默认：UTF8）
- `-l LOCALE` - locale 设置

**Example:**

```bash
createdb -h localhost -U postgres -O myuser mynewdb
dropdb -h localhost -U postgres olddb
```

## createuser / dropuser

用户管理 utilities。

**createuser Options:**

- `-s` - 用户将成为 superuser
- `-d` - 用户可以创建数据库
- `-r` - 用户可以创建 roles
- `-P` - 提示输入密码
- `--interactive` - 提示输入缺失的选项

**Example:**

```bash
createuser -h localhost -U postgres -d -P newuser
```

## pg_isready

检查与 PostgreSQL 服务器的连接状态。

**Options:**

- `-h HOST`, `-p PORT`, `-U NAME` - 连接参数
- `-t SECONDS` - timeout（默认：3）
- `-q` - quiet 模式

**Example:**

```bash
pg_isready -h localhost -p 5432
```

## Common Patterns

**连接到远程数据库：**

```bash
psql -h db.example.com -p 5432 -U admin -d production
```

**创建一个压缩的 backup：**

```bash
pg_dump -h localhost -U postgres -d mydb -F c -Z 9 -f backup.dump
```

**仅 dump 一张表：**

```bash
pg_dump -h localhost -U postgres -d mydb -t users -f users.sql
```

**还原到不同的数据库名称：**

```bash
createdb newdb
pg_restore -h localhost -U postgres -d newdb backup.dump
```

**从文件运行 SQL：**

```bash
psql -h localhost -U postgres -d mydb -f schema.sql
```

**设置环境变量以避免重复：**

```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGDATABASE=mydb

psql  # 现在会自动连接
```

大多数 PostgreSQL utilities 也会遵循 `PGPASSWORD` 环境变量，尽管在生产环境中使用 `.pgpass` 文件更加安全。