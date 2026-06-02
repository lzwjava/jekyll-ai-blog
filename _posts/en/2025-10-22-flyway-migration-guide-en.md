---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Flyway Database Migration Guide
translated: false
type: note
---

### Introduction to Flyway

Flyway is a popular open-source tool for managing database schema migrations in a version-controlled manner. It allows you to apply incremental changes to your database (like creating tables, altering columns, or inserting data) in a repeatable and safe way. In Java applications, Flyway can be integrated via its API, often run on application startup to ensure the database schema is up-to-date before your code interacts with it. It works with most databases via JDBC (e.g., PostgreSQL, MySQL, Oracle).

### Step 1: Add Flyway Dependency

Add Flyway to your build file. Use the open-source edition unless you need enterprise features.

**Maven (`pom.xml`)**:

```xml
<dependencies>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
        <version>11.14.1</version> <!-- Check for the latest version -->
    </dependency>
    <!-- Add your database JDBC driver, e.g., for PostgreSQL -->
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
    // Add your database JDBC driver
    implementation 'org.postgresql:postgresql:42.7.3'
}
```

You'll also need the JDBC driver for your target database.

### Step 2: Configure Flyway

Flyway uses a fluent API for configuration. Key settings include the database connection details, locations for migration scripts, and optional callbacks.

In your Java code, create a `Flyway` instance:

```java
import org.flywaydb.core.Flyway;

public class DatabaseMigration {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/mydb";
        String user = "username";
        String password = "password";

        Flyway flyway = Flyway.configure()
                .dataSource(url, user, password)
                .locations("classpath:db/migration")  // Folder for SQL scripts (default: db/migration)
                .load();
    }
}
```

- `locations`: Points to where your migration files are stored (e.g., `src/main/resources/db/migration` for classpath).
- Other common configs: `.baselineOnMigrate(true)` to baseline existing schemas, or `.table("flyway_schema_history")` to customize the history table.

### Step 3: Write Migration Scripts

Migration scripts are SQL files placed in the configured location (e.g., `src/main/resources/db/migration`). Flyway applies them in order.

#### Naming Conventions

- **Versioned migrations** (for one-time schema changes): `V<version>__<description>.sql` (e.g., `V1__Create_person_table.sql`, `V2__Add_age_column.sql`).
  - Version format: Use underscores for segments (e.g., `V1_1__Initial.sql`).
- **Repeatable migrations** (for ongoing tasks like views): `R__<description>.sql` (e.g., `R__Update_view.sql`). These run every time if changed.
- Files are applied in lexicographical order.

#### Example Scripts

Create these files in `src/main/resources/db/migration`.

**V1__Create_person_table.sql**:

```sql
CREATE TABLE person (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO person (id, name) VALUES (1, 'John Doe');
```

**V2__Add_age_column.sql**:

```sql
ALTER TABLE person ADD COLUMN age INT;
```

**R__Populate_names.sql** (repeatable):

```sql
UPDATE person SET name = CONCAT(name, ' (Updated)') WHERE id = 1;
```

Flyway tracks applied migrations in a `flyway_schema_history` table.

For complex logic not suited to SQL, use Java-based migrations (implement `org.flywaydb.core.api.migration.java.JavaMigration`).

### Step 4: Run Migrations Programmatically

Call `migrate()` to apply pending migrations. Integrate this into your app's startup (e.g., in `main()` or a Spring `@PostConstruct`).

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
            flyway.migrate();  // Applies all pending migrations
            System.out.println("Database migrated successfully!");
        } catch (FlywayException e) {
            System.err.println("Migration failed: " + e.getMessage());
            // Handle error (e.g., exit or rollback)
        }

        // Now start the rest of your application
    }
}
```

- `migrate()`: Applies versioned migrations in order, then repeatables.
- Other commands: `flyway.info()` for status, `flyway.repair()` to fix issues, `flyway.validate()` to check consistency.
- Run this before any database operations to ensure schema compatibility.

### Best Practices

- Keep migrations idempotent (safe to rerun).
- Test migrations on a copy of production data.
- Use version control for migration files.
- For Spring Boot, add `spring-boot-starter-jdbc` and set `spring.flyway.enabled=true` in `application.properties` for auto-configuration.

### References

- [Flyway API (Java) Documentation](https://documentation.red-gate.com/fd/api-java-277579358.html)
- [Flyway Migrations Documentation](https://documentation.red-gate.com/fd/migrations-271585107.html)
- [Flyway Getting Started](https://documentation.red-gate.com/fd/getting-started-with-flyway-184127223.html)
