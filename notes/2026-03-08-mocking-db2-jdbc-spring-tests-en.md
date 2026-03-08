---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mocking DB2 JDBC in Spring Tests
translated: false
type: note
---

Question: How do I mock an IBM DB2 JDBC database in a Java Spring project using Mockito and other testing tools?

Answer:

There are several strategies to mock or replace an IBM DB2 JDBC database during testing in a Spring project. Each has different trade-offs. Here is a comprehensive guide covering all major approaches.

---

## Strategy Overview

| Approach | Best For | DB2 Dependency Needed? |
|---|---|---|
| Mockito (mock JDBC layer) | Pure unit tests | No |
| Mock JdbcTemplate | Service/DAO unit tests | No |
| H2 In-Memory DB | Integration tests | No |
| Testcontainers (real DB2) | Integration tests needing real DB2 dialect | Yes (Docker) |

---

## Approach 1: Mock JDBC Objects with Mockito (Pure Unit Test)

You can mock key JDBC components — `DataSource`, `Connection`, `PreparedStatement`, and `ResultSet` — to test business logic in isolation without needing an actual database connection.

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

**Example: Mocking DataSource → Connection → PreparedStatement → ResultSet**

You mock `DataSource`, `Connection`, `PreparedStatement`, and `ResultSet` separately, then chain them together so that `ds.getConnection()` returns `c`, and `c.prepareStatement(any())` returns `stmt`.

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

**Limitations to be aware of:**

These tests tend to be fragile and verbose. JDBC has a low-level, imperative API, and mocking it requires carefully simulating every interaction. This can make tests difficult to maintain and prone to errors when the underlying SQL logic changes. Also, mocking JDBC does not test actual integration with the database — only how your code interacts with the mocks.

---

## Approach 2: Mock JdbcTemplate Directly (Simpler for Spring)

You can mock the `JdbcTemplate` object to test method functionality. First declare a mock `JdbcTemplate` with the `@Mock` annotation, then inject it into the DAO using `ReflectionTestUtils`. Then use `Mockito.when()` to mock the return result of the query — this allows testing without connecting to a database.

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

If the `JdbcTemplate` is a private field (not constructor-injected), inject it like this:

```java
ReflectionTestUtils.setField(employeeService, "jdbcTemplate", jdbcTemplate);
```

---

## Approach 3: H2 In-Memory Database (Recommended for Integration Tests)

This approach replaces DB2 entirely during tests with a lightweight in-memory H2 database. It is the easiest to maintain and requires no mocking boilerplate.

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

> **Note:** H2 supports a `MODE=DB2` compatibility mode, which makes it emulate many DB2-specific SQL behaviors. This reduces test failures caused by dialect differences.

**Integration Test using `@JdbcTest`:**

`@JdbcTest` is a Spring Boot annotation that bootstraps a test with an H2 database and a `JdbcTemplate` bean. You can use `@Sql` to specify SQL files to run before the test.

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

## Approach 4: Use Spring Profiles to Swap DataSources

You can define a test-specific `DataSource` bean annotated with `@Profile("test")` that uses H2. Then in your JUnit test class, specify `@ActiveProfiles("test")` to activate it.

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

## Approach 5: Testcontainers with Real DB2 (Most Faithful)

For maximum test fidelity when DB2-specific SQL is required (stored procedures, special types), use Testcontainers to spin up a real DB2 Docker instance.

**Maven Dependency:**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>db2</artifactId>
    <scope>test</scope>
</dependency>
```

**Test Class:**

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

## Choosing the Right Approach

- **Unit test (fast, no DB)** → Use **Mockito** to mock `JdbcTemplate` or JDBC interfaces.
- **Integration test (SQL compatibility matters)** → Use **H2 with MODE=DB2**.
- **Full fidelity with real DB2 SQL dialect** → Use **Testcontainers**.
- **Existing JNDI-based DataSource config** → Use Spring's profile-based `DataSource` bean swap.

A best practice is to introduce a data access abstraction layer (DAO or Repository interfaces) and write unit tests for the service layer using mocks, while separately testing the DAO or repository against a real (or in-memory) database. This reduces the need to mock low-level JDBC calls and promotes better separation of concerns.

References:

- [Spring JdbcTemplate Unit Testing – Baeldung](https://www.baeldung.com/spring-jdbctemplate-testing)
- [Mocking JDBC for Unit Testing – Baeldung](https://www.baeldung.com/mocking-jdbc-unit-testing)
- [Mocking JDBC Components in Unit Tests with Mockito – Java Code Geeks](https://www.javacodegeeks.com/mocking-jdbc-components-in-unit-tests-with-mockito.html)
- [Mockito Basic Example Using JDBC – DZone](https://dzone.com/articles/mockito-basic-example-using-jdbc)
- [Configuring Separate Spring DataSource for Tests – Baeldung](https://www.baeldung.com/spring-testing-separate-data-source)
- [Replace H2 with Real Database for Testing – Testcontainers Guide](https://testcontainers.com/guides/replace-h2-with-real-database-for-testing/)
- [Connect Java Spring Boot to Db2 Database – Baeldung](https://www.baeldung.com/java-spring-boot-db2-database)