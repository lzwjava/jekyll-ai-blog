---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: MongoDB完全指南
translated: true
type: note
---

MongoDB 是一种流行的开源 NoSQL 文档数据库，专为现代应用开发而设计。它使用灵活的类 JSON 文档（称为 BSON）存储数据，非常适合处理非结构化或半结构化数据。与传统关系型数据库不同，MongoDB 采用无模式设计，允许集合（文档组）拥有不同的结构。它具有高度可扩展性，支持通过分片实现水平扩展，并通过复制提供高可用性。MongoDB 可部署在本地、通过 MongoDB Atlas（托管服务）在云端或混合环境中运行。本指南涵盖从基础到高级主题的所有内容，并提供使用 MongoDB Shell (mongosh) 的示例。

## 简介

MongoDB 在需要快速开发、灵活数据模型和高性能的场景中表现出色。主要特性包括：

- **文档模型**：将数据存储为具有嵌套结构的自包含文档
- **查询语言**：使用类 JavaScript 对象语法的丰富查询功能
- **可扩展性**：内置分布式系统支持
- **生态系统**：通过官方驱动与 Python、Node.js、Java 等语言集成

被 Adobe、eBay 和 Forbes 等公司用于大数据、实时分析和内容管理等应用场景。

## 安装指南

MongoDB 提供社区版（免费开源）和企业版。安装方法因平台而异；请始终从官网下载以确保安全。

### Windows 系统

- 从 MongoDB 下载中心获取 MSI 安装程序
- 运行安装程序，选择"完整"安装，可包含 MongoDB Compass（图形化工具）
- 将 MongoDB 的 `bin` 目录（如 `C:\Program Files\MongoDB\Server\8.0\bin`）添加到 PATH 环境变量
- 创建数据目录：`mkdir -p C:\data\db`
- 启动服务：`mongod.exe --dbpath C:\data\db`

支持：Windows 11、Server 2022/2019

### macOS 系统

- 使用 Homebrew：`brew tap mongodb/brew && brew install mongodb-community`
- 或下载 TGZ 压缩包，解压后添加至 PATH
- 创建数据目录：`mkdir -p /data/db`
- 启动：`mongod --dbpath /data/db`（或使用 `brew services start mongodb/brew/mongodb-community`）

支持：macOS 11–14（x86_64 和 arm64 架构）

### Linux 系统

- Ubuntu/Debian：添加 MongoDB 仓库密钥和列表后执行 `apt-get install -y mongodb-org`
- RHEL/CentOS：使用 yum/dnf 配合仓库文件安装
- 创建数据目录：`sudo mkdir -p /data/db && sudo chown -R $USER /data/db`
- 启动：`sudo systemctl start mongod`

支持：Ubuntu 24.04、RHEL 9+、Debian 12、Amazon Linux 2023 等。建议使用 XFS/EXT4 文件系统，避免 32 位系统

### 云端（MongoDB Atlas）

- 在 mongodb.com/atlas 注册账号
- 通过界面或 CLI 创建免费集群：`atlas clusters create <名称> --provider AWS --region us-east-1 --tier M0`
- 设置 IP 白名单：`atlas network-access create <IP地址>`
- 获取连接字符串并连接：`mongosh "mongodb+srv://<用户名>:<密码>@cluster0.abcde.mongodb.net/"`

Atlas 自动处理备份、扩展和监控功能

## 核心概念

### 数据库

作为集合的容器，实现数据逻辑分离。首次使用时隐式创建：`use mydb`。切换数据库：`use mydb`。列出数据库：`show dbs`

### 集合

文档的分组，类似表但具有模式灵活性。隐式创建：`db.mycollection.insertOne({})`。列出集合：`show collections`

### 文档

数据基本单元：包含键值对的 BSON 对象。示例：

```javascript
{ "_id": ObjectId("..."), "name": "John", "age": 30, "address": { "city": "NYC", "zip": 10001 } }
```

支持数组、嵌套对象及日期、二进制等数据类型

### BSON

二进制格式，提供高效存储和网络传输。在 JSON 基础上扩展了 ObjectId、Date、Binary 等类型

### 命名空间

唯一标识符格式：`数据库.集合`（如 `mydb.orders`）

配置示例：

```javascript
use test
db.orders.insertMany([
  { item: "almonds", price: 12, quantity: 2 },
  { item: "pecans", price: 20, quantity: 1 }
])
```

## CRUD 操作

在 mongosh 中使用 `db.collection.method()` 语法。多文档 ACID 事务通过会话实现

### 创建（插入）

- 单文档：`db.users.insertOne({ name: "Alice", email: "alice@example.com" })`
- 多文档：`db.users.insertMany([{ name: "Bob" }, { name: "Charlie" }])`
返回插入的文档 ID

### 读取（查询）

- 全部文档：`db.users.find()`
- 条件筛选：`db.users.find({ age: { $gt: 25 } })`
- 格式化输出：`.pretty()`
- 限制/排序：`db.users.find().limit(5).sort({ age: -1 })`

### 更新

- 单文档：`db.users.updateOne({ name: "Alice" }, { $set: { age: 31 } })`
- 多文档：`db.users.updateMany({ age: { $lt: 20 } }, { $set: { status: "minor" } })`
- 数值递增：`{ $inc: { score: 10 } }`

### 删除

- 单文档：`db.users.deleteOne({ name: "Bob" })`
- 多文档：`db.users.deleteMany({ status: "inactive" })`
- 删除集合：`db.users.drop()`

## 查询与索引

### 查询操作

使用谓词条件进行筛选。支持等值、范围、逻辑运算等操作

- 基础查询：`db.inventory.find({ status: "A" })`（等效 SQL：`WHERE status = 'A'`）
- $in 操作符：`db.inventory.find({ status: { $in: ["A", "D"] } })`
- $lt/$gt 操作符：`db.inventory.find({ qty: { $lt: 30 } })`
- $or 操作符：`db.inventory.find({ $or: [{ status: "A" }, { qty: { $lt: 30 } }] })`
- 正则表达式：`db.inventory.find({ item: /^p/ })`（匹配以 "p" 开头的项目）
- 嵌套字段：`db.users.find({ "address.city": "NYC" })`

字段投影：`db.users.find({ age: { $gt: 25 } }, { name: 1, _id: 0 })`

### 索引机制

通过避免全表扫描提升查询速度。基于 B 树结构

- 索引类型：单字段（`db.users.createIndex({ name: 1 })`）、复合（`{ name: 1, age: -1 }`）、唯一（`{ email: 1 }`）
- 优势：加速等值/范围查询，优化排序结果
- 创建索引：`db.users.createIndex({ age: 1 })`（升序）
- 查看索引：`db.users.getIndexes()`
- 删除索引：`db.users.dropIndex("age_1")`

使用 Atlas Performance Advisor 获取优化建议。注意权衡：写入速度会受影响

## 聚合框架

通过管道阶段处理数据。类似 SQL GROUP BY 但功能更强大

- 基础聚合：`db.orders.aggregate([ { $match: { price: { $lt: 15 } } } ])`
- 处理阶段：`$match`（筛选）、`$group`（聚合：`{ $sum: "$price" }`）、`$sort`、`$lookup`（关联：`{ from: "inventory", localField: "item", foreignField: "sku", as: "stock" }`）、`$project`（重塑文档结构）
- 示例（关联与排序）：

```javascript
db.orders.aggregate([
  { $match: { price: { $lt: 15 } } },
  { $lookup: { from: "inventory", localField: "item", foreignField: "sku", as: "inventory_docs" } },
  { $sort: { price: 1 } }
])
```

表达式运算：`{ $add: [ "$price", 10 ] }`。可在 Atlas 界面预览聚合结果

## 模式设计

MongoDB 的灵活性避免了刚性模式约束，但需要为性能进行周密设计

- **设计原则**：根据访问模式（读/写）建模，使用索引，保持工作集在内存中
- **嵌入式设计**：将关联数据反规范化存储在同一文档中，实现原子读写。例如将评论嵌入博客文章。优点：查询快速。缺点：数据冗余，文档体积增大
- **引用式设计**：通过 ID 进行规范化关联。例如 `posts` 通过 `userId` 引用 `users`。使用 `$lookup` 进行关联查询。优点：减少冗余。缺点：需要多次查询
- 模式选择：一对少（嵌入）、一对多（引用或嵌入数组）、多对多（引用）
- 数据验证：通过 `db.createCollection("users", { validator: { $jsonSchema: { ... } } })` 强制执行

权衡数据冗余与原子性（仅文档级别）的取舍

## 复制与分片

### 复制机制

通过副本集（一组 `mongod` 实例）提供冗余和高可用性

- 核心组件：主节点（写入）、从节点（通过操作日志复制，可选读取）、仲裁节点（投票，不存储数据）
- 部署流程：使用 `rs.initiate({ _id: "rs0", members: [{ _id: 0, host: "host1:27017" }] })` 初始化。添加成员：`rs.add("host2:27017")`
- 选举机制：主节点故障时，从节点约 10-12 秒内完成选举
- 读取偏好设置：`primary`、`secondary`（可能存在延迟）
- 适用于故障转移、备份场景。启用流控制管理复制延迟

### 分片架构

水平扩展方案：将数据分布到多个分片

- 核心组件：分片（副本集）、Mongos（路由节点）、配置服务器（元数据存储）
- 分片键：用于数据分区的字段（例如哈希分片实现均匀分布）。需先创建索引
- 设置流程：启用分片 `sh.enableSharding("mydb")`，分片集合 `sh.shardCollection("mydb.users", { userId: "hashed" })`
- 均衡器：自动迁移数据块实现负载均衡。区域分片支持地理局部性
- 分片策略：哈希分片（均匀分布）、范围分片（定向查询优化）

通过 mongos 连接；支持跨分片事务

## 安全防护

通过分层保护机制确保部署安全

- **身份验证**：SCRAM、LDAP、OIDC、X.509。创建用户：`db.createUser({ user: "admin", pwd: "pass", roles: ["root"] })`
- **授权管理**：基于角色的访问控制（RBAC）。内置角色：read、readWrite、dbAdmin
- **加密机制**：传输层 TLS/SSL 加密，静态数据加密（EAR）通过 AWS KMS/Google Cloud KMS/Azure Key Vault 实现。客户端字段级加密（CSFLE）保护敏感字段
- 网络安全：IP 访问列表，Atlas 中的 VPC 对等连接
- 审计功能：记录操作日志

启动时启用认证：`--auth`。使用 Atlas 获得内置安全功能

## 最佳实践

- **生产环境配置**：以服务形式运行（systemctl/brew）。在 SSD 上分离数据/日志/日记文件。使用 WiredTiger 存储引擎（默认）
- **监控指标**：`mongostat`、`mongotop`、Atlas 监控图表。关注连接数（`connPoolStats`）、缓存淘汰、I/O 负载（`iostat`）
- **备份策略**：`mongodump`/`mongorestore` 或 Atlas 快照。逻辑备份（JSON）与物理备份（文件）对比
- **性能优化**：合理使用索引，限制返回字段，避免大数组。设置 `ulimit -n 64000`，禁用交换分区（`vm.swappiness=0`），优化 TCP 保活设置
- **扩展方案**：从副本集开始；数据量超过 100GB 或高吞吐量时分片
- **数据导入**：`mongoimport --db test --collection users --file users.json`
- **工具生态**：MongoDB Compass（图形界面）、mongosh（命令行）、应用开发驱动
- **常见误区**：过度嵌入（文档大小限制 16MB）、忽略索引、未处理复制延迟

开发环境建议使用 Atlas M0 免费层级。使用 `mongoperf` 测试工作负载

## 参考资源

- [MongoDB 官方手册](https://www.mongodb.com/docs/manual/)
- [MongoDB 安装指南](https://www.mongodb.com/docs/manual/installation/)
- [MongoDB 核心概念](https://www.mongodb.com/docs/manual/core/)
- [MongoDB CRUD 操作](https://www.mongodb.com/docs/manual/crud/)
- [MongoDB 查询文档](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- [MongoDB 索引指南](https://www.mongodb.com/docs/manual/indexes/)
- [MongoDB 聚合框架](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)
- [MongoDB 模式设计](https://www.mongodb.com/docs/manual/core/data-model-design/)
- [MongoDB 复制机制](https://www.mongodb.com/docs/manual/replication/)
- [MongoDB 分片架构](https://www.mongodb.com/docs/manual/sharding/)
- [MongoDB 安全指南](https://www.mongodb.com/docs/manual/core/security/)
- [MongoDB 生产环境说明](https://www.mongodb.com/docs/manual/administration/production-notes/)
