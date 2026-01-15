---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 春季物业推荐案例
translated: true
type: note
---

**Question:** 在 Spring properties 中我们应该使用哪种命名命名规范（Case）？

**Answer:**

在 Spring Boot（以及整个 Spring Framework）中，2025–2026 年间针对 **properties keys**（在 `application.properties`、`application.yml`、环境变量等中）**推荐且最常用**的命名规范是：

**kebab-case**（小写字母加连字符）

```properties
# 这是 Spring Boot 团队推荐的风格
server.port=8080
spring.datasource.url=jdbc:...
management.endpoints.web.exposure.include=health,info,prometheus
logging.level.org.springframework.web=DEBUG
spring.jpa.hibernate.ddl-auto=none
```

### 2025–2026 年的官方与社区惯例

| Style          | Example                              | Status in Spring Boot                  | When you still see it                     |
|----------------|--------------------------------------|----------------------------------------|--------------------------------------------|
| **kebab-case** | `spring.datasource.url`              | **Recommended • 官方默认**            | 文档、starters、示例中随处可见           |
| **camelCase**  | `spring.datasource.url`              | 支持，但**不推荐**                     | 旧代码，从 Java 开发转过来的人员          |
| **snake_case** | `spring_datasource_url`              | 支持（主要用于环境变量）               | Kubernetes ConfigMaps, 某些 Helm charts   |
| **UPPER_CASE** | `SPRING_DATASOURCE_URL`              | 支持（环境变量）                       | Docker, Kubernetes, CI/CD, 12-factor apps |

### 目前大多数团队遵守的快速规则

- 在 `application.properties` 和 `application.yml` 中使用 **kebab-case**
- 在编写 `@Value`、`@ConfigurationProperties` 前缀时使用 **kebab-case**
- 在从环境变量读取时使用 **UPPERCASE_WITH_UNDERSCORES**

```java
// 推荐
@ConfigurationProperties(prefix = "feature-toggle")
public class FeatureToggleProperties { … }

// 仍然有效，但现在较少见
@ConfigurationProperties(prefix = "featureToggle")
```

### YAML 更加严格 —— 为了可读性，kebab-case 基本上是强制性的

```yaml
spring:
  datasource:
    url: jdbc:postgresql://...
    username: app_user
    hikari:
      maximum-pool-size: 15
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus
```

### 总结 – 新代码中应使用的规范 (2026 最佳实践)

- `application.properties` / `application.yml` → **kebab-case**
- `@ConfigurationProperties` 前缀 → **kebab-case**
- 环境变量 → **UPPER_SNAKE_CASE**
- Java/Kotlin 字段名 → **camelCase** 或 **PascalCase**

几乎所有在 2024–2026 年启动的新 Spring Boot 项目在 properties 中都遵循 **kebab-case**。

**References:**

- [Spring Boot Externalized Configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [Spring Boot Appendix A – Common application properties](https://docs.spring.io/spring-boot/appendix/application-properties/index.html)