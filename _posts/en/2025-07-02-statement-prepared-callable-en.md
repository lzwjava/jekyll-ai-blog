---
audio: false
generated: true
lang: en
layout: post
title: Java SQL Statement Types Compared
translated: false
type: note
---

In Java's `java.sql` package, `Statement`, `PreparedStatement`, and `CallableStatement` are interfaces used to execute SQL queries, but they serve different purposes and have distinct characteristics. Here's a concise comparison:

1. **Statement**:
   - **Purpose**: Used to execute static SQL queries without parameters.
   - **How it works**: You pass a complete SQL query as a string to the `executeQuery()` or `executeUpdate()` method.
   - **Key Characteristics**:
     - Suitable for simple, one-off queries.
     - No parameter binding, so you manually concatenate values into the SQL string, which can lead to SQL injection risks.
     - Less efficient for repeated queries, as the database re-parses the SQL each time.
   - **Example**:
     ```java
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT * FROM users WHERE id = 1");
     ```

2. **PreparedStatement**:
   - **Purpose**: Used for precompiled SQL queries with parameterized inputs.
   - **How it works**: You define a query with placeholders (`?`) and set parameter values using methods like `setInt()`, `setString()`, etc.
   - **Key Characteristics**:
     - Prevents SQL injection by separating SQL logic from data.
     - More efficient for repeated queries, as the SQL is compiled once and reused.
     - Supports dynamic parameter binding, making it safer and more flexible.
   - **Example**:
     ```java
     PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
     pstmt.setInt(1, 1);
     ResultSet rs = pstmt.executeQuery();
     ```

3. **CallableStatement**:
   - **Purpose**: Used to execute stored procedures in the database.
   - **How it works**: Extends `PreparedStatement` to handle stored procedure calls, supporting input (`IN`), output (`OUT`), and input/output (`IN OUT`) parameters.
   - **Key Characteristics**:
     - Designed specifically for database stored procedures.
     - Allows registration of output parameters using methods like `registerOutParameter()`.
     - Supports complex parameter handling for stored procedure logic.
   - **Example**:
     ```java
     CallableStatement cstmt = conn.prepareCall("{call getUserName(?, ?)}");
     cstmt.setInt(1, 1);
     cstmt.registerOutParameter(2, Types.VARCHAR);
     cstmt.execute();
     String username = cstmt.getString(2);
     ```

**Key Differences**:
| Feature                | Statement                          | PreparedStatement                  | CallableStatement                 |
|------------------------|------------------------------------|------------------------------------|------------------------------------|
| **Purpose**            | Static SQL queries                | Parameterized SQL queries         | Stored procedure execution        |
| **SQL Injection**      | Vulnerable (manual concatenation) | Safe (parameter binding)          | Safe (parameter binding)          |
| **Performance**        | Less efficient (no precompilation)| More efficient (precompiled)      | Efficient for stored procedures   |
| **Use Case**           | Simple, one-time queries          | Repeated or parameterized queries | Stored procedures with parameters|
| **Parameter Support**  | None                              | Input parameters only             | Input, output, and IN/OUT params |

**When to Use**:
- Use `Statement` for simple, non-repetitive queries where security and performance are less critical.
- Use `PreparedStatement` for parameterized queries, repetitive execution, or when security (SQL injection prevention) is a concern.
- Use `CallableStatement` when invoking database stored procedures with input/output parameters.

This explanation is based on standard Java SQL API behavior as of my knowledge cutoff. If you need further details or examples, let me know!
