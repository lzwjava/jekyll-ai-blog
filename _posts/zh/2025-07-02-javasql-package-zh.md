---
audio: false
generated: true
lang: zh
layout: post
title: Java数据库连接SQL指南
translated: true
type: note
---

`java.sql` 包是 **Java JDBC API（Java 数据库连接）的核心组成部分**，使 Java 应用程序能够与 MySQL、PostgreSQL、Oracle、SQL Server 等关系型数据库进行交互。它提供了**连接数据库、执行 SQL 查询和检索结果**所需的接口和类。

---

## 📘 **`java.sql` 概述**

`java.sql` 包包含的类和接口可用于：

* 连接数据库（`DriverManager`、`Connection`）
* 执行 SQL 查询（`Statement`、`PreparedStatement`、`CallableStatement`）
* 处理结果（`ResultSet`）
* 处理元数据（`DatabaseMetaData`、`ResultSetMetaData`）
* 管理事务
* 处理 SQL 异常（`SQLException`）

---

## 🔧 **设置：所需准备**

### 1. **JDBC 驱动程序**

* 您需要目标数据库的 JDBC 驱动程序（例如，MySQL：`mysql-connector-java`，PostgreSQL：`postgresql`）。
* 您可以通过 Maven/Gradle 包含它，或手动添加 `.jar` 文件。

### 2. **数据库 URL**

每个 JDBC 驱动程序都有其连接 URL 格式：

```java
jdbc:mysql://localhost:3306/mydatabase
jdbc:postgresql://localhost:5432/mydatabase
```

---

## 🧩 **关键类和接口**

### 🔌 1. `DriverManager`

建立与数据库的连接。

```java
Connection conn = DriverManager.getConnection(url, user, password);
```

### 🧵 2. `Connection`

表示与数据库的会话。

* 创建 `Statement` 或 `PreparedStatement`
* 管理事务（提交、回滚）
* 关闭连接

```java
Connection conn = DriverManager.getConnection(...);
conn.setAutoCommit(false);  // 用于手动事务控制
```

### 📤 3. `Statement` / `PreparedStatement` / `CallableStatement`

#### `Statement`

用于执行静态 SQL 查询。

```java
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM users");
```

#### `PreparedStatement`

用于执行参数化查询。避免 SQL 注入。

```java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, 101);
ResultSet rs = ps.executeQuery();
```

#### `CallableStatement`

用于存储过程。

```java
CallableStatement cs = conn.prepareCall("{call getUser(?)}");
cs.setInt(1, 5);
ResultSet rs = cs.executeQuery();
```

### 📥 4. `ResultSet`

保存查询结果。

```java
while (rs.next()) {
    int id = rs.getInt("id");
    String name = rs.getString("name");
}
```

### 📚 5. 元数据

* `DatabaseMetaData`：数据库信息
* `ResultSetMetaData`：结果列信息

```java
DatabaseMetaData dbMeta = conn.getMetaData();
ResultSetMetaData rsMeta = rs.getMetaData();
```

---

## 🧪 **基础示例**

```java
import java.sql.*;

public class JdbcExample {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/testdb";
        String user = "root";
        String password = "password";

        try (Connection conn = DriverManager.getConnection(url, user, password)) {
            String sql = "SELECT * FROM users WHERE age > ?";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setInt(1, 18);

            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                System.out.println(rs.getInt("id") + " - " + rs.getString("name"));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

---

## 🔁 **事务**

```java
conn.setAutoCommit(false);  // 禁用自动提交

try {
    PreparedStatement ps1 = conn.prepareStatement("UPDATE accounts SET balance = balance - ? WHERE id = ?");
    ps1.setDouble(1, 100.0);
    ps1.setInt(2, 1);
    ps1.executeUpdate();

    PreparedStatement ps2 = conn.prepareStatement("UPDATE accounts SET balance = balance + ? WHERE id = ?");
    ps2.setDouble(1, 100.0);
    ps2.setInt(2, 2);
    ps2.executeUpdate();

    conn.commit(); // 提交事务

} catch (SQLException ex) {
    conn.rollback(); // 出错时回滚
}
```

---

## ❗ **异常处理**

```java
try {
    // 数据库代码
} catch (SQLException ex) {
    System.err.println("Error Code: " + ex.getErrorCode());
    System.err.println("SQL State: " + ex.getSQLState());
    ex.printStackTrace();
}
```

---

## 🧰 **`java.sql` 中的实用功能**

| 功能               | 接口/类                              | 用途                                       |
| ------------------ | ------------------------------------ | ------------------------------------------ |
| 元数据             | `DatabaseMetaData`                   | 数据库版本、支持的功能、表等               |
| 结果列信息         | `ResultSetMetaData`                  | 列数、类型、标签等                         |
| BLOB/CLOB 处理     | `Blob`, `Clob`                       | 存储/检索大型二进制/文本数据               |
| 批量执行           | `addBatch()`, `executeBatch()`       | 一起执行多个语句                           |
| 可滚动 ResultSet   | `ResultSet.TYPE_SCROLL_INSENSITIVE`  | 前后移动游标                               |
| 可更新 ResultSet   | `ResultSet.CONCUR_UPDATABLE`         | 直接在 `ResultSet` 中修改行                |

---

## 📦 **Maven 依赖示例 (MySQL)**

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

---

## 🧠 **最佳实践**

* 始终在 `finally` 块中关闭 `Connection`、`Statement`、`ResultSet`，或使用 try-with-resources。
* 使用 `PreparedStatement` 而不是 `Statement` 以防止 SQL 注入。
* 在生产环境中使用连接池（通过 HikariCP、Apache DBCP 等库）。
* 对多个相关查询使用事务。
* 不要在业务逻辑中硬编码 SQL——考虑使用 DAO 或 ORM 模式（如 JPA、Hibernate）。

---

## 🧮 **高级主题**

* **RowSet**：ResultSet 的断开连接版本 (`javax.sql.rowset`)
* **连接池**：将 `DataSource` 与池一起使用
* **JDBC 4+ 特性**：自动加载驱动程序、try-with-resources 支持
* **JDBC + Spring**：与 Spring JDBC Template 集成
* **JDBC + ORM**：在 Hibernate、JPA、MyBatis 底层使用 `java.sql`

---

## 🧾 **总结表格**

| 任务               | 类/接口                              |
| ------------------ | ------------------------------------ |
| 连接数据库         | `DriverManager`, `Connection`        |
| 执行 SQL           | `Statement`, `PreparedStatement`     |
| 存储过程           | `CallableStatement`                  |
| 读取结果           | `ResultSet`                          |
| 数据库信息         | `DatabaseMetaData`                   |
| 列信息             | `ResultSetMetaData`                  |
| 事务               | `Connection.commit()`, `rollback()`  |
| 异常处理           | `SQLException`                       |

---

如果您需要，我还可以提供：

* 一份速查表
* 一个 DAO 风格的可重用包装类
* 使用真实数据库（MySQL/PostgreSQL）的示例

请告诉我！
