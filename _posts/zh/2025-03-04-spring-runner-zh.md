---
audio: false
generated: true
lang: zh
layout: post
title: Java测试中的SpringRunner应用
translated: true
type: note
---

要在 Java 测试中将 `SpringRunner` 与 JUnit 的 `@RunWith` 运行器结合使用，请按照以下步骤操作。请注意，我假设您查询中的 "SpringRuner" 是拼写错误，实际应为 `SpringRunner`。以下是完整指南：

### 步骤 1：添加 Spring Test 依赖

要使用 `SpringRunner`，您需要在项目中添加 Spring Test 模块。如果使用 Maven，请在 `pom.xml` 中添加以下依赖：

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>${spring.version}</version>
    <scope>test</scope>
</dependency>
```

将 `${spring.version}` 替换为您使用的 Spring 版本（例如 `5.3.22`）。如果使用 Gradle，请在 `build.gradle` 中添加：

```gradle
testImplementation 'org.springframework:spring-test:${springVersion}'
```

这确保了 `SpringRunner` 和其他 Spring 测试工具可用。

### 步骤 2：使用 `@RunWith(SpringRunner.class)` 注解测试类

`@RunWith` 注解告诉 JUnit 使用特定的运行器而非默认运行器。对于 Spring 集成，请使用 `SpringRunner`，它是 Spring TestContext Framework 的一部分。将此注解添加到测试类：

```java
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class MyServiceTest {
    // 测试代码写在这里
}
```

`SpringRunner` 启用了 Spring 功能，如依赖注入和上下文加载。请注意 `@RunWith` 是 JUnit 4 注解，因此此方法假定您使用 JUnit 4。对于 JUnit 5，您应使用 `@ExtendWith(SpringExtension.class)`，但您提到的 "RunWith runner" 表明是 JUnit 4。

### 步骤 3：使用 `@ContextConfiguration` 配置 Spring 应用上下文

要在测试中使用 Spring 管理的 bean，需要加载 Spring 应用上下文。`@ContextConfiguration` 注解指定了加载方式。例如，如果您有配置类（如 `AppConfig`），请使用：

```java
import org.springframework.test.context.ContextConfiguration;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes = AppConfig.class)
public class MyServiceTest {
    // 测试代码写在这里
}
```

如果配置在 XML 文件中（如 `applicationContext.xml`），请使用：

```java
@ContextConfiguration(locations = "classpath:applicationContext.xml")
```

这告诉 `SpringRunner` 为测试加载哪些 bean 和配置。

### 步骤 4：使用 `@Autowired` 注入 Spring Bean

上下文加载后，您可以使用 `@Autowired` 将 Spring 管理的 bean 注入测试类。例如，如果您有名为 `MyService` 的服务：

```java
import org.springframework.beans.factory.annotation.Autowired;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes = AppConfig.class)
public class MyServiceTest {
    @Autowired
    private MyService myService;

    // 测试方法写在这里
}
```

这允许您在测试中使用注入的 bean。

### 步骤 5：使用 `@Test` 编写测试方法

使用 JUnit 的 `@Test` 注解定义测试方法。例如：

```java
import org.junit.Test;
import static org.junit.Assert.assertEquals;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes = AppConfig.class)
public class MyServiceTest {
    @Autowired
    private MyService myService;

    @Test
    public void testMyServiceMethod() {
        String result = myService.doSomething();
        assertEquals("Expected result", result);
    }
}
```

`@Test` 注解标记了 JUnit 应作为测试执行的方法。使用 `SpringRunner` 时，这些方法可以与 Spring 上下文交互。

### 示例：完整整合

以下是一个完整示例：

```java
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;
import static org.junit.Assert.assertEquals;

// 测试配置类
@Configuration
class AppConfig {
    @Bean
    public MyService myService() {
        return new MyService();
    }
}

// 待测试的服务类
class MyService {
    public String doSomething() {
        return "Hello, Spring!";
    }
}

// 测试类
@RunWith(SpringRunner.class)
@ContextConfiguration(classes = AppConfig.class)
public class MyServiceTest {
    @Autowired
    private MyService myService;

    @Test
    public void testMyServiceMethod() {
        String result = myService.doSomething();
        assertEquals("Hello, Spring!", result);
    }
}
```

### 补充说明

- **目的**：`SpringRunner` 适用于需要 Spring 依赖注入或上下文功能的集成测试。对于单元测试，请考虑使用 Mockito 或纯 JUnit。
- **常见问题**：确保包含 `spring-test` 依赖，否则会出现 `ClassNotFoundException` 等错误。同时验证 `@ContextConfiguration` 指向有效配置。
- **可选注解**：使用 `@Transactional` 处理修改数据库的测试（以回滚更改），或使用 `@ActiveProfiles` 指定配置文件（如 "test"）。

此设置允许您利用 Spring 测试支持运行 JUnit 测试，充分利用依赖注入和上下文管理等功能。
