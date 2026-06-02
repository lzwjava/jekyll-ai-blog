---
audio: false
generated: true
lang: zh
layout: post
title: Liquibase：数据库架构管理
translated: true
type: note
---

以下是关于如何在 Spring Boot 应用中使用 **Liquibase** 有效管理数据库架构变更的完整指南：

---

### 1. 添加 Liquibase 依赖

首先需要在项目中引入 Liquibase 依赖。如果使用 **Maven**，请在 `pom.xml` 中添加：

```xml
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
```

如果使用 **Gradle**，请在 `build.gradle` 中添加：

```groovy
implementation 'org.liquibase:liquibase-core'
```

这会将 Liquibase 核心库引入项目。

---

### 2. 配置 Liquibase

Liquibase 使用 **变更日志文件** 来管理数据库架构变更。默认情况下，Spring Boot 会在类路径中查找名为 `db/changelog/db.changelog-master.yaml`、`db/changelog/db.changelog-master.xml` 或 `db/changelog/db.changelog-master.sql` 的文件。你可以通过向 `application.properties`（或 `application.yml`）添加属性来自定义位置：

```properties
spring.liquibase.change-log=classpath:/db/changelog/db.changelog-master.xml
```

这会告知 Spring Boot 变更日志文件的存储位置。

---

### 3. 创建变更日志文件

变更日志文件用于定义要应用于数据库的变更。支持 XML、YAML 或 SQL 格式。以下是一个位于 `src/main/resources/db/changelog/db.changelog-master.xml` 的 **XML 变更日志** 示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">

    <changeSet id="1" author="your-name">
        <createTable tableName="users">
            <column name="id" type="int">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="username" type="varchar(255)"/>
            <column name="email" type="varchar(255)"/>
        </createTable>
    </changeSet>

</databaseChangeLog>
```

此示例创建了包含三列（`id`、`username` 和 `email`）的 `users` 表。每个 `<changeSet>` 代表一组要应用的变更。

---

### 4. 运行 Spring Boot 应用

启动 Spring Boot 应用时，Liquibase 会自动执行以下操作：

- 读取变更日志文件
- 检查已应用的变更集（通过 `DATABASECHANGELOG` 表记录）
- 对数据库执行新增的变更集

无需编写额外代码——Spring Boot 的自动配置会处理这些操作。

---

### 5. 自定义 Liquibase（可选）

可通过 `application.properties` 中的属性调整 Liquibase 行为。常用配置如下：

```properties
spring.liquibase.enabled=true          # 启用或禁用 Liquibase
spring.liquibase.drop-first=false      # 应用变更前清空数据库（慎用）
spring.liquibase.contexts=dev,prod     # 仅在特定环境中运行变更集
```

这些设置可帮助适配不同环境或工作流程。

---

### 6. 使用高级功能

Liquibase 提供增强架构管理的强大功能：

- **上下文与标签**：控制特定环境（如 `dev` 与 `prod`）中运行的变更集
- **前置条件**：确保应用变更集前满足特定条件（如表已存在）
- **回滚**：定义撤销变更集的方式
- **重构**：支持复杂数据库变更（如列重命名）

例如为变更集添加上下文：

```xml
<changeSet id="2" author="your-name" context="dev">
    <addColumn tableName="users">
        <column name="created_at" type="timestamp"/>
    </addColumn>
</changeSet>
```

此变更集仅在 `dev` 上下文中运行。

---

### 7. 使用内存数据库测试

测试时可将 Liquibase 与 H2 等内存数据库结合。添加 H2 依赖：

```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

然后在 `application.properties` 中配置测试参数：

```properties
spring.datasource.url=jdbc:h2:mem:testdb
spring.liquibase.change-log=classpath:/db/changelog/db.changelog-master.xml
```

测试期间 Liquibase 会将变更应用到内存数据库。

---

### 8. 版本控制变更日志

将变更日志文件与应用程序代码共同存储在版本控制系统（如 Git）中。这能确保数据库架构与代码库协同演进，使部署和回滚更可控。

---

### 总结

在 Spring Boot 应用中使用 Liquibase 的步骤：

1. 添加 Liquibase 依赖
2. 配置变更日志文件路径
3. 创建包含数据库变更的日志文件
4. 运行应用——Liquibase 将自动处理剩余流程

Liquibase 作为强大的数据库架构变更管理工具，通过结构化、版本控制的方式与 Spring Boot 无缝集成。
