---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DB2 迁移至 PostgreSQL 指南
translated: true
type: note
---

Question: 如果我们将数据库从 DB2 迁移到 PostgreSQL，应该如何操作？成本高吗？关于 Stored Procedures、SQL 以及 Java JDBC Driver 有哪些注意事项？

Answer:

将 **IBM DB2**（通常是 DB2 LUW）迁移到 **PostgreSQL** 是一种常见的异构数据库迁移，主要是由于消除了 DB2 的 Licensing 和维护费用，从长远来看可以大幅节省成本。然而，迁移本身可能会产生中到高的成本，这取决于数据库的复杂度，特别是如果你大量使用了 Stored Procedures、DB2 特有的 SQL 特性，或者拥有庞大的代码库。

### 成本是否高昂？

- **短期成本** — 通常较高，涉及评估、Schema/数据转换、代码修改、测试以及潜在的 Downtime。成本包括 Developer/DBA 的时间、可能用到的商业工具（如 Ispirer Toolkit、AWS SCT）以及测试环境的构建。
- **长期成本** — 通常**便宜得多**。PostgreSQL 是开源免费的，没有 Licensing 费用（不像 DB2 的 PVU 或按用户授权模式），运营成本更低，且在许多 Workload 下性能表现强劲。许多机构在迁移后报告了可观的资金节省。

总成本取决于：

- 数据库规模（如数据量、Object 数量）。
- Stored Procedures 和 Functions 的数量及复杂度。
- 应用程序代码对 DB2 特定特性的依赖程度。
- 是通过内部团队完成还是聘请咨询公司/使用第三方工具。

简单的迁移（主要为 Table + 基础 SQL）成本较低；而拥有数百个 Stored Procedures 的复杂迁移可能需要投入大量精力（数周到数月）。

### 如何迁移（主要步骤）

1. **评估与规划 (Assessment & Planning)**
   分析 Schema、Data types、Stored Procedures、Triggers、Functions、Views 以及应用程序 SQL 的不兼容性。估算工作量和成本。AWS Schema Conversion Tool (SCT) 等工具可以生成迁移评估报告。

2. **Schema 转换**
   将 DB2 DDL 转换为 PostgreSQL 兼容的 DDL。关键差异包括：
   - Data types：DB2 DECIMAL → PostgreSQL NUMERIC；某些 DB2 特有的类型需要映射。
   - Sequences vs. Identity Columns。
   - DB2 使用 `SYSIBM.SYSDUMMY1` 进行虚拟查询；PostgreSQL 使用不带 FROM 的 `SELECT ...` 或 `generate_series`。
   - 大小写敏感度和 Identifier 引号规则略有不同。

   工具：AWS SCT（对 AWS 用户免费）、db2topg（开源）、Ispirer Toolkit（商业，自动化程度高）或手动调整。

3. **Stored Procedures & Functions**
   这通常是**最昂贵且最耗时**的部分。
   - DB2 使用 SQL PL（类似于 PL/SQL）。
   - PostgreSQL 使用 **PL/pgSQL**（语法相似但不完全相同）。
   - 许多 DB2 Stored Procedures 必须重写为 PostgreSQL Functions（PostgreSQL 过去不像 DB2 拥有真正的 "Stored Procedures"，通常使用返回 void 或 refcursor 的 Functions）。
   - Cursors、Handlers（异常处理）、Dynamic SQL 和 Output Parameters 经常需要调整。
   - 自动化工具（Ispirer, AWS SCT）在理想情况下可以自动转换 70–90%，但复杂的逻辑（如 Handlers、返回结果集的 Cursors）往往需要手动修正。
   - Triggers 也需要重写（DB2 `MODE DB2SQL` → PL/pgSQL `EXECUTE FUNCTION`）。

4. **应用程序 SQL 查询**
   大多数标准 ANSI SQL 运行良好，但需注意：
   - DB2 特有的 Functions（例如 `RAND()` → `RANDOM()`）。
   - `FETCH FIRST n ROWS ONLY`（虽然兼容，但有语法细微差别）。
   - Date/time 处理、String 函数和隐式类型转换 (Implicit type casts)。
   - 应用程序可能需要调整查询，或使用抽象层（如 JPA/Hibernate 可以减少改动）。

5. **数据迁移 (Data Migration)**
   - 一次性全量加载：使用 DB2 `EXPORT` 到分隔符文件 → PostgreSQL `COPY`。
   - 最小化停机时间：AWS DMS (Database Migration Service) 等工具支持从 DB2 到 PostgreSQL 的增量同步 (CDC)。
   - 迁移后验证 Row counts、Sums 和样本数据。

6. **Java JDBC Driver 注意事项**
   - 从 **IBM DB2 JDBC driver**（如 `com.ibm.db2.jcc.DB2Driver`）切换到 **PostgreSQL JDBC driver** (`org.postgresql.Driver`)。
   - URL 变化：
     DB2: `jdbc:db2://host:port/dbname`
     PostgreSQL: `jdbc:postgresql://host:port/dbname`
   - 大多数标准 JDBC 代码（PreparedStatement, ResultSet, Transactions）工作方式相似。
   - 微小差异可能出现在：
     - Large Objects (Lobs) 的处理。
     - 特定数据类型映射（如 DB2 DECFLOAT → PostgreSQL NUMERIC）。
     - Error codes/messages（错误代码）。
     - Connection Pooling（连接池）属性。
   - 如果使用 ORM（Hibernate, Spring Data JPA），更新 Dialect (`org.hibernate.dialect.PostgreSQLDialect`) 和 Driver 依赖；许多更改会自动完成。

7. **测试与切换**
   - 对 Procedures 和应用查询进行单元/集成测试。
   - 性能测试（通常需要对 PostgreSQL 进行 Tuning）。
   - 如果可能，进行并行运行或 Shadow Testing。
   - 使用同步工具实现最小 Downtime 切换。

### 建议

- 从 Schema 的一个子集开始进行 Proof-of-concept (PoC)。
- 使用自动化工具减少手动工作。
- 如果在 AWS 上，考虑使用 AWS SCT + DMS 以简化迁移到 Aurora PostgreSQL 的路径。
- 为 Stored Procedures 预留额外的预算和时间——它们通常是最大的隐藏成本。

总的来说，虽然并非易事，但从 DB2 迁移到 PostgreSQL 是非常可行的，且为了节省成本和享受开源生态利好，这通常是值得的。

参考资料：

- [Migrating from DB2 to PostgreSQL - What You Should Know](https://severalnines.com/blog/migrating-db2-postgresql-what-you-should-know)
- [DB2 UDB To PostgreSQL Conversion Guide](https://wiki.postgresql.org/images/d/d1/DB2UDB-to-PG.pdf)
- [Migrate DB2 LUW to PostgreSQL - Ispirer](https://www.ispirer.com/products/db2-luw-to-postgresql-migration)
- [Migrate IBM Db2 LUW to Amazon Aurora PostgreSQL or Amazon RDS for PostgreSQL](https://aws.amazon.com/blogs/database/migrate-ibm-db2-luw-to-amazon-aurora-postgresql-or-amazon-rds-for-postgresql/)
