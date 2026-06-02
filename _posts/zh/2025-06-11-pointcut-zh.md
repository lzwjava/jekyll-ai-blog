---
audio: false
generated: true
lang: zh
layout: post
title: 理解切入点表达式
translated: true
type: note
---

你正在寻求关于AspectJ切点表达式的综合指南，特别是关于`execution`的用法、通配符的使用、类名匹配（前缀/后缀）以及其他通知类型如`@AfterReturning`。让我们来详细解析。

### Spring AOP中的切点表达式理解（AspectJ语法）

Spring AOP使用AspectJ切点表达式来确定通知（如`@Before`、`@AfterReturning`等）应该在*何处*应用。你问题的核心围绕`execution`切点指示符，这是最常用的一个。

#### `execution`切点指示符

`execution`切点指示符匹配方法执行。其通用语法是：

`execution(修饰符模式? 返回类型模式 声明类型模式?方法名模式(参数模式) 异常模式?)`

让我们分解这些组成部分：

* **`修饰符模式?`**: 可选。匹配方法修饰符（如`public`、`private`、`protected`）。
* **`返回类型模式`**: 必需。匹配方法的返回类型。
* **`声明类型模式?`**: 可选。匹配声明该方法的完全限定类名。
* **`方法名模式`**: 必需。匹配方法名。
* **`参数模式`**: 必需。匹配方法的参数。
* **`异常模式?`**: 可选。匹配方法抛出的异常。

#### 你的示例：`@Before("execution(* com.example.service.*.*(..))")`

让我们解析你给出的示例：

* `@Before`: 这是一个通知注解，意味着被注解的方法将在匹配的连接点*之前*运行。
* `execution()`: 切点指示符。
* `*`: 匹配任何返回类型。
* `com.example.service.*.*`:
  * `com.example.service`: 匹配包`com.example.service`。
  * `.*`: `service`后面的第一个`*`匹配`com.example.service`包中的任何类。
  * `.`: 包/类和方法之间的分隔符。
  * `*`: 第二个`*`匹配这些类中的任何方法名。
* `(..)`: 匹配任意数量的参数（零个或多个，任何类型）。

**通俗地说：** 这个切点匹配`com.example.service`包中*任何类*的*任何方法*的执行（以及其直接子包，如果有任何类直接在`com.example.service`中）。

---

### 切点表达式中的通配符

通配符对于创建灵活的切点表达式至关重要。

* **`*`（单星号）**:
  * 匹配名称模式中的任何单个元素（例如，任何返回类型、任何类名、任何方法名）。
  * 匹配包名中的任何单个段（例如，`com.example.*.service`将匹配`com.example.foo.service`）。
* **`..`（双点）**:
  * **在包模式中**: 匹配包名中的零个或多个段。
    * `com.example..service`: 匹配`com.example.service`、`com.example.foo.service`、`com.example.foo.bar.service`等。
  * **在参数模式中**: 匹配零个或多个任意类型的参数。
    * `(..)`: 匹配任意数量的参数。
    * `(java.lang.String, ..)`: 匹配第一个参数为`String`，后跟任意数量其他参数的方法。
    * `(.., java.lang.Long)`: 匹配以`Long`结尾，前面有任意数量参数的方法。

---

### 匹配类名

#### 1. 匹配后缀类名

要匹配以特定后缀结尾的类，将通配符放在后缀之前。

**示例：匹配所有以`ServiceImpl`结尾的类**

```java
@Before("execution(* com.example.service.*ServiceImpl.*(..))")
```

* `*ServiceImpl`: 匹配任何以`ServiceImpl`结尾的类名。

**示例：匹配`com.example.web`任何子包中所有以`Controller`结尾的类**

```java
@Before("execution(* com.example.web..*Controller.*(..))")
```

* `com.example.web..`: 匹配`com.example.web`及其任何子包。
* `*Controller`: 匹配任何以`Controller`结尾的类名。

#### 2. 匹配前缀类名

要匹配以特定前缀开头的类，将通配符放在前缀之后。

**示例：匹配所有以`User`开头的类**

```java
@Before("execution(* com.example.service.User*.*(..))")
```

* `User*`: 匹配任何以`User`开头的类名。

**示例：匹配`com.example.admin`包中所有以`Admin`开头的类**

```java
@Before("execution(* com.example.admin.Admin*.*(..))")
```

#### 3. 匹配特定类名（精确匹配）

精确匹配不需要通配符。

**示例：仅匹配`com.example.service.UserServiceImpl`中的方法**

```java
@Before("execution(* com.example.service.UserServiceImpl.*(..))")
```

---

### 不同类型的切点指示符

虽然`execution`是最常用的，但AspectJ提供了其他几个切点指示符来指定连接点。你可以使用逻辑运算符（`and`、`or`、`not`或`&&`、`||`、`!`）组合它们。

以下是最重要的一些：

1. **`execution()`**: 如前所述，匹配方法执行。
    * 示例: `@Before("execution(* com.example.service.UserService.*(..))")`

2. **`within()`**: 匹配代码在特定类型（类）内的连接点。这通常用于限制其他切点的范围。
    * 示例: `@Before("within(com.example.service.*) && execution(* *(..))")`
        * 这结合了`within`和`execution`。意思是"`com.example.service`包中任何类内的任何方法执行"。`execution`部分则只是任何方法的通配符，因为`within`处理了类匹配。

3. **`this()`**: 匹配代理*本身*是给定类型实例的连接点。这在简单通知中较少使用，更多用于引入或自调用问题。
    * 示例: `@Around("this(com.example.service.UserService)")`
        * 如果AOP代理实现了`UserService`则匹配。

4. **`target()`**: 匹配*目标对象*（被通知的实际对象，不是代理）是给定类型实例的连接点。当你关心底层实现时，这通常比`this()`更直观。
    * 示例: `@Around("target(com.example.service.UserServiceImpl)")`
        * 如果目标对象是`UserServiceImpl`的实例则匹配。

5. **`args()`**: 匹配参数是特定类型或匹配特定模式的连接点。
    * 示例: `@Before("execution(* com.example.service.*.*(String, ..))")`
        * 匹配第一个参数是`String`的方法。
    * 示例: `@Before("args(java.lang.String, int)")`
        * 匹配恰好接受一个`String`后跟一个`int`的方法。
    * 示例: `@Before("args(name, age)")` 其中`name`和`age`然后可以绑定到通知方法参数。

6. **`bean()`**: （Spring特有）匹配在具有特定名称或名称模式的Spring bean上执行的方法。
    * 示例: `@Before("bean(userService) && execution(* *(..))")`
        * 匹配名为"userService"的Spring bean上的任何方法执行。
    * 示例: `@Before("bean(*Service) && execution(* *(..))")`
        * 匹配名称以"Service"结尾的Spring bean上的任何方法执行。

7. **`@annotation()`**: 匹配目标方法（或类的`within`）带有特定注解的连接点。
    * 示例: `@Before("@annotation(com.example.annotation.Loggable)")`
        * 匹配任何带有`@Loggable`注解的方法。
    * 示例: `@Before("execution(* *(..)) && @annotation(org.springframework.transaction.annotation.Transactional)")`
        * 匹配任何带有`@Transactional`注解的方法执行。

8. **`@within()`**: 匹配声明类型（类）带有特定注解的连接点。
    * 示例: `@Before("@within(org.springframework.stereotype.Service) && execution(* *(..))")`
        * 匹配在带有`@Service`注解的类内的任何方法执行。

9. **`@target()`**: 匹配目标对象的类带有给定注解的连接点。
    * 示例: `@Around("@target(com.example.annotation.Auditable)")`

10. **`@args()`**: 匹配传递给方法的实际参数的运行时类型带有给定类型注解的连接点。
    * 示例: `@Before("@args(com.example.annotation.ValidInput)")`

---

### 通知类型（注解）

你提到了`@AfterReturning`和"我们可以在注解中使用的任何其他"。Spring AOP提供了几种通知类型，每种在连接点生命周期的不同点执行：

1. **`@Before`**:
    * 在匹配的方法执行*之前*执行。
    * 示例: 在服务方法运行前记录请求详情。
    * 不能阻止方法执行或改变其返回值。

2. **`@AfterReturning`**:
    * 在匹配的方法*成功*返回后（未抛出异常）执行。
    * 可以访问方法的返回值。
    * 语法: `@AfterReturning(pointcut="yourPointcut()", returning="result")`
    * 示例:

        ```java
        @AfterReturning(pointcut="execution(* com.example.service.UserService.getUserById(..))", returning="user")
        public void logUserRetrieval(Object user) {
            System.out.println("User retrieved: " + user);
        }
        ```

        *注意：`returning`属性名（本例中的`user`）必须与通知方法中的参数名匹配。*

3. **`@AfterThrowing`**:
    * 在匹配的方法抛出异常后执行。
    * 可以访问抛出的异常。
    * 语法: `@AfterThrowing(pointcut="yourPointcut()", throwing="ex")`
    * 示例:

        ```java
        @AfterThrowing(pointcut="execution(* com.example.service.*.*(..))", throwing="ex")
        public void logException(Exception ex) {
            System.err.println("Exception occurred: " + ex.getMessage());
        }
        ```

        *注意：`throwing`属性名（本例中的`ex`）必须与通知方法中的参数名匹配。*

4. **`@After`（最终通知）**:
    * 在匹配的方法完成后执行，无论它是成功返回还是抛出异常。
    * 类似于`finally`块。
    * 示例: 无论方法结果如何，都释放资源。

    * ```java
        @After("execution(* com.example.service.OrderService.placeOrder(..))")
        public void cleanupOrderProcess() {
            System.out.println("Order process completed (cleanup)");
        }
        ```

5. **`@Around`**:
    * 最强大和灵活的通知类型。
    * 在匹配的方法执行*周围*执行。
    * 你负责使用`ProceedingJoinPoint.proceed()`调用实际方法。
    * 可以检查、修改甚至抑制方法的参数和返回值。
    * 可以捕获和处理被通知方法抛出的异常。
    * 示例: 性能监控、事务管理、缓存。

    * ```java
        import org.aspectj.lang.ProceedingJoinPoint;
        import org.aspectj.lang.annotation.Around;
        import org.aspectj.lang.annotation.Aspect;

        @Aspect
        public class PerformanceMonitorAspect {

            @Around("execution(* com.example.service.*.*(..))")
            public Object profile(ProceedingJoinPoint joinPoint) throws Throwable {
                long start = System.currentTimeMillis();
                Object result = joinPoint.proceed(); // 执行原始方法
                long end = System.currentTimeMillis();
                System.out.println(joinPoint.getSignature().getName() + " executed in " + (end - start) + "ms");
                return result;
            }
        }
        ```

### 定义可重用的切点

为了更好的可读性和可重用性，你可以使用`@Pointcut`定义命名切点。

```java
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.AfterReturning;

@Aspect
public class MyServiceAspect {

    // 为com.example.service包中的所有方法定义切点
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}

    // 为返回User对象的方法定义切点
    @Pointcut("execution(com.example.model.User com.example.service.*.*(..))")
    public void returnsUser() {}

    // 使用定义的切点
    @Before("serviceMethods()")
    public void logBeforeServiceCall() {
        System.out.println("Before service method execution.");
    }

    // 使用逻辑AND组合切点
    @AfterReturning(pointcut="serviceMethods() && returnsUser()", returning="user")
    public void logUserReturned(Object user) {
        System.out.println("Service method returned user: " + user);
    }

    // 你也可以定义带参数的切点
    @Pointcut("execution(* com.example.repository.*.save(..)) && args(entity)")
    public void repositorySave(Object entity) {}

    @Before("repositorySave(entity)")
    public void logEntityBeforeSave(Object entity) {
        System.out.println("Saving entity: " + entity);
    }
}
```

这份综合指南涵盖了Spring AOP中切点表达式的基础知识、通配符用法、类名匹配和不同的通知类型。掌握这些概念将使你能够精确控制横切关注点的应用位置和时机。
