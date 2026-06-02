---
audio: false
generated: true
image: false
lang: en
layout: post
title: Statement vs CallableStatement in JDBC
translated: false
type: note
---

In Java’s JDBC (and other frameworks that build on it, like Hibernate or Spring), the concepts of **`Statement`** and **`CallableStatement`** are both interfaces used to send SQL commands to the database, but they serve different purposes.

---

### 1. `Statement`

* **Purpose**: Used to execute simple SQL queries without parameters.
* **Usage**: You create a `Statement` object from a `Connection` and use it to execute SQL strings.
* **Typical methods**:

  * `executeQuery(sql)` → for `SELECT` queries, returns a `ResultSet`.
  * `executeUpdate(sql)` → for `INSERT`, `UPDATE`, `DELETE`.
  * `execute(sql)` → generic, returns `true` if the result is a `ResultSet`.

**Example**:

```java
Connection conn = DriverManager.getConnection(url, user, pass);
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT id, name FROM employees");

while (rs.next()) {
    System.out.println(rs.getInt("id") + " " + rs.getString("name"));
}
```

* **When to use**: For static SQL statements with no parameters.
* **Drawback**: Can lead to SQL injection if used with dynamic user input.

---

### 2. `CallableStatement`

* **Purpose**: Used to execute **stored procedures** in the database.
* **Usage**: Created with `Connection.prepareCall()` and allows calling database routines with **IN**, **OUT**, and **INOUT** parameters.
* **Typical methods**:

  * `setInt`, `setString`, etc. → to set input parameters.
  * `registerOutParameter` → to register output parameters.
  * `execute()` or `executeQuery()` → to run the stored procedure.
  * `getInt`, `getString`, etc. → to retrieve output values.

**Example**:

```java
Connection conn = DriverManager.getConnection(url, user, pass);
CallableStatement cstmt = conn.prepareCall("{call getEmployeeName(?, ?)}");

// Set IN parameter
cstmt.setInt(1, 101);

// Register OUT parameter
cstmt.registerOutParameter(2, java.sql.Types.VARCHAR);

// Execute
cstmt.execute();

// Get OUT parameter
String empName = cstmt.getString(2);
System.out.println("Employee name: " + empName);
```

* **When to use**: For stored procedures/functions that encapsulate logic in the database.
* **Advantages**: Supports complex logic, multiple results, input/output parameters.

---

### Key Differences (without a table)

* `Statement` is for **static SQL** (ad-hoc queries).
* `CallableStatement` is for **stored procedures/functions**.
* `Statement` executes SQL directly, while `CallableStatement` interacts with database routines that may return multiple result sets and parameters.
* `Statement` is simple but less secure with dynamic input, while `CallableStatement` provides a structured way to call reusable logic stored in the DB.

---

👉 If you want, I can also explain how **`PreparedStatement`** fits between these two (safer, parameterized SQL, but not for stored procedures). Would you like me to add that?
