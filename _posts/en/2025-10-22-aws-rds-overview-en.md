---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: AWS Relational Database Services Overview
translated: false
type: note
---

### Relational Databases on AWS

AWS provides several managed services for relational databases, with **Amazon Relational Database Service (RDS)** being the primary offering. It handles setup, patching, backups, and scaling for various popular database engines. Additionally, **Amazon Aurora** is a high-performance, MySQL- and PostgreSQL-compatible relational database built into RDS.

Here's a summary of the key relational database options on AWS:

| Service/Engine | Description | Use Cases |
|---------------|-------------|-----------|
| **Amazon RDS for PostgreSQL** | Fully managed PostgreSQL, supporting advanced features like JSONB and full-text search. | Transactional applications, web apps, and analytics. |
| **Amazon RDS for MySQL** | Managed MySQL with high availability and read replicas. | E-commerce, content management, and general-purpose apps. |
| **Amazon RDS for MariaDB** | Fork of MySQL with enhanced performance and storage engines. | Web applications and read-heavy workloads. |
| **Amazon RDS for SQL Server** | Microsoft SQL Server with editions like Standard, Enterprise, and Web. | Enterprise apps, BI, and Windows-based systems. |
| **Amazon RDS for Oracle** | Oracle Database with BYOL (Bring Your Own License) or license-included options. | Mission-critical enterprise applications. |
| **Amazon RDS for Db2** | IBM Db2 with support for LUW (Linux, UNIX, Windows). | Large-scale transactional and analytical workloads. |
| **Amazon Aurora (MySQL-compatible)** | Cloud-native relational DB with up to 5x faster performance than standard MySQL. | High-throughput OLTP and global apps. |
| **Amazon Aurora (PostgreSQL-compatible)** | PostgreSQL-compatible with serverless options and auto-scaling storage. | Scalable apps requiring ACID compliance and high availability. |

For data warehousing (OLAP-focused relational workloads), AWS also offers **Amazon Redshift**, a fully managed, petabyte-scale data warehouse based on PostgreSQL.

These services integrate seamlessly with other AWS tools like EC2, Lambda, and S3. To get started, check the [AWS RDS documentation](https://aws.amazon.com/rds/) or [AWS Database Services overview](https://docs.aws.amazon.com/databases-on-aws-how-to-choose/).
