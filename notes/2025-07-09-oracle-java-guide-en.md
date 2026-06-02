---
audio: false
generated: true
lang: en
layout: post
title: Java Developers' Oracle Database Guide
translated: false
type: note
---

## Table of Contents
1. [Oracle Database Overview](#oracle-database-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Oracle Database Architecture](#oracle-database-architecture)
4. [SQL Fundamentals](#sql-fundamentals)
5. [Advanced Oracle Features](#advanced-oracle-features)
6. [Java Database Connectivity](#java-database-connectivity)
7. [Connection Management](#connection-management)
8. [ORM Frameworks](#orm-frameworks)
9. [Performance Optimization](#performance-optimization)
10. [Security Best Practices](#security-best-practices)
11. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Oracle Database Overview

Oracle Database is a multi-model database management system produced by Oracle Corporation. It's one of the most widely used relational database management systems (RDBMS) in enterprise environments.

### Key Features
- **ACID Compliance**: Ensures data integrity through Atomicity, Consistency, Isolation, and Durability
- **Multi-version Concurrency Control (MVCC)**: Allows multiple users to access data concurrently
- **Partitioning**: Divides large tables into smaller, manageable pieces
- **Advanced Security**: Built-in encryption, auditing, and access controls
- **High Availability**: Real Application Clusters (RAC) and Data Guard
- **Scalability**: Supports massive databases and high transaction volumes

### Oracle Database Editions
- **Express Edition (XE)**: Free, limited version for development and small deployments
- **Standard Edition**: Mid-range edition with core features
- **Enterprise Edition**: Full-featured version with advanced capabilities
- **Autonomous Database**: Cloud-based, self-managing database service

## Installation and Setup

### Oracle Database Installation

#### Using Oracle Database XE (Recommended for Development)
1. Download Oracle Database XE from Oracle's official website
2. Install following the platform-specific instructions
3. Configure the database using Database Configuration Assistant (DBCA)

#### Docker Installation (Quick Setup)
```bash
# Pull Oracle Database XE image
docker pull container-registry.oracle.com/database/express:21.3.0-xe

# Run Oracle Database XE container
docker run --name oracle-xe \
  -p 1521:1521 \
  -p 5500:5500 \
  -e ORACLE_PWD=your_password \
  -e ORACLE_CHARACTERSET=AL32UTF8 \
  container-registry.oracle.com/database/express:21.3.0-xe
```

### Client Tools
- **SQL*Plus**: Command-line interface
- **SQL Developer**: GUI-based development environment
- **Oracle Enterprise Manager**: Web-based management console
- **DBeaver**: Third-party database management tool

## Oracle Database Architecture

### Physical Architecture
- **Database Files**: Data files, control files, and redo log files
- **Parameter Files**: Configuration settings (PFILE/SPFILE)
- **Archive Log Files**: Backup of redo log files for recovery

### Logical Architecture
- **Tablespaces**: Logical storage units containing one or more data files
- **Schemas**: Collection of database objects owned by a user
- **Segments**: Space allocated for database objects
- **Extents**: Contiguous blocks of storage
- **Blocks**: Smallest unit of storage

### Memory Architecture
- **System Global Area (SGA)**: Shared memory area
  - Database Buffer Cache
  - Shared Pool
  - Redo Log Buffer
  - Large Pool
- **Program Global Area (PGA)**: Private memory for each process

## SQL Fundamentals

### Data Definition Language (DDL)

#### Creating Tables
```sql
-- Create a table
CREATE TABLE employees (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20) NOT NULL,
    last_name VARCHAR2(25) NOT NULL,
    email VARCHAR2(50) UNIQUE,
    hire_date DATE DEFAULT SYSDATE,
    job_id VARCHAR2(10),
    salary NUMBER(8,2),
    department_id NUMBER(4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add constraints
ALTER TABLE employees
ADD CONSTRAINT fk_dept_id
FOREIGN KEY (department_id)
REFERENCES departments(department_id);

-- Create index
CREATE INDEX idx_emp_dept ON employees(department_id);
```

#### Oracle-Specific Data Types
- **NUMBER**: Numeric data with precision and scale
- **VARCHAR2**: Variable-length character strings
- **CHAR**: Fixed-length character strings
- **DATE**: Date and time
- **TIMESTAMP**: Date and time with fractional seconds
- **CLOB**: Character Large Object
- **BLOB**: Binary Large Object
- **XMLTYPE**: XML data

### Data Manipulation Language (DML)

#### Advanced Queries
```sql
-- Window functions
SELECT
    employee_id,
    first_name,
    last_name,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as salary_rank,
    LAG(salary, 1) OVER (ORDER BY hire_date) as prev_salary
FROM employees;

-- Common Table Expressions (CTE)
WITH dept_avg_salary AS (
    SELECT department_id, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT e.*, d.avg_salary
FROM employees e
JOIN dept_avg_salary d ON e.department_id = d.department_id;

-- Hierarchical queries
SELECT employee_id, first_name, last_name, manager_id, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id
ORDER SIBLINGS BY last_name;
```

### PL/SQL Programming

#### Basic PL/SQL Block
```sql
DECLARE
    v_employee_count NUMBER;
    v_department_name VARCHAR2(30);
BEGIN
    SELECT COUNT(*) INTO v_employee_count
    FROM employees
    WHERE department_id = 10;

    IF v_employee_count > 0 THEN
        SELECT department_name INTO v_department_name
        FROM departments
        WHERE department_id = 10;

        DBMS_OUTPUT.PUT_LINE('Department: ' || v_department_name ||
                           ' has ' || v_employee_count || ' employees');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No data found');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/
```

#### Stored Procedures and Functions
```sql
-- Stored Procedure
CREATE OR REPLACE PROCEDURE update_employee_salary(
    p_employee_id IN NUMBER,
    p_salary_increase IN NUMBER
) AS
    v_current_salary NUMBER;
BEGIN
    SELECT salary INTO v_current_salary
    FROM employees
    WHERE employee_id = p_employee_id;

    UPDATE employees
    SET salary = v_current_salary + p_salary_increase
    WHERE employee_id = p_employee_id;

    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20001, 'Employee not found');
END;
/

-- Function
CREATE OR REPLACE FUNCTION calculate_annual_salary(
    p_employee_id IN NUMBER
) RETURN NUMBER AS
    v_monthly_salary NUMBER;
BEGIN
    SELECT salary INTO v_monthly_salary
    FROM employees
    WHERE employee_id = p_employee_id;

    RETURN v_monthly_salary * 12;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0;
END;
/
```

## Advanced Oracle Features

### Partitioning
```sql
-- Range partitioning
CREATE TABLE sales (
    sale_id NUMBER,
    sale_date DATE,
    amount NUMBER
) PARTITION BY RANGE (sale_date) (
    PARTITION p2023 VALUES LESS THAN (DATE '2024-01-01'),
    PARTITION p2024 VALUES LESS THAN (DATE '2025-01-01'),
    PARTITION p_max VALUES LESS THAN (MAXVALUE)
);

-- Hash partitioning
CREATE TABLE customers (
    customer_id NUMBER,
    name VARCHAR2(100)
) PARTITION BY HASH (customer_id) PARTITIONS 4;
```

### Sequences
```sql
-- Create sequence
CREATE SEQUENCE emp_seq
    START WITH 1000
    INCREMENT BY 1
    MAXVALUE 9999999
    NOCACHE
    NOCYCLE;

-- Use sequence
INSERT INTO employees (employee_id, first_name, last_name)
VALUES (emp_seq.NEXTVAL, 'John', 'Doe');
```

### Views and Materialized Views
```sql
-- Create view
CREATE VIEW employee_details AS
SELECT e.employee_id, e.first_name, e.last_name,
       d.department_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id;

-- Materialized view
CREATE MATERIALIZED VIEW emp_dept_summary
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT d.department_name, COUNT(*) as employee_count, AVG(salary) as avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name;
```

## Java Database Connectivity

### JDBC Driver Setup

#### Maven Dependencies
```xml
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ojdbc11</artifactId>
    <version>23.3.0.23.09</version>
</dependency>

<!-- For connection pooling -->
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ucp</artifactId>
    <version>23.3.0.23.09</version>
</dependency>
```

#### Basic JDBC Connection
```java
import java.sql.*;

public class OracleConnection {
    private static final String URL = "jdbc:oracle:thin:@localhost:1521:XE";
    private static final String USERNAME = "your_username";
    private static final String PASSWORD = "your_password";

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USERNAME, PASSWORD);
    }

    public static void main(String[] args) {
        try (Connection conn = getConnection()) {
            System.out.println("Connected to Oracle Database!");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

### CRUD Operations

#### Data Access Object (DAO) Pattern
```java
public class Employee {
    private int employeeId;
    private String firstName;
    private String lastName;
    private String email;
    private Date hireDate;
    private double salary;
    private int departmentId;

    // Constructors, getters, and setters
    // ...
}

public interface EmployeeDAO {
    void createEmployee(Employee employee);
    Employee getEmployeeById(int id);
    List<Employee> getAllEmployees();
    void updateEmployee(Employee employee);
    void deleteEmployee(int id);
}

public class EmployeeDAOImpl implements EmployeeDAO {
    private Connection connection;

    public EmployeeDAOImpl(Connection connection) {
        this.connection = connection;
    }

    @Override
    public void createEmployee(Employee employee) {
        String sql = "INSERT INTO employees (employee_id, first_name, last_name, email, salary, department_id) VALUES (emp_seq.NEXTVAL, ?, ?, ?, ?, ?)";

        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, employee.getFirstName());
            pstmt.setString(2, employee.getLastName());
            pstmt.setString(3, employee.getEmail());
            pstmt.setDouble(4, employee.getSalary());
            pstmt.setInt(5, employee.getDepartmentId());

            pstmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("Error creating employee", e);
        }
    }

    @Override
    public Employee getEmployeeById(int id) {
        String sql = "SELECT * FROM employees WHERE employee_id = ?";

        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setInt(1, id);
            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                return mapResultSetToEmployee(rs);
            }
        } catch (SQLException e) {
            throw new RuntimeException("Error retrieving employee", e);
        }
        return null;
    }

    @Override
    public List<Employee> getAllEmployees() {
        List<Employee> employees = new ArrayList<>();
        String sql = "SELECT * FROM employees ORDER BY employee_id";

        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            while (rs.next()) {
                employees.add(mapResultSetToEmployee(rs));
            }
        } catch (SQLException e) {
            throw new RuntimeException("Error retrieving employees", e);
        }
        return employees;
    }

    @Override
    public void updateEmployee(Employee employee) {
        String sql = "UPDATE employees SET first_name = ?, last_name = ?, email = ?, salary = ?, department_id = ? WHERE employee_id = ?";

        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, employee.getFirstName());
            pstmt.setString(2, employee.getLastName());
            pstmt.setString(3, employee.getEmail());
            pstmt.setDouble(4, employee.getSalary());
            pstmt.setInt(5, employee.getDepartmentId());
            pstmt.setInt(6, employee.getEmployeeId());

            pstmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("Error updating employee", e);
        }
    }

    @Override
    public void deleteEmployee(int id) {
        String sql = "DELETE FROM employees WHERE employee_id = ?";

        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setInt(1, id);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("Error deleting employee", e);
        }
    }

    private Employee mapResultSetToEmployee(ResultSet rs) throws SQLException {
        Employee employee = new Employee();
        employee.setEmployeeId(rs.getInt("employee_id"));
        employee.setFirstName(rs.getString("first_name"));
        employee.setLastName(rs.getString("last_name"));
        employee.setEmail(rs.getString("email"));
        employee.setHireDate(rs.getDate("hire_date"));
        employee.setSalary(rs.getDouble("salary"));
        employee.setDepartmentId(rs.getInt("department_id"));
        return employee;
    }
}
```

### Working with Stored Procedures
```java
public class StoredProcedureExample {

    public void updateEmployeeSalary(int employeeId, double salaryIncrease) {
        String sql = "{call update_employee_salary(?, ?)}";

        try (Connection conn = OracleConnection.getConnection();
             CallableStatement cstmt = conn.prepareCall(sql)) {

            cstmt.setInt(1, employeeId);
            cstmt.setDouble(2, salaryIncrease);
            cstmt.execute();

        } catch (SQLException e) {
            throw new RuntimeException("Error calling stored procedure", e);
        }
    }

    public double getAnnualSalary(int employeeId) {
        String sql = "{? = call calculate_annual_salary(?)}";

        try (Connection conn = OracleConnection.getConnection();
             CallableStatement cstmt = conn.prepareCall(sql)) {

            cstmt.registerOutParameter(1, Types.NUMERIC);
            cstmt.setInt(2, employeeId);
            cstmt.execute();

            return cstmt.getDouble(1);

        } catch (SQLException e) {
            throw new RuntimeException("Error calling function", e);
        }
    }
}
```

## Connection Management

### Connection Pooling with Oracle UCP
```java
import oracle.ucp.jdbc.PoolDataSource;
import oracle.ucp.jdbc.PoolDataSourceFactory;

public class ConnectionPoolManager {
    private static PoolDataSource poolDataSource;

    static {
        try {
            poolDataSource = PoolDataSourceFactory.getPoolDataSource();
            poolDataSource.setURL("jdbc:oracle:thin:@localhost:1521:XE");
            poolDataSource.setUser("your_username");
            poolDataSource.setPassword("your_password");
            poolDataSource.setConnectionFactoryClassName("oracle.jdbc.pool.OracleDataSource");

            // Pool configuration
            poolDataSource.setInitialPoolSize(5);
            poolDataSource.setMinPoolSize(5);
            poolDataSource.setMaxPoolSize(20);
            poolDataSource.setConnectionWaitTimeout(5);
            poolDataSource.setInactiveConnectionTimeout(300);

        } catch (SQLException e) {
            throw new RuntimeException("Error initializing connection pool", e);
        }
    }

    public static Connection getConnection() throws SQLException {
        return poolDataSource.getConnection();
    }
}
```

### Transaction Management
```java
public class TransactionExample {

    public void transferFunds(int fromAccount, int toAccount, double amount) {
        Connection conn = null;
        try {
            conn = ConnectionPoolManager.getConnection();
            conn.setAutoCommit(false); // Start transaction

            // Debit from source account
            String debitSql = "UPDATE accounts SET balance = balance - ? WHERE account_id = ?";
            try (PreparedStatement debitStmt = conn.prepareStatement(debitSql)) {
                debitStmt.setDouble(1, amount);
                debitStmt.setInt(2, fromAccount);
                debitStmt.executeUpdate();
            }

            // Credit to destination account
            String creditSql = "UPDATE accounts SET balance = balance + ? WHERE account_id = ?";
            try (PreparedStatement creditStmt = conn.prepareStatement(creditSql)) {
                creditStmt.setDouble(1, amount);
                creditStmt.setInt(2, toAccount);
                creditStmt.executeUpdate();
            }

            conn.commit(); // Commit transaction

        } catch (SQLException e) {
            if (conn != null) {
                try {
                    conn.rollback(); // Rollback on error
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
            throw new RuntimeException("Error in fund transfer", e);
        } finally {
            if (conn != null) {
                try {
                    conn.setAutoCommit(true); // Reset auto-commit
                    conn.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

## ORM Frameworks

### Hibernate Configuration
```xml
<!-- hibernate.cfg.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
    "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
    "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <property name="hibernate.connection.driver_class">oracle.jdbc.OracleDriver</property>
        <property name="hibernate.connection.url">jdbc:oracle:thin:@localhost:1521:XE</property>
        <property name="hibernate.connection.username">your_username</property>
        <property name="hibernate.connection.password">your_password</property>
        <property name="hibernate.dialect">org.hibernate.dialect.Oracle12cDialect</property>
        <property name="hibernate.hbm2ddl.auto">update</property>
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>

        <!-- Connection pool -->
        <property name="hibernate.c3p0.min_size">5</property>
        <property name="hibernate.c3p0.max_size">20</property>
        <property name="hibernate.c3p0.timeout">300</property>
        <property name="hibernate.c3p0.max_statements">50</property>
        <property name="hibernate.c3p0.idle_test_period">3000</property>
    </session-factory>
</hibernate-configuration>
```

### JPA Entity with Oracle-specific Features
```java
@Entity
@Table(name = "employees")
@SequenceGenerator(name = "emp_seq", sequenceName = "emp_seq", allocationSize = 1)
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "emp_seq")
    @Column(name = "employee_id")
    private Integer employeeId;

    @Column(name = "first_name", nullable = false, length = 20)
    private String firstName;

    @Column(name = "last_name", nullable = false, length = 25)
    private String lastName;

    @Column(name = "email", unique = true, length = 50)
    private String email;

    @Column(name = "hire_date")
    @Temporal(TemporalType.DATE)
    private Date hireDate;

    @Column(name = "salary", precision = 8, scale = 2)
    private BigDecimal salary;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;

    @CreationTimestamp
    @Column(name = "created_at")
    private Timestamp createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Timestamp updatedAt;

    // Constructors, getters, and setters
    // ...
}
```

### Spring Boot with Oracle
```yaml
# application.yml
spring:
  datasource:
    url: jdbc:oracle:thin:@localhost:1521:XE
    username: your_username
    password: your_password
    driver-class-name: oracle.jdbc.OracleDriver
    hikari:
      minimum-idle: 5
      maximum-pool-size: 20
      idle-timeout: 300000
      max-lifetime: 1800000
      connection-timeout: 30000

  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.Oracle12cDialect
        format_sql: true
        jdbc:
          batch_size: 20
        order_inserts: true
        order_updates: true
```

## Performance Optimization

### Query Optimization
```sql
-- Use indexes effectively
CREATE INDEX idx_emp_dept_salary ON employees(department_id, salary);

-- Use hints when necessary
SELECT /*+ INDEX(e idx_emp_dept_salary) */
       e.employee_id, e.first_name, e.last_name
FROM employees e
WHERE department_id = 10 AND salary > 50000;

-- Use bind variables to prevent SQL injection and improve performance
SELECT * FROM employees WHERE employee_id = :employee_id;
```

### Java Performance Tips
```java
// Use batch processing for multiple inserts
public void batchInsertEmployees(List<Employee> employees) {
    String sql = "INSERT INTO employees (employee_id, first_name, last_name, email, salary, department_id) VALUES (emp_seq.NEXTVAL, ?, ?, ?, ?, ?)";

    try (Connection conn = ConnectionPoolManager.getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {

        conn.setAutoCommit(false);

        for (Employee emp : employees) {
            pstmt.setString(1, emp.getFirstName());
            pstmt.setString(2, emp.getLastName());
            pstmt.setString(3, emp.getEmail());
            pstmt.setDouble(4, emp.getSalary());
            pstmt.setInt(5, emp.getDepartmentId());
            pstmt.addBatch();
        }

        pstmt.executeBatch();
        conn.commit();

    } catch (SQLException e) {
        throw new RuntimeException("Error in batch insert", e);
    }
}

// Use proper fetch sizes for large result sets
public List<Employee> getAllEmployeesOptimized() {
    List<Employee> employees = new ArrayList<>();
    String sql = "SELECT * FROM employees ORDER BY employee_id";

    try (Connection conn = ConnectionPoolManager.getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {

        pstmt.setFetchSize(1000); // Optimize fetch size
        ResultSet rs = pstmt.executeQuery();

        while (rs.next()) {
            employees.add(mapResultSetToEmployee(rs));
        }

    } catch (SQLException e) {
        throw new RuntimeException("Error retrieving employees", e);
    }
    return employees;
}
```

## Security Best Practices

### Connection Security
```java
// Use encrypted connections
String url = "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcps)(HOST=localhost)(PORT=2484))(CONNECT_DATA=(SERVICE_NAME=XE)))" +
            "?oracle.net.ssl_client_authentication=false" +
            "&oracle.net.ssl_server_cert_dn=\"CN=localhost\"";

// Use connection properties for security
Properties props = new Properties();
props.setProperty("user", username);
props.setProperty("password", password);
props.setProperty("oracle.net.encryption_client", "REQUIRED");
props.setProperty("oracle.net.encryption_types_client", "AES256");
props.setProperty("oracle.net.crypto_checksum_client", "REQUIRED");
props.setProperty("oracle.net.crypto_checksum_types_client", "SHA256");

Connection conn = DriverManager.getConnection(url, props);
```

### SQL Injection Prevention
```java
// Always use parameterized queries
public Employee findEmployeeByEmail(String email) {
    String sql = "SELECT * FROM employees WHERE email = ?"; // Safe
    // String sql = "SELECT * FROM employees WHERE email = '" + email + "'"; // DANGEROUS!

    try (Connection conn = ConnectionPoolManager.getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {

        pstmt.setString(1, email);
        ResultSet rs = pstmt.executeQuery();

        if (rs.next()) {
            return mapResultSetToEmployee(rs);
        }

    } catch (SQLException e) {
        throw new RuntimeException("Error finding employee", e);
    }
    return null;
}
```

## Monitoring and Maintenance

### Database Monitoring Queries
```sql
-- Check table sizes
SELECT table_name,
       ROUND(((num_rows * avg_row_len) / 1024 / 1024), 2) as size_mb
FROM user_tables
ORDER BY size_mb DESC;

-- Monitor active sessions
SELECT username, osuser, machine, program, status, logon_time
FROM v$session
WHERE username IS NOT NULL
ORDER BY logon_time;

-- Check tablespace usage
SELECT tablespace_name,
       ROUND(((total_bytes - free_bytes) / 1024 / 1024), 2) as used_mb,
       ROUND((free_bytes / 1024 / 1024), 2) as free_mb,
       ROUND(((total_bytes - free_bytes) / total_bytes * 100), 2) as percent_used
FROM (
    SELECT tablespace_name, SUM(bytes) as total_bytes
    FROM dba_data_files
    GROUP BY tablespace_name
) total,
(
    SELECT tablespace_name, SUM(bytes) as free_bytes
    FROM dba_free_space
    GROUP BY tablespace_name
) free
WHERE total.tablespace_name = free.tablespace_name(+);
```

### Application Monitoring
```java
// Connection pool monitoring
public class ConnectionPoolMonitor {

    public void printPoolStatistics() {
        try {
            oracle.ucp.jdbc.PoolDataSource pds = (oracle.ucp.jdbc.PoolDataSource) poolDataSource;

            System.out.println("=== Connection Pool Statistics ===");
            System.out.println("Available Connections: " + pds.getAvailableConnectionsCount());
            System.out.println("Borrowed Connections: " + pds.getBorrowedConnectionsCount());
            System.out.println("Peak Pool Size: " + pds.getPeakPoolSize());
            System.out.println("Connection Pool Size: " + pds.getPoolSize());
            System.out.println("================================");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

// Query performance monitoring
public class QueryPerformanceMonitor {

    public <T> T executeWithTiming(String operationName, Supplier<T> operation) {
        long startTime = System.currentTimeMillis();

        try {
            T result = operation.get();
            long duration = System.currentTimeMillis() - startTime;

            System.out.println(operationName + " executed in " + duration + "ms");

            if (duration > 1000) { // Log slow queries
                System.out.println("SLOW QUERY DETECTED: " + operationName);
            }

            return result;

        } catch (Exception e) {
            System.err.println("Error in " + operationName + ": " + e.getMessage());
            throw e;
        }
    }
}
```

## Best Practices Summary

### Database Design
- Use appropriate data types and constraints
- Implement proper indexing strategy
- Consider partitioning for large tables
- Use sequences for primary keys
- Normalize data appropriately

### Java Development
- Always use connection pooling
- Implement proper exception handling
- Use parameterized queries to prevent SQL injection
- Close resources properly (use try-with-resources)
- Consider using ORM frameworks for complex applications

### Performance
- Monitor and optimize slow queries
- Use batch operations for bulk data operations
- Implement proper caching strategies
- Monitor connection pool metrics
- Use appropriate fetch sizes

### Security
- Use encrypted connections in production
- Implement proper authentication and authorization
- Never hardcode credentials
- Use principle of least privilege
- Regular security audits

This comprehensive guide provides a solid foundation for working with Oracle Database in Java applications. Remember to always refer to the official Oracle documentation for the most up-to-date information and best practices.
