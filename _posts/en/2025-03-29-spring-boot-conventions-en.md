---
audio: false
generated: true
lang: en
layout: post
title: Spring Boot Java Coding Conventions
translated: false
type: note
---

## 1. Core Principles
- Follow the standard Java Code Conventions
- Prioritize readability and maintainability
- Consistency across the Spring ecosystem
- Align with core Java best practices

## 2. Code Formatting

### General Guidelines
- Use IntelliJ IDEA's default formatting
- 4-space indentation (not tabs)
- Maximum line length of 120 characters
- Use standard Java bracing style

### Specific Formatting Rules
- Blank line between methods
- No trailing whitespaces
- Use Unix-style line endings (LF)

## 3. Naming Conventions

### Class Naming
- Use descriptive, meaningful names
- Use UpperCamelCase
- Examples:
  - `ConfigurationProperties`
  - `AutoConfigurationImportSelector`
  - `SpringApplication`

### Method Naming
- Use lowerCamelCase
- Verb or verb phrases
- Examples:
  - `configure()`
  - `registerBeanDefinitions()`
  - `isEnabledByDefault()`

## 4. Annotation Practices

### Annotation Ordering
- Standard order for annotations:
  1. Override annotations (`@Override`)
  2. Scope annotations (`@Component`, `@Service`)
  3. Dependency injection annotations
  4. Transactional annotations
  5. Custom project annotations

### Annotation Placement
```java
@Component
@Transactional
public class UserService {
    @Autowired
    private UserRepository repository;
}
```

## 5. Dependency Injection

### Preferred Injection Method
- Constructor injection
- Avoid field injection
- Use `@Autowired` on constructor

```java
@Service
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

## 6. Logging
- Use SLF4J for logging
- Use `private static final Logger` or Lombok's `@Slf4j`

```java
@Slf4j
@Service
public class UserService {
    public void processUser(User user) {
        log.info("Processing user: {}", user.getUsername());
    }
}
```

## 7. Error Handling
- Use specific exceptions
- Provide meaningful error messages
- Use `@ControllerAdvice` for global exception handling

## 8. Configuration
- Use `application.yml` over `application.properties`
- Use profile-specific configurations
- Externalize configuration values

## 9. Testing
- Use JUnit 5
- Leverage Spring Boot Test utilities
- Follow Arrange-Act-Assert pattern

## 10. Additional Resources
- [Spring Boot GitHub Coding Style](https://github.com/spring-projects/spring-boot/blob/main/CONTRIBUTING.md)
- [Spring Framework Guidelines](https://github.com/spring-projects/spring-framework/wiki/Code-Style)
