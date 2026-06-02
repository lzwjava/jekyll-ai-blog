---
audio: false
generated: true
lang: zh
layout: post
title: Spring AOP 使用指南
translated: true
type: note
---

## 1. Spring AOP 简介

Spring AOP（面向切面编程）是 Spring 框架的关键组件，提供了一种将横切关注点（如日志记录、安全性、事务管理）与业务逻辑分离的实现方式。

### 核心概念：
- **横切关注点**：跨越多个层的功能（日志记录、安全性等）
- **切面**：跨多个类的关注点的模块化
- **连接点**：程序执行过程中的某个点（方法执行、异常处理等）
- **通知**：切面在特定连接点执行的动作
- **切点**：匹配连接点的谓词
- **织入**：将切面与其他应用程序类型链接以创建通知对象

## 2. Spring AOP 与 AspectJ 对比

| 特性               | Spring AOP | AspectJ |
|-------------------|-----------|---------|
| 实现方式          | 运行时代理 | 编译时/加载时织入 |
| 性能              | 较慢 | 较快 |
| 支持的连接点      | 仅方法执行 | 全部（方法、构造函数、字段访问等） |
| 复杂度            | 较简单 | 更复杂 |
| 依赖关系          | 无额外依赖 | 需要 AspectJ 编译器/织入器 |

## 3. 核心 AOP 组件

### 3.1 切面
使用 `@Aspect` 注解的类，包含通知和切点。

```java
@Aspect
@Component
public class LoggingAspect {
    // 此处将包含通知和切点
}
```

### 3.2 通知类型

1. **Before**：在连接点之前执行
   ```java
   @Before("execution(* com.example.service.*.*(..))")
   public void beforeAdvice() {
       System.out.println("方法执行前");
   }
   ```

2. **AfterReturning**：在连接点正常完成后执行
   ```java
   @AfterReturning(pointcut = "execution(* com.example.service.*.*(..))", returning = "result")
   public void afterReturningAdvice(Object result) {
       System.out.println("方法返回值: " + result);
   }
   ```

3. **AfterThrowing**：在方法通过抛出异常退出时执行
   ```java
   @AfterThrowing(pointcut = "execution(* com.example.service.*.*(..))", throwing = "ex")
   public void afterThrowingAdvice(Exception ex) {
       System.out.println("抛出异常: " + ex.getMessage());
   }
   ```

4. **After (Finally)**：在连接点之后执行，无论结果如何
   ```java
   @After("execution(* com.example.service.*.*(..))")
   public void afterAdvice() {
       System.out.println("方法执行后 (finally)");
   }
   ```

5. **Around**：包装连接点，最强大的通知类型
   ```java
   @Around("execution(* com.example.service.*.*(..))")
   public Object aroundAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
       System.out.println("执行前");
       Object result = joinPoint.proceed();
       System.out.println("执行后");
       return result;
   }
   ```

### 3.3 切点表达式

切点使用表达式定义通知应该应用的位置：

- **Execution**：匹配方法执行
  ```java
  @Pointcut("execution(public * com.example.service.*.*(..))")
  public void serviceMethods() {}
  ```

- **Within**：匹配特定类型内的所有连接点
  ```java
  @Pointcut("within(com.example.service..*)")
  public void inServiceLayer() {}
  ```

- **this**：匹配给定类型实例的 bean
- **target**：匹配可分配给给定类型的 bean
- **args**：匹配具有特定参数类型的方法
- **@annotation**：匹配具有特定注解的方法

### 3.4 组合切点

可以使用逻辑运算符组合切点：
```java
@Pointcut("execution(* com.example.service.*.*(..)) && !execution(* com.example.service.UserService.*(..))")
public void serviceMethodsExceptUserService() {}
```

## 4. 实现步骤

### 4.1 设置

1. 添加 Spring AOP 依赖（如果不使用 Spring Boot）：
   ```xml
   <dependency>
       <groupId>org.springframework</groupId>
       <artifactId>spring-aop</artifactId>
       <version>${spring.version}</version>
   </dependency>
   <dependency>
       <groupId>org.aspectj</groupId>
       <artifactId>aspectjweaver</artifactId>
       <version>${aspectj.version}</version>
   </dependency>
   ```

2. 对于 Spring Boot，只需包含 `spring-boot-starter-aop`：
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-aop</artifactId>
   </dependency>
   ```

3. 在配置中启用 AOP：
   ```java
   @Configuration
   @EnableAspectJAutoProxy
   public class AppConfig {
   }
   ```

### 4.2 创建切面

```java
@Aspect
@Component
public class LoggingAspect {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        logger.info("进入: {}.{}() 参数 = {}",
            joinPoint.getSignature().getDeclaringTypeName(),
            joinPoint.getSignature().getName(),
            Arrays.toString(joinPoint.getArgs()));
    }

    @AfterReturning(pointcut = "execution(* com.example.service.*.*(..))",
                   returning = "result")
    public void logAfterReturning(JoinPoint joinPoint, Object result) {
        logger.info("退出: {}.{}() 返回值 = {}",
            joinPoint.getSignature().getDeclaringTypeName(),
            joinPoint.getSignature().getName(),
            result);
    }

    @Around("@annotation(com.example.annotations.LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object proceed = joinPoint.proceed();
        long executionTime = System.currentTimeMillis() - start;
        logger.info("{} 执行耗时 {} 毫秒",
            joinPoint.getSignature(), executionTime);
        return proceed;
    }
}
```

### 4.3 自定义注解

创建自定义注解来标记需要特定 AOP 行为的方法：

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LogExecutionTime {
}
```

然后在方法上使用：
```java
@Service
public class UserService {

    @LogExecutionTime
    public User getUser(Long id) {
        // 实现
    }
}
```

## 5. 高级主题

### 5.1 切面排序

使用 `@Order` 控制切面执行顺序：
```java
@Aspect
@Component
@Order(1)
public class LoggingAspect {
    // ...
}

@Aspect
@Component
@Order(2)
public class ValidationAspect {
    // ...
}
```

### 5.2 访问方法信息

在通知方法中，可以访问：
- `JoinPoint`（用于 Before、After、AfterReturning、AfterThrowing）
- `ProceedingJoinPoint`（用于 Around）

```java
@Before("execution(* com.example.service.*.*(..))")
public void beforeAdvice(JoinPoint joinPoint) {
    String methodName = joinPoint.getSignature().getName();
    String className = joinPoint.getTarget().getClass().getName();
    Object[] args = joinPoint.getArgs();
    // ...
}
```

### 5.3 异常处理

```java
@AfterThrowing(pointcut = "execution(* com.example.service.*.*(..))",
               throwing = "ex")
public void handleException(JoinPoint joinPoint, Exception ex) {
    // 记录异常、发送警报等
}
```

### 5.4 代理机制

Spring AOP 使用两种代理类型：
- **JDK 动态代理**：接口的默认代理方式
- **CGLIB 代理**：当没有接口可用时使用（可通过 `proxyTargetClass=true` 强制使用）

## 6. 最佳实践

1. **保持切面专注**：每个切面应处理一个特定的横切关注点
2. **使用有意义的切点名称**：使代码更易读
3. **避免在切面中进行昂贵操作**：它们为每个匹配的连接点运行
4. **谨慎使用 Around 通知**：除非有意阻止执行，否则始终调用 `proceed()`
5. **彻底测试切面**：它们影响应用程序的多个部分
6. **文档化切面**：特别是当它们显著修改行为时
7. **考虑性能**：复杂的切点或多个切面可能影响性能

## 7. 常见用例

1. **日志记录**：方法进入/退出、参数、返回值
2. **性能监控**：测量执行时间
3. **事务管理**：（通常由 Spring 的 `@Transactional` 处理）
4. **安全性**：授权检查
5. **验证**：参数验证
6. **错误处理**：一致的异常处理
7. **缓存**：方法结果缓存
8. **审计**：跟踪谁在何时调用了什么

## 8. 限制

1. 仅适用于 Spring 管理的 bean
2. 仅支持方法执行连接点
3. 无法通知 final 类或方法
4. 自调用（类内方法调用同一类的另一个方法）会绕过代理
5. 与 AspectJ 相比，切点表达式有限

## 9. 故障排除

**问题**：通知未执行
- 检查 bean 是否由 Spring 管理
- 验证切点表达式是否匹配预期方法
- 确保存在 `@EnableAspectJAutoProxy`

**问题**：Around 通知未继续执行
- 确保在 `ProceedingJoinPoint` 上调用 `proceed()`

**问题**：代理类型不正确
- 使用 `@EnableAspectJAutoProxy(proxyTargetClass=true)` 强制使用 CGLIB

## 10. 结论

Spring AOP 提供了一种强大而简单的方法来实现应用程序中的横切关注点。虽然与完整的 AspectJ 相比有一些限制，但它与 Spring 无缝集成并涵盖了大多数常见用例。通过遵循本指南中概述的模式和最佳实践，您可以有效地模块化横切关注点，并保持业务逻辑的清晰和专注。

---

尽管 Spring AOP 不使用 AspectJ 的织入功能（它使用基于代理的 AOP），但您仍然需要 `aspectjweaver` 依赖，原因如下：

### 1. **AspectJ 注解支持**
Spring AOP 使用 AspectJ 的**注解**（如 `@Aspect`、`@Pointcut`、`@Before`、`@After` 等）来定义切面和通知。这些注解来自 `aspectjweaver` 库。

- 没有它，在使用 `@Aspect` 或其他 AOP 注解时会出现编译错误。

### 2. **切点表达式语言**
Spring AOP 借用 AspectJ 的**切点表达式语言**来定义通知应该应用的位置（例如 `execution(* com.example.service.*.*(..))`）。

- `aspectjweaver` 为这些表达式提供解析器和匹配逻辑。

### 3. **支持额外的连接点（有限）**
虽然 Spring AOP 仅支持**方法执行**连接点（与支持构造函数、字段访问等的 AspectJ 不同），但它仍然依赖 AspectJ 的底层切点匹配机制。

### 4. **加载时织入（可选）**
如果您决定在 Spring AOP 中使用**加载时织入（LTW）**（这种情况很少见但可能），则需要 `aspectjweaver`。LTW 允许在类加载时织入切面，而不是使用代理。

```java
@EnableLoadTimeWeaving
public class AppConfig { ... }
```

### 5. **与 @EnableAspectJAutoProxy 的兼容性**
当您使用 `@EnableAspectJAutoProxy` 时，Spring 在内部使用 AspectJ 的基础设施来处理 AOP 注解，即使它不进行完整的 AspectJ 织入。

---

### **是否总是需要它？**
- **如果使用 Spring Boot (`spring-boot-starter-aop`)**：不需要，因为它传递性地包含了 `aspectjweaver`。
- **如果使用普通 Spring AOP**：是的，您必须显式包含它。

### **替代方案？**
- 如果您使用**完整的 AspectJ**（编译时或加载时织入），您还需要 `aspectjrt` 和 `aspectjtools`。
- 但对于 **Spring AOP**，仅 `aspectjweaver` 就足够了。

### **结论**
Spring AOP 是**基于代理的**，但它**重用了 AspectJ 的注解和切点语法**，这就是为什么需要 `aspectjweaver` 的原因。它弥合了 Spring 的代理方法与 AspectJ 更强大的 AOP 模型之间的差距。
