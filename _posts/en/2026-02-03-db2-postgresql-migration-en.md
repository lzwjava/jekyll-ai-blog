---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DB2 to PostgreSQL Migration Guide
translated: false
type: note
---

Question: If we change from DB2 to PostgreSQL, how to migrate, and would it be costly? What to consider for stored procedures, SQL, etc., and the Java JDBC driver?

Answer: 

Migrating from **IBM DB2** (typically DB2 LUW) to **PostgreSQL** is a common heterogeneous database migration that can bring significant long-term savings, primarily due to eliminating DB2's licensing and maintenance costs. However, the migration itself can be moderately to highly costly depending on your database complexity, especially if you heavily use stored procedures, DB2-specific SQL features, or have a large codebase.

### Is It Costly?
- **Short-term costs** — Often yes, due to assessment, schema/data conversion, code changes, testing, and potential downtime. Costs include developer/DBA time, possible commercial tools (e.g., Ispirer Toolkit, AWS SCT), and testing environments.
- **Long-term** — Usually **much cheaper**. PostgreSQL is free/open-source with no licensing fees (unlike DB2's PVU or per-user models), lower operational costs, and strong performance in many workloads. Many organizations report substantial savings after migration.

The total cost depends on:
- Database size (e.g., data volume, number of objects).
- Number/complexity of stored procedures and functions.
- Application code dependencies on DB2-specific features.
- Whether you do it in-house or use consultants/tools.

Simple migrations (mostly tables + basic SQL) can be low-cost; complex ones with hundreds of stored procedures can require significant effort (weeks to months).

### How to Migrate (Main Steps)
1. **Assessment & Planning**  
   Analyze schema, data types, stored procedures, triggers, functions, views, and application SQL for incompatibilities. Estimate effort and cost. Tools like AWS Schema Conversion Tool (SCT) can generate a migration assessment report.

2. **Schema Conversion**  
   Convert DB2 DDL to PostgreSQL-compatible DDL. Key differences include:
   - Data types: DB2 DECIMAL → PostgreSQL NUMERIC; some DB2-specific types need mapping.
   - Sequences vs. identity columns.
   - DB2 uses `SYSIBM.SYSDUMMY1` for dummy selects; PostgreSQL uses `SELECT ...` without FROM or `generate_series`.
   - Case sensitivity and identifier quoting rules differ slightly.

   Tools: AWS SCT (free for AWS users), db2topg (open-source), Ispirer Toolkit (commercial, high automation), or manual adjustment.

3. **Stored Procedures & Functions**  
   This is usually the **most expensive and time-consuming** part.
   - DB2 uses SQL PL (similar to PL/SQL).
   - PostgreSQL uses **PL/pgSQL** (similar syntax but not identical).
   - Many DB2 stored procedures must be rewritten as PostgreSQL functions (PostgreSQL doesn't have true "stored procedures" like DB2; use functions returning void or refcursor).
   - Cursors, handlers (exception handling), dynamic SQL, and output parameters often need adjustment.
   - Automation tools (Ispirer, AWS SCT) can convert 70–90% automatically in good cases, but complex logic (e.g., handlers, cursors returning result sets) frequently needs manual fixes.
   - Triggers also need rewriting (DB2 `MODE DB2SQL` → PL/pgSQL `EXECUTE FUNCTION`).

4. **Application SQL Queries**  
   Most standard ANSI SQL works fine, but watch for:
   - DB2-specific functions (e.g., `RAND()` → `RANDOM()`).
   - `FETCH FIRST n ROWS ONLY` (compatible, but syntax nuances).
   - Date/time handling, string functions, and implicit type casts.
   - Applications may need query adjustments or use an abstraction layer (e.g., JPA/Hibernate can help reduce changes).

5. **Data Migration**  
   - One-time full load: Use DB2 `EXPORT` to delimited files → PostgreSQL `COPY`.
   - Minimal downtime: Tools like AWS DMS (Database Migration Service) support ongoing replication (CDC) from DB2 to PostgreSQL.
   - Validate row counts, sums, and sample data post-migration.

6. **Java JDBC Driver Considerations**  
   - Switch from **IBM DB2 JDBC driver** (e.g., `com.ibm.db2.jcc.DB2Driver`) to **PostgreSQL JDBC driver** (`org.postgresql.Driver`).
   - URL changes:  
     DB2: `jdbc:db2://host:port/dbname`  
     PostgreSQL: `jdbc:postgresql://host:port/dbname`
   - Most standard JDBC code (PreparedStatement, ResultSet, transactions) works similarly.
   - Minor differences may appear in:
     - Handling of large objects (LOBs).
     - Certain data type mappings (e.g., DB2 DECFLOAT → PostgreSQL numeric).
     - Error codes/messages.
     - Connection pooling properties.
   - If using ORM (Hibernate, Spring Data JPA), update dialect (`org.hibernate.dialect.PostgreSQLDialect`) and driver dependency; many changes become automatic.

7. **Testing & Cutover**  
   - Unit/integration tests for procedures and app queries.
   - Performance testing (PostgreSQL tuning often needed).
   - Parallel run or shadow testing if possible.
   - Cutover with minimal downtime using replication tools.

### Recommendations
- Start with a proof-of-concept on a subset of your schema.
- Use automation tools to reduce manual work.
- If on AWS, consider AWS SCT + DMS for a streamlined path to Aurora PostgreSQL.
- Budget extra time for stored procedures—they're often the biggest hidden cost.

Overall, while not trivial, DB2 → PostgreSQL migrations are very feasible and frequently worthwhile for cost savings and open-source benefits.

References:  

- [Migrating from DB2 to PostgreSQL - What You Should Know](https://severalnines.com/blog/migrating-db2-postgresql-what-you-should-know)
- [DB2 UDB To PostgreSQL Conversion Guide](https://wiki.postgresql.org/images/d/d1/DB2UDB-to-PG.pdf)
- [Migrate DB2 LUW to PostgreSQL - Ispirer](https://www.ispirer.com/products/db2-luw-to-postgresql-migration)
- [Migrate IBM Db2 LUW to Amazon Aurora PostgreSQL or Amazon RDS for PostgreSQL](https://aws.amazon.com/blogs/database/migrate-ibm-db2-luw-to-amazon-aurora-postgresql-or-amazon-rds-for-postgresql/)