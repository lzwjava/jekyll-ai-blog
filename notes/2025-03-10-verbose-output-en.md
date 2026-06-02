---
audio: false
generated: true
lang: en
layout: post
title: Verbose Output Examples
translated: false
type: note
---

Here are additional examples of enabling verbose output across various tools and systems, expanding on the theme of providing more detailed feedback or logging:

- **PowerShell**: To enable verbose output, use the `-Verbose` switch with cmdlets that support it. For example:
  ```powershell
  Get-Process -Verbose
  ```
  Alternatively, set the `$VerbosePreference` variable globally:
  ```powershell
  $VerbosePreference = "Continue"
  ```

- **CMake**: To get verbose output during the build process, use the `--verbose` flag or set `VERBOSE=1`:
  ```bash
  cmake --build . --verbose
  ```
  Or:
  ```bash
  make VERBOSE=1
  ```

- **Make**: To enable verbose output and see all commands executed, use the `-d` flag for debugging or avoid silencing output with `@`:
  ```bash
  make -d
  ```
  Or edit the Makefile to remove `@` prefixes from commands.

- **GCC (GNU Compiler Collection)**: For verbose compilation output, use the `-v` flag:
  ```bash
  gcc -v -o output source.c
  ```

- **GDB (GNU Debugger)**: To increase verbosity, use the `set verbose on` command within GDB:
  ```gdb
  (gdb) set verbose on
  (gdb) run
  ```

- **Ruby**: Run Ruby scripts with verbose mode using the `-v` or `--verbose` flag:
  ```bash
  ruby -v script.rb
  ```
  For additional warnings, use `-w`:
  ```bash
  ruby -w script.rb
  ```

- **Perl**: Enable verbose output with the `-v` flag or use the `diagnostics` pragma for detailed error messages:
  ```bash
  perl -v script.pl
  ```
  Or in the script:
  ```perl
  use diagnostics;
  ```

- **PHP**: Run PHP scripts with verbose error reporting by setting `error_reporting` and `display_errors` in `php.ini`:
  ```ini
  error_reporting = E_ALL
  display_errors = On
  ```
  Or from the command line:
  ```bash
  php -d error_reporting=E_ALL script.php
  ```

- **R**: To enable verbose output in R scripts, use the `verbose=TRUE` argument in functions that support it (e.g., `install.packages`):
  ```R
  install.packages("dplyr", verbose=TRUE)
  ```

- **Go (Golang)**: For verbose output during compilation or testing, use the `-v` flag:
  ```bash
  go build -v
  go test -v
  ```

- **Rust (Cargo)**: Enable verbose output with Cargo using the `-v` or `-vv` flags:
  ```bash
  cargo build -v
  cargo run -vv
  ```

- **Jenkins**: To enable verbose logging for a pipeline, add the `verbose` option in the script or configure the console output in the job settings. For example, in a Jenkinsfile:
  ```groovy
  sh 'some_command --verbose'
  ```
  Alternatively, set the system property `-Dhudson.model.TaskListener.verbose=true` when starting Jenkins.

- **Vagrant**: Get verbose output with the `--debug` flag:
  ```bash
  vagrant up --debug
  ```

- **Puppet**: Run Puppet with increased verbosity using the `--verbose` or `--debug` flags:
  ```bash
  puppet apply site.pp --verbose
  puppet apply site.pp --debug
  ```

- **Chef**: Enable verbose output with the `-l` (log level) flag:
  ```bash
  chef-client -l debug
  ```

- **SaltStack**: Increase verbosity with the `-l` flag (e.g., `debug` or `trace`):
  ```bash
  salt '*' test.ping -l debug
  ```

- **PostgreSQL (psql)**: To get verbose output from `psql`, use the `-e` flag to echo queries or `\set VERBOSITY verbose` for detailed error messages:
  ```bash
  psql -e -f script.sql
  ```
  Or in `psql`:
  ```sql
  \set VERBOSITY verbose
  ```

- **MySQL**: Run the MySQL client with verbose output using `--verbose`:
  ```bash
  mysql --verbose < script.sql
  ```

- **SQLite**: Use the `.explain` command for verbose query execution plans:
  ```sqlite
  sqlite3 database.db
  sqlite> .explain
  sqlite> SELECT * FROM table;
  ```

- **MongoDB**: Enable verbose logging by starting `mongod` with the `-v` flag (up to `-vvvvv` for more detail):
  ```bash
  mongod -v
  ```

- **Elasticsearch**: Start Elasticsearch with verbose logging by adjusting the `log4j2.properties` file:
  ```properties
  logger.action.level = debug
  ```
  Or pass `--verbose` when starting:
  ```bash
  elasticsearch --verbose
  ```

- **NGINX**: Test configuration with verbose output using `-T`:
  ```bash
  nginx -T
  ```
  For runtime verbosity, increase the `error_log` level in `nginx.conf`:
  ```nginx
  error_log /var/log/nginx/error.log debug;
  ```

- **Apache HTTP Server**: Enable verbose logging by setting the `LogLevel` directive in `httpd.conf` or `apache2.conf`:
  ```apache
  LogLevel debug
  ```

- **OpenSSL**: Get verbose output with commands like `s_client`:
  ```bash
  openssl s_client -connect example.com:443 -debug
  ```

- **JUnit (Java Testing)**: Run JUnit tests with verbose output by configuring the test runner (e.g., Maven Surefire plugin):
  ```xml
  <configuration>
      <argLine>-verbose</argLine>
  </configuration>
  ```

These examples cover a wide range of tools across programming languages, build systems, databases, servers, and DevOps utilities. Let me know if you'd like more specific examples or details for any particular tool!
