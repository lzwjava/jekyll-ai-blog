---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: MySQL 备份与恢复教程
translated: true
type: note
---

问题：提供一份关于 MySQL 备份和恢复的教程，内容包括：(1) 数据备份：完全备份与增量备份；mysqldump 命令 (2) 事务日志：概念、恢复原则；MySQL 的 7 种日志文件及其作用；二进制日志操作 (3) 使用二进制日志进行增量备份：启用/禁用 binlog，执行增量备份 (4) 恢复：简单和完全恢复模型；从 mysqldump 备份和二进制日志恢复。

回答：

# MySQL 备份与恢复教程

本教程涵盖了备份和恢复 MySQL 数据库的关键概念和实际步骤，重点讲解使用 `mysqldump` 进行逻辑备份，使用二进制日志进行增量备份，以及事务日志和恢复过程。

## 1. 数据备份：完全备份与增量备份；mysqldump 命令

### 完全备份

完全备份在特定时间点捕获整个数据库，包括所有表、数据、架构、触发器和存储过程。

- **优点**：完整且自包含；无需额外文件即可轻松恢复。
- **缺点**：对于大型数据库而言耗时且占用大量存储空间；重复的完全备份会浪费资源。

### 增量备份

增量备份仅捕获自上次完全备份或增量备份以来所做的更改。

- **优点**：速度更快，占用存储空间更少。
- **缺点**：需要完全备份作为基础；恢复涉及按顺序应用多个增量。
- 在 MySQL 中，增量备份是通过**二进制日志** (binlog) 实现的，它记录了所有数据修改语句。

### 使用 mysqldump 进行完全备份

`mysqldump` 是一个逻辑备份工具，它将数据导出为 SQL 语句。

单个数据库的基本命令：

```
mysqldump -u username -p database_name > backup_file.sql
```

所有数据库：

```
mysqldump -u username -p --all-databases > full_backup.sql
```

针对一致性备份的推荐选项 (特别是对于 InnoDB)：

```
mysqldump -u username -p --single-transaction --quick --lock-tables=false --all-databases > full_backup.sql
```

为了支持时间点恢复，请包含 binlog 位置：

```
mysqldump -u username -p --master-data=2 --single-transaction --all-databases > full_backup.sql
```

这会添加一个 `CHANGE MASTER TO` 注释，其中包含 binlog 文件和位置。

添加 `--flush-logs` 以在备份后轮换 binlog（开始新的增量更改）：

```
mysqldump -u username -p --flush-logs --master-data=2 --single-transaction --all-databases > full_backup.sql
```

## 2. 事务日志：概念、恢复原则；MySQL 的日志文件及其作用；二进制日志操作

### 事务日志概念和恢复原则

事务日志记录更改以确保 ACID 属性（原子性、一致性、隔离性、持久性）。

- **InnoDB Redo Log**：用于崩溃恢复的物理日志（重放已提交的更改）。
- **Binary Log**：用于复制和时间点恢复 (PITR) 的逻辑日志。
- 恢复原则：在崩溃恢复期间，InnoDB 使用 redo/undo 日志向前滚动已提交的事务并回滚未提交的事务。对于 PITR，恢复一个完全备份，并从备份点开始重放 binlog 事件。

### MySQL 的主要日志文件及其作用

MySQL 有几个日志文件。通常引用的有以下 7 种类型：

1. **Error Log**：记录服务器启动/关闭问题、错误和警告。用于故障排除。
2. **General Query Log**：记录所有客户端连接和执行的语句（用于审计，但开销较高）。
3. **Slow Query Log**：记录超出 `long_query_time` 的查询（用于性能调优）。
4. **Binary Log (binlog)**：记录更改数据的语句/事件。对于复制和增量/PITR 恢复至关重要。
5. **Relay Log**：在副本上，存储来自源服务器 binlog 的事件，用于复制。
6. **Redo Log (ib_logfile*)**：InnoDB 物理日志，用于崩溃恢复（重做已提交的更改）。
7. **Undo Log**：存储在 ibdata/undo 表空间中；回滚未提交的事务。

（注意：一些资料还包括 DDL log 或 audit log，但这些是教程中经常提及的 7 种核心日志。）

### 二进制日志操作

- 查看状态：`SHOW BINARY LOGS;`
- 查看事件：`SHOW BINLOG EVENTS IN 'binlog_file';`
- 读取 binlog：`mysqlbinlog binlog_file`
- 刷新（轮换）：`FLUSH BINARY LOGS;`
- 清除旧日志：`PURGE BINARY LOGS TO 'binlog_file';` 或 `PURGE BINARY LOGS BEFORE 'date';`

## 3. 使用二进制日志进行增量备份

MySQL 中的增量备份依赖于 binlog（必须启用）。

### 启用/禁用 Binlog

编辑 `my.cnf`（或 Windows 上的 `my.ini`）中 `[mysqld]` 部分：

要启用：

```
server-id = 1  # 复制/PITR 所必需
log_bin = /path/to/mysql-bin.log  # 或者只用 log_bin 使用默认路径
binlog_format = ROW  # 建议：ROW, STATEMENT, 或 MIXED
expire_logs_days = 14  # 自动清除旧日志
```

更改后重启 MySQL。

要禁用：

```
skip-log-bin
```

或注释掉 `log_bin`。

### 执行增量备份

1. 进行完全备份（使用 `--flush-logs` 以启动新的 binlog）：

   ```
   mysqldump -u root -p --flush-logs --master-data=2 --single-transaction --all-databases > full_backup_2025-12-23.sql
   ```

2. 从备份文件中记下 binlog 文件/位置。
3. 定期备份新的 binlog：
   - 刷新日志：`FLUSH BINARY LOGS;`
   - 将新的 binlog 文件（例如，mysql-bin.000002 及之后的文件）复制到备份存储。
   - 或者使用 `mysqlbinlog` 导出事件。

计划：每日完全备份 + 每小时 binlog 复制以获得良好的 RPO (Recovery Point Objective)。

## 4. 恢复：简单和完全恢复模型；从 mysqldump 和二进制日志恢复

### 恢复模型

MySQL **没有** SQL Server 风格的“简单”或“完全”恢复模型。

- 等同于**简单**：未启用 binlog → 只能恢复到上次完全备份（截断事务日志行为）。
- 等同于**完全**：已启用 binlog → 支持 PITR，通过重放日志（类似于带有日志备份的完全恢复）。

### 从 mysqldump 恢复（完全备份）

```
mysql -u username -p < full_backup.sql
```

或按数据库恢复：

```
mysql -u username -p database_name < backup_file.sql
```

### 使用 Binlog 进行时间点恢复 (Point-in-Time Recovery)

1. 恢复最新的完全备份：

   ```
   mysql -u root -p < full_backup.sql
   ```

2. 从备份的 binlog 位置到所需时间点重放 binlog：

   ```
   mysqlbinlog --start-position=XXXX binlog.000001 binlog.000002 ... | mysql -u root -p
   ```

   - 使用 `--stop-datetime` 或 `--start-datetime` 进行基于时间的恢复。
   - 如果需要，使用 `--exclude-gtids` 或手动编辑跳过有问题的事件。

要进行完整的 PITR：

- 恢复完全备份到其 binlog 位置。
- 顺序应用后续的 binlog。

始终在非生产环境中测试恢复！

参考资料：

- <https://dev.mysql.com/doc/refman/8.4/en/server-logs.html>
- <https://dev.mysql.com/doc/refman/8.4/en/binary-log.html>
- <https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html>
- <https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html>
- <https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html>
