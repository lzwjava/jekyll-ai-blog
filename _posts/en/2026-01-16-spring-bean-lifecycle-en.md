---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Spring Bean Initialization and Disposal Lifecycle
translated: false
type: note
---

**Question:** What are Disposable Bean and Initialization Bean in Spring?

**Answer:**

In Spring Framework, these two concepts refer to the **lifecycle callback methods** that let you run custom code at specific points in a bean's life:

| Concept              | Correct Spring Term              | When it is called                              | Main annotation          | Interface                     | Typical usage examples                              |
|----------------------|----------------------------------|------------------------------------------------|---------------------------|-------------------------------|------------------------------------------------------|
| Initialization Bean  | Bean initialization method       | After dependencies are injected and bean is created (but before it's fully ready for use) | `@PostConstruct`          | `InitializingBean`            | Setting default values, loading config, opening connections, validating state |
| Disposable Bean      | Bean destruction method          | When the container is shutting down (or when the bean is removed from context) | `@PreDestroy`             | `DisposableBean`              | Closing database connections, releasing files, stopping threads, cleanup resources |

### Most Common & Recommended Ways (Modern Spring)

```java
@Component
public class MyService {

    @PostConstruct
    public void init() {
        // runs once after bean creation + dependency injection
        System.out.println("Initializing MyService...");
        // e.g. warm up cache, open connection pool, etc.
    }

    @PreDestroy
    public void cleanup() {
        // runs when application context is closing
        System.out.println("Cleaning up MyService...");
        // e.g. close connections, flush buffers, stop background tasks
    }
}
```

### Older / Classic Style (Still works, but less used today)

```java
@Component
public class LegacyService 
    implements InitializingBean, DisposableBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        // same as @PostConstruct
    }

    @Override
    public void destroy() throws Exception {
        // same as @PreDestroy
    }
}
```

### Full Spring Bean Lifecycle (simplified)

1. Instantiate bean
2. Populate properties (dependency injection)
3. **BeanNameAware / BeanFactoryAware / ApplicationContextAware** callbacks
4. **@PostConstruct** or `afterPropertiesSet()`
5. Bean is ready and put into service
6. (long time passes – bean is used)
7. Container shutdown begins
8. **@PreDestroy** or `destroy()`
9. Bean is destroyed

### Quick Comparison Table – Which should you use?

| Style                | Recommended in 2024–2025? | Pros                              | Cons                                 | Most common in new code? |
|----------------------|----------------------------|------------------------------------|--------------------------------------|---------------------------|
| `@PostConstruct` / `@PreDestroy` | Yes – strongly preferred   | Clean, no interface needed, Jakarta EE standard | None for most cases                  | Yes                       |
| `InitializingBean` / `DisposableBean` | No (legacy)                | Very old Spring apps still use it  | Forces interface implementation      | No                        |
| `@Bean(initMethod=…, destroyMethod=…)` | Sometimes                  | Useful when you don't own the class | More verbose, error-prone strings    | Occasional                |

**Bottom line for new code (2025+):**

Use **`@PostConstruct`** for initialization and **`@PreDestroy`** for cleanup — they are the cleanest, most widely understood, and framework-agnostic approach.

**References:**

- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/postconstruct-and-predestroy-annotations.html
- https://docs.spring.io/spring-framework/reference/core/beans/factory-lifecycle.html