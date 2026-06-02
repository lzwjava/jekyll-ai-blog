---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter数据库配置概览
translated: true
type: note
---

### CodeIgniter 数据库配置概览

该 PHP 文件是 CodeIgniter 数据库连接的配置脚本。它定义了多个数据库连接组（如 'default'、'lzwjava'、'leo66'、'testing'）的设置，允许应用根据环境（开发、测试、生产）切换连接。`$active_group` 变量决定默认使用的连接组。

核心组件：

- **$query_builder**：设为 `TRUE` 可启用查询构造器类，提供面向对象的 SQL 查询构建方式。
- **$db[][]**：关联数组，每个子数组（如 'default'）包含数据库连接的详细配置选项。

`$active_group` 根据 `ENVIRONMENT` 常量动态设置（例如通过 switch 语句），确保不同部署阶段使用不同配置。下面将结合 CodeIgniter 文档和标准用法详解各配置项。注意：实际敏感值（如凭证）已出于安全考虑省略，实践中应通过环境变量等方式安全存储。

### 详细配置选项

每个数据库组都是包含以下键的数组。大多数配置项较为直观，但部分（如 `encrypt`）支持高级功能的子选项。

- **dsn** (字符串)：完整数据源名称字符串，用于描述连接。这是单独指定主机名、用户名等字段的替代方案，适用于 ODBC 等复杂设置。若提供此参数，将覆盖独立的主机/凭证字段。示例格式：`'dsn' => 'mysql:host=yourhost;dbname=yourdatabase'`。

- **hostname** (字符串)：数据库服务器地址（如 'localhost' 或 IP '127.0.0.1'），用于标识数据库运行位置，支持 TCP/IP 或套接字连接。

- **username** (字符串)：用于数据库服务器身份验证的账户名，需与数据库管理系统中的有效用户匹配。

- **password** (字符串)：与用户名配对的密钥，用于身份验证。务必安全存储以防泄露。

- **database** (字符串)：要连接的特定数据库名称，所有查询将默认在此数据库执行。

- **dbdriver** (字符串)：指定使用的数据库驱动（如 MySQL 用 'mysqli'）。常见驱动包括 'cubrid'、'ibase'、'mssql'、'mysql'、'mysqli'、'oci8'、'odbc'、'pdo'、'postgre'、'sqlite'、'sqlite3' 和 'sqlsrv'。'mysqli' 是 MySQL 的现代安全选择。

- **dbprefix** (字符串)：使用 CodeIgniter 查询构造器时自动添加到表名的前缀（如设为 'prefix_' 时，'mytable' 将变为 'prefix_mytable'），适用于共享主机或多租户应用的表命名空间隔离。

- **pconnect** (布尔值)：启用持久连接（`TRUE`）或常规连接（`FALSE`）。持久连接可复用链接提升高负载应用性能，但过度使用可能耗尽服务器资源。

- **db_debug** (布尔值)：控制是否显示数据库错误（`TRUE`）用于调试。生产环境应禁用（`FALSE`）以避免向用户泄露敏感错误信息。

- **cache_on** (布尔值)：启用（`TRUE`）或禁用（`FALSE`）查询缓存。启用后，重复查询结果将被存储以加速查询。

- **cachedir** (字符串)：缓存查询结果的目录路径，需确保 Web 服务器具有写权限。结合 `cache_on` 使用可降低数据库负载。

- **char_set** (字符串)：数据库通信的字符编码（如现代 Unicode 支持推荐 'utf8mb4'），确保多语言应用的数据完整性。

- **dbcollat** (字符串)：字符排序和比较的校对规则（如大小写不敏感的 Unicode 校对 'utf8mb4_unicode_ci'）。此设置作为旧版 PHP/MySQL 的备用方案，其他情况下会被忽略。

- **swap_pre** (字符串)：用于动态替换 `dbprefix` 的表前缀，适用于无需重命名表即可切换现有应用前缀的场景。

- **encrypt** (布尔值或数组)：加密支持配置。对于 'mysql'（已弃用）、'sqlsrv' 和 'pdo/sqlsrv'，使用 `TRUE`/`FALSE` 启用/禁用 SSL。对于 'mysqli' 和 'pdo/mysql'，需使用包含 SSL 子选项的数组：
  - 'ssl_key'：私钥文件路径（如客户端证书）。
  - 'ssl_cert'：公钥证书文件路径。
  - 'ssl_ca'：证书授权文件路径（用于验证服务器证书）。
  - 'ssl_capath'：PEM 格式可信 CA 证书目录路径。
  - 'ssl_cipher'：允许的密码列表（冒号分隔，如 'AES128-SHA'）。
  - 'ssl_verify'：仅适用于 'mysqli'；`TRUE` 验证服务器证书，`FALSE` 跳过验证（安全性较低，适用于自签名证书）。

- **compress** (布尔值)：为 MySQL 连接启用客户端压缩（仅限 MySQL，其他驱动会忽略此设置），可减少网络流量。

- **stricton** (布尔值)：强制启用「严格模式」连接（`TRUE`），执行严格 SQL 规则以尽早捕获错误（如无效数据类型），适用于开发阶段。

- **ssl_options** (数组)：用于 'pdo' 等驱动的高级 SSL 配置选项，允许微调 `encrypt` 未覆盖的加密参数。

- **failover** (数组)：主连接失败时自动切换的备用连接数组。每个元素需包含与主配置相同的结构（如备用主机名/端口）。示例：`array(array('hostname' => 'backuphost', ...))`。

- **save_queries** (布尔值)：在内存中保存已执行查询用于调试（`TRUE`），可通过 `$this->db->last_query()` 等方法访问，但可能增加内存使用，生产环境建议禁用（`FALSE`）以节省资源。

### 数据库组与环境切换

- **default**：基础配置数组，作为配置模板，设置为生产环境默认值（如关闭调试、安全设置）。
- **lzwjava**：继承基础配置但覆盖用户名为不同值（密码留空，暗示无认证或默认认证）。
- **leo66**：继承基础配置但将主机名改为本地回环地址，用户名/密码改为默认值，并添加端口号（3306，MySQL 标准端口）。
- **testing**：专用于测试环境的连接组，继承基础配置。

通过 `switch` 语句根据 `ENVIRONMENT` 激活对应连接组：

- 开发环境：使用 'lzwjava'
- 测试环境：使用 'testing'
- 生产环境：使用 'default'

此配置方案为本地开发、测试和线上部署提供了灵活性。务必对输入进行消毒处理以防 SQL 注入，建议将凭证移至环境变量提升安全性。完整文档请参阅 CodeIgniter 官方用户指南的数据库连接章节。如有具体配置项或连接组需要进一步说明，请随时告知！
