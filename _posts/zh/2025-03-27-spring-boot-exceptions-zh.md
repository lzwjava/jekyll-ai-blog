---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot异常处理
translated: true
type: note
---

在使用 Spring Boot 或更广泛的 Spring 框架时，开发者经常会因配置问题、运行时错误或 API 使用不当而遇到异常。以下列出了您可能遇到的常见异常及其典型原因和潜在解决方案。为清晰起见，这些异常已按类别分组。

---

### **1. 配置相关异常**

- **`org.springframework.beans.factory.BeanCreationException`**：
  - **原因**：由于缺少依赖项、配置错误或实例化错误，Bean 创建失败。
  - **示例**：缺少 `@Component`、`@Service` 或 `@Autowired` 依赖项未找到。
  - **解决方案**：检查 Bean 定义，确保依赖项可用，并验证注解。

- **`org.springframework.beans.factory.NoSuchBeanDefinitionException`**：
  - **原因**：Spring 在应用上下文中找不到请求类型或名称的 Bean。
  - **示例**：尝试 `@Autowired` 一个未定义或未被扫描到的 Bean。
  - **解决方案**：确保 Bean 已注解（例如 `@Component`）并在组件扫描路径内。

- **`org.springframework.context.ApplicationContextException`**：
  - **原因**：Spring 应用上下文初始化失败。
  - **示例**：`application.properties` 中的配置无效或 `@Configuration` 类中存在语法错误。
  - **解决方案**：查看堆栈跟踪以找到根本原因（例如无效属性或缺失资源）。

- **`org.springframework.beans.factory.UnsatisfiedDependencyException`**：
  - **原因**：Bean 所需的依赖项无法满足。
  - **示例**：循环依赖或接口缺少实现。
  - **解决方案**：打破循环依赖（例如使用 `@Lazy`）或提供缺失的依赖项。

---

### **2. Web 和 REST 相关异常**

- **`org.springframework.web.bind.MissingServletRequestParameterException`**：
  - **原因**：HTTP 请求中缺少必需的请求参数。
  - **示例**：指定了 `@RequestParam("id")`，但客户端未发送 `id`。
  - **解决方案**：将参数设为可选（`required = false`）或确保客户端包含该参数。

- **`org.springframework.http.converter.HttpMessageNotReadableException`**：
  - **原因**：请求体无法反序列化（例如格式错误的 JSON）。
  - **示例**：向 `@RequestBody` 端点发送无效的 JSON。
  - **解决方案**：验证请求负载并确保其与目标对象结构匹配。

- **`org.springframework.web.method.annotation.MethodArgumentTypeMismatchException`**：
  - **原因**：方法参数无法转换为预期类型。
  - **示例**：将字符串（如 `"abc"`）传递给期望 `int` 类型的参数。
  - **解决方案**：验证输入或使用自定义转换器。

- **`org.springframework.web.servlet.NoHandlerFoundException`**：
  - **原因**：请求的 URL 没有对应的控制器映射。
  - **示例**：`@RequestMapping` 中存在拼写错误或缺少控制器。
  - **解决方案**：验证端点映射并确保控制器已被扫描。

---

### **3. 数据访问（Spring Data/JPA/Hibernate）异常**

- **`org.springframework.dao.DataIntegrityViolationException`**：
  - **原因**：数据库操作违反了约束（例如唯一键或外键）。
  - **示例**：插入重复的主键值。
  - **解决方案**：检查数据的唯一性或优雅地处理异常。

- **`org.springframework.orm.jpa.JpaSystemException`**：
  - **原因**：与 JPA 相关的运行时错误，通常包装了 Hibernate 异常。
  - **示例**：约束违规或连接问题。
  - **解决方案**：检查嵌套异常（例如 `SQLException`）以获取详细信息。

- **`org.hibernate.LazyInitializationException`**：
  - **原因**：尝试在活动会话之外访问延迟加载的实体。
  - **示例**：在事务结束后访问 `@OneToMany` 关系。
  - **解决方案**：使用急切获取、在查询中获取（例如 `JOIN FETCH`）或确保会话处于打开状态。

- **`org.springframework.dao.InvalidDataAccessApiUsageException`**：
  - **原因**：错误使用 Spring Data 或 JDBC API。
  - **示例**：向需要值的查询传递了 null 参数。
  - **解决方案**：验证查询参数和 API 使用方式。

---

### **4. 安全相关异常**

- **`org.springframework.security.access.AccessDeniedException`**：
  - **原因**：经过身份验证的用户缺少对资源的权限。
  - **示例**：在没有所需角色的情况下访问受保护的端点。
  - **解决方案**：检查 `@PreAuthorize` 或安全配置，并调整角色/权限。

- **`org.springframework.security.authentication.BadCredentialsException`**：
  - **原因**：由于用户名或密码错误导致身份验证失败。
  - **示例**：用户在登录表单中输入了错误的凭据。
  - **解决方案**：确保凭据正确；自定义错误处理以向用户提供反馈。

- **`org.springframework.security.authentication.DisabledException`**：
  - **原因**：用户账户已被禁用。
  - **示例**：`UserDetails` 实现返回 `isEnabled() == false`。
  - **解决方案**：启用账户或更新用户状态。

---

### **5. 其他运行时异常**

- **`java.lang.IllegalStateException`**：
  - **原因**：Spring 在执行过程中遇到无效状态。
  - **示例**：在尚未完全初始化的 Bean 上调用方法。
  - **解决方案**：检查生命周期方法或 Bean 初始化顺序。

- **`org.springframework.transaction.TransactionException`**：
  - **原因**：事务管理过程中出现问题。
  - **示例**：由于未处理的异常导致事务回滚。
  - **解决方案**：确保正确使用 `@Transactional` 并在事务内处理异常。

- **`java.lang.NullPointerException`**：
  - **原因**：尝试访问空对象引用。
  - **示例**：由于配置错误，`@Autowired` 依赖项未被注入。
  - **解决方案**：添加空值检查或调试依赖项缺失的原因。

---

### **6. Spring Boot 特定异常**

- **`org.springframework.boot.context.embedded.EmbeddedServletContainerException`**（旧版本）或 **`org.springframework.boot.web.server.WebServerException`**（新版本）：
  - **原因**：启动嵌入式 Web 服务器（例如 Tomcat、Jetty）失败。
  - **示例**：端口已被占用（例如 `8080`）。
  - **解决方案**：在 `application.properties` 中更改端口（`server.port=8081`）或释放被占用的端口。

- **`org.springframework.boot.autoconfigure.jdbc.DataSourceProperties$DataSourceBeanCreationException`**：
  - **原因**：数据源配置失败。
  - **示例**：缺少或不正确的 `spring.datasource.url/username/password`。
  - **解决方案**：验证 `application.properties` 或 `application.yml` 中的数据源属性。

- **`org.springframework.boot.SpringApplication - Application run failed`**：
  - **原因**：Spring Boot 启动期间发生通用故障。
  - **示例**：配置错误、Bean 缺失或依赖冲突。
  - **解决方案**：检查完整堆栈跟踪以找到根本原因。

---

### **处理异常的最佳实践**

1. **全局异常处理**：
   - 使用 `@ControllerAdvice` 和 `@ExceptionHandler` 在整个应用中一致地捕获和处理异常。
   - 示例：

     ```java
     @ControllerAdvice
     public class GlobalExceptionHandler {
         @ExceptionHandler(DataIntegrityViolationException.class)
         public ResponseEntity<String> handleDataIntegrityViolation() {
             return ResponseEntity.status(HttpStatus.CONFLICT).body("发生数据完整性冲突。");
         }
     }
     ```

2. **日志记录**：
   - 使用 SLF4J/Logback 等框架记录异常，以辅助调试。

3. **自定义异常**：
   - 定义应用特定的异常，并将其映射到适当的 HTTP 状态码。

4. **验证**：
   - 使用 `@Valid` 和 Bean 验证（例如 `@NotNull`）尽早捕获错误，避免运行时异常。

5. **调试**：
   - 在 `application.properties` 中启用详细日志（`logging.level.org.springframework=DEBUG`）以跟踪问题。

---

### **结论**

这些异常是使用 Spring Boot 或 Spring 框架时最常遇到的一部分。了解其原因和解决方案可以显著加快开发和调试速度。如果您遇到特定异常并需要深入探讨，请随时分享详细信息，我将提供针对性的解释！
