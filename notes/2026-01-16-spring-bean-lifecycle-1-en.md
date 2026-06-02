---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Phases of the Spring Bean Lifecycle
translated: false
type: note
---

**Question:** What are the phases of the Spring Bean Lifecycle?

**Answer:**

The Spring container manages beans through a well-defined **lifecycle**. Here are all the main phases in the order they occur (most complete version, including awareness callbacks and all common extension points):

1. **Instantiation**
   Spring creates the bean instance (calls the constructor).

2. **Populate properties**
   Dependency injection happens — `@Autowired`, constructor args, setter injection, `@Value`, etc.

3. **Aware interface callbacks** (in this order):
   - `BeanNameAware.setBeanName()`
   - `BeanClassLoaderAware.setBeanClassLoader()` (rarely used)
   - `BeanFactoryAware.setBeanFactory()` (or `ApplicationContextAware.setApplicationContext()` for ApplicationContext)

4. **BeanPostProcessor.postProcessBeforeInitialization()**
   First extension point — runs for *every* bean (customizers, AOP proxies, `@Required` checks, etc.)

5. **Initialization callbacks** (one of these):
   - `@PostConstruct` annotated method
   - `InitializingBean.afterPropertiesSet()`
   - Custom `init-method` defined in XML or `@Bean(initMethod = "...")`

6. **BeanPostProcessor.postProcessAfterInitialization()**
   Second extension point — very commonly used by Spring (AOP proxy wrapping, caching decorators, etc.)

7. **Bean is ready**
   The bean is fully initialized and placed into the container — it can now be used by the application.

8. **Container shutdown / bean destruction phase** (when context is closed):
   - `@PreDestroy` annotated method
   - `DisposableBean.destroy()`
   - Custom `destroy-method` defined in XML or `@Bean(destroyMethod = "...")`

### Summary Table – Spring Bean Lifecycle (most common order in modern Spring)

| Step # | Phase                              | Mechanism / Annotation / Interface                          | Runs for every bean? | Typical use case                              |
|-------|------------------------------------|-------------------------------------------------------------|----------------------|-----------------------------------------------|
| 1     | Instantiate                        | Constructor call                                            | Yes                  | —                                             |
| 2     | Inject dependencies                | Setter / constructor / field injection                      | Yes                  | —                                             |
| 3     | Aware callbacks                    | `BeanNameAware`, `ApplicationContextAware`, etc.            | Yes (if implemented) | Access bean name, factory, context            |
| 4     | Before Initialization              | `BeanPostProcessor.postProcessBeforeInitialization()`       | Yes                  | Modify bean before init (AOP, validation…)    |
| 5     | Initialization                     | `@PostConstruct` → `afterPropertiesSet()` → `init-method`   | Yes (if declared)    | Open connections, load cache, start threads   |
| 6     | After Initialization               | `BeanPostProcessor.postProcessAfterInitialization()`        | Yes                  | Wrap with proxy (AOP, transactions, security) |
| —     | In service (long time)             | —                                                           | —                    | Normal usage                                  |
| 7     | Destruction                        | `@PreDestroy` → `destroy()` → `destroy-method`              | Yes (if declared)    | Close connections, cleanup resources          |

### Quick Modern Recommendation (2025+)

Most new Spring Boot / Spring applications use only these:

```java
@PostConstruct     // instead of InitializingBean
@PreDestroy        // instead of DisposableBean
```

…and rely on Spring’s built-in `BeanPostProcessor`s (especially for AOP, `@Transactional`, `@ConfigurationProperties`, etc.).

Very few developers implement `BeanPostProcessor` themselves anymore — libraries and Spring Boot auto-configuration usually handle it.

**References:**

- https://docs.spring.io/spring-framework/reference/core/beans/factory-lifecycle.html
- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/postconstruct-and-predestroy-annotations.html
