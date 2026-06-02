---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: MySQL Backup and Recovery Tutorial
translated: false
type: note
---

Question: Provide a tutorial on MySQL backup and recovery covering: (1) Data backup: full vs. incremental backup; mysqldump command (2) Transaction logs: concept, recovery principles; MySQL’s 7 types of log files and their roles; binary log operations (3) Incremental backup using binary logs: enabling/disabling binlog, performing incremental backup (4) Recovery: simple and full recovery models; restoring from mysqldump backups and binary logs.

Answer:

# MySQL Backup and Recovery Tutorial

This tutorial covers key concepts and practical steps for backing up and recovering MySQL databases, focusing on logical backups using `mysqldump`, binary logs for incremental backups, transaction logs, and recovery processes.

## 1. Data Backup: Full vs. Incremental Backup; mysqldump Command

### Full Backup

A full backup captures the entire database at a specific point in time, including all tables, data, schemas, triggers, and procedures.

- **Pros**: Complete and self-contained; easy to restore without additional files.
- **Cons**: Time-consuming and storage-intensive for large databases; repeated full backups waste resources.

### Incremental Backup

An incremental backup captures only changes made since the last full or incremental backup.

- **Pros**: Faster and uses less storage.
- **Cons**: Requires a full backup as a base; recovery involves applying multiple increments sequentially.
- In MySQL, incremental backups are achieved using **binary logs** (binlog), which record all data-modifying statements.

### Using mysqldump for Full Backups

`mysqldump` is a logical backup tool that exports data as SQL statements.

Basic command for a single database:

```
mysqldump -u username -p database_name > backup_file.sql
```

For all databases:

```
mysqldump -u username -p --all-databases > full_backup.sql
```

Recommended options for consistent backups (especially with InnoDB):

```
mysqldump -u username -p --single-transaction --quick --lock-tables=false --all-databases > full_backup.sql
```

To support point-in-time recovery, include binlog position:

```
mysqldump -u username -p --master-data=2 --single-transaction --all-databases > full_backup.sql
```

This adds a `CHANGE MASTER TO` comment with the binlog file and position.

Add `--flush-logs` to rotate binlogs after the backup (starts new incremental changes):

```
mysqldump -u username -p --flush-logs --master-data=2 --single-transaction --all-databases > full_backup.sql
```

## 2. Transaction Logs: Concept, Recovery Principles; MySQL’s Log Files and Roles; Binary Log Operations

### Transaction Logs Concept and Recovery Principles

Transaction logs record changes to ensure ACID properties (Atomicity, Consistency, Isolation, Durability).

- **InnoDB Redo Log**: Physical logs for crash recovery (replays committed changes).
- **Binary Log**: Logical logs for replication and point-in-time recovery (PITR).
- Recovery principle: During crash recovery, InnoDB uses redo/undo logs to roll forward committed transactions and roll back uncommitted ones. For PITR, restore a full backup and replay binlog events from the backup point onward.

### MySQL’s Main Log Files and Their Roles

MySQL has several log files. Commonly referenced are these 7 types:

1. **Error Log**: Records server startup/shutdown issues, errors, and warnings. Used for troubleshooting.
2. **General Query Log**: Logs all client connections and executed statements (useful for auditing, but high overhead).
3. **Slow Query Log**: Logs queries exceeding `long_query_time` (for performance tuning).
4. **Binary Log (binlog)**: Records data-changing statements/events. Essential for replication and incremental/PITR recovery.
5. **Relay Log**: On replicas, stores events from the source server's binlog for replication.
6. **Redo Log (ib_logfile*)**: InnoDB physical logs for crash recovery (redo committed changes).
7. **Undo Log**: Stored in ibdata/undo tablespaces; rolls back uncommitted transactions.

(Note: Some sources include DDL log or audit log, but these are the core 7 often mentioned in tutorials.)

### Binary Log Operations

- View status: `SHOW BINARY LOGS;`
- View events: `SHOW BINLOG EVENTS IN 'binlog_file';`
- Read binlog: `mysqlbinlog binlog_file`
- Flush (rotate): `FLUSH BINARY LOGS;`
- Purge old logs: `PURGE BINARY LOGS TO 'binlog_file';` or `PURGE BINARY LOGS BEFORE 'date';`

## 3. Incremental Backup Using Binary Logs

Incremental backups in MySQL rely on binlog (must be enabled).

### Enabling/Disabling Binlog

Edit `my.cnf` (or `my.ini` on Windows) under `[mysqld]`:

To enable:

```
server-id = 1  # Required for replication/PITR
log_bin = /path/to/mysql-bin.log  # Or just log_bin to use default
binlog_format = ROW  # Recommended: ROW, STATEMENT, or MIXED
expire_logs_days = 14  # Auto-purge old logs
```

Restart MySQL after changes.

To disable:

```
skip-log-bin
```

Or comment out `log_bin`.

### Performing Incremental Backup

1. Take a full backup (with `--flush-logs` to start fresh binlogs):

   ```
   mysqldump -u root -p --flush-logs --master-data=2 --single-transaction --all-databases > full_backup_2025-12-23.sql
   ```

2. Note the binlog file/position from the backup file.
3. Periodically back up new binlogs:
   - Flush logs: `FLUSH BINARY LOGS;`
   - Copy new binlog files (e.g., mysql-bin.000002 and later) to backup storage.
   - Or use `mysqlbinlog` to export events.

Schedule: Daily full + hourly binlog copies for good RPO (Recovery Point Objective).

## 4. Recovery: Simple and Full Recovery Models; Restoring from mysqldump and Binary Logs

### Recovery Models

MySQL does **not** have SQL Server-style "Simple" or "Full" recovery models.

- Equivalent to **Simple**: No binlog enabled → Recovery only to last full backup (truncate transaction log behavior).
- Equivalent to **Full**: Binlog enabled → Supports PITR by replaying logs (like full recovery with log backups).

### Restoring from mysqldump (Full Backup)

```
mysql -u username -p < full_backup.sql
```

Or per database:

```
mysql -u username -p database_name < backup_file.sql
```

### Point-in-Time Recovery Using Binlog

1. Restore the latest full backup:

   ```
   mysql -u root -p < full_backup.sql
   ```

2. Replay binlogs from the backup's binlog position to desired point:

   ```
   mysqlbinlog --start-position=XXXX binlog.000001 binlog.000002 ... | mysql -u root -p
   ```

   - Use `--stop-datetime` or `--start-datetime` for time-based recovery.
   - Skip problematic events if needed with `--exclude-gtids` or manual editing.

For complete PITR:

- Restore full backup up to its binlog position.
- Apply subsequent binlogs sequentially.

Always test recoveries in a non-production environment!

References:

- <https://dev.mysql.com/doc/refman/8.4/en/server-logs.html>
- <https://dev.mysql.com/doc/refman/8.4/en/binary-log.html>
- <https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html>
- <https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html>
- <https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html>
