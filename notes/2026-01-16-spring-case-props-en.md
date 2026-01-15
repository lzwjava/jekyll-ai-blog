---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Recommended Case for Spring Properties
translated: false
type: note
---

**Question:** What case should we use in Spring properties?

**Answer:**

In Spring Boot (and Spring Framework in general), the **recommended and most commonly used** case for **properties keys** (in `application.properties`, `application.yml`, environment variables, etc.) in 2025–2026 is:

**kebab-case** (lowercase with hyphens)

```properties
# This is the Spring Boot team recommended style
server.port=8080
spring.datasource.url=jdbc:...
management.endpoints.web.exposure.include=health,info,prometheus
logging.level.org.springframework.web=DEBUG
spring.jpa.hibernate.ddl-auto=none
```

### Official & community conventions in 2025–2026

| Style          | Example                              | Status in Spring Boot                  | When you still see it                     |
|----------------|--------------------------------------|----------------------------------------|--------------------------------------------|
| **kebab-case** | `spring.datasource.url`              | **Recommended • Official default**     | Everywhere in docs, starters, examples    |
| **camelCase**  | `spring.datasource.url`              | Supported, but **not preferred**       | Old code, people coming from Java-land    |
| **snake_case** | `spring_datasource_url`              | Supported (mostly env vars)            | Kubernetes ConfigMaps, some Helm charts   |
| **UPPER_CASE** | `SPRING_DATASOURCE_URL`              | Supported (environment variables)      | Docker, Kubernetes, CI/CD, 12-factor apps |

### Quick rules most teams follow today

- Use **kebab-case** in `application.properties` and `application.yml`
- Use **kebab-case** when writing `@Value`, `@ConfigurationProperties` prefixes
- Use **UPPERCASE_WITH_UNDERSCORES** when reading from environment variables

```java
// Recommended
@ConfigurationProperties(prefix = "feature-toggle")
public class FeatureToggleProperties { … }

// Still works, but less common now
@ConfigurationProperties(prefix = "featureToggle")
```

### YAML is even stricter — kebab-case is basically mandatory for readability

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

### Summary – what to use in new code (2026 best practice)

- `application.properties` / `application.yml` → **kebab-case**
- `@ConfigurationProperties` prefix → **kebab-case**
- Environment variables → **UPPER_SNAKE_CASE**
- Java/Kotlin field names → **camelCase** or **PascalCase**

Almost every new Spring Boot project started in 2024–2026 follows **kebab-case** for properties.

**References:**

- [Spring Boot Externalized Configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [Spring Boot Appendix A – Common application properties](https://docs.spring.io/spring-boot/appendix/application-properties/index.html)