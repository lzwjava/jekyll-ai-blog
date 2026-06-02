---
audio: false
generated: true
lang: en
layout: post
title: Using SpringRunner in Java Tests
translated: false
type: note
---

To use `SpringRunner` with JUnit's `@RunWith` runner in Java tests, follow these steps. Note that I assume "SpringRuner" in your query is a typo and you mean `SpringRunner`. Here's a complete guide:

### Step 1: Add the Spring Test Dependency

To use `SpringRunner`, you need the Spring Test module in your project. If you're using Maven, add this dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>${spring.version}</version>
    <scope>test</scope>
</dependency>
```

Replace `${spring.version}` with the version of Spring you're using (e.g., `5.3.22`). If you're using Gradle, add this to your `build.gradle`:

```gradle
testImplementation 'org.springframework:spring-test:${springVersion}'
```

This ensures that `SpringRunner` and other Spring testing utilities are available.

### Step 2: Annotate the Test Class with `@RunWith(SpringRunner.class)`

The `@RunWith` annotation tells JUnit to use a specific runner instead of its default one. For Spring integration, use `SpringRunner`, which is part of the Spring TestContext Framework. Add this annotation to your test class:

```java
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class MyServiceTest {
    // Test code goes here
}
```

`SpringRunner` enables Spring features like dependency injection and context loading in your tests. Note that `@RunWith` is a JUnit 4 annotation, so this approach assumes you're using JUnit 4. For JUnit 5, you'd use `@ExtendWith(SpringExtension.class)` instead, but your mention of "RunWith runner" suggests JUnit 4.

### Step 3: Configure the Spring Application Context with `@ContextConfiguration`

To use Spring-managed beans in your tests, you need to load a Spring application context. The `@ContextConfiguration` annotation specifies how to do this. For example, if you have a configuration class (e.g., `AppConfig`), use:

```java
import org.springframework.test.context.ContextConfiguration;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes = AppConfig.class)
public class MyServiceTest {
    // Test code goes here
}
```

If your configuration is in an XML file (e.g., `applicationContext.xml`), use:

```java
@ContextConfiguration(locations = "classpath:applicationContext.xml")
```

This tells `SpringRunner` which beans and configurations to load for the test.

### Step 4: Inject Spring Beans with `@Autowired`

Once the context is loaded, you can inject Spring-managed beans into your test class using `@Autowired`. For example, if you have a service called `MyService`:

```java
import org.springframework.beans.factory.annotation.Autowired;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes = AppConfig.class)
public class MyServiceTest {
    @Autowired
    private MyService myService;

    // Test methods go here
}
```

This allows you to use the injected bean in your tests.

### Step 5: Write Test Methods with `@Test`

Define your test methods using JUnit's `@Test` annotation. For example:

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

The `@Test` annotation marks methods that JUnit should execute as tests. With `SpringRunner`, these methods can interact with the Spring context.

### Example: Putting It All Together

Here’s a complete example:

```java
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;
import static org.junit.Assert.assertEquals;

// Configuration class for the test
@Configuration
class AppConfig {
    @Bean
    public MyService myService() {
        return new MyService();
    }
}

// Service class to test
class MyService {
    public String doSomething() {
        return "Hello, Spring!";
    }
}

// Test class
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

### Additional Notes

- **Purpose**: `SpringRunner` is ideal for integration tests where you need Spring's dependency injection or context features. For unit tests, consider Mockito or plain JUnit instead.
- **Common Issues**: Ensure the `spring-test` dependency is included, or you’ll get errors like `ClassNotFoundException`. Also, verify that `@ContextConfiguration` points to a valid configuration.
- **Optional Annotations**: Use `@Transactional` for tests that modify the database (to roll back changes) or `@ActiveProfiles` to specify a profile (e.g., "test").

This setup allows you to run JUnit tests with Spring’s testing support, leveraging features like dependency injection and context management.
