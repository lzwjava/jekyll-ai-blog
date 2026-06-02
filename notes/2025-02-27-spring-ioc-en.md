---
audio: false
generated: true
lang: en
layout: post
title: Spring IoC (Inversion of Control) Container
translated: false
type: note
---

Let me break down how to use the Spring IoC (Inversion of Control) Container in a clear and practical way. The Spring IoC Container is the core of the Spring Framework, responsible for managing the lifecycle and configuration of application objects (called beans). It "inverts" the control by handling object creation and dependency injection for you, rather than you manually creating and wiring them.

Here’s a step-by-step guide to get you started:

---

### 1. **Understand the Basics**
- **What it does**: The IoC Container creates, configures, and manages beans (your application objects) based on metadata you provide (via XML, Java annotations, or Java code).
- **Key concepts**:
  - **Beans**: Objects managed by the container.
  - **Dependency Injection (DI)**: The container injects dependencies (other beans or values) into your objects.
  - **Configuration**: You tell the container what beans to create and how to wire them.

---

### 2. **Set Up Your Project**
To use Spring IoC, you need a Spring project. If you’re starting fresh:
- Use **Spring Boot** (simplest way) or plain Spring.
- Add dependencies in your `pom.xml` (if using Maven):
  ```xml
  <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>6.1.3</version> <!-- Use the latest version -->
  </dependency>
  ```
- For Spring Boot, use:
  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter</artifactId>
      <version>3.2.2</version> <!-- Latest as of now -->
  </dependency>
  ```

---

### 3. **Define Your Beans**
You can define beans in three main ways:

#### a) **Using Annotations (Most Common)**
- Create a simple Java class and annotate it with `@Component` (or specialized annotations like `@Service`, `@Repository`, etc.).
- Example:
  ```java
  import org.springframework.stereotype.Component;

  @Component
  public class MyService {
      public void doSomething() {
          System.out.println("Doing something!");
      }
  }
  ```

#### b) **Using Java Configuration**
- Create a configuration class with `@Configuration` and define beans with `@Bean`.
- Example:
  ```java
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;

  @Configuration
  public class AppConfig {
      @Bean
      public MyService myService() {
          return new MyService();
      }
  }
  ```

#### c) **Using XML (Legacy Approach)**
- Define beans in an XML file (e.g., `beans.xml`):
  ```xml
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.springframework.org/schema/beans
         http://www.springframework.org/schema/beans/spring-beans.xsd">
      <bean id="myService" class="com.example.MyService"/>
  </beans>
  ```

---

### 4. **Initialize the IoC Container**
You need to start the container to manage your beans.

#### a) **With Spring Boot**
- Spring Boot does this automatically. Just create a main class with `@SpringBootApplication`:
  ```java
  import org.springframework.boot.SpringApplication;
  import org.springframework.boot.autoconfigure.SpringBootApplication;

  @SpringBootApplication
  public class MyApp {
      public static void main(String[] args) {
          SpringApplication.run(MyApp.class, args);
      }
  }
  ```
- The container scans for `@Component` classes and manages them.

#### b) **With Plain Spring (Annotation-Based)**
- Use `AnnotationConfigApplicationContext`:
  ```java
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;

  public class Main {
      public static void main(String[] args) {
          AnnotationConfigApplicationContext context =
              new AnnotationConfigApplicationContext(AppConfig.class);
          MyService service = context.getBean(MyService.class);
          service.doSomething();
          context.close();
      }
  }
  ```

#### c) **With XML**
- Use `ClassPathXmlApplicationContext`:
  ```java
  import org.springframework.context.support.ClassPathXmlApplicationContext;

  public class Main {
      public static void main(String[] args) {
          ClassPathXmlApplicationContext context =
              new ClassPathXmlApplicationContext("beans.xml");
          MyService service = context.getBean("myService", MyService.class);
          service.doSomething();
          context.close();
      }
  }
  ```

---

### 5. **Inject Dependencies**
The IoC Container can inject dependencies into your beans.

#### a) **Constructor Injection (Recommended)**
```java
@Component
public class MyController {
    private final MyService myService;

    public MyController(MyService myService) {
        this.myService = myService;
    }

    public void execute() {
        myService.doSomething();
    }
}
```

#### b) **Setter Injection**
```java
@Component
public class MyController {
    private MyService myService;

    @Autowired
    public void setMyService(MyService myService) {
        this.myService = myService;
    }
}
```

#### c) **Field Injection (Less Preferred)**
```java
@Component
public class MyController {
    @Autowired
    private MyService myService;

    public void execute() {
        myService.doSomething();
    }
}
```
- Use `@Autowired` (Spring-specific) or `@Inject` (JSR-330 standard) to mark injection points.

---

### 6. **Run and Use the Beans**
- Once the container is running, it wires your beans and their dependencies. You can retrieve beans with `context.getBean()` (plain Spring) or let Spring Boot handle it automatically via injection.

Example with Spring Boot:
```java
@SpringBootApplication
public class MyApp {
    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(MyApp.class, args);
        MyController controller = context.getBean(MyController.class);
        controller.execute();
    }
}
```

---

### 7. **Additional Tips**
- **Scopes**: By default, beans are singletons. Use `@Scope("prototype")` for new instances per request.
- **Component Scanning**: Add `@ComponentScan` to your configuration class if beans are in different packages.
- **Profiles**: Use `@Profile` to activate beans in specific environments (e.g., "dev", "prod").
- **Close the Context**: In non-Spring Boot apps, call `context.close()` to free resources.

---

That’s the gist of it! Start with Spring Boot and annotations for simplicity. If you’re stuck on a specific part—like wiring a tricky dependency or debugging—feel free to ask, and I’ll dive deeper with you!
