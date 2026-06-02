---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Spring 测试中模拟 DB2 JDBC
translated: true
type: note
---

问题：如何在 Java Spring 项目中使用 Mockito 和其他测试工具 mock IBM DB2 JDBC 数据库？

回答：

在 Spring 项目中 mock 或替换 IBM DB2 JDBC 数据库进行测试有多种策略。每种策略都有不同的权衡权衡。以下是涵盖所有主要方法的全面指南。

---

## 策略概述

| 方法 | 最适合 | 需要 DB2 依赖吗？ |
|---|---|---|
| Mockito (mock JDBC 层) | 纯单元测试 | 否 |
| Mock JdbcTemplate | Service/DAO 单元测试 | 否 |
| H2 In-Memory DB | 集成测试 | 否 |
| Testcontainers (真实 DB2) | 需要真实 DB2 方言的集成测试 | 是 (Docker) |

---

## 方法 1：使用 Mockito mock JDBC 对象（纯单元测试）

您可以 mock 关键的 JDBC 组件 — `DataSource`、`Connection`、`PreparedStatement` 和 `ResultSet` — 来隔离测试业务逻辑，而无需实际的数据库连接。

**Maven Dependencies:**

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

**示例：Mocking DataSource → Connection → PreparedStatement → ResultSet**

您分别 mock `DataSource`、`Connection`、`PreparedStatement` 和 `ResultSet`，然后将它们串联起来，使得 `ds.getConnection()` 返回 `c`，`c.prepareStatement(any())` 返回 `stmt`。

```java
@ExtendWith(MockitoExtension.class)
public class EmployeeDaoTest {

    @Mock
    private DataSource dataSource;

    @Mock
    private Connection connection;

    @Mock
    private PreparedStatement preparedStatement;

    @Mock
    private ResultSet resultSet;

    @InjectMocks
    private EmployeeDao employeeDao;

    @BeforeEach
    void setUp() throws Exception {
        when(dataSource.getConnection()).thenReturn(connection);
        when(connection.prepareStatement(any(String.class))).thenReturn(preparedStatement);
        when(preparedStatement.executeQuery()).thenReturn(resultSet);
    }

    @Test
    void testFindEmployee() throws Exception {
        // Simulate a single row in ResultSet
        when(resultSet.next()).thenReturn(true, false);
        when(resultSet.getInt("id")).thenReturn(42);
        when(resultSet.getString("name")).thenReturn("John Doe");

        Employee emp = employeeDao.findById(42);

        assertNotNull(emp);
        assertEquals("John Doe", emp.getName());
        verify(preparedStatement).setInt(1, 42);
    }
}
```

**注意的限制：**

这些测试往往脆弱且冗长。JDBC 具有低级、命令式 API，mock 它需要仔细模拟每个交互。这会使测试难以维护，并且当底层 SQL 逻辑更改时容易出错。此外，mock JDBC 不会测试与数据库的实际集成 — 仅测试您的代码如何与 mock 交互。

---

## 方法 2：直接 Mock JdbcTemplate（适用于 Spring 的更简单方法）

您可以 mock `JdbcTemplate` 对象来测试方法功能。首先使用 `@Mock` 注解声明一个 mock `JdbcTemplate`，然后使用 `ReflectionTestUtils` 将其注入 DAO。然后使用 `Mockito.when()` 来 mock 查询的返回结果 — 这允许在不连接数据库的情况下进行测试。

```java
@ExtendWith(MockitoExtension.class)
public class EmployeeServiceTest {

    @Mock
    private JdbcTemplate jdbcTemplate;

    @InjectMocks
    private EmployeeService employeeService;

    @Test
    void testGetEmployeeCount() {
        // Mock exact SQL match
        when(jdbcTemplate.queryForObject(
            "SELECT COUNT(*) FROM EMPLOYEE", Integer.class))
            .thenReturn(5);

        assertEquals(5, employeeService.getCount());
    }

    @Test
    void testGetEmployeeCountWithAnyString() {
        // Use anyString() for flexibility
        when(jdbcTemplate.queryForObject(
            anyString(), eq(Integer.class)))
            .thenReturn(10);

        assertEquals(10, employeeService.getCount());
    }
}
```

如果 `JdbcTemplate` 是私有字段（非构造函数注入），则像这样注入：

```java
ReflectionTestUtils.setField(employeeService, "jdbcTemplate", jdbcTemplate);
```

---

## 方法 3：H2 In-Memory Database（推荐用于集成测试）

此方法在测试期间完全用轻量级的内存 H2 数据库替换 DB2。它最易维护，且无需 mock 样板代码。

**Maven Dependencies:**

```xml
<!-- Main DB2 driver (runtime scope only in production) -->
<dependency>
    <groupId>com.ibm.db2</groupId>
    <artifactId>jcc</artifactId>
    <scope>runtime</scope>
</dependency>

<!-- H2 for tests -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

**`src/test/resources/application.properties`:**

```properties
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=DB2
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=create-drop
spring.sql.init.mode=always
```

> **注意：** H2 支持 `MODE=DB2` 兼容模式，这使其模拟许多 DB2 特定的 SQL 行为。这减少了由方言差异引起的测试失败。

**使用 `@JdbcTest` 的集成测试：**

`@JdbcTest` 是 Spring Boot 注解，它使用 H2 数据库和 `JdbcTemplate` bean 启动测试。您可以使用 `@Sql` 指定在测试前运行的 SQL 文件。

```java
@JdbcTest
@Sql({"classpath:schema.sql", "classpath:test-data.sql"})
class EmployeeDaoIntegrationTest {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void whenUsingH2_thenReturnCorrectCount() {
        EmployeeDao dao = new EmployeeDao();
        dao.setJdbcTemplate(jdbcTemplate);
        assertEquals(4, dao.getCount());
    }
}
```

**`src/test/resources/schema.sql`:**

```sql
CREATE TABLE EMPLOYEE (
    ID INT PRIMARY KEY,
    NAME VARCHAR(100),
    DEPARTMENT VARCHAR(50)
);
```

**`src/test/resources/test-data.sql`:**

```sql
INSERT INTO EMPLOYEE VALUES (1, 'Alice', 'Engineering');
INSERT INTO EMPLOYEE VALUES (2, 'Bob', 'HR');
```

---

## 方法 4：使用 Spring Profiles 切换 DataSource

您可以定义一个带有 `@Profile("test")` 注解的测试专用 `DataSource` bean，使用 H2。然后在 JUnit 测试类中指定 `@ActiveProfiles("test")` 来激活它。

```java
@Configuration
public class TestDataSourceConfig {

    @Bean
    @Profile("test")
    public DataSource dataSource() {
        DriverManagerDataSource ds = new DriverManagerDataSource();
        ds.setDriverClassName("org.h2.Driver");
        ds.setUrl("jdbc:h2:mem:db2test;MODE=DB2;DB_CLOSE_DELAY=-1");
        ds.setUsername("sa");
        ds.setPassword("");
        return ds;
    }
}
```

```java
@SpringBootTest
@ActiveProfiles("test")
public class EmployeeServiceIntegrationTest {
    @Autowired
    private EmployeeService employeeService;

    @Test
    void testFindAll() {
        assertNotNull(employeeService.findAll());
    }
}
```

---

## 方法 5：使用 Testcontainers 和真实 DB2（最忠实）

当需要 DB2 特定 SQL（存储过程、特殊类型）以获得最大测试保真度时，使用 Testcontainers 来启动真实的 DB2 Docker 实例。

**Maven Dependency:**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>db2</artifactId>
    <scope>test</scope>
</dependency>
```

**测试类：**

```java
@SpringBootTest
@Testcontainers
class EmployeeRepositoryDb2Test {

    @Container
    static Db2Container db2 = new Db2Container("ibmcom/db2:11.5.8.0")
        .acceptLicense();

    @DynamicPropertySource
    static void setDatasource(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", db2::getJdbcUrl);
        registry.add("spring.datasource.username", db2::getUsername);
        registry.add("spring.datasource.password", db2::getPassword);
    }

    @Autowired
    private EmployeeRepository repository;

    @Test
    void testFindAll() {
        assertFalse(repository.findAll().isEmpty());
    }
}
```

---

## 选择正确的方法

- **单元测试（快速，无 DB）** → 使用 **Mockito** mock `JdbcTemplate` 或 JDBC 接口。
- **集成测试（SQL 兼容性重要）** → 使用 **H2 with MODE=DB2**。
- **使用真实 DB2 SQL 方言的全保真度** → 使用 **Testcontainers**。
- **现有的基于 JNDI 的 DataSource 配置** → 使用 Spring 的基于 profile 的 `DataSource` bean 切换。

一个最佳实践是引入数据访问抽象层（DAO 或 Repository 接口），并为服务层编写使用 mock 的单元测试，同时单独针对真实（或内存）数据库测试 DAO 或 repository。这减少了对低级 JDBC 调用的 mock 需求，并促进更好的关注点分离。

References:

- [Spring JdbcTemplate Unit Testing – Baeldung](https://www.baeldung.com/spring-jdbctemplate-testing)
- [Mocking JDBC for Unit Testing – Baeldung](https://www.baeldung.com/mocking-jdbc-unit-testing)
- [Mocking JDBC Components in Unit Tests with Mockito – Java Code Geeks](https://www.javacodegeeks.com/mocking-jdbc-components-in-unit-tests-with-mockito.html)
- [Mockito Basic Example Using JDBC – DZone](https://dzone.com/articles/mockito-basic-example-using-jdbc)
- [Configuring Separate Spring DataSource for Tests – Baeldung](https://www.baeldung.com/spring-testing-separate-data-source)
- [Replace H2 with Real Database for Testing – Testcontainers Guide](https://testcontainers.com/guides/replace-h2-with-real-database-for-testing/)
- [Connect Java Spring Boot to Db2 Database – Baeldung](https://www.baeldung.com/java-spring-boot-db2-database)
