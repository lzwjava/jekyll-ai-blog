---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Flyway数据库迁移指南
translated: true
type: note
---

### Flyway 简介

Flyway 是一款流行的开源工具，用于以版本控制的方式管理数据库架构迁移。它允许您以可重复且安全的方式对数据库应用增量更改（例如创建表、修改列或插入数据）。在 Java 应用程序中，Flyway 可以通过其 API 集成，通常在应用程序启动时运行，以确保在代码与数据库交互之前数据库架构是最新的。它通过 JDBC 与大多数数据库（例如 PostgreSQL、MySQL、Oracle）协同工作。

### 步骤 1：添加 Flyway 依赖

将 Flyway 添加到您的构建文件中。除非需要企业版功能，否则请使用开源版本。

**Maven (`pom.xml`)**:

```xml
<dependencies>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
        <version>11.14.1</version> <!-- 请检查最新版本 -->
    </dependency>
    <!-- 添加您的数据库 JDBC 驱动，例如 PostgreSQL -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>42.7.3</version>
    </dependency>
</dependencies>
```

**Gradle (`build.gradle`)**:

```groovy
dependencies {
    implementation 'org.flywaydb:flyway-core:11.14.1'
    // 添加您的数据库 JDBC 驱动
    implementation 'org.postgresql:postgresql:42.7.3'
}
```

您还需要目标数据库的 JDBC 驱动。

### 步骤 2：配置 Flyway

Flyway 使用流畅的 API 进行配置。关键设置包括数据库连接详细信息、迁移脚本的位置以及可选的回调。

在您的 Java 代码中，创建一个 `Flyway` 实例：

```java
import org.flywaydb.core.Flyway;

public class DatabaseMigration {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/mydb";
        String user = "username";
        String password = "password";

        Flyway flyway = Flyway.configure()
                .dataSource(url, user, password)
                .locations("classpath:db/migration")  // SQL 脚本的文件夹（默认：db/migration）
                .load();
    }
}
```

- `locations`：指向存储迁移文件的位置（例如，类路径下的 `src/main/resources/db/migration`）。
- 其他常见配置：`.baselineOnMigrate(true)` 用于基线化现有架构，或 `.table("flyway_schema_history")` 用于自定义历史记录表。

### 步骤 3：编写迁移脚本

迁移脚本是 SQL 文件，放置在配置的位置（例如 `src/main/resources/db/migration`）。Flyway 按顺序应用它们。

#### 命名约定

- **版本化迁移**（用于一次性架构更改）：`V<版本>__<描述>.sql`（例如 `V1__Create_person_table.sql`、`V2__Add_age_column.sql`）。
  - 版本格式：使用下划线分隔段（例如 `V1_1__Initial.sql`）。
- **可重复迁移**（用于视图等持续任务）：`R__<描述>.sql`（例如 `R__Update_view.sql`）。如果更改，这些迁移每次都会运行。
- 文件按字典顺序应用。

#### 示例脚本

在 `src/main/resources/db/migration` 中创建这些文件。

**V1__Create_person_table.sql**：

```sql
CREATE TABLE person (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO person (id, name) VALUES (1, 'John Doe');
```

**V2__Add_age_column.sql**：

```sql
ALTER TABLE person ADD COLUMN age INT;
```

**R__Populate_names.sql**（可重复）：

```sql
UPDATE person SET name = CONCAT(name, ' (Updated)') WHERE id = 1;
```

Flyway 在 `flyway_schema_history` 表中跟踪已应用的迁移。

对于不适合 SQL 的复杂逻辑，请使用基于 Java 的迁移（实现 `org.flywaydb.core.api.migration.java.JavaMigration`）。

### 步骤 4：以编程方式运行迁移

调用 `migrate()` 来应用挂起的迁移。将此集成到您的应用程序启动中（例如，在 `main()` 或 Spring 的 `@PostConstruct` 中）。

```java
import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

public class DatabaseMigration {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/mydb";
        String user = "username";
        String password = "password";

        Flyway flyway = Flyway.configure()
                .dataSource(url, user, password)
                .locations("classpath:db/migration")
                .load();

        try {
            flyway.migrate();  // 应用所有挂起的迁移
            System.out.println("数据库迁移成功！");
        } catch (FlywayException e) {
            System.err.println("迁移失败：" + e.getMessage());
            // 处理错误（例如，退出或回滚）
        }

        // 现在启动应用程序的其余部分
    }
}
```

- `migrate()`：按顺序应用版本化迁移，然后是可重复迁移。
- 其他命令：`flyway.info()` 用于查看状态，`flyway.repair()` 用于修复问题，`flyway.validate()` 用于检查一致性。
- 在任何数据库操作之前运行此命令，以确保架构兼容性。

### 最佳实践

- 保持迁移是幂等的（可以安全地重新运行）。
- 在生产数据的副本上测试迁移。
- 对迁移文件使用版本控制。
- 对于 Spring Boot，添加 `spring-boot-starter-jdbc` 并在 `application.properties` 中设置 `spring.flyway.enabled=true` 以进行自动配置。

### 参考资料

- [Flyway API (Java) 文档](https://documentation.red-gate.com/fd/api-java-277579358.html)
- [Flyway 迁移文档](https://documentation.red-gate.com/fd/migrations-271585107.html)
- [Flyway 入门指南](https://documentation.red-gate.com/fd/getting-started-with-flyway-184127223.html)
