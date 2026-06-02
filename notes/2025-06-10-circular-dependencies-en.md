---
audio: false
generated: true
lang: en
layout: post
title: Circular Dependencies in Spring
translated: false
type: note
---

Circular dependencies in Spring or Spring Boot occur when two or more beans depend on each other, either directly or indirectly, during initialization. This creates a cycle where Spring's dependency injection mechanism cannot resolve the dependencies because each bean requires the other to be fully initialized first. This issue typically arises during bean creation in the Spring Application Context, leading to a `BeanCurrentlyInCreationException`.

### Why Circular Dependencies Happen

Spring manages beans in a dependency injection container, and beans are typically created in a specific order based on their dependencies. When beans reference each other in a cyclic manner (e.g., Bean A depends on Bean B, and Bean B depends on Bean A), Spring cannot instantiate them because it gets stuck in an infinite loop during initialization. This is especially common in complex applications with tightly coupled components.

The problem is more likely to occur in the following scenarios:

1. **Constructor Injection**: When beans are wired via constructors, Spring must resolve dependencies at instantiation time, which can lead to circularity issues if beans reference each other.
2. **Field or Setter Injection with Eager Initialization**: If beans are eagerly initialized (default behavior for singleton beans), Spring tries to resolve dependencies immediately, exposing circular dependencies.
3. **Misconfigured or Overly Complex Bean Relationships**: Poor design or lack of separation of concerns can lead to unintended cycles.
4. **Annotations like `@Autowired` or `@Component`**: Automatic dependency injection in tightly coupled components can inadvertently create cycles.

### Common Examples of Circular Dependencies

#### Example 1: Constructor Injection Cycle

```java
@Component
public class BeanA {
    private final BeanB beanB;

    @Autowired
    public BeanA(BeanB beanB) {
        this.beanB = beanB;
    }
}

@Component
public class BeanB {
    private final BeanA beanA;

    @Autowired
    public BeanB(BeanA beanA) {
        this.beanA = beanA;
    }
}
```

**Problem**: `BeanA` requires `BeanB` in its constructor, and `BeanB` requires `BeanA` in its constructor. Spring cannot create either bean because each depends on the other being fully initialized first.

**Error**: `BeanCurrentlyInCreationException: Error creating bean with name 'beanA': Requested bean is currently in creation: Is there an unresolvable circular reference?`

#### Example 2: Field Injection Cycle

```java
@Component
public class BeanA {
    @Autowired
    private BeanB beanB;
}

@Component
public class BeanB {
    @Autowired
    private BeanA beanA;
}
```

**Problem**: Both `BeanA` and `BeanB` use `@Autowired` to inject each other via fields. Even though field injection is more flexible than constructor injection, Spring still detects the cycle during bean initialization if both are singleton beans (default scope).

#### Example 3: Indirect Circular Dependency

```java
@Component
public class BeanA {
    @Autowired
    private BeanB beanB;
}

@Component
public class BeanB {
    @Autowired
    private BeanC beanC;
}

@Component
public class BeanC {
    @Autowired
    private BeanA beanA;
}
```

**Problem**: `BeanA` depends on `BeanB`, `BeanB` depends on `BeanC`, and `BeanC` depends on `BeanA`, forming a cycle. This indirect dependency is harder to spot but still causes the same issue.

#### Example 4: `@Configuration` Classes with Circular References

```java
@Configuration
public class ConfigA {
    @Autowired
    private ConfigB configB;

    @Bean
    public ServiceA serviceA() {
        return new ServiceA(configB);
    }
}

@Configuration
public class ConfigB {
    @Autowired
    private ConfigA configA;

    @Bean
    public ServiceB serviceB() {
        return new ServiceB(configA);
    }
}
```

**Problem**: The `@Configuration` classes `ConfigA` and `ConfigB` depend on each other, creating a cycle when Spring tries to initialize the beans defined in these classes.

### Common Causes in Spring Boot

- **Auto-Configuration**: Spring Boot’s auto-configuration can sometimes introduce dependencies that lead to cycles, especially when custom beans interact with auto-configured ones.
- **Component Scanning**: Overuse of `@ComponentScan` or misconfigured packages can pick up unintended beans, leading to cyclic dependencies.
- **Tightly Coupled Design**: Business logic that tightly couples services, repositories, or controllers can inadvertently create cycles.
- **Prototype Scope Misuse**: While prototype-scoped beans can sometimes avoid circular dependencies, combining them with singleton beans in a cyclic manner can still cause issues.

### How to Resolve Circular Dependencies

1. **Use `@Lazy` Annotation**:
   - Annotate one of the dependencies with `@Lazy` to delay its initialization until it’s actually needed.

   ```java
   @Component
   public class BeanA {
       @Autowired
       @Lazy
       private BeanB beanB;
   }
   ```

   This breaks the cycle by allowing `BeanA` to be partially initialized before `BeanB` is resolved.

2. **Switch to Setter or Field Injection**:
   - Instead of constructor injection, use setter or field injection for one of the beans to allow Spring to initialize the bean first and inject dependencies later.

   ```java
   @Component
   public class BeanA {
       private BeanB beanB;

       @Autowired
       public void setBeanB(BeanB beanB) {
           this.beanB = beanB;
       }
   }
   ```

3. **Refactor Code to Break the Cycle**:
   - Introduce an interface or intermediate component to decouple the beans.
   - Example: Extract a common dependency into a third bean or use a service layer to mediate interactions.

   ```java
   public interface Service {
       void performAction();
   }

   @Component
   public class BeanA implements Service {
       @Autowired
       private BeanB beanB;

       public void performAction() {
           // Logic
       }
   }

   @Component
   public class BeanB {
       @Autowired
       private Service service; // Depends on interface, not BeanA directly
   }
   ```

4. **Use `@DependsOn` Annotation**:
   - Explicitly control the order of bean initialization to avoid cycles in specific cases.

   ```java
   @Component
   @DependsOn("beanB")
   public class BeanA {
       @Autowired
       private BeanB beanB;
   }
   ```

5. **Enable Proxying with `@EnableAspectJAutoProxy`**:
   - Ensure Spring uses proxies (CGLIB or JDK dynamic proxies) to handle dependencies, which can resolve some circularity issues by injecting a proxy instead of the actual bean.

6. **Reevaluate Design**:
   - Circular dependencies often indicate a design flaw. Consider refactoring to adhere to the Single Responsibility Principle or Dependency Inversion Principle.

### How to Debug Circular Dependencies

- **Check Stack Trace**: The `BeanCurrentlyInCreationException` stack trace will indicate the beans involved in the cycle.
- **Enable Debug Logging**: Set `spring.main.lazy-initialization=true` or enable debug logging for `org.springframework` to see bean creation details.
- **Use Tools**: Tools like Spring Boot Actuator or IDE plugins (e.g., Spring Tools Suite) can visualize bean dependencies.

### Preventing Circular Dependencies

- **Follow Best Practices**: Use dependency injection patterns like interfaces or abstractions to reduce tight coupling.
- **Modularize Code**: Break down large applications into smaller, loosely coupled modules.
- **Test Early**: Run integration tests to catch circular dependencies during development.
- **Limit Component Scanning**: Be specific with `@ComponentScan` to avoid picking up unnecessary beans.

### When Circular Dependencies Are Less Likely

- **Prototype Scope**: Beans with prototype scope are created on demand, reducing the likelihood of circularity (but not eliminating it entirely).
- **Lazy Initialization**: Enabling global lazy initialization (`spring.main.lazy-initialization=true`) can defer bean creation, though it may only mask the issue.

### Conclusion

Circular dependencies in Spring/Spring Boot arise from tight coupling between beans, often exacerbated by constructor injection or complex configurations. Common solutions include using `@Lazy`, switching to setter/field injection, or refactoring to break the cycle. By understanding the root cause and applying best practices, you can prevent or resolve these issues effectively. If you encounter a specific circular dependency, share the relevant code or error details, and I can help analyze it further!
