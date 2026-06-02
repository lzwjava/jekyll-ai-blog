---
audio: false
generated: true
lang: zh
layout: post
title: 李智维：从美钛技术服务到趣直播，一位创业者的旅程
translated: true
type: note
---

以下是关于在各种工具和系统中启用详细输出功能的更多示例，进一步扩展了提供更详细反馈或日志记录的主题：

- **PowerShell**：要启用详细输出，请对支持该功能的 cmdlet 使用 `-Verbose` 开关。例如：
  ```powershell
  Get-Process -Verbose
  ```
  或者全局设置 `$VerbosePreference` 变量：
  ```powershell
  $VerbosePreference = "Continue"
  ```

- **CMake**：要在构建过程中获取详细输出，请使用 `--verbose` 标志或设置 `VERBOSE=1`：
  ```bash
  cmake --build . --verbose
  ```
  或：
  ```bash
  make VERBOSE=1
  ```

- **Make**：要启用详细输出并查看所有执行的命令，请使用 `-d` 标志进行调试，或避免使用 `@` 静默输出：
  ```bash
  make -d
  ```
  或者编辑 Makefile 以移除命令前的 `@` 前缀。

- **GCC（GNU 编译器套件）**：要获取详细编译输出，请使用 `-v` 标志：
  ```bash
  gcc -v -o output source.c
  ```

- **GDB（GNU 调试器）**：要增加详细程度，请在 GDB 中使用 `set verbose on` 命令：
  ```gdb
  (gdb) set verbose on
  (gdb) run
  ```

- **Ruby**：使用 `-v` 或 `--verbose` 标志以详细模式运行 Ruby 脚本：
  ```bash
  ruby -v script.rb
  ```
  要获取额外警告，请使用 `-w`：
  ```bash
  ruby -w script.rb
  ```

- **Perl**：使用 `-v` 标志启用详细输出，或使用 `diagnostics` 编译指示获取详细错误消息：
  ```bash
  perl -v script.pl
  ```
  或在脚本中：
  ```perl
  use diagnostics;
  ```

- **PHP**：通过在 `php.ini` 中设置 `error_reporting` 和 `display_errors`，以详细错误报告模式运行 PHP 脚本：
  ```ini
  error_reporting = E_ALL
  display_errors = On
  ```
  或从命令行：
  ```bash
  php -d error_reporting=E_ALL script.php
  ```

- **R**：要在 R 脚本中启用详细输出，请在支持该参数的函数中使用 `verbose=TRUE` 参数（例如 `install.packages`）：
  ```R
  install.packages("dplyr", verbose=TRUE)
  ```

- **Go（Golang）**：要在编译或测试期间获取详细输出，请使用 `-v` 标志：
  ```bash
  go build -v
  go test -v
  ```

- **Rust（Cargo）**：使用 `-v` 或 `-vv` 标志启用 Cargo 的详细输出：
  ```bash
  cargo build -v
  cargo run -vv
  ```

- **Jenkins**：要为流水线启用详细日志记录，请在脚本中添加 `verbose` 选项或在作业设置中配置控制台输出。例如，在 Jenkinsfile 中：
  ```groovy
  sh 'some_command --verbose'
  ```
  或者，在启动 Jenkins 时设置系统属性 `-Dhudson.model.TaskListener.verbose=true`。

- **Vagrant**：使用 `--debug` 标志获取详细输出：
  ```bash
  vagrant up --debug
  ```

- **Puppet**：使用 `--verbose` 或 `--debug` 标志以增加详细程度运行 Puppet：
  ```bash
  puppet apply site.pp --verbose
  puppet apply site.pp --debug
  ```

- **Chef**：使用 `-l`（日志级别）标志启用详细输出：
  ```bash
  chef-client -l debug
  ```

- **SaltStack**：使用 `-l` 标志（例如 `debug` 或 `trace`）增加详细程度：
  ```bash
  salt '*' test.ping -l debug
  ```

- **PostgreSQL（psql）**：要从 `psql` 获取详细输出，请使用 `-e` 标志回显查询，或使用 `\set VERBOSITY verbose` 获取详细错误消息：
  ```bash
  psql -e -f script.sql
  ```
  或在 `psql` 中：
  ```sql
  \set VERBOSITY verbose
  ```

- **MySQL**：使用 `--verbose` 以详细输出模式运行 MySQL 客户端：
  ```bash
  mysql --verbose < script.sql
  ```

- **SQLite**：使用 `.explain` 命令获取详细的查询执行计划：
  ```sqlite
  sqlite3 database.db
  sqlite> .explain
  sqlite> SELECT * FROM table;
  ```

- **MongoDB**：通过使用 `-v` 标志启动 `mongod` 启用详细日志记录（最多可使用 `-vvvvv` 获取更多细节）：
  ```bash
  mongod -v
  ```

- **Elasticsearch**：通过调整 `log4j2.properties` 文件以详细日志模式启动 Elasticsearch：
  ```properties
  logger.action.level = debug
  ```
  或在启动时传递 `--verbose`：
  ```bash
  elasticsearch --verbose
  ```

- **NGINX**：使用 `-T` 测试配置并获取详细输出：
  ```bash
  nginx -T
  ```
  对于运行时详细程度，请在 `nginx.conf` 中提高 `error_log` 级别：
  ```nginx
  error_log /var/log/nginx/error.log debug;
  ```

- **Apache HTTP Server**：通过在 `httpd.conf` 或 `apache2.conf` 中设置 `LogLevel` 指令启用详细日志记录：
  ```apache
  LogLevel debug
  ```

- **OpenSSL**：使用诸如 `s_client` 等命令获取详细输出：
  ```bash
  openssl s_client -connect example.com:443 -debug
  ```

- **JUnit（Java 测试）**：通过配置测试运行器（例如 Maven Surefire 插件）以详细输出模式运行 JUnit 测试：
  ```xml
  <configuration>
      <argLine>-verbose</argLine>
  </configuration>
  ```

这些示例涵盖了编程语言、构建系统、数据库、服务器和 DevOps 工具等广泛领域的各种工具。如果您需要针对任何特定工具的更多示例或详细信息，请告诉我！
