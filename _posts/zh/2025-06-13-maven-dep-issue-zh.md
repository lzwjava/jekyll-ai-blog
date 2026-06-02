---
audio: false
generated: true
lang: zh
layout: post
title: Maven依赖问题
translated: true
type: note
---

### 问题概述

用户在使用 Maven 运行 Spring Boot 应用时遇到构建失败。错误信息显示出现了由 `NoClassDefFoundError: org/springframework/beans/factory/aot/BeanRegistrationExcludeFilter` 引起的 `IllegalArgumentException`。这表明项目依赖项中存在版本不兼容问题，导致应用无法正常启动。提供的 `pom.xml` 文件及 Maven 输出为我们提供了诊断和解决问题的上下文。

### 根本原因

该错误的发生是因为 Spring Boot 应用无法实例化 `SharedMetadataReaderFactoryContextInitializer`，该类参与 Spring Boot 的自动配置过程。其根本原因是缺少 `BeanRegistrationExcludeFilter` 类，该类属于 Spring Framework 6.0 及更高版本。项目使用了 Spring Boot 3.4.2，它依赖于 Spring Framework 6.1.14。然而，`pom.xml` 中指定了较旧且不兼容的 Spring Framework 依赖版本，导致了类路径冲突。

以下是 `pom.xml` 中识别出的关键问题：

1. **不兼容的 Spring Boot Maven 插件版本：**
   - `spring-boot-maven-plugin` 被设置为版本 `2.7.0`，该版本是为 Spring Boot 2.x 设计的，而不是 Spring Boot 3.4.2（一个 3.x 版本）。此不匹配可能导致构建和运行时阶段出现问题。

2. **显式声明了不兼容的 Spring Framework 依赖：**
   - `pom.xml` 显式声明了 `spring-aop` 和 `spring-aspects` 的版本为 `5.3.23`（Spring Framework 5.x），而 Spring Boot 3.4.2 要求 Spring Framework 6.1.14。Maven 会优先使用这些显式声明的版本，而不是由 Spring Boot 管理的版本，导致类路径上混合了 Spring Framework 5.x 和 6.x 的组件。这种混合导致了 `NoClassDefFoundError`，因为当加载较旧的 5.x jar 包时，`BeanRegistrationExcludeFilter`（来自 Spring Framework 6.x）不可用。

### 解决方案

为了解决这个问题，我们需要确保项目的所有组件都与 Spring Boot 3.4.2 兼容，并且由 Spring Boot 管理其依赖项的版本以避免冲突。应对 `pom.xml` 进行以下更改：

1. **更新 Spring Boot Maven 插件版本：**
   - 将 `spring-boot-maven-plugin` 的版本从 `2.7.0` 更改为 `3.4.2`，以与项目中使用的 Spring Boot 版本保持一致。

2. **移除显式声明的 Spring Framework 依赖：**
   - 移除显式声明的版本为 `5.3.23` 的 `spring-aop` 和 `spring-aspects` 依赖。Spring Boot 3.4.2 通过其 starter（例如，`spring-boot-starter-web` 包含了正确版本 6.1.14 的 `spring-aop`）来管理这些依赖。通过移除这些显式声明，可以防止 Maven 覆盖 Spring Boot 的依赖管理。

### 更新后的 `pom.xml`

以下是应用了必要更改后的修正版 `pom.xml` 文件：

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

### 更改说明

- **Spring Boot Maven 插件更新：**
  - 在 `spring-boot-maven-plugin` 配置中将 `<version>2.7.0</version>` 更改为 `<version>3.4.2</version>`。这确保了插件与 Spring Boot 3.4.2 兼容，支持 3.x 系列特有的功能和配置。

- **移除 `spring-aop` 和 `spring-aspects`：**
  - 移除了以下依赖项：

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

  - `spring-aop` 已经包含在 `spring-boot-starter-web` 中（通过 `spring-web`），并且 Spring Boot 将其版本管理为 6.1.14，这与 3.4.2 兼容。
  - `spring-aspects` 不是 Spring Boot starter 中的标准依赖项。如果项目明确需要它（例如，用于自定义切面），可以不加版本号重新添加（让 Spring Boot 的依赖管理来处理）或将其版本设置为 `6.1.14`。然而，由于错误发生在启动期间并且与自动配置相关而不是缺少切面功能，因此这里很可能不需要它，可以安全地移除。

### 补充说明

- **AspectJ 依赖：**
  - `aspectjrt` 和 `aspectjweaver` 依赖（版本 1.9.22）保留在 `pom.xml` 中，因为它们与 Spring Framework 6.1.14 兼容，并且如果项目使用 AspectJ 功能，则可能需要它们。这些依赖与 Spring Boot 3.4.2 没有冲突。

- **最佳实践：**
  - 对于 Spring Boot 项目，建议使用 `spring-boot-starter-parent` 作为父 POM 或导入 `spring-boot-dependencies` BOM 来自动管理依赖版本。当前的 `pom.xml` 没有这样做，但此解决方案在不要求此更改的情况下仍然有效，因为当显式覆盖被移除后，`spring-boot-starter-web` 和其他 starter 仍然强制版本一致性。

- **验证：**
  - 应用这些更改后，运行 `mvn clean spring-boot:run` 以验证应用是否在没有错误的情况下启动。如果项目依赖于 `spring-aspects`（例如，用于特定的 AOP 功能），并且移除它导致问题，请将其添加回来，使用 `<version>6.1.14</version>` 或不指定版本并确保正确的依赖管理。

### 结论

通过将 `spring-boot-maven-plugin` 更新到版本 3.4.2 并移除显式的 `spring-aop` 和 `spring-aspects` 依赖，项目将使用一致的 Spring Boot (3.4.2) 和 Spring Framework (6.1.14) 版本。这解决了导致 `NoClassDefFoundError` 的类路径冲突，并允许应用成功启动。
