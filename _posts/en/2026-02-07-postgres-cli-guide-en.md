---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: PostgreSQL CLI Essentials Guide
translated: false
type: note
---

PostgreSQL offers several command-line utilities, each with extensive options. Here's a comprehensive guide to the most important ones.

## psql (Interactive Terminal)

The `psql` command is your primary interface for interacting with PostgreSQL databases.

**Connection Options:**
- `-h HOST` or `--host=HOST` - database server host (default: local socket)
- `-p PORT` or `--port=PORT` - server port (default: 5432)
- `-U NAME` or `--username=NAME` - database user name
- `-d DBNAME` or `--dbname=DBNAME` - database to connect to
- `-W` or `--password` - force password prompt

**Output Options:**
- `-c COMMAND` - run a single SQL command and exit
- `-f FILE` - execute commands from a file
- `-o FILE` - send query results to file
- `-t` - print rows only (no headers/footers)
- `-A` - unaligned table output mode
- `-H` - HTML output format
- `-x` - turn on expanded table output
- `-q` - quiet mode (suppress welcome message)

**Behavior Options:**
- `-v NAME=VALUE` - set psql variable
- `-1` - execute as a single transaction
- `-L FILENAME` - log session to file
- `--no-psqlrc` - don't read startup file (~/.psqlrc)

**Example:**
```bash
psql -h localhost -U postgres -d mydb -c "SELECT * FROM users LIMIT 5"
```

## pg_dump (Backup Utility)

Creates backup copies of databases.

**General Options:**
- `-h HOST` - database server host
- `-p PORT` - database server port
- `-U NAME` - connect as specified user
- `-d DBNAME` - database to dump
- `-f FILE` - output file name

**Output Format:**
- `-F FORMAT` - output format (p=plain SQL, c=custom, d=directory, t=tar)
- `-a` - dump only data, not schema
- `-s` - dump only schema, not data
- `-c` - include DROP commands before CREATE
- `-C` - include CREATE DATABASE command

**Selective Dumping:**
- `-t TABLE` - dump only specified table(s)
- `-T TABLE` - exclude specified table(s)
- `-n SCHEMA` - dump only specified schema(s)
- `-N SCHEMA` - exclude specified schema(s)
- `--data-only` - dump only data
- `--schema-only` - dump only schema

**Compression:**
- `-Z 0-9` - compression level for custom format

**Example:**
```bash
pg_dump -h localhost -U postgres -d mydb -F c -f mydb_backup.dump
```

## pg_restore (Restore Utility)

Restores databases from backups created by pg_dump.

**Connection Options:**
- `-h HOST`, `-p PORT`, `-U NAME`, `-d DBNAME` - same as other tools

**Restore Options:**
- `-a` - restore only data
- `-s` - restore only schema
- `-c` - clean (drop) database objects before recreating
- `-C` - create the database before restoring
- `-1` - restore as single transaction
- `--if-exists` - use IF EXISTS when dropping objects

**Selective Restore:**
- `-t TABLE` - restore only specified table(s)
- `-n SCHEMA` - restore only specified schema(s)
- `-I INDEX` - restore only specified index
- `-P FUNCTION` - restore only specified function

**Example:**
```bash
pg_restore -h localhost -U postgres -d mydb -c mydb_backup.dump
```

## createdb / dropdb

Quick database creation and deletion utilities.

**createdb Options:**
- `-O OWNER` - database owner
- `-T TEMPLATE` - template database to copy
- `-E ENCODING` - encoding (default: UTF8)
- `-l LOCALE` - locale settings

**Example:**
```bash
createdb -h localhost -U postgres -O myuser mynewdb
dropdb -h localhost -U postgres olddb
```

## createuser / dropuser

User management utilities.

**createuser Options:**
- `-s` - user will be superuser
- `-d` - user can create databases
- `-r` - user can create roles
- `-P` - prompt for password
- `--interactive` - prompt for missing options

**Example:**
```bash
createuser -h localhost -U postgres -d -P newuser
```

## pg_isready

Checks connection status to PostgreSQL server.

**Options:**
- `-h HOST`, `-p PORT`, `-U NAME` - connection parameters
- `-t SECONDS` - timeout (default: 3)
- `-q` - quiet mode

**Example:**
```bash
pg_isready -h localhost -p 5432
```

## Common Patterns

**Connecting to remote database:**
```bash
psql -h db.example.com -p 5432 -U admin -d production
```

**Creating a compressed backup:**
```bash
pg_dump -h localhost -U postgres -d mydb -F c -Z 9 -f backup.dump
```

**Dumping just one table:**
```bash
pg_dump -h localhost -U postgres -d mydb -t users -f users.sql
```

**Restoring to a different database name:**
```bash
createdb newdb
pg_restore -h localhost -U postgres -d newdb backup.dump
```

**Running SQL from a file:**
```bash
psql -h localhost -U postgres -d mydb -f schema.sql
```

**Setting environment variables to avoid repetition:**
```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGDATABASE=mydb

psql  # now connects automatically
```

Most PostgreSQL utilities also respect `PGPASSWORD` environment variable, though using a `.pgpass` file is more secure for production use.
