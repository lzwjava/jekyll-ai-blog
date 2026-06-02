---
audio: false
generated: true
lang: en
layout: post
title: Java SQL for Database Connectivity
translated: false
type: note
---

The `java.sql` package is a **core part of Java's JDBC API (Java Database Connectivity)**, enabling Java applications to interact with relational databases like MySQL, PostgreSQL, Oracle, SQL Server, and others. It provides the interfaces and classes required to **connect to a database, execute SQL queries, and retrieve results**.

---

## 📘 **Overview of `java.sql`**

The `java.sql` package includes classes and interfaces to:

* Connect to databases (`DriverManager`, `Connection`)
* Execute SQL queries (`Statement`, `PreparedStatement`, `CallableStatement`)
* Process results (`ResultSet`)
* Handle metadata (`DatabaseMetaData`, `ResultSetMetaData`)
* Manage transactions
* Handle SQL exceptions (`SQLException`)

---

## 🔧 **Setup: What You Need**

### 1. **JDBC Driver**

* You need a JDBC driver for your target database (e.g., MySQL: `mysql-connector-java`, PostgreSQL: `postgresql`).
* You can include it via Maven/Gradle or manually add the `.jar`.

### 2. **Database URL**

Each JDBC driver has a connection URL format:

```java
jdbc:mysql://localhost:3306/mydatabase
jdbc:postgresql://localhost:5432/mydatabase
```

---

## 🧩 **Key Classes and Interfaces**

### 🔌 1. `DriverManager`

Establishes a connection to a database.

```java
Connection conn = DriverManager.getConnection(url, user, password);
```

### 🧵 2. `Connection`

Represents a session with a database.

* Create `Statement` or `PreparedStatement`
* Manage transactions (commit, rollback)
* Close the connection

```java
Connection conn = DriverManager.getConnection(...);
conn.setAutoCommit(false);  // for manual transaction control
```

### 📤 3. `Statement` / `PreparedStatement` / `CallableStatement`

#### `Statement`

Used for executing static SQL queries.

```java
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM users");
```

#### `PreparedStatement`

Used for executing parameterized queries. Avoids SQL injection.

```java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, 101);
ResultSet rs = ps.executeQuery();
```

#### `CallableStatement`

Used for stored procedures.

```java
CallableStatement cs = conn.prepareCall("{call getUser(?)}");
cs.setInt(1, 5);
ResultSet rs = cs.executeQuery();
```

### 📥 4. `ResultSet`

Holds the result of a query.

```java
while (rs.next()) {
    int id = rs.getInt("id");
    String name = rs.getString("name");
}
```

### 📚 5. Metadata

* `DatabaseMetaData`: Info about DB
* `ResultSetMetaData`: Info about result columns

```java
DatabaseMetaData dbMeta = conn.getMetaData();
ResultSetMetaData rsMeta = rs.getMetaData();
```

---

## 🧪 **Basic Example**

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

## 🔁 **Transactions**

```java
conn.setAutoCommit(false);  // Disable auto-commit

try {
    PreparedStatement ps1 = conn.prepareStatement("UPDATE accounts SET balance = balance - ? WHERE id = ?");
    ps1.setDouble(1, 100.0);
    ps1.setInt(2, 1);
    ps1.executeUpdate();

    PreparedStatement ps2 = conn.prepareStatement("UPDATE accounts SET balance = balance + ? WHERE id = ?");
    ps2.setDouble(1, 100.0);
    ps2.setInt(2, 2);
    ps2.executeUpdate();

    conn.commit(); // Commit the transaction

} catch (SQLException ex) {
    conn.rollback(); // Roll back on error
}
```

---

## ❗ **Exception Handling**

```java
try {
    // DB code
} catch (SQLException ex) {
    System.err.println("Error Code: " + ex.getErrorCode());
    System.err.println("SQL State: " + ex.getSQLState());
    ex.printStackTrace();
}
```

---

## 🧰 **Useful Features in `java.sql`**

| Feature              | Interface/Class                     | Purpose                                      |
| -------------------- | ----------------------------------- | -------------------------------------------- |
| Metadata             | `DatabaseMetaData`                  | DB version, supported features, tables, etc. |
| Result column info   | `ResultSetMetaData`                 | Column count, type, label, etc.              |
| BLOB/CLOB Handling   | `Blob`, `Clob`                      | Store/retrieve large binary/text data        |
| Batch Execution      | `addBatch()`, `executeBatch()`      | Execute many statements together             |
| Scrollable ResultSet | `ResultSet.TYPE_SCROLL_INSENSITIVE` | Move cursor back and forth                   |
| Updatable ResultSet  | `ResultSet.CONCUR_UPDATABLE`        | Modify rows directly in `ResultSet`          |

---

## 📦 **Maven Dependency Example (MySQL)**

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

---

## 🧠 **Best Practices**

* Always close `Connection`, `Statement`, `ResultSet` in `finally` block or use try-with-resources.
* Use `PreparedStatement` over `Statement` to prevent SQL injection.
* Use connection pooling in production (via libraries like HikariCP, Apache DBCP).
* Use transactions for multiple related queries.
* Don't hardcode SQL in business logic — consider DAO or ORM patterns (like JPA, Hibernate).

---

## 🧮 **Advanced Topics**

* **RowSet**: Disconnected version of ResultSet (`javax.sql.rowset`)
* **Connection Pooling**: Use `DataSource` with pools
* **JDBC 4+ Features**: Auto-loading drivers, try-with-resources support
* **JDBC + Spring**: Integration with Spring JDBC Template
* **JDBC + ORM**: Use `java.sql` underneath Hibernate, JPA, MyBatis

---

## 🧾 **Summary Table**

| Task               | Class/Interface                     |
| ------------------ | ----------------------------------- |
| Connect to DB      | `DriverManager`, `Connection`       |
| Execute SQL        | `Statement`, `PreparedStatement`    |
| Stored Procedures  | `CallableStatement`                 |
| Read Results       | `ResultSet`                         |
| DB Info            | `DatabaseMetaData`                  |
| Column Info        | `ResultSetMetaData`                 |
| Transactions       | `Connection.commit()`, `rollback()` |
| Exception Handling | `SQLException`                      |

---

If you'd like, I can also give:

* A cheat sheet
* A DAO-style reusable wrapper class
* Examples with a real database (MySQL/PostgreSQL)

Let me know!
