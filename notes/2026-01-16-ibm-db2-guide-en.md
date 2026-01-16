---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IBM Db2 Privileges and Authorities Guide
translated: false
type: note
---

**Question:** What privileges does DB2 have, such as EXECUTE, SELECT, etc.?

**Answer:** 

IBM Db2 (primarily referring to **Db2 for Linux, UNIX, and Windows (LUW)**, the most common modern version) supports a variety of **privileges** and **authorities**. Privileges are typically granted on specific objects (tables, views, schemas, packages, etc.) using the `GRANT` statement, while authorities are higher-level permissions (often database- or instance-wide).

### Common Object-Level Privileges
These are the most frequently used privileges on tables, views, nicknames, etc.:

- **SELECT** — Read data from a table or view.
- **INSERT** — Add new rows to a table.
- **UPDATE** — Modify existing rows (optionally on specific columns).
- **DELETE** — Remove rows from a table.
- **REFERENCES** — Create foreign keys referencing the table (or specific columns).
- **INDEX** — Create indexes on the table.
- **CONTROL** — Full control over the object, including the ability to drop it and grant/revoke privileges on it (WITH GRANT OPTION is automatic with CONTROL).
- **ALL** — Grants all applicable privileges at once (e.g., `GRANT ALL ON table TO user` typically includes SELECT, INSERT, UPDATE, DELETE, etc.).

Example:
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON schema.table_name TO user_name;
```

### Privileges on Other Objects
- **EXECUTE** — On stored procedures, functions, methods, packages, or modules (very common for calling routines).
- **BIND** — Bind or rebind a package.
- **USAGE** — On workloads, modules, sequences, etc.
- Schema privileges: **CREATEIN**, **ALTERIN**, **DROPIN** (allow creating/altering/dropping objects in a schema).

### Database-Level Authorities (Higher-Level)
These are granted at the database level and often include multiple implicit privileges:
- **CONNECT** — Connect to the database.
- **CREATETAB** — Create tables.
- **BINDADD** — Create packages.
- **IMPLICIT_SCHEMA** — Create schemas implicitly.
- **LOAD** — Perform LOAD operations.
- **ACCESSCTRL** — Grant/revoke most object privileges.
- **DATAACCESS** — Grants SELECT, INSERT, UPDATE, DELETE on all tables/views.
- **DBADM** — Database administrator (broad powers, including most grants).
- **SECADM** — Security administrator (manages privileges and roles).
- **WLMADM** — Manage workloads.
- **SQLADM** — Manage SQL performance objects.

Higher instance-level authorities include:
- **SYSADM** — Highest level (instance-wide).
- **SYSCTRL** — System control.
- **SYSMAINT** — System maintenance.

### WITH GRANT OPTION
As in your example (`GRANT SELECT ON object_name TO user_name WITH GRANT OPTION`), this allows the recipient to further grant the same privilege to others.

Db2 for z/OS has some differences (e.g., more use of primary/secondary auth IDs and different authority names like PACKADM), but core object privileges like SELECT, INSERT, UPDATE, DELETE, EXECUTE are similar.

For the exact syntax and full list in your specific Db2 version/edition, refer to the official IBM Db2 documentation (SQL Reference → GRANT statement).

**References:**  

- [IBM Db2 Documentation - GRANT (table or view privileges)](https://www.ibm.com/docs/en/db2/11.5?topic=statements-grant-table-view-privileges)
- [IBM Db2 Documentation - Authorization, privileges and object ownership](https://www.ibm.com/docs/en/db2/11.5?topic=model-authorization-privileges-object-ownership)
- [IBM Db2 Documentation - GRANT (package privileges)](https://www.ibm.com/docs/en/db2/11.5?topic=statements-grant-package-privileges)