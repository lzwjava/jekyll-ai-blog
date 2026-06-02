---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot 与 Spring 框架对比
translated: true
type: note
---

下面我们来深入探讨 **Spring Boot** 与 **Spring**（通常指 Spring 框架）之间的区别。虽然它们密切相关，但在 Java 生态系统中扮演着不同的角色。我将从核心目标、配置方式、开发速度和适用场景等关键维度进行解析。

### 1. **核心定位**

- **Spring 框架**：Java 应用的奠基性框架，诞生于 2002 年。它通过依赖注入和模块化设计，为企业级 Java 开发提供全面的编程与配置模型，包含 Spring MVC、Spring Security、Spring Data 等核心模块。
- **Spring Boot**：构建在 Spring 框架之上的增强层，于 2014 年推出。它通过"开箱即用"的设计理念极大简化了 Spring 应用的初始搭建，可理解为"内置电池的 Spring"，专注于快速应用开发和生产环境就绪。

### 2. **配置方式**

- **Spring**：需要手动配置。开发者需通过 XML 文件或 Java 注解明确定义 Bean、依赖关系和组件配置。这种方式虽然提供精细控制，但耗时且容易出错，尤其对新手不友好。
- **Spring Boot**：强调**自动配置**。根据项目依赖智能预设配置（例如引入 Spring Web 模块会自动配置 Tomcat 服务器）。保留手动覆盖默认配置的能力，但核心目标是实现零配置起步。

### 3. **开发效率**

- **Spring**：初始开发周期较长，需要手动组装依赖、服务器配置、数据库连接等组件。虽然功能强大，但构建基础应用就需要较多准备工作。
- **Spring Boot**：基于"约定优于配置"原则大幅提升效率。例如仅需几行代码即可快速搭建 REST API，这得益于嵌入式服务器和标准化依赖管理。

### 4. **依赖管理**

- **Spring**：依赖 Maven/Gradle 手动管理。需要开发者自行选择 Spring 模块（如 Spring Core、Spring MVC）和第三方库，存在版本冲突风险。
- **Spring Boot**：通过**起步依赖**（如 `spring-boot-starter-web`、`spring-boot-starter-data-jpa`）统一管理兼容版本的工具链，有效避免依赖冲突。

### 5. **服务器部署**

- **Spring**：不包含内置服务器，需要部署到外部容器（Tomcat/JBoss/WebSphere），涉及额外的环境配置。
- **Spring Boot**：默认集成嵌入式服务器（Tomcat/Jetty/Undertow），支持通过 `java -jar` 命令直接运行可执行 JAR 包，特别适合容器化部署场景。

### 6. **生产就绪**

- **Spring**：提供 Spring Security、事务管理等基础工具，但监控、健康检查、指标收集等功能需要自行集成。
- **Spring Boot**：内置 **Spring Boot Actuator** 模块，直接提供健康端点、运行指标、日志管理等生产级功能，实现开箱即用的应用监控。

### 7. **灵活性对比**

- **Spring**：具备高度可定制性，适合需要精确控制应用每个细节的复杂场景，但伴随的是较高的复杂度。
- **Spring Boot**：通过预设约定（如项目结构、默认配置）换取开发效率，在保持可定制能力的同时更注重开发体验的统一性。

### 8. **适用场景**

- **Spring**：适合需要集成异构系统或遗留组件的复杂企业级应用，不介意初始配置成本。
- **Spring Boot**：适用于微服务架构、REST API、独立应用和原型开发等现代快速开发场景。

### 实战对比

- **Spring 基础配置**：

  ```java
  // 基于 Spring MVC 的手动配置
  @Configuration
  @EnableWebMvc
  public class WebConfig implements WebMvcConfigurer {
      @Bean
      public ViewResolver viewResolver() {
          InternalResourceViewResolver resolver = new InternalResourceViewResolver();
          resolver.setPrefix("/WEB-INF/views/");
          resolver.setSuffix(".jsp");
          return resolver;
      }
  }
  ```

  还需配置 `web.xml` 或 Servlet 初始化器，并部署至外部服务器。

- **Spring Boot 等效实现**：

  ```java
  @RestController
  public class HelloController {
      @GetMapping("/hello")
      public String sayHello() {
          return "Hello, World!";
      }
  }
  ```

  在 `pom.xml` 添加 `spring-boot-starter-web` 依赖后即可直接运行，内置服务器自动启动。

### 特性对比表

| 对比维度         | Spring 框架                | Spring Boot                |
|------------------|----------------------------|----------------------------|
| **核心目标**     | Java 应用开发基础框架      | 简化 Spring 应用开发       |
| **配置方式**     | 手动配置（XML/注解）       | 自动配置                   |
| **服务器**       | 外部服务器（如 Tomcat）    | 嵌入式服务器（Tomcat 等）  |
| **依赖管理**     | 手动管理                   | 起步依赖自动管理           |
| **开发速度**     | 初始搭建较慢               | 快速原型开发               |
| **灵活性**       | 高可定制性                 | 约定优先，灵活性受限       |
| **适用场景**     | 复杂企业应用               | 微服务/快速应用开发        |

### 总结

- **Spring 框架**是基石——功能强大且灵活，适合需要精细控制的复杂系统或遗留项目改造。
- **Spring Boot**是加速器——专为现代化快速开发场景设计，特别适合微服务和独立应用开发。

对于新项目优先考虑开发效率时推荐 Spring Boot；面对需要深度定制的复杂系统时 Spring 框架更为合适。需要针对某个特性展开深入探讨吗？
