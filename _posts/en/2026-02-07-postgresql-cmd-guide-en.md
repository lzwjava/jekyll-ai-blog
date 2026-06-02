---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: PostgreSQL Server Command Guide
translated: false
type: note
---

You're encountering the issue where the `postgres` server process doesn't know where its data directory is located. Let me explain both the direct `postgres` command and the more commonly used `pg_ctl` wrapper.

## postgres (Database Server Process)

The `postgres` command starts the actual PostgreSQL server. It requires knowing where the data directory is.

**Specifying the Data Directory (Required):**

- `-D DATADIR` - specify the data directory path
- Or set `PGDATA` environment variable

**Connection Options:**

- `-p PORT` - TCP port (default: 5432)
- `-h HOSTNAME` - hostnames/IPs to listen on (default: localhost)
- `-k DIRECTORY` - Unix socket directory
- `-i` - enable TCP/IP connections (deprecated, use `-h`)

**Configuration:**

- `-c NAME=VALUE` - set configuration parameter
- `--config-file=FILE` - use specified main config file
- `--hba-file=FILE` - use specified pg_hba.conf file
- `--ident-file=FILE` - use specified pg_ident.conf file

**Logging:**

- `-d LEVEL` - debug level (1-5)
- `-F` - turn off fsync (dangerous, for testing only)
- `-N MAX-CONNECT` - maximum concurrent connections

**Examples:**

```bash
# Start server with data directory
postgres -D /var/lib/postgresql/data

# Or using environment variable
export PGDATA=/var/lib/postgresql/data
postgres

# Start on different port
postgres -D /var/lib/postgresql/data -p 5433

# Override config parameter
postgres -D /var/lib/postgresql/data -c shared_buffers=256MB
```

## pg_ctl (Server Control Utility)

`pg_ctl` is the recommended way to start, stop, and manage PostgreSQL servers. It's a wrapper around `postgres` that provides better control.

**Basic Commands:**

- `pg_ctl start` - start server
- `pg_ctl stop` - stop server
- `pg_ctl restart` - restart server
- `pg_ctl reload` - reload configuration files
- `pg_ctl status` - show server status
- `pg_ctl promote` - promote standby to primary

**Common Options:**

- `-D DATADIR` - data directory location
- `-l FILENAME` - log file location
- `-o OPTIONS` - options to pass to postgres
- `-m MODE` - shutdown mode (smart, fast, immediate)
- `-w` - wait for operation to complete
- `-W` - don't wait for operation to complete
- `-t SECONDS` - timeout for waiting

**Shutdown Modes:**

- `smart` - wait for all clients to disconnect
- `fast` - disconnect clients, abort transactions
- `immediate` - immediate shutdown (may require recovery on restart)

**Examples:**

```bash
# Start server
pg_ctl -D /var/lib/postgresql/data start

# Start with custom options
pg_ctl -D /var/lib/postgresql/data -o "-p 5433" start

# Start with log file
pg_ctl -D /var/lib/postgresql/data -l /var/log/postgresql/server.log start

# Stop server gracefully
pg_ctl -D /var/lib/postgresql/data stop -m smart

# Fast shutdown
pg_ctl -D /var/lib/postgresql/data stop -m fast

# Restart server
pg_ctl -D /var/lib/postgresql/data restart

# Reload configuration without restart
pg_ctl -D /var/lib/postgresql/data reload

# Check status
pg_ctl -D /var/lib/postgresql/data status
```

## initdb (Initialize Data Directory)

Before you can start PostgreSQL, you need to initialize a data directory with `initdb`.

**Options:**

- `-D DATADIR` - location for data directory
- `-U USERNAME` - database superuser name
- `-W` - prompt for superuser password
- `--pwfile=FILE` - read superuser password from file
- `-E ENCODING` - default encoding (default: UTF8)
- `--locale=LOCALE` - default locale
- `--data-checksums` - enable data checksums
- `-A METHOD` - default authentication method

**Example:**

```bash
# Initialize new database cluster
initdb -D /var/lib/postgresql/data -U postgres -W

# With specific locale and encoding
initdb -D /var/lib/postgresql/data -E UTF8 --locale=en_US.UTF-8
```

## Solving Your Specific Error

When you see "postgres does not know where to find the server configuration file", you need to either:

**Option 1: Set PGDATA environment variable**

```bash
export PGDATA=/var/lib/postgresql/data
postgres
```

**Option 2: Use -D flag**

```bash
postgres -D /var/lib/postgresql/data
```

**Option 3: Use pg_ctl (recommended)**

```bash
pg_ctl -D /var/lib/postgresql/data start
```

## Common Workflow

**First-time setup:**

```bash
# 1. Initialize database cluster
initdb -D /var/lib/postgresql/data

# 2. Start server
pg_ctl -D /var/lib/postgresql/data -l logfile start

# 3. Create a database
createdb mydb

# 4. Connect
psql mydb
```

**Daily operations:**

```bash
# Start
pg_ctl -D /var/lib/postgresql/data start

# Check if running
pg_ctl -D /var/lib/postgresql/data status

# Reload config after editing postgresql.conf
pg_ctl -D /var/lib/postgresql/data reload

# Stop
pg_ctl -D /var/lib/postgresql/data stop
```

## Configuration Files

Once initialized, the data directory contains:

- `postgresql.conf` - main configuration file
- `pg_hba.conf` - client authentication configuration
- `pg_ident.conf` - user name mapping

You can edit these and reload with `pg_ctl reload` without restarting the server (for most settings).

The key takeaway is that PostgreSQL always needs to know where its data directory is, and the most user-friendly way to manage the server is through `pg_ctl` rather than calling `postgres` directly.
