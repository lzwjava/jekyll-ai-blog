---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: IBM Db2 系统目录概览
translated: true
type: note
---

### IBM Db2 系统表简介

IBM Db2 中的系统目录（也称为 Db2 目录）是一个内置的元数据存储库，用于存储数据库中每个对象和元素的详细信息。这包括表、视图、索引、列、用户、权限、例程等。它本质上是数据库的"电话簿"——当您创建、修改或删除对象时，由 Db2 自动维护。该目录帮助数据库管理员（DBA）、开发人员和工具查询数据库的结构和状态，而无需解析应用程序代码或外部文件。

与常规用户表不同，系统目录对大多数用户是只读的，并针对元数据查询而非高容量数据操作进行了优化。它在创建新数据库时自动创建，并驻留在特殊的表空间中（如 Db2 LUW 中的 SYSCATSPACE）。

#### 关键组件和结构
系统目录包括：
- **基表**：这些是存储原始元数据的底层规范化表。它们位于 **SYSIBM** 模式中，最终用户无法直接查询，以防止意外修改或性能问题。例如 SYSIBM.SYSTABLES（基本表信息）和 SYSIBM.SYSCOLUMNS（列详细信息）。
- **目录视图**：基于基表构建的用户友好型非规范化视图。这些视图更易于查询，并提供符合 SQL 标准（如 ISO）的标准化接口。它们按模式分组：
  - **SYSCAT**：关于数据库对象的核心元数据（例如表、索引、触发器）。
  - **SYSCOLUMNS**：详细的列级信息。
  - **SYSSTAT**：查询优化器使用的统计数据（例如行数、基数）。
  - **SYSPROC** 和其他：用于过程、函数和 XML 相关信息。

在 Db2 for z/OS 中，目录位于数据库 DSNDB06 中，但概念在不同平台（LUW、z/OS、i）上是相似的。

#### 用途
- **发现**：了解存在哪些对象、它们的属性和关系。
- **管理**：监控权限、依赖关系和性能统计信息。
- **开发**：生成 DDL 脚本、验证模式或与 Db2 Data Studio 等工具集成。
- **优化**：查询优化器使用 SYSSTAT 视图来选择执行计划。

#### 如何访问和查询
1. **连接到数据库**：使用 `db2 connect to <dbname>`。
2. **权限**：默认情况下，PUBLIC 对目录视图具有 SELECT 权限。基本查询不需要特殊授权，但 SYSIBM 基表需要 SYSADM 或更高权限。
3. **查询**：使用标准 SQL SELECT 语句。视图是模式限定的（例如 `SELECT * FROM SYSCAT.TABLES`）。

**示例查询**：
- **列出当前模式中的所有表**：
  ```
  SELECT TABSCHEMA, TABNAME, TYPE FROM SYSCAT.TABLES
  WHERE TABSCHEMA = CURRENT SCHEMA;
  ```
  - 输出：显示模式、表名和类型（例如 'T' 表示表，'V' 表示视图）。

- **获取表的列详细信息**：
  ```
  SELECT COLNAME, TYPENAME, LENGTH, NULLS
  FROM SYSCOLUMNS
  WHERE TABSCHEMA = 'YOUR_SCHEMA' AND TABNAME = 'YOUR_TABLE';
  ```
  - 输出：列名、数据类型、长度和可空性。

- **检查表统计信息**：
  ```
  SELECT CARD, NPAGES FROM SYSSTAT.TABLES
  WHERE TABNAME = 'YOUR_TABLE';
  ```
  - CARD：估计的行数；NPAGES：页数。

要获取完整列表，请运行 `SELECT * FROM SYSCAT.VIEWS WHERE VIEWNAME LIKE 'SYSCAT%'` 以发现所有可用视图。

#### 重要注意事项
- **性能**：目录查询速度很快，但在大型数据库上可能消耗大量资源；使用过滤器（例如 WHERE 子句）来限制结果。
- **更新**：Db2 自动更新目录——不要尝试手动 INSERT/UPDATE。
- **版本差异**：在 Db2 11.5+ 中，视图更加标准化。对于 z/OS，某些视图具有平台特定的列。
- **工具集成**：使用 Db2 的 `db2look` 命令从目录数据生成 DDL：`db2look -d <dbname> -t <table>`。
- 除非您是系统管理员，否则避免直接访问基表，因为这可能导致不一致。

要进行更深入的了解，请查阅官方文档或在测试数据库中实验。

#### 参考资料
- [Db2 目录概述](https://www.ibm.com/docs/en/db2-for-zos/12?topic=objects-db2-catalog)
- [Db2 LUW 中的系统目录视图](https://www.ibm.com/docs/en/db2/11.5?topic=views-system-catalog)
- [从 DB2 系统目录获取有用信息](https://developer.ibm.com/articles/dm-0411melnyk/)
