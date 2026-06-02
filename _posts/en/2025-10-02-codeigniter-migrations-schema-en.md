---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Migrations Database Schema Management
translated: false
type: note
---

### What Are CodeIgniter Migrations?

CodeIgniter (CI) migrations are a feature that helps manage database schema changes in a version-controlled way, similar to tools like Flyway or Liquibase. They allow you to write PHP scripts that define database alterations (e.g., creating tables, adding columns, or modifying data), then run them in sequence to keep your schema up-to-date across environments. This prevents manual SQL errors and supports rollback.

Migrations work by:

- Storing migration files in a directory (default: `application/migrations/`).
- Tracking "versions" in a database table to know which migrations have been applied.
- Running scripts forward (up) or backward (down) based on your needs.

The config file you shared (`migration.php`) controls how migrations behave. It uses PHP arrays to set options. Below, I'll explain the key settings with examples.

### Key Configuration Settings

| Setting | Value in Your Code | Explanation | How It Works |
|---------|---------------------|-------------|-------------|
| `migration_enabled` | `FALSE` | Enables or disables migrations globally. When `FALSE`, you can't run migrations (for security, as they modify the DB). | CI checks this before executing any migration command. Set to `TRUE` during development, then back to `FALSE` in production. Example: If enabled, run via `$this->migration->current()` in a controller. |
| `migration_type` | `'timestamp'` | File naming style: `'sequential'` (e.g., `001_add_blog.php`) or `'timestamp'` (e.g., `20121031104401_add_blog.php`). Timestamp is recommended for better version control. | Files are loaded in chronological order. Timestamp uses `YYYYMMDDHHIISS` format (e.g., `20121031104401` for Oct 31, 2012, 10:44:01). |
| `migration_table` | `'migrations'` | Name of the DB table that tracks applied migrations. Required. | CI creates this table if it doesn't exist. It stores the latest migration version. Deletes or updates this table reset migration history. |
| `migration_auto_latest` | `FALSE` | If `TRUE` and `migration_enabled` is `TRUE`, auto-runs migrations to the latest version when the Migration library loads (e.g., on page load). | Useful for dev environments to auto-sync schemas. Set `FALSE` to run migrations manually for control (safer in prod). |
| `migration_version` | `0` | The target version/number to migrate to. Set to the filename prefix (e.g., `20121031104401`). `0` means no migrations applied. | Running `$this->migration->version(20121031104401)` migrates up to that point. Used for targeted rollbacks—negative numbers downgrade. |
| `migration_path` | `APPPATH.'migrations/'` | Directory where migration files are stored. `APPPATH` is a CI constant pointing to `application/`. | CI scans this folder for PHP files matching the naming convention. Must be writable by the web server. Custom paths like `BASEPATH.'custom/migrations/'` are possible. |

### How to Use Migrations (Step-by-Step)

1. **Enable Migrations**: Temporarily set `$config['migration_enabled'] = TRUE;` in the config file.

2. **Create a Migration File**: Add a PHP file in `application/migrations/` with a name like `20121031104401_add_blog.php`. Inside, use CI's Migration class:

   ```php
   defined('BASEPATH') OR exit('No direct script access allowed');

   class Migration_Add_blog extends CI_Migration {
       public function up() {
           $this->dbforge->add_field('id');
           $this->dbforge->create_table('blogs');
       }

       public function down() {
           $this->dbforge->drop_table('blogs');
       }
   }
   ```

   - `up()` applies changes (e.g., create table).
   - `down()` reverses them (e.g., drop table).

3. **Run Migrations**:
   - Load the library: `$this->load->library('migration');`
   - To latest: `$this->migration->current();`
   - To specific: `$this->migration->version('20121031104401');`
   - From command line (if CLI enabled): `php index.php migrate current`

4. **Common Commands**:
   - `$this->migration->latest()`: Alias for `current()`.
   - `$this->migration->find_migratables()`: Lists available files.
   Errors log to CI's log files or throw exceptions.

5. **Best Practices**:
   - Keep migrations idempotent (safe to re-run).
   - Test in dev first; avoid enabling auto-migrate in production to prevent accidental schema changes.
   - Use transactions if your DB supports them for atomic changes.
   - Disable after use: Set back to `FALSE` for security.

If you run into issues (e.g., permissions on the path), check CI's logs or documentation at [codeigniter.com/user_guide/libraries/migration.html](https://codeigniter.com/user_guide/libraries/migration.html). Specify your CI version for more tailored advice!
