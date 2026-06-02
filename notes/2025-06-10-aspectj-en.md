---
audio: false
generated: true
lang: en
layout: post
title: AspectJ with Java and Spring Boot
translated: false
type: note
---

## Table of Contents
1. [Introduction to Aspect-Oriented Programming (AOP)](#introduction-to-aspect-oriented-programming-aop)
2. [AspectJ Overview](#aspectj-overview)
3. [AspectJ with Java](#aspectj-with-java)
4. [AspectJ with Spring Boot](#aspectj-with-spring-boot)
5. [Common Use Cases](#common-use-cases)
6. [Best Practices](#best-practices)
7. [Performance Considerations](#performance-considerations)

## Introduction to Aspect-Oriented Programming (AOP)

AOP is a programming paradigm that aims to increase modularity by allowing separation of cross-cutting concerns. Cross-cutting concerns are functionalities that span multiple parts of a system (like logging, security, transaction management).

Key AOP concepts:
- **Aspect**: A modularization of a concern that cuts across multiple classes
- **Join point**: A point during program execution (method call, field access, etc.)
- **Advice**: Action taken at a particular join point
- **Pointcut**: Predicate that matches join points
- **Weaving**: Linking aspects with other application types

## AspectJ Overview

AspectJ is the most popular and full-featured AOP implementation for Java. It provides:
- A powerful pointcut language
- Different weaving mechanisms (compile-time, post-compile, load-time)
- Full AOP support beyond what Spring AOP offers

### AspectJ vs Spring AOP

| Feature            | AspectJ | Spring AOP |
|--------------------|---------|------------|
| Join Points        | Method execution, constructor calls, field access, etc. | Only method execution |
| Weaving            | Compile-time, post-compile, load-time | Runtime proxying |
| Performance        | Better (no runtime overhead) | Slightly slower (uses proxies) |
| Complexity         | More complex | Simpler |
| Dependencies       | Requires AspectJ compiler/weaver | Built into Spring |

## AspectJ with Java

### Setup

1. Add AspectJ dependencies to your `pom.xml` (Maven):

```xml
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjrt</artifactId>
    <version>1.9.7</version>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.9.7</version>
</dependency>
```

2. Configure the AspectJ Maven plugin for compile-time weaving:

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>aspectj-maven-plugin</artifactId>
    <version>1.14.0</version>
    <configuration>
        <complianceLevel>11</complianceLevel>
        <source>11</source>
        <target>11</target>
        <showWeaveInfo>true</showWeaveInfo>
        <verbose>true</verbose>
        <Xlint>ignore</Xlint>
        <encoding>UTF-8</encoding>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>compile</goal>
                <goal>test-compile</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### Creating Aspects

```java
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;

@Aspect
public class LoggingAspect {

    // Pointcut definition
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}

    // Advice
    @Before("serviceMethods()")
    public void logBeforeServiceMethods() {
        System.out.println("A service method is about to be executed");
    }
}
```

### Advice Types

1. **Before**: Executed before a join point
2. **After**: Executed after a join point completes (normally or exceptionally)
3. **AfterReturning**: Executed after a join point completes normally
4. **AfterThrowing**: Executed if a method exits by throwing an exception
5. **Around**: Surrounds a join point (most powerful advice)

### Pointcut Expressions

AspectJ provides a rich pointcut expression language:

```java
// Method execution in package
@Pointcut("execution(* com.example.service.*.*(..))")

// Method execution in class
@Pointcut("execution(* com.example.service.UserService.*(..))")

// Method with specific name
@Pointcut("execution(* *..find*(..))")

// With specific return type
@Pointcut("execution(public String com.example..*(..))")

// With specific parameter types
@Pointcut("execution(* *.*(String, int))")

// Combining pointcuts
@Pointcut("serviceMethods() && findMethods()")
```

## AspectJ with Spring Boot

### Setup

1. Add Spring AOP and AspectJ dependencies:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.9.7</version>
</dependency>
```

2. Enable AspectJ support in your Spring Boot application:

```java
@SpringBootApplication
@EnableAspectJAutoProxy
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

### Example: Logging Execution Time

```java
@Aspect
@Component
public class ExecutionTimeAspect {

    private static final Logger logger = LoggerFactory.getLogger(ExecutionTimeAspect.class);

    @Around("@annotation(com.example.annotation.LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();

        Object proceed = joinPoint.proceed();

        long executionTime = System.currentTimeMillis() - startTime;

        logger.info("{} executed in {} ms",
            joinPoint.getSignature(), executionTime);

        return proceed;
    }
}
```

Create a custom annotation:

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LogExecutionTime {
}
```

Use it on methods:

```java
@Service
public class UserService {

    @LogExecutionTime
    public List<User> getAllUsers() {
        // implementation
    }
}
```

### Example: Transaction Management

```java
@Aspect
@Component
public class TransactionAspect {

    @Autowired
    private PlatformTransactionManager transactionManager;

    @Around("@annotation(com.example.annotation.Transactional)")
    public Object manageTransaction(ProceedingJoinPoint joinPoint) throws Throwable {
        TransactionDefinition def = new DefaultTransactionDefinition();
        TransactionStatus status = transactionManager.getTransaction(def);

        try {
            Object result = joinPoint.proceed();
            transactionManager.commit(status);
            return result;
        } catch (Exception e) {
            transactionManager.rollback(status);
            throw e;
        }
    }
}
```

## Common Use Cases

1. **Logging**: Centralized logging of method entries/exceptions
2. **Performance Monitoring**: Track execution times
3. **Transaction Management**: Declarative transaction boundaries
4. **Security**: Authorization checks
5. **Error Handling**: Consistent exception handling
6. **Caching**: Automatic method result caching
7. **Validation**: Parameter validation
8. **Auditing**: Track who did what and when

## Best Practices

1. **Keep aspects focused**: Each aspect should handle one concern
2. **Use meaningful names**: Clear aspect and pointcut names
3. **Avoid business logic in aspects**: Aspects should handle cross-cutting concerns, not core logic
4. **Document aspects**: Especially complex pointcuts
5. **Consider performance**: Around advice can impact performance
6. **Test aspects**: Aspects need testing like any other code
7. **Use annotations**: Custom annotations make aspects more declarative
8. **Be careful with execution() vs @annotation()**: Know when to use each

## Performance Considerations

1. **Compile-time weaving** is generally the fastest option
2. **Load-time weaving** adds some overhead during class loading
3. **Runtime weaving** (Spring AOP) has the most overhead
4. **Complex pointcuts** can impact performance
5. **Around advice** is more expensive than other advice types

For maximum performance in production:
- Use compile-time weaving where possible
- Keep pointcuts simple
- Avoid overly broad pointcut expressions

## Conclusion

AspectJ provides a powerful way to implement cross-cutting concerns in Java and Spring Boot applications. While Spring AOP is simpler and sufficient for many cases, AspectJ offers more capabilities when you need to go beyond method interception. By following the patterns and best practices outlined in this guide, you can effectively use AspectJ to create more modular, maintainable applications.
