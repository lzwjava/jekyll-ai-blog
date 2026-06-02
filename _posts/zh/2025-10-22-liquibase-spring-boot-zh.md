---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Liquibase与Spring Boot集成指南
translated: true
type: note
---

## 将 Liquibase 与 Spring Boot 集成

Liquibase 是一种流行的开源工具，用于以版本控制的方式管理数据库模式变更（迁移）。Spring Boot 为 Liquibase 提供了出色的自动配置支持，使其易于集成。本指南假设您使用的是 Spring Boot 3.x（截至 2025 年的最新版本）和 Maven，但这些概念同样适用于 Gradle。我们将逐步介绍基础知识。

### 前提条件

- 已设置好的 Spring Boot 项目（例如，通过 Spring Initializr 创建）。
- 在 `application.properties` 中配置好的数据库（例如，用于测试的 H2，用于生产环境的 PostgreSQL/MySQL）。

### 步骤 1：添加 Liquibase 依赖

在您的 `pom.xml` 中包含 Liquibase Spring Boot starter。这会引入 Liquibase 并将其无缝集成。

```xml
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId> <!-- 用于数据库连接 -->
</dependency>
```

对于 Gradle，请添加到 `build.gradle`：

```groovy
implementation 'org.liquibase:liquibase-core'
implementation 'org.springframework.boot:spring-boot-starter-jdbc'
```

运行 `mvn clean install`（或 `./gradlew build`）以下载依赖项。

### 步骤 2：配置 Liquibase

如果您将变更日志文件放在默认位置，Spring Boot 会自动检测 Liquibase。通过 `application.properties`（或等效的 `.yml` 文件）进行自定义。

示例 `application.properties`：

```properties
# 数据库设置（根据您的数据库进行调整）
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# Liquibase 配置
spring.liquibase.change-log=classpath:db/changelog/db.changelog-master.xml
spring.liquibase.enabled=true  # 默认为 true
spring.liquibase.drop-first=false  # 在开发环境中设置为 true，以便在启动时删除模式
```

- `change-log`：您的主变更日志文件的路径（默认：`db/changelog/db.changelog-master.xml`）。
- 使用 `spring.liquibase.enabled` 启用/禁用。
- 对于上下文/配置文件，使用 `spring.liquibase.contexts=dev` 来运行特定的变更。

### 步骤 3：创建变更日志文件

Liquibase 使用“变更日志”来定义模式变更。在 `src/main/resources` 下创建目录结构：

```
src/main/resources/
└── db/
    └── changelog/
        ├── db.changelog-master.xml  # 包含其他文件的主文件
        └── changes/
            ├── 001-create-users-table.xml  # 单个变更
            └── 002-add-email-column.xml
```

#### 主变更日志 (`db.changelog-master.xml`)

此文件包含其他变更日志：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
                        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.24.xsd">

    <include file="changes/001-create-users-table.xml"/>
    <include file="changes/002-add-email-column.xml"/>
</databaseChangeLog>
```

#### 示例变更 (`001-create-users-table.xml`)

定义一个表创建：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
                                       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.24.xsd">

    <changeSet id="001" author="yourname">
        <createTable tableName="users">
            <column name="id" type="bigint">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="name" type="varchar(255)">
                <constraints nullable="false"/>
            </column>
        </createTable>
    </changeSet>
</databaseChangeLog>
```

- 使用 XML、YAML、JSON 或 SQL 格式作为变更日志。
- 每个 `<changeSet>` 是一个迁移，具有一个 ID（用于跟踪）。
- 运行 `java -jar target/your-app.jar` 启动应用程序——Liquibase 在引导时自动应用变更。

### 步骤 4：运行和测试

- **启动时**：Spring Boot 在您的应用程序完全启动之前运行 Liquibase。
- **回滚**：使用 `spring.liquibase.rollback-file` 或 CLI 进行测试。
- **CLI 集成**：对于手动运行，添加 Liquibase Maven 插件：

  ```xml
  <plugin>
      <groupId>org.liquibase</groupId>
      <artifactId>liquibase-maven-plugin</artifactId>
      <version>4.24.0</version>
      <configuration>
          <changeLogFile>src/main/resources/db/changelog/db.changelog-master.xml</changeLogFile>
          <url>jdbc:h2:mem:testdb</url>
          <username>sa</username>
          <password></password>
      </configuration>
  </plugin>
  ```

  然后运行 `mvn liquibase:update`。

- **验证**：启用 `spring.liquibase.validate-on-migrate=true` 以检查变更日志。

### 常见技巧

- **配置文件**：如果需要，在 bean 上使用 `@Profile("dev")`，但除非经过过滤，否则 Liquibase 会全局运行。
- **前置条件**：在变更集中添加 `<preConditions>` 以检查数据库状态。
- **SQL 格式**：对于原始 SQL，创建 `.sql` 文件并将其包含在内：`<sqlFile path="changes/create-users.sql" relativeToChangelogFile="true"/>`。
- **故障排除**：检查日志中的错误（例如，以 `liquibase` 为前缀）。确保数据库 URL 正确。
- **生产环境**：如果您愿意，可以使用 Flyway，但 Liquibase 在处理复杂变更和多数据库支持方面表现出色。

有关高级功能（如标记回滚或自定义扩展），请参阅文档。

### 参考资料

- [Spring Boot Liquibase 自动配置](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#io.liquibase)
- [Liquibase 官方文档](https://docs.liquibase.com/start/home.html)
- [Baeldung Spring Boot + Liquibase 教程](https://www.baeldung.com/liquibase-refactor-schema-of-jpa-entity-in-spring-boot)
