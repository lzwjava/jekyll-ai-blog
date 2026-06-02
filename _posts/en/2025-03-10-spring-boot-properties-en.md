---
audio: false
generated: true
lang: en
layout: post
title: How Properties Work in Spring Boot
translated: false
type: note
---

Let’s explore how properties work in Spring Boot, including how to use YAML or `.properties` files, how to override them with command-line arguments like `-D`, the various ways to initialize properties, and how to test them effectively.

---

### **How Properties Work in Spring Boot**
Spring Boot provides a flexible system for managing application configuration through properties, which are key-value pairs. These properties can be defined in multiple sources, and Spring Boot resolves them based on a specific order of precedence. This allows you to customize your application for different environments or deployment scenarios. Properties are loaded into the **Spring Environment**, making them accessible throughout your application.

The main sources of properties include:
- Configuration files (e.g., `application.properties` or `application.yml`)
- Command-line arguments (e.g., `--server.port=8081`)
- System properties (e.g., `-Dserver.port=8081`)
- Environment variables
- Java code (e.g., via `@Value` or `@ConfigurationProperties`)

---

### **Using YAML or Properties Files**
Spring Boot supports two primary formats for configuration files, both typically placed in `src/main/resources`:

#### **1. `.properties` Files**
This is a simple, flat key-value format:
```properties
server.port=8080
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
```

#### **2. `.yml` or `.yaml` Files**
This is a structured, hierarchical format using indentation:
```yaml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
```

**Key Points:**
- Use `.properties` for simple configurations and `.yml` for nested or complex setups.
- Profile-specific files (e.g., `application-dev.yml`) can be used for environment-specific settings.
- Example: Setting `server.port=8080` changes the port your Spring Boot application runs on.

---

### **Using Command-Line Arguments to Override Properties**
You can override properties defined in configuration files using command-line arguments in two ways:

#### **1. Using `--` for Spring Boot Properties**
Pass properties directly when running the application:
```bash
java -jar myapp.jar --server.port=8081 --spring.datasource.url=jdbc:mysql://localhost:3306/testdb
```
These take precedence over configuration files.

#### **2. Using `-D` for System Properties**
Set system properties with `-D`, which Spring Boot also recognizes:
```bash
java -Dserver.port=8081 -Dspring.datasource.url=jdbc:mysql://localhost:3306/testdb -jar myapp.jar
```
System properties override configuration file values as well.

---

### **Different Ways to Initialize Properties**
Spring Boot offers several methods to define or initialize properties beyond files and command-line arguments:

#### **1. Environment Variables**
Properties can be set via environment variables. For example:
- Set `SERVER_PORT=8081` in your environment, and Spring Boot maps it to `server.port`.
- **Naming Convention:** Convert property names to uppercase and replace dots (`.`) with underscores (`_`), e.g., `spring.datasource.url` becomes `SPRING_DATASOURCE_URL`.

#### **2. Java Code**
You can initialize properties programmatically:
- **Using `@Value`**: Inject a specific property into a field.
  ```java
  @Value("${server.port}")
  private int port;
  ```
- **Using `@ConfigurationProperties`**: Bind a group of properties to a Java object.
  ```java
  @Component
  @ConfigurationProperties(prefix = "app")
  public class AppProperties {
      private String name;
      // getters and setters
  }
  ```
  This binds properties like `app.name` to the `name` field.

#### **3. Default Values**
Provide fallback values if a property isn’t defined:
- In `@Value`: `@Value("${server.port:8080}")` uses `8080` if `server.port` is unset.
- In configuration files: Set defaults in `application.properties` or YAML.

---

### **Property Precedence**
Spring Boot resolves properties from multiple sources in this order (higher precedence overrides lower):
1. Command-line arguments (`--property=value`)
2. System properties (`-Dproperty=value`)
3. Environment variables
4. Configuration files (`application.properties` or `application.yml`)
5. Default values in code

**Example:** If `server.port=8080` is in `application.properties` but you run `java -jar myapp.jar --server.port=8081`, the port will be `8081`.

---

### **How to Test Properties**
Testing properties ensures your application behaves as expected. Here are common approaches:

#### **1. Using `@TestPropertySource`**
Override properties in unit tests:
```java
@SpringBootTest
@TestPropertySource(properties = {"server.port=9090"})
public class MyTest {
    // Test code
}
```

#### **2. Using `application-test.properties`**
Place a test-specific file in `src/test/resources`:
```properties
server.port=9090
```
Spring Boot loads this automatically during tests.

#### **3. Programmatic Overrides**
Set properties in test setup:
```java
@SpringBootTest
public class MyTest {
    @BeforeEach
    public void setup() {
        System.setProperty("server.port", "9090");
    }
}
```

#### **4. Using `@ActiveProfiles`**
Activate profile-specific properties:
- Define `application-test.yml` with test settings.
- Use:
  ```java
  @SpringBootTest
  @ActiveProfiles("test")
  public class MyTest {
      // Test code
  }
  ```

---

### **Summary**
- **Configuration Files**: Use `application.properties` or `application.yml` for default settings.
- **Command-Line Arguments**: Override with `--property=value` or `-Dproperty=value`.
- **Initialization Methods**: Leverage environment variables, Java code (`@Value`, `@ConfigurationProperties`), or defaults.
- **Testing**: Use `@TestPropertySource`, test-specific files, programmatic overrides, or profiles.

This covers the essentials of working with properties in Spring Boot. Let me know if you’d like more details!
