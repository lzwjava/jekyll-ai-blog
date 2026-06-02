---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Spring Boot中使用H2数据库进行测试
translated: true
type: note
---

### 在 Spring Boot 的 JUnit 测试中使用 H2 数据库

H2 是一款轻量级内存数据库，特别适合 Java 应用（尤其是 Spring Boot 项目）的单元测试和集成测试。它能让您快速运行测试而无需搭建外部数据库。以下指南假设您正在使用基于 JPA/Hibernate 的 Spring Boot 项目。若未使用 Spring，可通过原生 JDBC 使用 H2（文末附说明）。

#### 第一步：添加 H2 依赖

在 `pom.xml`（Maven）或 `build.gradle`（Gradle）中添加 H2 依赖，并将其作用域限定为 `test` 以避免混入生产环境。

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

此配置将仅限测试执行时加载 H2 JAR 包。

#### 第二步：在测试配置中设置 H2

创建或更新 `src/test/resources/application.properties`（或 `application-test.yml`）指向 H2 数据库，这将覆盖生产环境的数据源配置。

**application.properties:**

```
# H2 数据库配置
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# H2 控制台（可选，用于调试）
spring.h2.console.enabled=true

# JPA/Hibernate 设置
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true
```

- `mem:testdb`：名为 "testdb" 的内存数据库
- `create-drop`：启动时自动建表，关闭时自动清空
- 测试期间可通过 `http://localhost:8080/h2-console` 启用 H2 控制台进行数据查看（需使用 JDBC URL: `jdbc:h2:mem:testdb`）

若使用多环境配置，请在测试类中添加 `@ActiveProfiles("test")` 注解激活配置。

#### 第三步：编写 JUnit 测试

使用 `@SpringBootTest` 进行全上下文测试，或使用 `@DataJpaTest` 进行仓储层专注测试。配合 `@Test` 注解并基于 JUnit 5（`@ExtendWith(SpringExtension.class)`）。

**示例：测试 JPA 仓储**
假设已有 `User` 实体类和继承 `JpaRepository` 的 `UserRepository`。

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest  // 仅加载 JPA 相关组件以加速测试
@ActiveProfiles("test")  // 激活测试配置
public class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    public void shouldSaveAndFindUser() {
        // 准备数据
        User user = new User("John Doe", "john@example.com");
        userRepository.save(user);

        // 执行查询
        User foundUser = userRepository.findByEmail("john@example.com").orElse(null);

        // 验证结果
        assertThat(foundUser).isNotNull();
        assertThat(foundUser.getName()).isEqualTo("John Doe");
    }
}
```

- `@DataJpaTest`：自动配置 H2 并在每个测试后回滚事务
- 使用 `AssertJ` 或 `JUnit` 断言进行验证
- 服务层测试建议使用 `@SpringBootTest` 并注入服务/仓储组件

通过 `mvn test` 或 IDE 测试运行器执行。每个测试都会使用全新的数据库实例。

#### 第四步：进阶技巧

- **Flyway/Liquibase 迁移**：若使用数据库版本管理，将迁移脚本置于 `src/test/resources` 目录下，H2 会自动执行
- **真实环境模拟**：H2 虽兼容多数 SQL 方言，但与生产环境数据库（如 PostgreSQL）存在差异。如需高度一致，可考虑使用 Testcontainers 搭配真实数据库容器
- **排除生产环境配置**：在 `pom.xml` 中使用配置环境排除真实数据库驱动：

  ```xml
  <profile>
      <id>test</id>
      <dependencies>
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-data-jpa</artifactId>
              <exclusions>
                  <exclusion>
                      <groupId>mysql</groupId>  <!-- 或您使用的生产环境数据库 -->
                      <artifactId>mysql-connector-java</artifactId>
                  </exclusion>
              </exclusions>
          </dependency>
      </dependencies>
  </profile>
  ```

- **故障排查**：若测试误连生产数据库，请确认 `spring.profiles.active=test` 或使用 `@TestPropertySource` 注解

#### 独立 JUnit 测试（无 Spring 框架）

使用原生 JDBC 进行测试：

1. 添加 H2 依赖（同上）
2. 在测试类中：

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

此方案会为每个测试创建独立的内存数据库。

更多细节请参考以下文献：

[Spring Boot 测试环境 H2 数据库配置指南](https://medium.com/@paulkunda/setting-up-h2-for-testing-in-spring-boot-245d3a98e405)
[基于内存数据库的自包含测试 | Baeldung](https://www.baeldung.com/spring-jpa-test-in-memory-database)
[Spring Boot 应用测试环境 H2 配置详解](https://medium.com/@akshatakanaje08/setting-up-h2-for-testing-in-spring-boot-application-7f016220a475)
[使用 H2 内存数据库测试 Spring Data 仓储层](https://www.geekyhacker.com/test-spring-data-repositories-with-h2-in-memory-database/)
