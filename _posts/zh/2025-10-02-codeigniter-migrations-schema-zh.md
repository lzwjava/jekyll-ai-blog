---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter 数据库迁移与架构管理
translated: true
type: note
---

### 什么是 CodeIgniter 数据迁移？

CodeIgniter（CI）数据迁移是一项帮助以版本控制方式管理数据库架构变更的功能，类似于 Flyway 或 Liquibase 等工具。它允许您编写 PHP 脚本来定义数据库变更（例如创建表、添加列或修改数据），然后按顺序运行这些脚本来保持各环境中的架构最新。这可以避免手动 SQL 错误并支持回滚。

数据迁移的工作原理：

- 将迁移文件存储在目录中（默认：`application/migrations/`）。
- 在数据库表中跟踪"版本"以了解哪些迁移已应用。
- 根据需要向前（up）或向后（down）运行脚本。

您分享的配置文件（`migration.php`）控制迁移的行为方式。它使用 PHP 数组来设置选项。下面，我将通过示例解释关键设置。

### 关键配置设置

| 设置 | 代码中的值 | 说明 | 工作原理 |
|------|------------|------|----------|
| `migration_enabled` | `FALSE` | 全局启用或禁用迁移。当设置为 `FALSE` 时，无法运行迁移（出于安全考虑，因为它们会修改数据库）。 | CI 在执行任何迁移命令前会检查此设置。在开发期间设置为 `TRUE`，然后在生产环境中改回 `FALSE`。示例：如果启用，可通过控制器中的 `$this->migration->current()` 运行。 |
| `migration_type` | `'timestamp'` | 文件命名风格：`'sequential'`（例如 `001_add_blog.php`）或 `'timestamp'`（例如 `20121031104401_add_blog.php`）。推荐使用时间戳以实现更好的版本控制。 | 文件按时间顺序加载。时间戳使用 `YYYYMMDDHHIISS` 格式（例如 `20121031104401` 表示 2012年10月31日 10:44:01）。 |
| `migration_table` | `'migrations'` | 用于跟踪已应用迁移的数据库表名称。必需设置。 | 如果此表不存在，CI 会创建它。它存储最新的迁移版本。删除或更新此表会重置迁移历史记录。 |
| `migration_auto_latest` | `FALSE` | 如果设置为 `TRUE` 且 `migration_enabled` 也为 `TRUE`，则在加载 Migration 库时（例如页面加载时）自动运行迁移到最新版本。 | 在开发环境中自动同步架构很有用。设置为 `FALSE` 可手动运行迁移以进行控制（在生产环境中更安全）。 |
| `migration_version` | `0` | 要迁移到的目标版本/编号。设置为文件名前缀（例如 `20121031104401`）。`0` 表示未应用任何迁移。 | 运行 `$this->migration->version(20121031104401)` 会迁移到该点。用于目标回滚——负数会降级。 |
| `migration_path` | `APPPATH.'migrations/'` | 存储迁移文件的目录。`APPPATH` 是指向 `application/` 的 CI 常量。 | CI 扫描此文件夹以查找符合命名约定的 PHP 文件。必须可由 Web 服务器写入。可以使用自定义路径，如 `BASEPATH.'custom/migrations/'`。 |

### 如何使用数据迁移（分步指南）

1. **启用迁移**：在配置文件中临时设置 `$config['migration_enabled'] = TRUE;`。

2. **创建迁移文件**：在 `application/migrations/` 中添加一个 PHP 文件，名称类似 `20121031104401_add_blog.php`。内部使用 CI 的 Migration 类：

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

   - `up()` 应用变更（例如创建表）。
   - `down()` 撤销变更（例如删除表）。

3. **运行迁移**：
   - 加载库：`$this->load->library('migration');`
   - 到最新版本：`$this->migration->current();`
   - 到特定版本：`$this->migration->version('20121031104401');`
   - 从命令行运行（如果启用了 CLI）：`php index.php migrate current`

4. **常用命令**：
   - `$this->migration->latest()`：`current()` 的别名。
   - `$this->migration->find_migratables()`：列出可用文件。
   错误会记录到 CI 的日志文件或抛出异常。

5. **最佳实践**：
   - 保持迁移的幂等性（可安全重新运行）。
   - 先在开发环境中测试；避免在生产环境中启用自动迁移以防止意外架构变更。
   - 如果数据库支持，使用事务以实现原子性变更。
   - 使用后禁用：改回 `FALSE` 以确保安全。

如果遇到问题（例如路径权限），请查看 CI 的日志或文档：[codeigniter.com/user_guide/libraries/migration.html](https://codeigniter.com/user_guide/libraries/migration.html)。请指定您的 CI 版本以获得更针对性的建议！
