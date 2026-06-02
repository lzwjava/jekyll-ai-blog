---
audio: false
generated: true
lang: zh
layout: post
title: 使用MySQL Workbench
translated: true
type: note
---

### 核心要点

- MySQL Workbench 很可能是一款用于管理 MySQL 数据库的免费开源工具，支持 Windows、macOS 和 Linux 系统。
- 您可以从官网下载并安装该工具，然后使用服务器详细信息（如主机名和用户名）设置连接。
- 研究表明，您可以通过图形界面和 SQL 语句两种方式创建数据库、数据表并执行查询。
- 现有证据表明该工具还提供数据建模和服务器管理等高级功能，这对初学者来说可能是意料之外的。

### 什么是 MySQL Workbench？

MySQL Workbench 是一款帮助您设计、开发和管理 MySQL 数据库的工具。它免费开源，支持 Windows、macOS 和 Linux 系统，因此可供众多用户使用。该工具提供图形界面，这意味着您不一定需要编写代码来管理数据库，当然您也可以选择使用代码方式。

### 快速入门

首先访问官方下载页面 [https://www.mysql.com/products/workbench/](https://www.mysql.com/products/workbench/) 获取适用于您操作系统的版本。按照提供的安装步骤进行操作，这些步骤简单明了，在各个平台上都类似。

### 设置与使用

安装完成后，打开 MySQL Workbench，点击"MySQL Connections"旁边的"+"按钮创建新连接。您需要填写服务器的主机名、端口（通常为 3306）、用户名和密码等详细信息。测试连接以确保其正常工作。

连接成功后，您可以：

- **创建数据库：** 在 SQL 编辑器中运行 `CREATE DATABASE database_name;`，或者右键点击"Schemas"并选择"Create Schema..."
- **创建数据表：** 在 SQL 编辑器中编写 CREATE TABLE 语句，或通过右键点击数据库使用图形化选项
- **执行查询：** 在 SQL 编辑器中编写 SQL 查询语句并执行以查看结果

### 高级功能

除了基础功能外，MySQL Workbench 还提供了一些意想不到的高级功能，例如数据建模（您可以使用 ER 图可视化设计数据库）以及服务器管理工具（如管理用户和配置）。这些功能可以通过"Model"标签页和其他菜单进行探索。

---

### 调研说明：MySQL Workbench 使用全面指南

本节详细探讨 MySQL Workbench 的使用方法，在直接回答的基础上扩展了更多背景信息和技术细节。旨在涵盖研究中讨论的所有方面，确保为不同专业水平的用户提供全面理解。

#### MySQL Workbench 简介

MySQL Workbench 被描述为一款面向数据库架构师、开发人员和数据库管理员（DBA）的统一可视化工具。根据官方产品页面 [MySQL Workbench](https://www.mysql.com/products/workbench/) 的说明，它是免费开源工具，支持包括 Windows、macOS 和 Linux 在内的主流操作系统。这种跨平台可用性确保了工具的可访问性，并且它是与 MySQL Server 8.0 共同开发和测试的，根据手册 [MySQL Workbench Manual](https://dev.mysql.com/doc/workbench/en/) 的说明，对于 8.4 及更高版本可能存在兼容性问题。该工具集成了数据建模、SQL 开发和管理功能，使其成为数据库管理的全面解决方案。

#### 安装流程

安装过程因操作系统而异，但在教程 [Ultimate MySQL Workbench Installation Guide](https://www.simplilearn.com/tutorials/mysql-tutorial/mysql-workbench-installation) 中找到了 Windows 的详细步骤。对于 Windows 用户，需要访问 [MySQL Downloads](https://www.mysql.com/downloads/) 选择安装程序，选择自定义设置，然后安装 MySQL Server、Workbench 和 shell。该过程涉及授予权限、设置网络和配置 root 密码，通常默认设置就足够了。对于其他操作系统，过程类似，建议用户遵循特定平台的说明，确保不需要 Java（与最初的推测相反），因为 MySQL Workbench 使用 Qt 框架。

为清晰起见，下面提供了 Windows 安装步骤的总结表格：

| 步骤编号 | 操作                                                                                     | 详情                                                                 |
|----------|------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| 0        | 打开 MySQL 网站                                                                          | 访问 [MySQL Downloads](https://www.mysql.com/downloads/)            |
| 1        | 选择下载选项                                                                             | -                                                                   |
| 2        | 选择适用于 Windows 的 MySQL Installer                                                    | -                                                                   |
| 3        | 选择所需的安装程序并点击下载                                                             | -                                                                   |
| 4        | 打开下载的安装程序                                                                       | -                                                                   |
| 5        | 授予权限并选择设置类型                                                                   | 点击 Yes，然后选择 Custom                                          |
| 6        | 点击 Next                                                                               | -                                                                   |
| 7        | 安装 MySQL server、Workbench 和 shell                                                    | 在安装程序中选择并移动组件                                          |
| 8        | 点击 Next，然后点击 Execute                                                              | 下载并安装组件                                                      |
| 9        | 配置产品，使用默认的 Type 和 Networking 设置                                             | 点击 Next                                                          |
| 10       | 设置身份验证为强密码加密，设置 MySQL Root 密码                                           | 点击 Next                                                          |
| 11       | 使用默认的 Windows 服务设置，应用配置                                                    | 点击 Execute，配置完成后点击 Finish                                |
| 12       | 完成安装，启动 MySQL Workbench 和 Shell                                                  | 选择 Local instance，输入密码即可使用                              |

安装后，用户可以按照教程建议运行 `Show Databases;` 等基本 SQL 命令来验证功能。

#### 设置连接

连接到 MySQL 服务器是关键步骤，在 [SiteGround Tutorials](https://www.siteground.com/tutorials/php-mysql/mysql-workbench/) 和 [w3resource MySQL Workbench Tutorial](https://www.w3resource.com/mysql/administration-tools/mysql-workbench-tutorial.php) 等多个来源中找到了详细指导。用户打开 MySQL Workbench，点击"MySQL Connections"旁边的"+"按钮，输入连接名称、方法（通常为 Standard TCP/IP）、主机名、端口（默认 3306）、用户名、密码以及可选的默认模式等详细信息。建议测试连接，w3resource 教程中的幻灯片通过"MySQL Workbench 新连接步骤 1"到"步骤 4"直观地引导完成整个过程。

对于远程连接，额外注意事项包括确保服务器的防火墙允许 IP 地址访问，如 [Connect MySQL Workbench](https://www.inmotionhosting.com/support/website/connect-database-remotely-mysql-workbench/) 所述。这对于连接到基于云的 MySQL 实例（如 Azure Database for MySQL）的用户至关重要，详细内容见 [Quickstart: Connect MySQL Workbench](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/connect-workbench)。

#### 执行数据库操作

连接成功后，用户可以使用图形和基于 SQL 的两种方法执行各种操作。创建数据库可以通过 SQL 编辑器使用 `CREATE DATABASE database_name;` 完成，或者通过右键点击"Schemas"选择"Create Schema..."以图形方式完成，如教程所示。类似地，创建表涉及编写 CREATE TABLE 语句或使用图形界面，具有编辑表数据和管理模式的选项，如 [A Complete Guide on MySQL Workbench](https://www.simplilearn.com/tutorials/mysql-tutorial/mysql-workbench) 中所述。

SQL 编辑器促进了查询的执行，它提供语法高亮、自动完成和查询历史记录等功能，增强了可用性。这些功能在 [MySQL Workbench](https://www.mysql.com/products/workbench/) 中有所强调，使其对初学者和高级用户都友好。

#### 高级功能和工具

MySQL Workbench 超越了基础功能，提供高级功能，例如使用实体关系（ER）图进行数据建模、正向和逆向工程以及变更管理，如 [MySQL Workbench Manual](https://dev.mysql.com/doc/workbench/en/) 所述。"Model"标签页允许可视化设计，生成 SQL 脚本，这对数据库架构师特别有用。服务器管理工具包括管理用户、权限和配置，带有可视化控制台以提供更好的可见性，如 [MySQL Workbench](https://www.mysql.com/products/workbench/) 所示。

其他功能包括数据库迁移、性能优化和备份/恢复能力，以及用于备份数据库的 Data Export 等工具，详细内容见 [SiteGround Tutorials](https://www.siteground.com/tutorials/php-mysql/mysql-workbench/)。这些高级功能对于数据库管理新手来说可能是意料之外的，为全面的数据库管理提供了一套强大的工具集。

#### 提示与最佳实践

用户应确保 MySQL 服务器正在运行且连接详细信息正确，并检查远程连接的防火墙设置。建议使用强密码和安全方法，特别是对于敏感数据。保存 SQL 脚本和探索版本控制可以优化工作流程，尽管直接回答中未详细说明，但这是社区洞察中的最佳实践的一部分。

#### 结论

本调研说明提供了使用 MySQL Workbench 的全面指南，涵盖了安装、连接设置、基础和高级操作以及提示。它利用了多个可靠来源，确保截至 2025 年 2 月 28 日的准确性，并为寻求详细技术指导的用户设计。

#### 主要引用文献

- [MySQL Workbench Manual about 10 words](https://dev.mysql.com/doc/workbench/en/)
- [MySQL Workbench product page about 10 words](https://www.mysql.com/products/workbench/)
- [Ultimate MySQL Workbench Installation Guide about 10 words](https://www.simplilearn.com/tutorials/mysql-tutorial/mysql-workbench-installation)
- [SiteGround Tutorials MySQL Workbench about 10 words](https://www.siteground.com/tutorials/php-mysql/mysql-workbench/)
- [w3resource MySQL Workbench Tutorial about 10 words](https://www.w3resource.com/mysql/administration-tools/mysql-workbench-tutorial.php)
- [Connect MySQL Workbench remotely about 10 words](https://www.inmotionhosting.com/support/website/connect-database-remotely-mysql-workbench/)
- [Quickstart Connect MySQL Workbench Azure about 10 words](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/connect-workbench)
- [A Complete Guide on MySQL Workbench about 10 words](https://www.simplilearn.com/tutorials/mysql-tutorial/mysql-workbench)
