---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Psycopg2 Python的PostgreSQL适配器
translated: true
type: note
---

**Psycopg2** 是一个流行的开源 PostgreSQL 数据库适配器（也称为驱动程序），适用于 Python 编程语言。它允许 Python 应用程序连接 PostgreSQL 数据库、执行 SQL 查询并高效处理数据。主要特性包括：

- 完全符合 Python DB API 2.0 规范
- 支持异步通知、服务器端游标和 COPY 操作
- 采用 C 语言编写以获得更好性能，可选二进制支持以实现更快的数据传输
- 广泛应用于生产环境，如 Web 开发、数据分析和 ETL 处理

这是 psycopg 库的第二代产品（因此命名为 "2"），虽然 psycopg3 是较新版本，但 psycopg2 仍为保持向后兼容性而稳定维护。

安装时可以使用 `pip install psycopg2-binary`（二进制版本对初学者更友好）。

[Psycopg 官方文档](https://www.psycopg.org/docs/)
[GeeksforGeeks 介绍](https://www.geeksforgeeks.org/python/introduction-to-psycopg2-module-in-python/)
[PyPI 软件包页面](https://pypi.org/project/psycopg2/)
