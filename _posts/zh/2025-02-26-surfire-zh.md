---
audio: false
generated: true
lang: zh
layout: post
title: Maven Surefire插件
translated: true
type: note
---

以下是关于 **Maven Surefire 插件** 的说明，该插件是基于 Maven 的项目在构建过程中运行单元测试的关键组件。本文涵盖其用途、配置、使用方法和自定义选项。

---

## 什么是 Maven Surefire 插件？

**Maven Surefire 插件** 是 Apache Maven 中的一个插件，用于在构建生命周期中执行单元测试。它与 Maven 的 `test` 阶段无缝集成，并在运行诸如 `mvn test`、`mvn package` 或 `mvn install` 等命令时自动触发。该插件支持流行的测试框架，如 JUnit（版本 3、4 和 5）和 TestNG，并生成测试报告以帮助开发人员评估测试结果。

### 主要特性

- 在独立的 JVM 进程中运行测试以实现隔离。
- 支持多种测试框架（JUnit、TestNG 等）。
- 生成 XML 和纯文本等格式的测试报告。
- 提供跳过测试、运行特定测试或自定义执行的灵活性。

---

## 在 `pom.xml` 中的基本设置

Surefire 插件默认包含在 Maven 的构建生命周期中，因此基本使用时无需配置。但您可以在 `pom.xml` 文件中显式声明它以指定版本或自定义其行为。

### 最小配置

如果不添加任何配置，Maven 将使用插件的默认设置：

- 测试文件位于 `src/test/java`。
- 测试文件遵循命名模式，如 `**/*Test.java`、`**/Test*.java` 或 `**/*Tests.java`。

### 显式声明

要自定义插件或确保使用特定版本，请将其添加到 `pom.xml` 的 `<build><plugins>` 部分。以下是一个示例：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M5</version> <!-- 使用最新版本 -->
        </plugin>
    </plugins>
</build>
```

---

## 使用 Surefire 运行测试

该插件与 Maven 生命周期的 `test` 阶段绑定。以下是使用方法：

### 运行所有测试

要执行所有单元测试，请运行：

```
mvn test
```

### 在更大的构建中运行测试

当运行包含 `test` 阶段的命令时，测试会自动执行，例如：

```
mvn package
mvn install
```

### 跳过测试

您可以使用命令行标志跳过测试执行：

- **跳过运行测试**：`-DskipTests`

  ```
  mvn package -DskipTests
  ```

- **跳过测试编译和执行**：`-Dmaven.test.skip=true`

  ```
  mvn package -Dmaven.test.skip=true
  ```

---

## 自定义 Surefire 插件

您可以通过在 `pom.xml` 中添加 `<configuration>` 部分来自定义插件的行为。以下是一些常见的自定义选项：

### 包含或排除特定测试

使用模式指定要运行或跳过的测试：

```xml
<configuration>
    <includes>
        <include>**/My*Test.java</include>
    </includes>
    <excludes>
        <exclude>**/SlowTest.java</exclude>
    </excludes>
</configuration>
```

### 并行运行测试

通过并发运行测试来加速执行：

```xml
<configuration>
    <parallel>methods</parallel>
    <threadCount>2</threadCount>
</configuration>
```

*注意*：在启用此功能之前，请确保您的测试是线程安全的。

### 传递系统属性

为测试 JVM 设置属性：

```xml
<configuration>
    <systemPropertyVariables>
        <propertyName>propertyValue</propertyName>
    </systemPropertyVariables>
</configuration>
```

### 生成报告

默认情况下，报告保存在 `target/surefire-reports` 中。要生成 HTML 报告，请使用 `maven-surefire-report-plugin`：

```xml
<reporting>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-report-plugin</artifactId>
            <version>3.0.0-M5</version>
        </plugin>
    </plugins>
</reporting>
```

运行 `mvn surefire-report:report` 以生成 HTML 报告。

---

## 处理测试失败

### 测试失败时使构建失败

默认情况下，测试失败会导致构建失败。要忽略失败并继续：

```
mvn test -Dmaven.test.failure.ignore=true
```

### 重新运行失败的测试

通过重试失败来处理不稳定的测试：

```xml
<configuration>
    <rerunFailingTestsCount>2</rerunFailingTestsCount>
</configuration>
```

这将最多重新运行失败的测试 2 次。

---

## 与测试框架一起使用 Surefire

该插件支持多种测试框架，且设置简单：

### JUnit 4

无需额外配置；Surefire 会自动检测 JUnit 4 测试。

### JUnit 5

添加 JUnit 5 依赖：

```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.8.1</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

使用 Surefire 2.22.0 或更高版本以获得完整支持。

### TestNG

添加 TestNG 依赖：

```xml
<dependencies>
    <dependency>
        <groupId>org.testng</groupId>
        <artifactId>testng</artifactId>
        <version>7.4.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

Surefire 将自动运行 TestNG 测试。

---

## 关键注意事项

- **测试位置**：测试文件应位于 `src/test/java`，资源文件位于 `src/test/resources`。
- **命名约定**：默认模式包括 `**/*Test.java`、`**/Test*.java` 等，但这些可以自定义。
- **插件版本**：使用最新版本（例如 3.0.0-M5）以获得最新功能和对框架的支持。

---

## 总结

**Maven Surefire 插件** 是在 Maven 项目中运行单元测试的关键工具。使用方法如下：

1. 依赖其默认行为，或在 `pom.xml` 中显式声明以进行自定义。
2. 使用 `mvn test` 或在更大的构建（如 `mvn package`）中运行测试。
3. 使用包含/排除模式、并行执行或系统属性等选项进行自定义。
4. 通过跳过测试、忽略失败或重新运行不稳定的测试来处理失败。
5. 通过添加正确的依赖确保与测试框架（JUnit、TestNG）的兼容性。

该插件为您的 Maven 项目提供了一种强大而灵活的方式来管理单元测试！
