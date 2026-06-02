---
audio: false
generated: true
lang: zh
layout: post
title: Java SQL语句类型对比
translated: true
type: note
---

在 Java 的 `java.sql` 包中，`Statement`、`PreparedStatement` 和 `CallableStatement` 都是用于执行 SQL 查询的接口，但它们的用途和特性各不相同。以下是简明对比：

1. **Statement**：
   - **用途**：用于执行不带参数的静态 SQL 查询。
   - **工作原理**：将完整的 SQL 查询语句以字符串形式传递给 `executeQuery()` 或 `executeUpdate()` 方法。
   - **主要特性**：
     - 适用于简单的一次性查询。
     - 不支持参数绑定，需要手动将值拼接到 SQL 字符串中，存在 SQL 注入风险。
     - 重复查询效率较低，因为数据库每次都需要重新解析 SQL。
   - **示例**：

     ```java
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT * FROM users WHERE id = 1");
     ```

2. **PreparedStatement**：
   - **用途**：用于预编译的带参数 SQL 查询。
   - **工作原理**：通过占位符（`?`）定义查询语句，并使用 `setInt()`、`setString()` 等方法设置参数值。
   - **主要特性**：
     - 通过分离 SQL 逻辑与数据来防止 SQL 注入。
     - 对重复查询更高效，因为 SQL 只需编译一次即可重复使用。
     - 支持动态参数绑定，更安全灵活。
   - **示例**：

     ```java
     PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
     pstmt.setInt(1, 1);
     ResultSet rs = pstmt.executeQuery();
     ```

3. **CallableStatement**：
   - **用途**：用于执行数据库中的存储过程。
   - **工作原理**：继承 `PreparedStatement` 以处理存储过程调用，支持输入（`IN`）、输出（`OUT`）和输入输出（`IN OUT`）参数。
   - **主要特性**：
     - 专为数据库存储过程设计。
     - 支持通过 `registerOutParameter()` 等方法注册输出参数。
     - 支持存储过程逻辑的复杂参数处理。
   - **示例**：

     ```java
     CallableStatement cstmt = conn.prepareCall("{call getUserName(?, ?)}");
     cstmt.setInt(1, 1);
     cstmt.registerOutParameter(2, Types.VARCHAR);
     cstmt.execute();
     String username = cstmt.getString(2);
     ```

**核心区别**：

| 特性                   | Statement                          | PreparedStatement                  | CallableStatement                 |
|------------------------|------------------------------------|------------------------------------|------------------------------------|
| **用途**               | 静态 SQL 查询                     | 参数化 SQL 查询                   | 存储过程执行                     |
| **SQL 注入防护**       | 存在风险（手动拼接）              | 安全（参数绑定）                  | 安全（参数绑定）                  |
| **性能**               | 较低（无预编译）                  | 较高（预编译）                    | 存储过程场景高效                 |
| **适用场景**           | 简单一次性查询                    | 重复或参数化查询                  | 带参数的存储过程调用             |
| **参数支持**           | 无                                | 仅输入参数                        | 输入、输出及输入输出参数         |

**使用场景建议**：

- 对安全性、性能要求不高的简单非重复查询可使用 `Statement`。
- 需要参数化查询、重复执行或防范 SQL 注入时建议使用 `PreparedStatement`。
- 当调用含输入输出参数的数据库存储过程时需使用 `CallableStatement`。

以上说明基于当前 Java SQL API 的标准行为。如需更多细节或示例，欢迎进一步探讨！
