---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AWS关系型数据库服务概览
translated: true
type: note
---

### AWS 上的关系型数据库

AWS 提供了多种托管式关系数据库服务，其中**Amazon 关系型数据库服务 (RDS)** 是核心产品。它负责各类主流数据库引擎的配置、补丁安装、备份和扩展。此外，**Amazon Aurora** 是一款内置于 RDS 的高性能关系型数据库，兼容 MySQL 和 PostgreSQL。

以下是 AWS 上主要关系型数据库选项的概要：

| 服务/引擎 | 描述 | 适用场景 |
|---------------|-------------|-----------|
| **Amazon RDS for PostgreSQL** | 全托管式 PostgreSQL，支持 JSONB 和全文检索等高级功能 | 事务型应用、Web 应用及分析系统 |
| **Amazon RDS for MySQL** | 具备高可用性和只读副本的托管式 MySQL | 电子商务、内容管理系统及通用应用程序 |
| **Amazon RDS for MariaDB** | MySQL 分支版本，具有增强性能和存储引擎 | Web 应用程序及读密集型工作负载 |
| **Amazon RDS for SQL Server** | 支持标准版、企业版和 Web 版的 Microsoft SQL Server | 企业应用、商业智能及基于 Windows 的系统 |
| **Amazon RDS for Oracle** | 支持自带许可 (BYOL) 或含许可选项的 Oracle 数据库 | 关键任务型企业应用程序 |
| **Amazon RDS for Db2** | 支持 LUW (Linux, UNIX, Windows) 的 IBM Db2 | 大规模事务处理和分析工作负载 |
| **Amazon Aurora (MySQL 兼容版)** | 云原生关系数据库，性能最高可达标准 MySQL 的 5 倍 | 高吞吐量 OLTP 及全球化应用 |
| **Amazon Aurora (PostgreSQL 兼容版)** | 兼容 PostgreSQL，支持无服务器选项和自动扩展存储 | 需要 ACID 合规性和高可用性的可扩展应用 |

针对数据仓库场景（侧重 OLAP 的关系型工作负载），AWS 还提供基于 PostgreSQL 的完全托管 PB 级数据仓库服务 **Amazon Redshift**。

这些服务可与 EC2、Lambda 和 S3 等其他 AWS 工具无缝集成。如需快速入门，请查阅 [AWS RDS 文档](https://aws.amazon.com/rds/) 或 [AWS 数据库服务概览](https://docs.aws.amazon.com/databases-on-aws-how-to-choose/)。
