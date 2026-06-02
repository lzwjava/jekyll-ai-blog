---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot 属性机制解析
translated: true
type: note
---

让我们深入探讨 Spring Boot 中属性的工作机制，包括如何使用 YAML 或 `.properties` 文件、如何通过 `-D` 等命令行参数覆盖属性、不同的属性初始化方式，以及如何进行有效的属性测试。

---

### **Spring Boot 属性的工作机制**
Spring Boot 通过属性（键值对）提供了一个灵活的应用程序配置管理系统。这些属性可以在多个来源中定义，Spring Boot 会根据特定的优先级顺序进行解析。这使得您能够为不同环境或部署场景自定义应用程序。属性会被加载到 **Spring 环境** 中，从而在整个应用程序中可访问。

属性的主要来源包括：
- 配置文件（如 `application.properties` 或 `application.yml`）
- 命令行参数（如 `--server.port=8081`）
- 系统属性（如 `-Dserver.port=8081`）
- 环境变量
- Java 代码（如通过 `@Value` 或 `@ConfigurationProperties`）

---

### **使用 YAML 或 Properties 文件**
Spring Boot 支持两种主要的配置文件格式，通常放置在 `src/main/resources` 目录下：

#### **1. `.properties` 文件**
这是一种简单的扁平键值对格式：
```properties
server.port=8080
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
```

#### **2. `.yml` 或 `.yaml` 文件**
这是一种使用缩进的结构化分层格式：
```yaml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
```

**关键点：**
- 简单配置使用 `.properties`，嵌套或复杂配置使用 `.yml`。
- 可以使用特定于配置文件的文件（如 `application-dev.yml`）来设置环境特定的配置。
- 示例：设置 `server.port=8080` 可以更改 Spring Boot 应用程序运行的端口。

---

### **使用命令行参数覆盖属性**
您可以通过两种方式使用命令行参数覆盖配置文件中定义的属性：

#### **1. 使用 `--` 设置 Spring Boot 属性**
在运行应用程序时直接传递属性：
```bash
java -jar myapp.jar --server.port=8081 --spring.datasource.url=jdbc:mysql://localhost:3306/testdb
```
这些参数的优先级高于配置文件。

#### **2. 使用 `-D` 设置系统属性**
使用 `-D` 设置系统属性，Spring Boot 也能识别：
```bash
java -Dserver.port=8081 -Dspring.datasource.url=jdbc:mysql://localhost:3306/testdb -jar myapp.jar
```
系统属性同样会覆盖配置文件中的值。

---

### **不同的属性初始化方式**
除了配置文件和命令行参数，Spring Boot 还提供了多种定义或初始化属性的方法：

#### **1. 环境变量**
可以通过环境变量设置属性。例如：
- 在环境中设置 `SERVER_PORT=8081`，Spring Boot 会将其映射到 `server.port`。
- **命名约定：** 将属性名转换为大写，并用下划线（`_`）替换点（`.`），例如 `spring.datasource.url` 变为 `SPRING_DATASOURCE_URL`。

#### **2. Java 代码**
可以通过编程方式初始化属性：
- **使用 `@Value`**：将特定属性注入到字段中。
  ```java
  @Value("${server.port}")
  private int port;
  ```
- **使用 `@ConfigurationProperties`**：将一组属性绑定到 Java 对象。
  ```java
  @Component
  @ConfigurationProperties(prefix = "app")
  public class AppProperties {
      private String name;
      // getters and setters
  }
  ```
  这将把诸如 `app.name` 的属性绑定到 `name` 字段。

#### **3. 默认值**
如果属性未定义，可以提供回退值：
- 在 `@Value` 中：`@Value("${server.port:8080}")` 如果 `server.port` 未设置，则使用 `8080`。
- 在配置文件中：在 `application.properties` 或 YAML 中设置默认值。

---

### **属性优先级**
Spring Boot 按以下顺序从多个来源解析属性（优先级高的覆盖优先级低的）：
1. 命令行参数（`--property=value`）
2. 系统属性（`-Dproperty=value`）
3. 环境变量
4. 配置文件（`application.properties` 或 `application.yml`）
5. 代码中的默认值

**示例：** 如果 `application.properties` 中设置了 `server.port=8080`，但您运行 `java -jar myapp.jar --server.port=8081`，则端口将是 `8081`。

---

### **如何测试属性**
测试属性可以确保应用程序按预期运行。以下是常见的方法：

#### **1. 使用 `@TestPropertySource`**
在单元测试中覆盖属性：
```java
@SpringBootTest
@TestPropertySource(properties = {"server.port=9090"})
public class MyTest {
    // 测试代码
}
```

#### **2. 使用 `application-test.properties`**
在 `src/test/resources` 目录下放置测试专用的文件：
```properties
server.port=9090
```
Spring Boot 在测试期间会自动加载此文件。

#### **3. 编程式覆盖**
在测试设置中设置属性：
```java
@SpringBootTest
public class MyTest {
    @BeforeEach
    public void setup() {
        System.setProperty("server.port", "9090");
    }
}
```

#### **4. 使用 `@ActiveProfiles`**
激活特定配置文件的属性：
- 在 `application-test.yml` 中定义测试设置。
- 使用：
  ```java
  @SpringBootTest
  @ActiveProfiles("test")
  public class MyTest {
      // 测试代码
  }
  ```

---

### **总结**
- **配置文件**：使用 `application.properties` 或 `application.yml` 进行默认设置。
- **命令行参数**：使用 `--property=value` 或 `-Dproperty=value` 进行覆盖。
- **初始化方法**：利用环境变量、Java 代码（`@Value`、`@ConfigurationProperties`）或默认值。
- **测试**：使用 `@TestPropertySource`、测试专用文件、编程式覆盖或配置文件。

以上涵盖了在 Spring Boot 中使用属性的基本要点。如果您需要更多详细信息，请随时告知！
