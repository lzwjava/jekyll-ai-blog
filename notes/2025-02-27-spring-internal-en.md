---
audio: false
generated: true
lang: en
layout: post
title: Spring Internal Workings
translated: false
type: note
---

Let’s dive about Spring and its internal workings. Spring is a robust framework for building Java applications, and I’ll address each part of your query step-by-step with clear explanations.

### How Does Spring Work?
Spring operates on the principle of **Inversion of Control (IoC)**. This means that instead of your application code controlling the creation and management of objects, Spring takes charge. It does this through a component called the **IoC container**. The IoC container is responsible for:

- **Instantiating** objects (called beans in Spring).
- **Configuring** them based on your specifications.
- **Assembling** them by managing their dependencies.

This approach reduces tight coupling in your code, making it more modular and easier to maintain.

### How Does Spring Manage Beans?
In Spring, **beans** are the objects managed by the IoC container. Here’s how Spring handles them:

1. **Definition**: You define beans either in:
   - **XML configuration files**.
   - **Java-based configuration** using annotations like `@Bean`, `@Component`, `@Service`, etc.
2. **Creation**: When the application starts, the IoC container reads these definitions and creates the beans.
3. **Dependency Injection (DI)**: Spring automatically injects dependencies (other beans) into a bean where needed, using:
   - **Constructor injection**.
   - **Setter injection**.
   - **Field injection** (via `@Autowired`).

The container manages the entire lifecycle of these beans—from creation to destruction—and ensures they’re available when required.

### Difference Between a Service and a Controller
In the context of **Spring MVC** (Spring’s web framework), these two components serve distinct purposes:

- **Controller**:
  - Handles **HTTP requests** from users.
  - Processes input, invokes business logic, and decides which **view** (e.g., a webpage) to return.
  - Annotated with `@Controller` or `@RestController`.
  - Lives in the **web layer**.

- **Service**:
  - Encapsulates the **business logic** of the application.
  - Performs tasks like calculations, data processing, or interacting with databases.
  - Annotated with `@Service`.
  - Lives in the **business layer**.

**Example**:
- A controller might receive a request to display a user’s profile and call a service to fetch the user data.
- The service retrieves the data from a database and returns it to the controller, which then sends it to the view.

In short: **Controllers manage web interactions**, while **services handle the core functionality**.

### What Does Spring Provide?
Spring is a comprehensive framework offering a wide range of tools for enterprise applications. Key features include:

- **Dependency Injection**: Simplifies managing object dependencies.
- **Aspect-Oriented Programming (AOP)**: Adds cross-cutting concerns like logging or security.
- **Transaction Management**: Ensures data consistency across operations.
- **Spring MVC**: Builds robust web applications.
- **Spring Boot**: Simplifies setup with pre-configured defaults and embedded servers.
- **Spring Data**: Streamlines database access.
- **Security**: Provides authentication and authorization tools.

Spring’s modular design lets you pick only the features you need.

### How Does Spring Look for Objects or Beans?
When a Spring application starts:

1. The **IoC container** initializes.
2. It scans for **bean definitions** in:
   - XML files.
   - Annotated classes (e.g., `@Component`, `@Bean`).
3. The container creates the beans and stores them in a **map**, indexed by name or type.
4. When a bean is needed (e.g., for injection or direct retrieval), the container provides it using:
   - **By-name lookup**.
   - **By-type lookup** (e.g., via `@Autowired`).

This process ensures beans are readily available throughout the application.

### How to Use Tomcat or Netty as a Server?
Spring Boot, an extension of Spring, simplifies server setup by embedding servers directly into your application. Here’s how it works with **Tomcat** and **Netty**:

- **Tomcat** (Servlet-Based):
  - Default server in Spring Boot’s `spring-boot-starter-web` dependency.
  - Add this to your `pom.xml`:
    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    ```
  - Spring Boot embeds Tomcat, and your app runs as a standalone executable JAR.

- **Netty** (Non-Servlet-Based):
  - Used for reactive web applications (e.g., with Spring WebFlux).
  - Replace Tomcat by excluding it and adding Netty:
    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    ```
  - Spring Boot embeds Netty instead, supporting asynchronous, non-blocking I/O.

You configure the server via `application.properties` (e.g., setting the port with `server.port=8080`). No external server deployment is needed—Spring Boot handles it all.

### Summary
- **Spring’s Core**: Uses an IoC container for object management.
- **Bean Management**: Defined via XML or annotations, with dependencies injected automatically.
- **Service vs. Controller**: Services handle business logic; controllers manage web requests.
- **Features**: Offers DI, AOP, web support, and more.
- **Bean Lookup**: Container finds and provides beans from configurations.
- **Servers**: Spring Boot embeds Tomcat or Netty with simple dependency changes.
