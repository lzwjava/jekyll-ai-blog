---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: MySQL 命令行核心工具
translated: true
type: note
---

**Question:** MySQL 命令行选项全面介绍

**Answer:**

### 最重要且最常用的 MySQL 命令行客户端及其主要选项

| Client              | Main purpose                              | Most important / most frequently used options                             |
|---------------------|-------------------------------------------|---------------------------------------------------------------------------|
| `mysql`             | Interactive client + execute queries      | `-u`, `-p`, `-h`, `-P`, `--database`, `-e`, `--defaults-file`, `-s`, `-B`, `--xml`, `--table`, `-v -v -v` |
| `mysqladmin`        | Administration (status, variables, flush..) | `ping`, `status`, `version`, `processlist`, `kill`, `flush-*`, `-i` (interval) |
| `mysqldump`         | Logical backup (SQL dump)                 | `--single-transaction`, `--routines`, `--triggers`, `--events`, `--databases`, `--all-databases`, `--where`, `--no-data`, `--no-create-info`, `--skip-add-drop-table`, `--skip-comments`, `--compact`, `--quick`, `--opt`, `--set-gtid-purged=OFF` |
| `mysqlpump`         | Modern logical backup (faster than mysqldump) | `--default-parallelism`, `--exclude-databases`, `--include-tables`, `--users`, `--add-drop-user` |
| `mysqlbinlog`       | Read & decode binary log files            | `--start-datetime`, `--stop-datetime`, `--start-position`, `--stop-position`, `--base64-output=DECODE-ROWS`, `-v`, `-vv`, `--verify-binlog-checksum` |
| `mysqlslap`         | Load testing / benchmark                  | `--concurrency`, `--iterations`, `--query`, `--create`, `--delimiter`, `--auto-generate-sql` |
| `mysqlimport`       | Bulk import from CSV/TSV files            | `--local`, `--fields-terminated-by`, `--columns`, `--ignore`, `--replace`, `--ignore-lines` |
| `mysqld`            | The server itself                         | `--port`, `--datadir`, `--socket`, `--innodb-buffer-pool-size`, `--log-bin`, `--server-id`, `--skip-grant-tables`, `--initialize`, `--console` |

### mysql 客户端 – 最重要的选项 (90% 的日常使用场景)

```bash
# 最常见的连接模式
mysql -u root -p
mysql -h 127.0.0.1 -u root -p
mysql -h db.example.com -P 3306 -u app_user -psecret123 mydatabase
mysql --defaults-file=~/.myprod.cnf
mysql --defaults-extra-file=extra.cnf

# 单行命令 - 非常频繁使用
mysql -u root -p -e "SELECT @@version"
mysql prod -e "SHOW PROCESSLIST\G"
mysql -B -N -e "SELECT id,name FROM users"   # tab 分隔，无表头

# 漂亮的输出格式
mysql -t               # 类似 mysql workbench 的表格 (默认交互模式)
mysql -B               # batch / tab 分隔
mysql -E               # 纵向输出 \G 风格，即使在 batch 模式下也有效
mysql -s               # silent (无列名，无表格边框)
mysql --xml            # xml 输出 (对某些脚本很有用)
mysql -H               # html 输出
```

### 快速参考 – 最实用的 mysql 客户端选项

```text
Connection / Credentials
-u, --user              用户名
-p[password], --password[=password]
-h, --host              主机名/IP
-P, --port              端口 (默认 3306)
-S, --socket            unix socket 路径
--protocol={TCP,SOCKET,PIPE,MEMORY}

Files & Profiles
--defaults-file=FILE    仅使用此文件 (忽略 ~/.my.cnf!)
--defaults-extra-file=FILE   在读取标准配置文件后读取此文件
--no-defaults           忽略所有配置文件

Output Control
-e, --execute=stmt      执行语句并退出
-B, --batch             tab 分隔，不显示 ascii 表格
-t, --table             强制表格输出 (交互模式默认)
-E, --vertical          纵向输出 (类似 \G)
-s, --silent            静默模式
-v, -vv, -vvv           更详细的日志 (verbose)
--column-names          显示列名 (默认)
--skip-column-names     (= -N) 配合 -B 非常有用
--raw                   不转义特殊字符

Others very useful
--reconnect             自动重连 (默认开启)
--disable-reconnect
--safe-updates          (= --i-am-a-dummy)   防止没有 WHERE 条件的危险 update/delete
--init-command=stmt     连接后立即执行的语句
--ssl-mode=REQUIRED     (DISABLED,REQUIRED,VERIFY_CA,VERIFY_IDENTITY)
```

### 非常实用的组合示例 (可直接复制)

```bash
# 快速检查版本
mysql -u root -p -e "SELECT @@version, @@version_comment\G"

# 快速备份单张表 (结构 + 数据)
mysqldump -u root -p --single-transaction --quick --set-gtid-purged=OFF prod orders > orders.sql

# 非常干净的 tab 分隔导出 (非常适合 Excel / pandas)
mysql prod -B -N -e "SELECT * FROM users" > users.tsv

# 以排序方式获取所有数据库的大小
mysql -u root -p -e "SELECT table_schema 'DB', ROUND(SUM(data_length+index_length)/1024/1024,1) 'Size_MB'
                     FROM information_schema.tables GROUP BY 1 ORDER BY 2 DESC"

# 每 2 秒查看一次 processlist
watch -n 2 'mysql -u root -p -e "SHOW PROCESSLIST\G" | grep -v Sleep'
```

### 快速备忘单 – 选择你的风格

```bash
# 我想要美观的表格 ........................ mysql -t
# 我想要快速且适合脚本处理 .................. mysql -B -N
# 我想要在批处理中使用 \G 风格的纵向输出 ..... mysql -E
# 我想要执行一个命令就退出 .................. mysql -e "..."
# 我想要使用文件中的连接设置 ................ mysql --defaults-file=...
```

你最常使用哪种风格或用例？
(我可以针对特定目的为你提供更多专业的示例)

**References:**

- [MySQL 8.0 Reference Manual - mysql Client Options](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)
- [MySQL 8.0 Reference Manual - mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
- [MySQL 8.0 Reference Manual - mysqladmin](https://dev.mysql.com/doc/refman/8.0/en/mysqladmin.html)
