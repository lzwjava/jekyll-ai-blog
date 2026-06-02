---
audio: false
generated: true
lang: en
layout: post
title: Understanding Pointcut Expressions
translated: false
type: note
---

You're asking for a comprehensive guide on AspectJ pointcut expressions, specifically focusing on `execution` and how to use wildcards, match class names (prefix/suffix), and also about other advice types like `@AfterReturning`. Let's break this down.

### Understanding Pointcut Expressions in Spring AOP (AspectJ Syntax)

Spring AOP uses AspectJ pointcut expressions to determine *where* an advice (like `@Before`, `@AfterReturning`, etc.) should be applied. The core of your question revolves around the `execution` pointcut designator, which is the most commonly used one.

#### The `execution` Pointcut Designator

The `execution` pointcut designator matches method executions. Its general syntax is:

`execution(modifiers-pattern? ret-type-pattern declaring-type-pattern?name-pattern(param-pattern) throws-pattern?)`

Let's break down the components:

* **`modifiers-pattern?`**: Optional. Matches method modifiers (e.g., `public`, `private`, `protected`).
* **`ret-type-pattern`**: Required. Matches the return type of the method.
* **`declaring-type-pattern?`**: Optional. Matches the fully qualified class name where the method is declared.
* **`name-pattern`**: Required. Matches the name of the method.
* **`param-pattern`**: Required. Matches the parameters of the method.
* **`throws-pattern?`**: Optional. Matches the exceptions thrown by the method.

#### Your Example: `@Before("execution(* com.example.service.*.*(..))")`

Let's dissect your given example:

* `@Before`: This is an advice annotation, meaning the annotated method will run *before* the matched join point.
* `execution()`: The pointcut designator.
* `*`: Matches any return type.
* `com.example.service.*.*`:
    * `com.example.service`: Matches the package `com.example.service`.
    * `.*`: The first `*` after `service` matches any class within the `com.example.service` package.
    * `.`: Separator between package/class and method.
    * `*`: The second `*` matches any method name within those classes.
* `(..)`: Matches any number of parameters (zero or more, of any type).

**In plain English:** This pointcut matches the execution of *any method* in *any class* within the `com.example.service` package (and its direct sub-packages, if any classes are directly in `com.example.service`).

---

### Wildcards in Pointcut Expressions

Wildcards are crucial for creating flexible pointcut expressions.

* **`*` (single asterisk)**:
    * Matches any single element in a name pattern (e.g., any return type, any class name, any method name).
    * Matches any single segment in a package name (e.g., `com.example.*.service` would match `com.example.foo.service`).
* **`..` (double dot)**:
    * **In package patterns**: Matches zero or more segments in a package name.
        * `com.example..service`: Matches `com.example.service`, `com.example.foo.service`, `com.example.foo.bar.service`, etc.
    * **In parameter patterns**: Matches zero or more arguments of any type.
        * `(..)`: Matches any number of arguments.
        * `(java.lang.String, ..)`: Matches methods with a `String` as the first argument, followed by any number of other arguments.
        * `(.., java.lang.Long)`: Matches methods with any number of initial arguments, ending with a `Long`.

---

### Matching Class Names

#### 1. Matching Suffix Class Name

To match classes ending with a specific suffix, you place the wildcard before the suffix.

**Example: Match all classes ending with `ServiceImpl`**

```java
@Before("execution(* com.example.service.*ServiceImpl.*(..))")
```

* `*ServiceImpl`: Matches any class name that ends with `ServiceImpl`.

**Example: Match all classes ending with `Controller` in any sub-package of `com.example.web`**

```java
@Before("execution(* com.example.web..*Controller.*(..))")
```

* `com.example.web..`: Matches `com.example.web` and any of its sub-packages.
* `*Controller`: Matches any class name ending with `Controller`.

#### 2. Matching Prefix Class Name

To match classes starting with a specific prefix, you place the wildcard after the prefix.

**Example: Match all classes starting with `User`**

```java
@Before("execution(* com.example.service.User*.*(..))")
```

* `User*`: Matches any class name that starts with `User`.

**Example: Match all classes starting with `Admin` in `com.example.admin` package**

```java
@Before("execution(* com.example.admin.Admin*.*(..))")
```

#### 3. Matching Specific Class Names (Exact Match)

No wildcards needed for exact matches.

**Example: Match methods in `com.example.service.UserServiceImpl` only**

```java
@Before("execution(* com.example.service.UserServiceImpl.*(..))")
```

---

### Different Kinds of Pointcut Designators

While `execution` is the most common, AspectJ provides several other pointcut designators to specify join points. You can combine these using logical operators (`and`, `or`, `not` or `&&`, `||`, `!`).

Here are the most important ones:

1.  **`execution()`**: As discussed, matches method executions.
    * Example: `@Before("execution(* com.example.service.UserService.*(..))")`

2.  **`within()`**: Matches join points where the code is within a certain type (class). This is often used to restrict the scope of other pointcuts.
    * Example: `@Before("within(com.example.service.*) && execution(* *(..))")`
        * This combines `within` and `execution`. It means "any method execution within any class in the `com.example.service` package." The `execution` part is then just a wildcard for any method, as `within` handles the class matching.

3.  **`this()`**: Matches join points where the proxy *itself* is an instance of the given type. This is less commonly used for simple advice and more for introductions or self-invocation issues.
    * Example: `@Around("this(com.example.service.UserService)")`
        * Matches if the AOP proxy implements `UserService`.

4.  **`target()`**: Matches join points where the *target object* (the actual object being advised, not the proxy) is an instance of the given type. This is often more intuitive than `this()` when you care about the underlying implementation.
    * Example: `@Around("target(com.example.service.UserServiceImpl)")`
        * Matches if the target object is an instance of `UserServiceImpl`.

5.  **`args()`**: Matches join points where the arguments are of a certain type or match a certain pattern.
    * Example: `@Before("execution(* com.example.service.*.*(String, ..))")`
        * Matches methods where the first argument is a `String`.
    * Example: `@Before("args(java.lang.String, int)")`
        * Matches methods that take exactly a `String` followed by an `int`.
    * Example: `@Before("args(name, age)")` where `name` and `age` can then be bound to the advice method parameters.

6.  **`bean()`**: (Spring-specific) Matches methods executed on Spring beans with specific names or name patterns.
    * Example: `@Before("bean(userService) && execution(* *(..))")`
        * Matches any method execution on the Spring bean named "userService".
    * Example: `@Before("bean(*Service) && execution(* *(..))")`
        * Matches any method execution on Spring beans whose names end with "Service".

7.  **`@annotation()`**: Matches join points where the target method (or class for `within`) is annotated with a specific annotation.
    * Example: `@Before("@annotation(com.example.annotation.Loggable)")`
        * Matches any method that is annotated with `@Loggable`.
    * Example: `@Before("execution(* *(..)) && @annotation(org.springframework.transaction.annotation.Transactional)")`
        * Matches any method execution that is annotated with `@Transactional`.

8.  **`@within()`**: Matches join points where the declaring type (class) is annotated with a specific annotation.
    * Example: `@Before("@within(org.springframework.stereotype.Service) && execution(* *(..))")`
        * Matches any method execution within a class that is annotated with `@Service`.

9.  **`@target()`**: Matches join points where the class of the target object has the given annotation.
    * Example: `@Around("@target(com.example.annotation.Auditable)")`

10. **`@args()`**: Matches join points where the runtime type of the actual arguments passed to the method has annotations of the given type(s).
    * Example: `@Before("@args(com.example.annotation.ValidInput)")`

---

### Advice Types (Annotations)

You mentioned `@AfterReturning` and "any other we can use in annotations." Spring AOP provides several advice types, each executing at a different point in the join point's lifecycle:

1.  **`@Before`**:
    * Executes *before* the matched method execution.
    * Example: Logging request details before a service method runs.
    * Cannot prevent the method from executing or alter its return value.

2.  **`@AfterReturning`**:
    * Executes *after* the matched method returns *successfully* (without throwing an exception).
    * Can access the return value of the method.
    * Syntax: `@AfterReturning(pointcut="yourPointcut()", returning="result")`
    * Example:
        ```java
        @AfterReturning(pointcut="execution(* com.example.service.UserService.getUserById(..))", returning="user")
        public void logUserRetrieval(Object user) {
            System.out.println("User retrieved: " + user);
        }
        ```
        *Note: The `returning` attribute name (`user` in this case) must match the parameter name in the advice method.*

3.  **`@AfterThrowing`**:
    * Executes *after* the matched method throws an exception.
    * Can access the thrown exception.
    * Syntax: `@AfterThrowing(pointcut="yourPointcut()", throwing="ex")`
    * Example:
        ```java
        @AfterThrowing(pointcut="execution(* com.example.service.*.*(..))", throwing="ex")
        public void logException(Exception ex) {
            System.err.println("Exception occurred: " + ex.getMessage());
        }
        ```
        *Note: The `throwing` attribute name (`ex` in this case) must match the parameter name in the advice method.*

4.  **`@After` (finally advice)**:
    * Executes *after* the matched method completes, regardless of whether it returned successfully or threw an exception.
    * Similar to a `finally` block.
    * Example: Releasing resources, regardless of method outcome.
    * ```java
        @After("execution(* com.example.service.OrderService.placeOrder(..))")
        public void cleanupOrderProcess() {
            System.out.println("Order process completed (cleanup)");
        }
        ```

5.  **`@Around`**:
    * The most powerful and flexible advice type.
    * Executes *around* the matched method execution.
    * You are responsible for invoking the actual method using `ProceedingJoinPoint.proceed()`.
    * Can inspect, modify, or even suppress the method's arguments and return value.
    * Can catch and handle exceptions thrown by the advised method.
    * Example: Performance monitoring, transaction management, caching.
    * ```java
        import org.aspectj.lang.ProceedingJoinPoint;
        import org.aspectj.lang.annotation.Around;
        import org.aspectj.lang.annotation.Aspect;

        @Aspect
        public class PerformanceMonitorAspect {

            @Around("execution(* com.example.service.*.*(..))")
            public Object profile(ProceedingJoinPoint joinPoint) throws Throwable {
                long start = System.currentTimeMillis();
                Object result = joinPoint.proceed(); // Execute the original method
                long end = System.currentTimeMillis();
                System.out.println(joinPoint.getSignature().getName() + " executed in " + (end - start) + "ms");
                return result;
            }
        }
        ```

### Defining Reusable Pointcuts

For better readability and reusability, you can define named pointcuts using `@Pointcut`.

```java
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.AfterReturning;

@Aspect
public class MyServiceAspect {

    // Define a pointcut for all methods in com.example.service package
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}

    // Define a pointcut for methods that return a User object
    @Pointcut("execution(com.example.model.User com.example.service.*.*(..))")
    public void returnsUser() {}

    // Using the defined pointcut
    @Before("serviceMethods()")
    public void logBeforeServiceCall() {
        System.out.println("Before service method execution.");
    }

    // Combining pointcuts with logical AND
    @AfterReturning(pointcut="serviceMethods() && returnsUser()", returning="user")
    public void logUserReturned(Object user) {
        System.out.println("Service method returned user: " + user);
    }

    // You can also define pointcuts with arguments
    @Pointcut("execution(* com.example.repository.*.save(..)) && args(entity)")
    public void repositorySave(Object entity) {}

    @Before("repositorySave(entity)")
    public void logEntityBeforeSave(Object entity) {
        System.out.println("Saving entity: " + entity);
    }
}
```

This comprehensive guide covers the essentials of pointcut expressions, wildcard usage, class name matching, and the different advice types in Spring AOP. Mastering these concepts will allow you to precisely control where and when your cross-cutting concerns are applied.
