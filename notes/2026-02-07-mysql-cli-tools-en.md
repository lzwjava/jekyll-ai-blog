---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Essential MySQL Command Line Tools
translated: false
type: note
---

**Question:** Comprehensive introduction to MySQL command line options

**Answer:**

### Most Important & Most Frequently Used MySQL Command Line Clients & Their Main Options

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

### mysql Client – The Most Important Options (90% of daily usage)

```bash
# Most common connection patterns
mysql -u root -p
mysql -h 127.0.0.1 -u root -p
mysql -h db.example.com -P 3306 -u app_user -psecret123 mydatabase
mysql --defaults-file=~/.myprod.cnf
mysql --defaults-extra-file=extra.cnf

# One-liners - very frequently used
mysql -u root -p -e "SELECT @@version"
mysql prod -e "SHOW PROCESSLIST\G"
mysql -B -N -e "SELECT id,name FROM users"   # tab separated, no headers

# Pretty output formats
mysql -t               # table like mysql workbench (default interactive)
mysql -B               # batch / tab separated
mysql -E               # vertical \G style even in batch mode
mysql -s               # silent (no column names, no table borders)
mysql --xml            # xml output (useful for some scripts)
mysql -H               # html output (yes, still exists...)
```

### Quick Reference – Most Useful mysql Client Options

```text
Connection / Credentials
-u, --user              username
-p[password], --password[=password]
-h, --host              hostname/ip
-P, --port              port (default 3306)
-S, --socket            unix socket path
--protocol={TCP,SOCKET,PIPE,MEMORY}

Files & Profiles
--defaults-file=FILE    only this file (~/.my.cnf is ignored!)
--defaults-extra-file=FILE   read this file after normal files
--no-defaults           ignore all config files

Output Control
-e, --execute=stmt      execute statement and exit
-B, --batch             tab separated, no ascii table
-t, --table             force table output (default in interactive)
-E, --vertical          vertical output (like \G)
-s, --silent            be more silent
-v, -vv, -vvv           more verbose
--column-names          show column names on top (default)
--skip-column-names     (= -N) very useful with -B
--raw                   don't escape special characters

Others very useful
--reconnect             auto reconnect (default on)
--disable-reconnect
--safe-updates          (= --i-am-a-dummy)   prevents dangerous updates/deletes without WHERE
--init-command=stmt     execute this after connect
--ssl-mode=REQUIRED     (DISABLED,REQUIRED,VERIFY_CA,VERIFY_IDENTITY)
```

### Very Useful Combination Examples (copy-paste friendly)

```bash
# Quick version check
mysql -u root -p -e "SELECT @@version, @@version_comment\G"

# Fast dump of one table (structure + data)
mysqldump -u root -p --single-transaction --quick --set-gtid-purged=OFF prod orders > orders.sql

# Very clean tab separated export (great for Excel / pandas)
mysql prod -B -N -e "SELECT * FROM users" > users.tsv

# Get all database sizes nicely sorted
mysql -u root -p -e "SELECT table_schema 'DB', ROUND(SUM(data_length+index_length)/1024/1024,1) 'Size_MB' 
                     FROM information_schema.tables GROUP BY 1 ORDER BY 2 DESC"

# Watch processlist every 2 seconds
watch -n 2 'mysql -u root -p -e "SHOW PROCESSLIST\G" | grep -v Sleep'
```

### Quick cheatsheet – pick your style

```bash
# I want beautiful table ........................ mysql -t
# I want fast & script friendly .................. mysql -B -N
# I want vertical like \G in batch ............... mysql -E
# I want one command and bye ..................... mysql -e "..."
# I want to use connection settings from file .... mysql --defaults-file=...
```

Which style / use-case do you use the most?  
(I can give you many more specialized examples for that exact purpose)

**References:**

- [MySQL 8.0 Reference Manual - mysql Client Options](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)
- [MySQL 8.0 Reference Manual - mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
- [MySQL 8.0 Reference Manual - mysqladmin](https://dev.mysql.com/doc/refman/8.0/en/mysqladmin.html)