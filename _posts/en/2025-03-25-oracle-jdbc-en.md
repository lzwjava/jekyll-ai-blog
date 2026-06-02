---
audio: false
generated: true
lang: en
layout: post
title: Oracle JDBC Driver
translated: false
type: note
---

Oracle JDBC (Java Database Connectivity) drivers allow Java applications to connect to and interact with Oracle databases. Let me explain the key components and how to use them.

The main class for Oracle JDBC connections is `oracle.jdbc.driver.OracleDriver`, though in newer versions you'll often use `oracle.jdbc.OracleDriver` (which is the recommended class since Oracle 10g).

Here's how to use Oracle JDBC in a Java application:

1. First, you need to include the Oracle JDBC driver JAR in your project (typically ojdbc.jar).

2. Load the driver class:

```java
Class.forName("oracle.jdbc.OracleDriver");
```

3. Establish a connection using a connection URL:

```java
String url = "jdbc:oracle:thin:@hostname:port:SID";
// Or for service name based connection
// String url = "jdbc:oracle:thin:@//hostname:port/service_name";
String username = "your_username";
String password = "your_password";

Connection connection = DriverManager.getConnection(url, username, password);
```

4. Create and execute statements:

```java
Statement statement = connection.createStatement();
ResultSet resultSet = statement.executeQuery("SELECT * FROM employees");

while (resultSet.next()) {
    // Process each row
    String name = resultSet.getString("name");
    System.out.println(name);
}
```

5. Always close resources when done:

```java
resultSet.close();
statement.close();
connection.close();
```

The Oracle JDBC driver comes in several types:

- Thin driver: Pure Java implementation that doesn't require Oracle client installation
- OCI driver: Uses Oracle Call Interface and requires Oracle client software
- Kerberos driver: For Kerberos authentication
- JDBC-OCI driver: Combination of JDBC and OCI

The thin driver is most commonly used since it doesn't require additional Oracle client software on the client machine.

Would you like more specific information about connection pooling, prepared statements, or any other aspects of Oracle JDBC usage?
