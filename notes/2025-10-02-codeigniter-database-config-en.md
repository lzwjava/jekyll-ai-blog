---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Database Configuration Overview
translated: false
type: note
---

### Overview of CodeIgniter Database Configuration

This PHP file is a configuration script for CodeIgniter's database connectivity. It defines connection settings for various database groups (e.g., 'default', 'lzwjava', 'leo66', 'testing'), allowing the application to switch between them based on the environment (development, testing, production). The `$active_group` variable determines which connection group is used by default.

Key components:

- **$query_builder**: Set to `TRUE` to enable loading the Query Builder class, which provides an object-oriented way to build SQL queries.
- **$db[][]**: An associative array where each sub-array (e.g., 'default') holds detailed configuration options for a database connection.

The `$active_group` is dynamically set based on the `ENVIRONMENT` constant (e.g., via a switch statement), ensuring different settings for different deployment stages. Below, I'll explain each configuration option in detail, drawing from CodeIgniter's documentation and standard usage. Note that actual sensitive values (like credentials) are omitted here for security; in practice, these should be stored securely, e.g., via environment variables.

### Detailed Configuration Options

Each database group is an array with the following keys. Most are straightforward settings, but some (like `encrypt`) support sub-options for advanced features.

- **dsn** (string): The full Data Source Name (DSN) string describing the connection. This is an alternative to specifying hostname, username, etc., separately. It's useful for complex setups like ODBC. If provided, it overrides individual host/credential fields. Example format: `'dsn' => 'mysql:host=yourhost;dbname=yourdatabase'`.

- **hostname** (string): The database server's address (e.g., 'localhost' or an IP like '127.0.0.1'). This identifies where the database is running, allowing connections over TCP/IP or sockets.

- **username** (string): The account name used to authenticate with the database server. This should match a valid user in the database management system.

- **password** (string): The secret key paired with the username for authentication. Always store this securely to prevent exposure.

- **database** (string): The specific database name you want to connect to on the server. All queries will target this database unless otherwise specified.

- **dbdriver** (string): Specifies the database driver to use (e.g., 'mysqli' for MySQL). Common drivers include 'cubrid', 'ibase', 'mssql', 'mysql', 'mysqli', 'oci8', 'odbc', 'pdo', 'postgre', 'sqlite', 'sqlite3', and 'sqlsrv'. 'mysqli' is a modern, secure choice for MySQL.

- **dbprefix** (string): An optional prefix added to table names when using CodeIgniter's Query Builder (e.g., if set to 'prefix_', 'mytable' becomes 'prefix_mytable'). This helps namespace tables in shared hosting or multi-tenant apps.

- **pconnect** (boolean): Enables persistent connections (`TRUE`) or regular connections (`FALSE`). Persistent connections reuse the same link, improving performance for high-load apps, but they can exhaust server resources if overused.

- **db_debug** (boolean): Controls whether database errors are displayed (`TRUE`) for debugging. Disable (`FALSE`) in production to avoid leaking sensitive error details to users.

- **cache_on** (boolean): Enables (`TRUE`) or disables (`FALSE`) query caching. When enabled, results are stored to speed up repeated queries.

- **cachedir** (string): File path to the directory where cached query results are stored. Must be writable by the web server. Combined with `cache_on`, this reduces database load.

- **char_set** (string): The character encoding for database communication (e.g., 'utf8mb4' for modern Unicode support). Ensures data integrity for multi-language apps.

- **dbcollat** (string): The collation for sorting and comparing characters (e.g., 'utf8mb4_unicode_ci' for case-insensitive Unicode). This works as a fallback for older PHP/MySQL; ignored otherwise.

- **swap_pre** (string): A table prefix to replace `dbprefix` dynamically. Useful for swapping prefixes in existing apps without renaming tables.

- **encrypt** (boolean or array): For encryption support. For 'mysql' (deprecated), 'sqlsrv', and 'pdo/sqlsrv', use `TRUE`/`FALSE` to enable/disable SSL. For 'mysqli' and 'pdo/mysql', use an array with SSL sub-options:
  - 'ssl_key': Path to the private key file (e.g., for client certificates).
  - 'ssl_cert': Path to the public key certificate file.
  - 'ssl_ca': Path to the certificate authority file (validates server cert).
  - 'ssl_capath': Path to a directory of trusted CA certificates in PEM format.
  - 'ssl_cipher': Colon-separated list of allowed ciphers (e.g., 'AES128-SHA').
  - 'ssl_verify': For 'mysqli' only; `TRUE` to verify server certificates, `FALSE` to skip (less secure; use for self-signed certs).

- **compress** (boolean): Enables client-side compression for MySQL connections, reducing network traffic (MySQL only; ignored by other drivers).

- **stricton** (boolean): Forces 'Strict Mode' connections (`TRUE`), which enforces strict SQL rules to catch errors early (e.g., invalid data types). Useful during development.

- **ssl_options** (array): Advanced SSL configuration options for drivers like 'pdo'. Allows fine-tuning encryption parameters not covered by `encrypt`.

- **failover** (array): Backup connection array(s) for automatic switching if the primary connection fails. Each element mirrors the main config (e.g., alternative hostname/port). Example: `array(array('hostname' => 'backuphost', ...))`.

- **save_queries** (boolean): Saves executed queries in memory for debugging (`TRUE`). Provides access to methods like `$this->db->last_query()` but can increase memory use; disable (`FALSE`) in prod to save resources.

### Database Groups and Environment Switching

- **default**: The base configuration array, serving as a template. It's set to 'production' defaults (e.g., no debugging, secured settings).
- **lzwjava**: Inherits from the base but overrides username to a different value (password left blank, implying no auth or default).
- **leo66**: Inherits base settings but changes hostname to local loopback, username/password to defaults, and adds a port (3306, standard for MySQL).
- **testing**: A dedicated group for test environments; inherits base config.

The `switch` statement activates the appropriate group based on `ENVIRONMENT`:

- Development: Uses 'lzwjava'.
- Testing: Uses 'testing'.
- Production: Uses 'default'.

This setup promotes flexibility for local dev, testing, and live deployments. Always sanitize inputs to prevent SQL injection, and consider moving credentials to environment variables for security. For full docs, refer to CodeIgniter's official User Guide on database connections. If you have a specific option or group to clarify, let me know!
