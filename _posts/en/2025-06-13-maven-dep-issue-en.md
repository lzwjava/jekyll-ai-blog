---
audio: false
generated: true
lang: en
layout: post
title: Maven Dependency Issue
translated: false
type: note
---

### Problem Overview

The user is encountering a build failure when running a Spring Boot application using Maven. The error message indicates an `IllegalArgumentException` caused by `NoClassDefFoundError: org/springframework/beans/factory/aot/BeanRegistrationExcludeFilter`. This suggests a version incompatibility issue within the project's dependencies, preventing the application from starting correctly. The provided `pom.xml` file and Maven output give us the context needed to diagnose and resolve the issue.

### Root Cause

The error occurs because the Spring Boot application is unable to instantiate `SharedMetadataReaderFactoryContextInitializer`, a class involved in Spring Boot's auto-configuration process. The underlying cause is a missing class, `BeanRegistrationExcludeFilter`, which is part of Spring Framework 6.0 and later. The project uses Spring Boot 3.4.2, which depends on Spring Framework 6.1.14. However, the `pom.xml` specifies older, incompatible versions of Spring Framework dependencies, leading to a classpath conflict.

Here are the key issues identified in the `pom.xml`:

1. **Incompatible Spring Boot Maven Plugin Version:**
   - The `spring-boot-maven-plugin` is set to version `2.7.0`, which is designed for Spring Boot 2.x, not Spring Boot 3.4.2 (a 3.x version). This mismatch can cause issues during the build and runtime phases.

2. **Explicit Incompatible Spring Framework Dependencies:**
   - The `pom.xml` explicitly declares `spring-aop` and `spring-aspects` with version `5.3.23` (Spring Framework 5.x), while Spring Boot 3.4.2 requires Spring Framework 6.1.14. Maven prioritizes these explicitly declared versions over the versions managed by Spring Boot, resulting in a mix of Spring Framework 5.x and 6.x on the classpath. This mix causes the `NoClassDefFoundError` because `BeanRegistrationExcludeFilter` (from Spring Framework 6.x) is unavailable when older 5.x jars are loaded.

### Solution

To resolve the issue, we need to ensure that all components of the project are compatible with Spring Boot 3.4.2 and that Spring Boot manages the versions of its dependencies to avoid conflicts. The following changes should be made to the `pom.xml`:

1. **Update the Spring Boot Maven Plugin Version:**
   - Change the `spring-boot-maven-plugin` version from `2.7.0` to `3.4.2` to align with the Spring Boot version used in the project.

2. **Remove Explicit Spring Framework Dependencies:**
   - Remove the explicit declarations of `spring-aop` and `spring-aspects` with version `5.3.23`. Spring Boot 3.4.2 manages these dependencies via its starters (e.g., `spring-boot-starter-web` includes `spring-aop` with the correct version, 6.1.14). By removing these, we prevent Maven from overriding Spring Boot's dependency management.

### Updated `pom.xml`

Below is the corrected `pom.xml` file with the necessary changes applied:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.lzwjava</groupId>
    <artifactId>blog-server</artifactId>
    <version>1.0</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.4.2</version>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>5.9.3</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>5.9.3</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-core</artifactId>
            <version>5.3.1</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>3.4.2</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjrt</artifactId>
            <version>1.9.22</version>
        </dependency>
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
            <version>1.9.22</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>3.4.2</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0-M8</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-checkstyle-plugin</artifactId>
                <version>3.1.1</version>
                <configuration>
                    <configLocation>google_checks.xml</configLocation>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>check</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### Explanation of Changes

- **Spring Boot Maven Plugin Update:**
  - Changed `<version>2.7.0</version>` to `<version>3.4.2</version>` in the `spring-boot-maven-plugin` configuration. This ensures the plugin is compatible with Spring Boot 3.4.2, supporting features and configurations specific to the 3.x series.

- **Removal of `spring-aop` and `spring-aspects`:**
  - Removed the following dependencies:
    ```xml
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-aop</artifactId>
        <version>5.3.23</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-aspects</artifactId>
        <version>5.3.23</version>
    </dependency>
    ```
  - `spring-aop` is already included in `spring-boot-starter-web` (via `spring-web`), and Spring Boot manages its version to 6.1.14, which is compatible with 3.4.2.
  - `spring-aspects` is not a standard dependency in Spring Boot starters. If the project explicitly requires it (e.g., for custom aspects), it can be re-added without a version (letting Spring Boot's dependency management handle it) or set to `6.1.14`. However, since the error occurs during startup and relates to auto-configuration rather than missing aspects, it’s likely unnecessary here and can be safely removed.

### Additional Notes

- **AspectJ Dependencies:**
  - The `aspectjrt` and `aspectjweaver` dependencies (version 1.9.22) remain in the `pom.xml` as they are compatible with Spring Framework 6.1.14 and may be required if the project uses AspectJ features. These do not conflict with Spring Boot 3.4.2.

- **Best Practices:**
  - For Spring Boot projects, it’s recommended to use the `spring-boot-starter-parent` as the parent POM or import the `spring-boot-dependencies` BOM to manage dependency versions automatically. The current `pom.xml` does neither, but the solution works without requiring this change since `spring-boot-starter-web` and other starters still enforce version consistency when explicit overrides are removed.

- **Verification:**
  - After applying these changes, run `mvn clean spring-boot:run` to verify that the application starts without errors. If the project relies on `spring-aspects` (e.g., for specific AOP functionality), and removing it causes issues, add it back with `<version>6.1.14</version>` or omit the version and ensure proper dependency management.

### Conclusion

By updating the `spring-boot-maven-plugin` to version 3.4.2 and removing the explicit `spring-aop` and `spring-aspects` dependencies, the project will use consistent versions of Spring Boot (3.4.2) and Spring Framework (6.1.14). This resolves the classpath conflict causing the `NoClassDefFoundError` and allows the application to start successfully.
