---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用Amazon RDS部署MySQL
translated: true
type: note
---

Amazon RDS（关系型数据库服务）for MySQL 是一项托管式数据库服务，可帮助您在云端轻松设置、操作和扩展 MySQL 数据库。它能自动处理备份、补丁安装和扩展等日常任务，让您专注于应用程序开发。本指南将带您了解基础知识：创建 MySQL 数据库实例、连接到实例以及执行简单操作。为简化流程，我们将使用 AWS 管理控制台。

**费用说明：** AWS 免费套餐为新账户提供有限用量，但超出部分将产生费用。请务必在完成后删除资源，避免意外账单。生产环境请遵循安全最佳实践，例如使用 VPC、加密和最小权限访问。

## 先决条件
- AWS 账户（如需请访问 [aws.amazon.com](https://aws.amazon.com) 注册）
- 对 AWS 控制台和 MySQL 的基本了解
- 为测试安全连接，我们将在同一 VPC（虚拟私有云）中创建 EC2 实例。请确定您的公网 IP 地址（例如通过 [checkip.amazonaws.com](https://checkip.amazonaws.com)）用于 SSH 访问
- 选择离您较近的 AWS 区域（例如美国东部（弗吉尼亚北部））

**最佳实践：** 在 VPC 中使用私有数据库实例，仅允许受信任资源访问。启用 SSL/TLS 实现加密连接。

## 步骤 1：创建用于连接的 EC2 实例
此步骤将设置一个简单的 Linux 服务器用于连接私有数据库实例。

1. 登录 [AWS 管理控制台](https://console.aws.amazon.com) 并打开 EC2 控制台
2. 选择您的区域
3. 点击 **启动实例**
4. 配置：
   - **名称：** `ec2-database-connect`
   - **AMI：** Amazon Linux 2023（符合免费套餐条件）
   - **实例类型：** t3.micro（符合免费套餐条件）
   - **密钥对：** 创建或选择现有密钥对用于 SSH 访问
   - **网络设置：** 编辑 > 允许 SSH 流量来源选择 **我的 IP**（或您的特定 IP，例如 `192.0.2.1/32`）。出于安全考虑请避免使用 `0.0.0.0/0`
   - 存储和标签保持默认设置
5. 点击 **启动实例**
6. 从实例详情中记录实例 ID、公网 IPv4 DNS 和密钥对名称
7. 等待状态显示为 **运行中**（2-5 分钟）

**安全提示：** 将 SSH 访问限制为仅限您的 IP 地址。安全下载密钥对（.pem 文件）

## 步骤 2：创建 MySQL 数据库实例
使用"轻松创建"功能通过默认设置快速配置。

1. 打开 [RDS 控制台](https://console.aws.amazon.com/rds/)
2. 选择与 EC2 实例相同的区域
3. 在导航窗格中点击 **数据库** > **创建数据库**
4. 选择 **轻松创建**
5. **配置** 部分：
   - 引擎类型：**MySQL**
   - 模板：**免费套餐**（付费账户选择 **沙盒**）
   - 数据库实例标识符：`database-test1`（或自定义名称）
   - 主用户名：`admin`（或自定义）
   - 主密码：自动生成或设置强密码（请安全保存）
6. （可选）在 **连接** 部分，选择 **连接到 EC2 计算资源** 并选择您的 EC2 实例以简化设置
7. 点击 **创建数据库**
8. 查看弹出的凭据信息（用户名/密码）——请立即保存，密码后续无法检索
9. 等待状态变为 **可用**（最多 10-20 分钟）。从 **连接与安全** 标签页记录 **终端节点**（DNS 名称）和端口（默认：3306）

**最佳实践：** 生产环境请使用"标准创建"自定义 VPC、备份（启用自动备份）和存储。启用删除保护和多可用区以实现高可用性。

## 步骤 3：连接到数据库实例
从 EC2 实例使用 MySQL 客户端进行连接。

1. SSH 登录 EC2 实例：
   ```
   ssh -i /路径/您的密钥对.pem ec2-user@您的-EC2-公网-DNS
   ```
   （请替换为您的实际信息，例如：`ssh -i ec2-database-connect-key-pair.pem ec2-user@ec2-12-345-678-90.compute-1.amazonaws.com`）

2. 在 EC2 实例上更新软件包：
   ```
   sudo dnf update -y
   ```

3. 安装 MySQL 客户端：
   ```
   sudo dnf install mariadb105 -y
   ```

4. 连接到数据库：
   ```
   mysql -h 您的数据库终端节点 -P 3306 -u admin -p
   ```
   根据提示输入主密码

连接成功后将显示 MySQL 提示符（`mysql>`）

**故障排除：** 确保安全组允许来自 EC2 实例的 3306 端口入站流量。外部连接需将数据库设为公开（不推荐）或使用堡垒主机/VPN

**安全提示：** 使用 `--ssl-mode=REQUIRED` 建立加密连接：`mysql -h 终端节点 -P 3306 -u admin -p --ssl-mode=REQUIRED`

## 步骤 4：基本使用
连接成功后即可运行 SQL 命令。示例如下：

- 显示数据库：`SHOW DATABASES;`
- 创建示例数据库：`CREATE DATABASE myapp;`
- 使用数据库：`USE myapp;`
- 创建表：
  ```
  CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100)
  );
  ```
- 插入数据：`INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');`
- 查询：`SELECT * FROM users;`
- 退出：`EXIT;`

在应用程序（如 Python、Node.js）中，使用标准 MySQL 驱动程序配合终端节点、端口、用户名和密码作为连接字符串

**最佳实践：** 通过 CloudWatch 监控性能，启用自动备份，根据需要垂直扩展（实例规格）或水平扩展（只读副本）

## 清理：删除资源
停止计费操作：

1. **删除 EC2 实例：** EC2 控制台 > 选择实例 > **实例状态** > **终止** > 确认
2. **删除数据库实例：** RDS 控制台 > 选择数据库 > **操作** > **删除** > 取消勾选创建快照 > 确认

检查 AWS 计费控制台确认无运行中资源

有关迁移、性能调优或 API/CLI 使用等高级主题，请参阅 AWS 文档

## 参考资料
- [创建并连接到 MySQL 数据库实例](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html)
- [Amazon RDS for MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html)
- [Amazon RDS 入门指南](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html)
