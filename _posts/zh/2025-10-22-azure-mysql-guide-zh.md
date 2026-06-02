---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Azure Database for MySQL 灵活服务器指南
translated: true
type: note
---

Azure Database for MySQL 是由 MySQL 社区版提供支持的完全托管式关系型数据库服务。它能自动处理备份、补丁管理和监控等日常任务，让您专注于应用程序开发。推荐使用**灵活服务器**部署选项，相比旧版单一服务器（已逐步停用）提供更多配置选项和更优性能。

本指南将介绍如何创建服务器、建立连接及执行基础操作。为简化流程，本文以 Azure 门户操作为基准。

## 先决条件
- 有效的 Azure 订阅（若无可前往 [azure.microsoft.com](https://azure.microsoft.com/free/) 创建）
- 可访问 Azure 门户 (portal.azure.com)
- 具备 MySQL 基础概念知识
- 出站网络需开放 3306 端口（MySQL 默认端口）
- 已安装 MySQL Workbench 连接工具（从 [mysql.com](https://dev.mysql.com/downloads/workbench/) 下载）

## 步骤 1：在 Azure 门户创建灵活服务器
按以下步骤配置服务器：

1. 登录 [Azure 门户](https://portal.azure.com)

2. 在顶部搜索栏输入 "Azure Database for MySQL Flexible Servers" 并选择

3. 点击 **创建** 启动配置向导

4. 在 **基础** 标签页配置：
   - **订阅**：选择您的订阅
   - **资源组**：新建（如 `myresourcegroup`）或选择现有组
   - **服务器名称**：唯一名称（如 `mydemoserver`），3-63 字符，支持小写字母/数字/连字符。完整主机名格式为 `<名称>.mysql.database.azure.com`
   - **区域**：选择离用户最近的区域
   - **MySQL 版本**：8.0（最新主版本）
   - **工作负载类型**：开发（测试环境；生产环境请选小型/中型）
   - **计算+存储**：可突增层级，Standard_B1ms（1 个 vCore），10 GiB 存储，100 IOPS，7 天备份。可根据需求调整（如迁移时需增加 IOPS）
   - **可用区**：无首选项（或选择与应用相同的可用区）
   - **高可用性**：初始建议禁用（生产环境需启用区域冗余）
   - **身份验证**：同时启用 MySQL 和 Microsoft Entra（提升灵活性）
   - **管理员用户名**：例如 `mydemouser`（不可使用 root/admin 等，最长 32 字符）
   - **密码**：强密码（8-128 字符，包含大小写字母/数字/符号）

5. 切换到 **网络** 标签页：
   - **连接方法**：公共访问（简化配置；生产环境建议使用私有 VNet）
   - **防火墙规则**：添加当前客户端 IP 地址（或允许 Azure 服务）。此设置后续不可修改

6. 在 **查看 + 创建** 中检查配置，点击 **创建**。部署过程约需 5-10 分钟，可通过通知栏监控进度

7. 部署完成后，可将服务器固定到仪表板，进入资源 **概述** 页面。默认数据库包含 `information_schema`、`mysql` 等

## 步骤 2：连接至服务器
推荐使用 MySQL Workbench 进行图形化连接（也可选用 Azure Data Studio、mysql CLI 或 Azure Cloud Shell）

1. 在门户中进入服务器 **概述** 页面，记录：
   - 服务器名称（如 `mydemoserver.mysql.database.azure.com`）
   - 管理员用户名
   - 如需可重置密码

2. 打开 MySQL Workbench

3. 点击 **新建连接**（或编辑现有连接）

4. 在 **参数** 标签页配置：
   - **连接名称**：例如 `Demo Connection`
   - **连接方法**：Standard (TCP/IP)
   - **主机名**：完整服务器名称
   - **端口**：3306
   - **用户名**：管理员用户名
   - **密码**：输入密码并保存到密钥库

5. 点击 **测试连接**。若失败请检查：
   - 确认门户中的连接信息
   - 确保防火墙已允许当前 IP
   - 强制启用 TLS/SSL（TLS 1.2）；如需绑定 CA 证书，请从 [DigiCert](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem) 下载证书，在 Workbench 的 SSL 标签页中设置（使用 SSL > 需要并指定 CA 文件）

6. 点击 **确定** 保存连接。双击连接图标即可打开查询编辑器

## 步骤 3：创建和管理数据库
连接成功后可通过门户或客户端管理数据库

### 通过 Azure 门户：
1. 在服务器页面选择左侧菜单的 **数据库**
2. 点击 **+ 添加**：
   - **数据库名称**：例如 `testdb`
   - **字符集**：utf8（默认）
   - **排序规则**：utf8_general_ci
3. 点击 **保存**

删除操作：选择数据库后点击 **删除**

### 通过 MySQL Workbench（SQL 查询）：
在查询编辑器中执行以下命令：

- 创建数据库：`CREATE DATABASE testdb CHARACTER SET utf8 COLLATE utf8_general_ci;`
- 列出数据库：`SHOW DATABASES;`
- 使用数据库：`USE testdb;`
- 创建表：`CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));`
- 插入数据：`INSERT INTO users (name) VALUES ('Alice');`
- 查询数据：`SELECT * FROM users;`

若未启用自动提交，需通过 `COMMIT;` 提交更改

## 基础使用技巧
- **扩展性**：通过 **概述** > **计算+存储** 调整 vCore/存储/IOPS（多数配置变更无需停机）
- **备份**：支持自动每日备份；35 天内时间点还原（在 **备份** 设置中配置）
- **监控**：使用 **指标** 查看 CPU/存储数据；设置告警规则
- **安全性**：始终启用 SSL（强制要求）。生产环境建议启用高可用、私有网络和 Entra ID 认证
- **迁移**：小型数据库可使用 mysqldump；大型数据库推荐使用 DMS
- **成本**：按计算/存储资源计费；建议从小规格开始逐步扩展。可通过 [azure.microsoft.com](https://azure.microsoft.com/pricing/calculator/) 费用计算器估算
- **清理**：删除资源组即可移除服务器并停止计费

如需使用读取副本或服务器参数等高级功能，请探索门户左侧菜单选项

## 参考文档
- [快速入门：通过 Azure 门户创建灵活服务器](https://learn.microsoft.com/zh-cn/azure/mysql/flexible-server/quickstart-create-server-portal)
- [使用 MySQL Workbench 进行连接](https://learn.microsoft.com/zh-cn/azure/mysql/flexible-server/connect-workbench)
- [创建和管理数据库](https://learn.microsoft.com/zh-cn/azure/mysql/flexible-server/how-to-create-manage-databases)
- [Azure Database for MySQL 文档中心](https://learn.microsoft.com/zh-cn/azure/mysql/)
