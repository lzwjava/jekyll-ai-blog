---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 请求过滤器对比：WebSphere与Spring Boot
translated: true
type: note
---

### 概述
IBM WebSphere Application Server（WAS，传统版或 Liberty）和 Spring Boot 都支持基于标准 Java Servlet API 的 `javax.servlet.Filter` 和 `FilterChain` 的**请求处理链**概念。传入的 HTTP 请求在到达 servlet（或控制器/处理器）之前会经过一系列过滤器，并且可以在返回途中修改响应。

- 过滤器允许对请求/响应进行预处理（例如，身份验证、日志记录、压缩）和后处理。
- 核心机制——实现 `Filter`，调用 `chain.doFilter(request, response)` 以继续——是**相同的**，因为两者都在 Servlet 容器中运行（WAS 拥有自己的完整 Java EE Web 容器；Spring Boot 默认嵌入 Tomcat/Jetty/Undertow）。

基本的“请求链过滤器”的工作方式没有根本区别。然而，由于每个平台的架构不同，配置、排序和集成过滤器的方式存在显著差异。

### 关键比较

| 方面                   | IBM WebSphere Application Server（传统版/Liberty） | Spring Boot |
|------------------------|-----------------------------------------------------|-------------|
| **底层机制**           | 标准 Servlet 过滤器（`javax.servlet.Filter`）。WAS 在某些场景（例如门户或自定义 IBM API）中还有专有扩展，如用于内部请求转发/链式的 `ChainedRequest`/`ChainedResponse`。 | 标准 Servlet 过滤器。Spring Boot 自动注册任何 `@Component` Filter bean，或者您可以通过 `FilterRegistrationBean` 显式注册。 |
| **配置**               | 主要通过 `web.xml`（声明式）或编程式注册。对于全局过滤器（跨所有应用）：复杂——需要共享库、自定义监听器或 IBM 特定扩展（没有像 Tomcat 那样的简单服务器范围的 web.xml）。 | 约定优于配置：使用 `@Component` + `@Order` 注解进行自动注册，或使用 `FilterRegistrationBean` 进行精细控制（URL 模式、分发器类型）。非常开发者友好。 |
| **排序**               | 在 `web.xml` 中定义顺序，或者如果是编程式则通过 `@Order`。全局排序很棘手。 | 使用 `@Order(n)`（数值越小优先级越高）或 `Ordered` 接口很容易。Spring Boot 自动管理链。 |
| **安全过滤器链**       | 使用标准 Servlet 过滤器或 IBM 特定安全机制（例如 TAI、JEE 角色）。没有像 Spring Security 那样的内置安全链。 | Spring Security 提供了一个强大的 `SecurityFilterChain`（通过 `FilterChainProxy`），包含 15 个以上有序过滤器（CSRF、身份验证、会话管理等）。高度可定制，支持每个路径多个链。 |
| **添加自定义过滤器的便利性** | 更繁琐，特别是对于全局/跨应用过滤器。通常需要管理员控制台调整或共享库。 | 极其简单——只需一个 `@Component` bean 或配置类。自动集成到嵌入式容器中。 |
| **部署模型**           | 传统的完整 Java EE 服务器。应用部署为 WAR/EAR。支持重量级企业功能（集群、事务、JMS）。 | 嵌入式容器（默认独立可执行 JAR）。可以作为 WAR 部署到外部服务器（包括 WAS）。轻量级/面向微服务。 |
| **性能/开销**          | 更高的开销（完整的应用服务器）。传输链、Web 容器通道增加了层。 | 较低的开销（嵌入式轻量级容器）。更快的启动速度，更少的资源使用。 |
| **过滤器何时运行**     | 在 WAS Web 容器入站链中。可以有服务器级传输过滤器（例如，TCP 通道上的 IP 过滤）。 | 在嵌入式容器的过滤器链中。Spring Boot 添加了自己的过滤器（错误处理、字符编码等）。 |
| **常见用例**           | 企业单体应用、门户、需要全局安全/日志记录的遗留 Java EE 应用。 | 现代微服务、REST API、利用 Spring Security 进行快速开发。 |

### 实际示例

**标准自定义过滤器（相同代码在两者中均可工作）：**
```java
@Component  // 仅 Spring Boot；在 WAS 中需在 web.xml 中声明
@Order(1)
public class LoggingFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        System.out.println("Request: " + ((HttpServletRequest) req).getRequestURI());
        chain.doFilter(req, res);  // 关键：传递给下一个过滤器/servlet
    }
    // init/destroy...
}
```

**在 Spring Boot 中（自动注册）：**
只需上述类 + `@Component`。

**在 WAS 中：**
添加到 `web.xml`：
```xml
<filter>
    <filter-name>LoggingFilter</filter-name>
    <filter-class>com.example.LoggingFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>LoggingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

### 何时选择哪个
- **使用 WAS 过滤器** 如果您处于传统的 IBM 环境中，需要完整的 Java EE 功能，或者必须在许多应用之间全局应用过滤器而无需更改代码。
- **使用 Spring Boot 过滤器**（尤其是与 Spring Security 一起）用于新的/绿地项目、微服务、快速迭代，或者当您需要多个安全链和简单排序时。

总之，**请求链过滤器的概念是相同的**（Servlet 规范），但对于大多数现代用例，**Spring Boot 使其更加简单和强大**，而 WAS 则更偏向企业级重量级和配置密集型。

[IBM WAS Servlet 过滤文档](https://www.ibm.com/docs/en/was/9.0.5?topic=extensions-servlet-filtering)
[Spring Boot 自定义过滤器](https://www.baeldung.com/spring-boot-add-filter)
[Spring Security 过滤器链](https://docs.spring.io/spring-security/reference/servlet/architecture.html)
