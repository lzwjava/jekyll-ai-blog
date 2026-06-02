---
audio: false
generated: true
lang: zh
layout: post
title: Spring内部工作机制
translated: true
type: note
---

让我们深入探讨 Spring 及其内部工作原理。Spring 是一个用于构建 Java 应用程序的强大框架，我将通过清晰解释逐步回答您的每个问题。

### Spring 如何工作？
Spring 基于**控制反转（IoC）**原则运行。这意味着不是由您的应用程序代码控制对象的创建和管理，而是由 Spring 接管。它通过一个称为 **IoC 容器** 的组件实现这一点。IoC 容器负责：

- **实例化**对象（在 Spring 中称为 bean）。
- 根据您的规范**配置**它们。
- 通过管理它们的依赖关系来**组装**它们。

这种方法减少了代码中的紧密耦合，使其更加模块化且易于维护。

### Spring 如何管理 Bean？
在 Spring 中，**bean** 是由 IoC 容器管理的对象。以下是 Spring 处理它们的方式：

1. **定义**：您可以通过以下方式定义 bean：
   - **XML 配置文件**。
   - 使用注解（如 `@Bean`、`@Component`、`@Service` 等）的 **Java 配置**。
2. **创建**：当应用程序启动时，IoC 容器读取这些定义并创建 bean。
3. **依赖注入（DI）**：Spring 自动将依赖项（其他 bean）注入到需要它们的 bean 中，使用：
   - **构造函数注入**。
   - **Setter 注入**。
   - **字段注入**（通过 `@Autowired`）。

容器管理这些 bean 的整个生命周期——从创建到销毁——并确保在需要时可用。

### Service 和 Controller 的区别
在 **Spring MVC**（Spring 的 Web 框架）的上下文中，这两个组件有不同的用途：

- **Controller**：
  - 处理来自用户的 **HTTP 请求**。
  - 处理输入，调用业务逻辑，并决定返回哪个**视图**（例如，网页）。
  - 使用 `@Controller` 或 `@RestController` 注解。
  - 位于 **Web 层**。

- **Service**：
  - 封装应用程序的**业务逻辑**。
  - 执行计算、数据处理或与数据库交互等任务。
  - 使用 `@Service` 注解。
  - 位于**业务层**。

**示例**：
- Controller 可能接收显示用户资料的请求，并调用 Service 来获取用户数据。
- Service 从数据库检索数据并将其返回给 Controller，然后 Controller 将其发送到视图。

简而言之：**Controller 管理 Web 交互**，而 **Service 处理核心功能**。

### Spring 提供什么？
Spring 是一个全面的框架，为企业应用程序提供广泛的工具。主要功能包括：

- **依赖注入**：简化对象依赖关系管理。
- **面向切面编程（AOP）**：添加横切关注点，如日志记录或安全性。
- **事务管理**：确保操作之间的数据一致性。
- **Spring MVC**：构建强大的 Web 应用程序。
- **Spring Boot**：通过预配置的默认值和嵌入式服务器简化设置。
- **Spring Data**：简化数据库访问。
- **安全性**：提供身份验证和授权工具。

Spring 的模块化设计让您可以选择仅需要的功能。

### Spring 如何查找对象或 Bean？
当 Spring 应用程序启动时：

1. **IoC 容器**初始化。
2. 它在以下位置扫描 **bean 定义**：
   - XML 文件。
   - 带注解的类（例如 `@Component`、`@Bean`）。
3. 容器创建 bean 并将其存储在**映射**中，按名称或类型索引。
4. 当需要 bean 时（例如，用于注入或直接检索），容器通过以下方式提供它：
   - **按名称查找**。
   - **按类型查找**（例如，通过 `@Autowired`）。

此过程确保 bean 在整个应用程序中随时可用。

### 如何使用 Tomcat 或 Netty 作为服务器？
Spring Boot 是 Spring 的扩展，通过将服务器直接嵌入到您的应用程序中来简化服务器设置。以下是它与 **Tomcat** 和 **Netty** 的配合方式：

- **Tomcat**（基于 Servlet）：
  - Spring Boot 的 `spring-boot-starter-web` 依赖项中的默认服务器。
  - 将此添加到您的 `pom.xml`：
    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    ```
  - Spring Boot 嵌入 Tomcat，您的应用程序作为独立可执行 JAR 运行。

- **Netty**（非基于 Servlet）：
  - 用于响应式 Web 应用程序（例如，与 Spring WebFlux 一起使用）。
  - 通过排除 Tomcat 并添加 Netty 来替换它：
    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    ```
  - Spring Boot 改为嵌入 Netty，支持异步、非阻塞 I/O。

您可以通过 `application.properties` 配置服务器（例如，使用 `server.port=8080` 设置端口）。无需外部服务器部署——Spring Boot 处理所有内容。

### 总结
- **Spring 核心**：使用 IoC 容器进行对象管理。
- **Bean 管理**：通过 XML 或注解定义，自动注入依赖项。
- **Service 与 Controller**：Service 处理业务逻辑；Controller 管理 Web 请求。
- **功能**：提供 DI、AOP、Web 支持等。
- **Bean 查找**：容器从配置中查找并提供 bean。
- **服务器**：Spring Boot 通过简单的依赖项更改嵌入 Tomcat 或 Netty。
