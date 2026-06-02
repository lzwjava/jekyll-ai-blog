---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Integrating Liquibase with Spring Boot
translated: false
type: note
---

## Integrating Liquibase with Spring Boot

Liquibase is a popular open-source tool for managing database schema changes (migrations) in a version-controlled way. Spring Boot provides excellent auto-configuration support for Liquibase, making it easy to integrate. This guide assumes you're using Spring Boot 3.x (the latest as of 2025) with Maven, but the concepts apply to Gradle too. We'll cover the basics step by step.

### Prerequisites

- A Spring Boot project set up (e.g., via Spring Initializr).
- A database (e.g., H2 for testing, PostgreSQL/MySQL for production) configured in `application.properties`.

### Step 1: Add Liquibase Dependency

Include the Liquibase Spring Boot starter in your `pom.xml`. This pulls in Liquibase and integrates it seamlessly.

```xml
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId> <!-- For database connectivity -->
</dependency>
```

For Gradle, add to `build.gradle`:

```groovy
implementation 'org.liquibase:liquibase-core'
implementation 'org.springframework.boot:spring-boot-starter-jdbc'
```

Run `mvn clean install` (or `./gradlew build`) to fetch dependencies.

### Step 2: Configure Liquibase

Spring Boot auto-detects Liquibase if you place changelog files in the default location. Customize via `application.properties` (or `.yml` equivalent).

Example `application.properties`:

```properties
# Database setup (adjust for your DB)
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# Liquibase configuration
spring.liquibase.change-log=classpath:db/changelog/db.changelog-master.xml
spring.liquibase.enabled=true  # Default is true
spring.liquibase.drop-first=false  # Set to true for dev to drop schema on startup
```

- `change-log`: Path to your master changelog file (default: `db/changelog/db.changelog-master.xml`).
- Enable/disable with `spring.liquibase.enabled`.
- For contexts/profiles, use `spring.liquibase.contexts=dev` to run specific changes.

### Step 3: Create Changelog Files

Liquibase uses "changelogs" to define schema changes. Create a directory structure under `src/main/resources`:

```
src/main/resources/
└── db/
    └── changelog/
        ├── db.changelog-master.xml  # Master file including others
        └── changes/
            ├── 001-create-users-table.xml  # Individual changes
            └── 002-add-email-column.xml
```

#### Master Changelog (`db.changelog-master.xml`)

This includes other changelogs:

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

#### Sample Change (`001-create-users-table.xml`)

Define a table creation:

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

- Use XML, YAML, JSON, or SQL formats for changelogs.
- Each `<changeSet>` is a migration with an ID (for tracking).
- Run `java -jar target/your-app.jar` to start the app—Liquibase applies changes automatically on bootstrap.

### Step 4: Running and Testing

- **On Startup**: Spring Boot runs Liquibase before your app fully starts.
- **Rollback**: Use `spring.liquibase.rollback-file` or CLI for testing.
- **CLI Integration**: For manual runs, add the Liquibase Maven plugin:

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

  Then run `mvn liquibase:update`.

- **Validation**: Enable `spring.liquibase.validate-on-migrate=true` to check changelogs.

### Common Tips

- **Profiles**: Use `@Profile("dev")` on beans if needed, but Liquibase runs globally unless filtered.
- **Preconditions**: Add `<preConditions>` in changesets to check DB state.
- **SQL Format**: For raw SQL, create `.sql` files and include them: `<sqlFile path="changes/create-users.sql" relativeToChangelogFile="true"/>`.
- **Troubleshooting**: Check logs for errors (e.g., `liquibase` prefixed). Ensure DB URL is correct.
- **Production**: Use Flyway if you prefer, but Liquibase excels with complex changes and multi-DB support.

For advanced features like tagged rollbacks or custom extensions, refer to the docs.

### References

- [Spring Boot Liquibase Auto-Configuration](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#io.liquibase)
- [Liquibase Official Documentation](https://docs.liquibase.com/start/home.html)
- [Baeldung Spring Boot + Liquibase Tutorial](https://www.baeldung.com/liquibase-refactor-schema-of-jpa-entity-in-spring-boot)
