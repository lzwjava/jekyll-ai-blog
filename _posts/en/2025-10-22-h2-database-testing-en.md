---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Testing with H2 Database in Spring Boot
translated: false
type: note
---

### Using H2 Database in JUnit Tests with Spring Boot

H2 is a lightweight, in-memory database ideal for unit and integration testing in Java applications, especially with Spring Boot. It allows you to run tests quickly without needing an external database setup. Below is a step-by-step guide assuming a Spring Boot project with JPA/Hibernate. If you're not using Spring, you can use H2 via plain JDBC (see notes at the end).

#### Step 1: Add H2 Dependency

Include the H2 dependency in your `pom.xml` (Maven) or `build.gradle` (Gradle). Scope it to `test` to avoid production inclusion.

**Maven (`pom.xml`):**

```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

**Gradle (`build.gradle`):**

```gradle
testImplementation 'com.h2database:h2'
```

This pulls in the H2 JAR for test execution only.

#### Step 2: Configure H2 in Test Properties

Create or update `src/test/resources/application.properties` (or `application-test.yml`) to point to H2. This overrides production DB settings.

**application.properties:**

```
# H2 Database Configuration
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# H2 Console (optional, for debugging)
spring.h2.console.enabled=true

# JPA/Hibernate Settings
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true
```

- `mem:testdb`: In-memory database named "testdb".
- `create-drop`: Auto-creates tables on startup and drops them on shutdown.
- Enable the H2 console at `http://localhost:8080/h2-console` during tests for inspection (use JDBC URL: `jdbc:h2:mem:testdb`).

If using profiles, activate with `@ActiveProfiles("test")` in your test class.

#### Step 3: Write a JUnit Test

Use `@SpringBootTest` for full context or `@DataJpaTest` for repository-focused tests. Annotate with `@Test` and use JUnit 5 (`@ExtendWith(SpringExtension.class)`).

**Example: Testing a JPA Repository**
Assume you have an `Entity` like `User` and a `UserRepository` extending `JpaRepository`.

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest  // Loads only JPA-related beans for faster tests
@ActiveProfiles("test")  // Activates test profile
public class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    public void shouldSaveAndFindUser() {
        // Given
        User user = new User("John Doe", "john@example.com");
        userRepository.save(user);

        // When
        User foundUser = userRepository.findByEmail("john@example.com").orElse(null);

        // Then
        assertThat(foundUser).isNotNull();
        assertThat(foundUser.getName()).isEqualTo("John Doe");
    }
}
```

- `@DataJpaTest`: Auto-configures H2 and rolls back transactions after each test.
- Use `AssertJ` or `JUnit` assertions for verification.
- For service-layer tests, use `@SpringBootTest` and inject services/repositories.

Run with `mvn test` or your IDE's test runner. Each test starts with a fresh DB.

#### Step 4: Advanced Tips

- **Flyway/Liquibase Migration**: If using schema migrations, add them to `src/test/resources` and H2 will apply them.
- **Realistic Testing**: H2 mimics most SQL dialects but may differ from production (e.g., PostgreSQL). For closer matches, consider Testcontainers with a real DB container.
- **Exclude Production Config**: In `pom.xml`, use profiles to exclude real DB drivers in tests:

  ```xml
  <profile>
      <id>test</id>
      <dependencies>
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-data-jpa</artifactId>
              <exclusions>
                  <exclusion>
                      <groupId>mysql</groupId>  <!-- Or your prod DB -->
                      <artifactId>mysql-connector-java</artifactId>
                  </exclusion>
              </exclusions>
          </dependency>
      </dependencies>
  </profile>
  ```

- **Troubleshooting**: If tests use the production DB, ensure `spring.profiles.active=test` or use `@TestPropertySource`.

#### Standalone JUnit (No Spring)

For plain JDBC without Spring:

1. Add H2 dependency (as above).
2. In your test:

```java
import org.h2.jdbcx.JdbcDataSource;
import org.junit.jupiter.api.Test;

public class StandaloneH2Test {
    @Test
    public void testH2Connection() throws Exception {
        JdbcDataSource ds = new JdbcDataSource();
        ds.setURL("jdbc:h2:mem:test;DB_CLOSE_DELAY=-1");
        ds.setUser("sa");
        ds.setPassword("");

        try (Connection conn = ds.getConnection();
             Statement stmt = conn.createStatement()) {
            stmt.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(255))");
            stmt.execute("INSERT INTO users VALUES (1, 'Test User')");
            ResultSet rs = stmt.executeQuery("SELECT * FROM users");
            assertTrue(rs.next());
        }
    }
}
```

This creates an in-memory DB per test.

For more details, see the references below.

[Setting Up H2 for Testing in Spring Boot](https://medium.com/@paulkunda/setting-up-h2-for-testing-in-spring-boot-245d3a98e405)
[Self-Contained Testing Using an In-Memory Database | Baeldung](https://www.baeldung.com/spring-jpa-test-in-memory-database)
[Setting Up H2 for Testing in Spring Boot application](https://medium.com/@akshatakanaje08/setting-up-h2-for-testing-in-spring-boot-application-7f016220a475)
[Test Spring Data Repositories with H2 in-memory database](https://www.geekyhacker.com/test-spring-data-repositories-with-h2-in-memory-database/)
