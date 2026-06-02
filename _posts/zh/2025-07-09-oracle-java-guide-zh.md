---
audio: false
generated: true
lang: zh
layout: post
title: Java开发者Oracle数据库指南
translated: true
type: note
---

## 目录

1. [Oracle数据库概述](#oracle数据库概述)
2. [安装与设置](#安装与设置)
3. [Oracle数据库架构](#oracle数据库架构)
4. [SQL基础](#sql基础)
5. [高级Oracle功能](#高级oracle功能)
6. [Java数据库连接](#java数据库连接)
7. [连接管理](#连接管理)
8. [ORM框架](#orm框架)
9. [性能优化](#性能优化)
10. [安全最佳实践](#安全最佳实践)
11. [监控与维护](#监控与维护)

## Oracle数据库概述

Oracle数据库是由Oracle公司生产的多模型数据库管理系统。它是企业环境中使用最广泛的关系数据库管理系统（RDBMS）之一。

### 主要特性

- **ACID合规性**：通过原子性、一致性、隔离性和持久性确保数据完整性
- **多版本并发控制（MVCC）**：允许多个用户并发访问数据
- **分区**：将大表分割成更小、更易管理的部分
- **高级安全性**：内置加密、审计和访问控制
- **高可用性**：实时应用集群（RAC）和数据卫士
- **可扩展性**：支持海量数据库和高事务量

### Oracle数据库版本

- **Express版（XE）**：免费、功能有限的版本，适用于开发和小型部署
- **标准版**：具有核心功能的中端版本
- **企业版**：具有高级功能的完整版本
- **自治数据库**：基于云的自我管理数据库服务

## 安装与设置

### Oracle数据库安装

#### 使用Oracle数据库XE（推荐用于开发）

1. 从Oracle官网下载Oracle数据库XE
2. 按照平台特定说明进行安装
3. 使用数据库配置助手（DBCA）配置数据库

#### Docker安装（快速设置）

```bash
# 拉取Oracle数据库XE镜像
docker pull container-registry.oracle.com/database/express:21.3.0-xe

# 运行Oracle数据库XE容器
docker run --name oracle-xe \
  -p 1521:1521 \
  -p 5500:5500 \
  -e ORACLE_PWD=your_password \
  -e ORACLE_CHARACTERSET=AL32UTF8 \
  container-registry.oracle.com/database/express:21.3.0-xe
```

### 客户端工具

- **SQL*Plus**：命令行界面
- **SQL Developer**：基于GUI的开发环境
- **Oracle Enterprise Manager**：基于Web的管理控制台
- **DBeaver**：第三方数据库管理工具

## Oracle数据库架构

### 物理架构

- **数据库文件**：数据文件、控制文件和重做日志文件
- **参数文件**：配置设置（PFILE/SPFILE）
- **归档日志文件**：用于恢复的重做日志文件备份

### 逻辑架构

- **表空间**：包含一个或多个数据文件的逻辑存储单元
- **模式**：由用户拥有的数据库对象集合
- **段**：为数据库对象分配的空间
- **区段**：连续的存储块
- **块**：最小的存储单元

### 内存架构

- **系统全局区（SGA）**：共享内存区域
  - 数据库缓冲区缓存
  - 共享池
  - 重做日志缓冲区
  - 大池
- **程序全局区（PGA）**：每个进程的私有内存

## SQL基础

### 数据定义语言（DDL）

#### 创建表

```sql
-- 创建表
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

-- 添加约束
ALTER TABLE employees
ADD CONSTRAINT fk_dept_id
FOREIGN KEY (department_id)
REFERENCES departments(department_id);

-- 创建索引
CREATE INDEX idx_emp_dept ON employees(department_id);
```

#### Oracle特定数据类型

- **NUMBER**：具有精度和小数位数的数值数据
- **VARCHAR2**：可变长度字符串
- **CHAR**：固定长度字符串
- **DATE**：日期和时间
- **TIMESTAMP**：具有小数秒的日期和时间
- **CLOB**：字符大对象
- **BLOB**：二进制大对象
- **XMLTYPE**：XML数据

### 数据操作语言（DML）

#### 高级查询

```sql
-- 窗口函数
SELECT
    employee_id,
    first_name,
    last_name,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as salary_rank,
    LAG(salary, 1) OVER (ORDER BY hire_date) as prev_salary
FROM employees;

-- 公共表表达式（CTE）
WITH dept_avg_salary AS (
    SELECT department_id, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT e.*, d.avg_salary
FROM employees e
JOIN dept_avg_salary d ON e.department_id = d.department_id;

-- 层次查询
SELECT employee_id, first_name, last_name, manager_id, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id
ORDER SIBLINGS BY last_name;
```

### PL/SQL编程

#### 基本PL/SQL块

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

        DBMS_OUTPUT.PUT_LINE('部门: ' || v_department_name ||
                           ' 有 ' || v_employee_count || ' 名员工');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('未找到数据');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('错误: ' || SQLERRM);
END;
/
```

#### 存储过程和函数

```sql
-- 存储过程
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
        RAISE_APPLICATION_ERROR(-20001, '未找到员工');
END;
/

-- 函数
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

## 高级Oracle功能

### 分区

```sql
-- 范围分区
CREATE TABLE sales (
    sale_id NUMBER,
    sale_date DATE,
    amount NUMBER
) PARTITION BY RANGE (sale_date) (
    PARTITION p2023 VALUES LESS THAN (DATE '2024-01-01'),
    PARTITION p2024 VALUES LESS THAN (DATE '2025-01-01'),
    PARTITION p_max VALUES LESS THAN (MAXVALUE)
);

-- 哈希分区
CREATE TABLE customers (
    customer_id NUMBER,
    name VARCHAR2(100)
) PARTITION BY HASH (customer_id) PARTITIONS 4;
```

### 序列

```sql
-- 创建序列
CREATE SEQUENCE emp_seq
    START WITH 1000
    INCREMENT BY 1
    MAXVALUE 9999999
    NOCACHE
    NOCYCLE;

-- 使用序列
INSERT INTO employees (employee_id, first_name, last_name)
VALUES (emp_seq.NEXTVAL, 'John', 'Doe');
```

### 视图和物化视图

```sql
-- 创建视图
CREATE VIEW employee_details AS
SELECT e.employee_id, e.first_name, e.last_name,
       d.department_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id;

-- 物化视图
CREATE MATERIALIZED VIEW emp_dept_summary
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT d.department_name, COUNT(*) as employee_count, AVG(salary) as avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name;
```

## Java数据库连接

### JDBC驱动设置

#### Maven依赖

```xml
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ojdbc11</artifactId>
    <version>23.3.0.23.09</version>
</dependency>

<!-- 用于连接池 -->
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ucp</artifactId>
    <version>23.3.0.23.09</version>
</dependency>
```

#### 基本JDBC连接

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
            System.out.println("已连接到Oracle数据库！");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

### CRUD操作

#### 数据访问对象（DAO）模式

```java
public class Employee {
    private int employeeId;
    private String firstName;
    private String lastName;
    private String email;
    private Date hireDate;
    private double salary;
    private int departmentId;

    // 构造函数、getter和setter
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
            throw new RuntimeException("创建员工时出错", e);
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
            throw new RuntimeException("检索员工时出错", e);
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
            throw new RuntimeException("检索员工列表时出错", e);
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
            throw new RuntimeException("更新员工时出错", e);
        }
    }

    @Override
    public void deleteEmployee(int id) {
        String sql = "DELETE FROM employees WHERE employee_id = ?";

        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setInt(1, id);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("删除员工时出错", e);
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

### 使用存储过程

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
            throw new RuntimeException("调用存储过程时出错", e);
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
            throw new RuntimeException("调用函数时出错", e);
        }
    }
}
```

## 连接管理

### 使用Oracle UCP进行连接池管理

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

            // 连接池配置
            poolDataSource.setInitialPoolSize(5);
            poolDataSource.setMinPoolSize(5);
            poolDataSource.setMaxPoolSize(20);
            poolDataSource.setConnectionWaitTimeout(5);
            poolDataSource.setInactiveConnectionTimeout(300);

        } catch (SQLException e) {
            throw new RuntimeException("初始化连接池时出错", e);
        }
    }

    public static Connection getConnection() throws SQLException {
        return poolDataSource.getConnection();
    }
}
```

### 事务管理

```java
public class TransactionExample {

    public void transferFunds(int fromAccount, int toAccount, double amount) {
        Connection conn = null;
        try {
            conn = ConnectionPoolManager.getConnection();
            conn.setAutoCommit(false); // 开始事务

            // 从源账户扣款
            String debitSql = "UPDATE accounts SET balance = balance - ? WHERE account_id = ?";
            try (PreparedStatement debitStmt = conn.prepareStatement(debitSql)) {
                debitStmt.setDouble(1, amount);
                debitStmt.setInt(2, fromAccount);
                debitStmt.executeUpdate();
            }

            // 向目标账户存款
            String creditSql = "UPDATE accounts SET balance = balance + ? WHERE account_id = ?";
            try (PreparedStatement creditStmt = conn.prepareStatement(creditSql)) {
                creditStmt.setDouble(1, amount);
                creditStmt.setInt(2, toAccount);
                creditStmt.executeUpdate();
            }

            conn.commit(); // 提交事务

        } catch (SQLException e) {
            if (conn != null) {
                try {
                    conn.rollback(); // 出错时回滚
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
            throw new RuntimeException("资金转账时出错", e);
        } finally {
            if (conn != null) {
                try {
                    conn.setAutoCommit(true); // 重置自动提交
                    conn.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

## ORM框架

### Hibernate配置

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

        <!-- 连接池 -->
        <property name="hibernate.c3p0.min_size">5</property>
        <property name="hibernate.c3p0.max_size">20</property>
        <property name="hibernate.c3p0.timeout">300</property>
        <property name="hibernate.c3p0.max_statements">50</property>
        <property name="hibernate.c3p0.idle_test_period">3000</property>
    </session-factory>
</hibernate-configuration>
```

### 具有Oracle特定功能的JPA实体

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

    // 构造函数、getter和setter
    // ...
}
```

### Spring Boot与Oracle

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

## 性能优化

### 查询优化

```sql
-- 有效使用索引
CREATE INDEX idx_emp_dept_salary ON employees(department_id, salary);

-- 必要时使用提示
SELECT /*+ INDEX(e idx_emp_dept_salary) */
       e.employee_id, e.first_name, e.last_name
FROM employees e
WHERE department_id = 10 AND salary > 50000;

-- 使用绑定变量防止SQL注入并提高性能
SELECT * FROM employees WHERE employee_id = :employee_id;
```

### Java性能提示

```java
// 对多个插入使用批处理
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
        throw new RuntimeException("批插入时出错", e);
    }
}

// 对大型结果集使用适当的获取大小
public List<Employee> getAllEmployeesOptimized() {
    List<Employee> employees = new ArrayList<>();
    String sql = "SELECT * FROM employees ORDER BY employee_id";

    try (Connection conn = ConnectionPoolManager.getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {

        pstmt.setFetchSize(1000); // 优化获取大小
        ResultSet rs = pstmt.executeQuery();

        while (rs.next()) {
            employees.add(mapResultSetToEmployee(rs));
        }

    } catch (SQLException e) {
        throw new RuntimeException("检索员工列表时出错", e);
    }
    return employees;
}
```

## 安全最佳实践

### 连接安全

```java
// 使用加密连接
String url = "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcps)(HOST=localhost)(PORT=2484))(CONNECT_DATA=(SERVICE_NAME=XE)))" +
            "?oracle.net.ssl_client_authentication=false" +
            "&oracle.net.ssl_server_cert_dn=\"CN=localhost\"";

// 使用连接属性进行安全配置
Properties props = new Properties();
props.setProperty("user", username);
props.setProperty("password", password);
props.setProperty("oracle.net.encryption_client", "REQUIRED");
props.setProperty("oracle.net.encryption_types_client", "AES256");
props.setProperty("oracle.net.crypto_checksum_client", "REQUIRED");
props.setProperty("oracle.net.crypto_checksum_types_client", "SHA256");

Connection conn = DriverManager.getConnection(url, props);
```

### SQL注入预防

```java
// 始终使用参数化查询
public Employee findEmployeeByEmail(String email) {
    String sql = "SELECT * FROM employees WHERE email = ?"; // 安全
    // String sql = "SELECT * FROM employees WHERE email = '" + email + "'"; // 危险！

    try (Connection conn = ConnectionPoolManager.getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {

        pstmt.setString(1, email);
        ResultSet rs = pstmt.executeQuery();

        if (rs.next()) {
            return mapResultSetToEmployee(rs);
        }

    } catch (SQLException e) {
        throw new RuntimeException("查找员工时出错", e);
    }
    return null;
}
```

## 监控与维护

### 数据库监控查询

```sql
-- 检查表大小
SELECT table_name,
       ROUND(((num_rows * avg_row_len) / 1024 / 1024), 2) as size_mb
FROM user_tables
ORDER BY size_mb DESC;

-- 监控活动会话
SELECT username, osuser, machine, program, status, logon_time
FROM v$session
WHERE username IS NOT NULL
ORDER BY logon_time;

-- 检查表空间使用情况
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

### 应用程序监控

```java
// 连接池监控
public class ConnectionPoolMonitor {

    public void printPoolStatistics() {
        try {
            oracle.ucp.jdbc.PoolDataSource pds = (oracle.ucp.jdbc.PoolDataSource) poolDataSource;

            System.out.println("=== 连接池统计信息 ===");
            System.out.println("可用连接数: " + pds.getAvailableConnectionsCount());
            System.out.println("借用连接数: " + pds.getBorrowedConnectionsCount());
            System.out.println("峰值池大小: " + pds.getPeakPoolSize());
            System.out.println("连接池大小: " + pds.getPoolSize());
            System.out.println("================================");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

// 查询性能监控
public class QueryPerformanceMonitor {

    public <T> T executeWithTiming(String operationName, Supplier<T> operation) {
        long startTime = System.currentTimeMillis();

        try {
            T result = operation.get();
            long duration = System.currentTimeMillis() - startTime;

            System.out.println(operationName + " 执行时间: " + duration + "毫秒");

            if (duration > 1000) { // 记录慢查询
                System.out.println("检测到慢查询: " + operationName);
            }

            return result;

        } catch (Exception e) {
            System.err.println(operationName + " 出错: " + e.getMessage());
            throw e;
        }
    }
}
```

## 最佳实践总结

### 数据库设计

- 使用适当的数据类型和约束
- 实施适当的索引策略
- 对大表考虑分区
- 对主键使用序列
- 适当规范化数据

### Java开发

- 始终使用连接池
- 实施适当的异常处理
- 使用参数化查询防止SQL注入
- 正确关闭资源（使用try-with-resources）
- 对复杂应用程序考虑使用ORM框架

### 性能

- 监控和优化慢查询
- 对批量数据操作使用批处理操作
- 实施适当的缓存策略
- 监控连接池指标
- 使用适当的获取大小

### 安全

- 在生产环境中使用加密连接
- 实施适当的身份验证和授权
- 切勿硬编码凭据
- 使用最小权限原则
- 定期进行安全审计

本综合指南为在Java应用程序中使用Oracle数据库提供了坚实的基础。请始终参考官方Oracle文档以获取最新的信息和最佳实践。
