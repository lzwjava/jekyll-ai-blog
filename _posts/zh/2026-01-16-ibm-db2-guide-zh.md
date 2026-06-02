---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: IBM Db2 权限与特权指南
translated: true
type: note
---

**Question:** DB2 有哪些权限，例如 EXECUTE、SELECT 等？

**Answer:**

IBM Db2（主要指 **Db2 for Linux, UNIX, and Windows (LUW)**，这是最常见的现代版本）支持多种 **privileges**（权限）和 **authorities**（管理特权）。Privileges 通常通过 `GRANT` 语句授予特定对象（tables、views、schemas、packages 等），而 authorities 是更高级别的权限（通常针对整个 database 或 instance）。

### Common Object-Level Privileges
这些是针对 tables、views、nicknames 等最常用的权限：

- **SELECT** — 从 table 或 view 中读取数据。
- **INSERT** — 向 table 中添加新行。
- **UPDATE** — 修改现有行（可选针对特定列）。
- **DELETE** — 从 table 中删除行。
- **REFERENCES** — 创建引用该 table（或特定列）的外键（foreign keys）。
- **INDEX** — 在 table 上创建索引。
- **CONTROL** — 对对象的完全控制权，包括删除（drop）对象以及授予/撤销（grant/revoke）该对象权限的能力（CONTROL 权限自动包含 WITH GRANT OPTION）。
- **ALL** — 一次性授予所有适用的权限（例如，`GRANT ALL ON table TO user` 通常包括 SELECT、INSERT、UPDATE、DELETE 等）。

示例：
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON schema.table_name TO user_name;
```

### Privileges on Other Objects
- **EXECUTE** — 针对 stored procedures、functions、methods、packages 或 modules（常用于调用 routine）。
- **BIND** — 绑定或重新绑定 package。
- **USAGE** — 针对 workloads、modules、sequences 等。
- Schema 权限：**CREATEIN**、**ALTERIN**、**DROPIN**（允许在 schema 中创建/修改/删除对象）。

### Database-Level Authorities (Higher-Level)
这些在 database 级别授予，通常包含多个隐式权限：
- **CONNECT** — 连接到 database。
- **CREATETAB** — 创建 tables。
- **BINDADD** — 创建 packages。
- **IMPLICIT_SCHEMA** — 隐式创建 schemas。
- **LOAD** — 执行 LOAD 操作。
- **ACCESSCTRL** — 授予/撤销大多数对象权限。
- **DATAACCESS** — 授予对所有 tables/views 的 SELECT、INSERT、UPDATE、DELETE 权限。
- **DBADM** — Database 管理员（拥有广泛权力，包括大多数授权操作）。
- **SECADM** — 安全管理员（管理权限和 roles）。
- **WLMADM** — 管理 workloads。
- **SQLADM** — 管理 SQL 性能对象。

更高级别的 instance-level authorities 包括：
- **SYSADM** — 最高级别（instance 范围）。
- **SYSCTRL** — 系统控制。
- **SYSMAINT** — 系统维护。

### WITH GRANT OPTION
正如你的例子中提到的（`GRANT SELECT ON object_name TO user_name WITH GRANT OPTION`），这允许接收者进一步将相同的权限授予他人。

Db2 for z/OS 存在一些差异（例如，更多地使用 primary/secondary auth IDs 以及不同的 authority 名称如 PACKADM），但核心的对象权限如 SELECT、INSERT、UPDATE、DELETE、EXECUTE 是相似的。

有关你所使用的特定 Db2 版本/版本的确切语法和完整列表，请参阅官方 IBM Db2 文档（SQL Reference → GRANT statement）。

**References:**

- [IBM Db2 Documentation - GRANT (table or view privileges)](https://www.ibm.com/docs/en/db2/11.5?topic=statements-grant-table-view-privileges)
- [IBM Db2 Documentation - Authorization, privileges and object ownership](https://www.ibm.com/docs/en/db2/11.5?topic=model-authorization-privileges-object-ownership)
- [IBM Db2 Documentation - GRANT (package privileges)](https://www.ibm.com/docs/en/db2/11.5?topic=statements-grant-package-privileges)
