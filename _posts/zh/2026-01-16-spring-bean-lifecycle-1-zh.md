---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Spring Bean 生命周期的阶段
translated: true
type: note
---

**Question:** Spring Bean Lifecycle 的阶段有哪些？

**Answer:**

Spring 容器通过一个定义良好的 **lifecycle** 来管理 Bean。以下是按发生顺序排列的所有主要阶段（最完整版本，包括 aware callbacks 和所有常见扩展点）：

1. **Instantiation**
   Spring 创建 Bean 实例（调用构造函数）。

2. **Populate properties**
   进行 Dependency injection —— `@Autowired`、构造函数参数、setter 注入、`@Value` 等。

3. **Aware interface callbacks**（按此顺序）：
   - `BeanNameAware.setBeanName()`
   - `BeanClassLoaderAware.setBeanClassLoader()`（很少使用）
   - `BeanFactoryAware.setBeanFactory()`（或对于 ApplicationContext 为 `ApplicationContextAware.setApplicationContext()`）

4. **BeanPostProcessor.postProcessBeforeInitialization()**
   第一个扩展点 —— 为 *每一个* Bean 运行（自定义器、AOP proxies、`@Required` 检查等）。

5. **Initialization callbacks**（其一）：
   - `@PostConstruct` 注解的方法
   - `InitializingBean.afterPropertiesSet()`
   - 在 XML 或 `@Bean(initMethod = "...")` 中定义的自定义 `init-method`

6. **BeanPostProcessor.postProcessAfterInitialization()**
   第二个扩展点 —— Spring 非常常用（AOP proxy 包装、caching decorators 等）。

7. **Bean is ready**
   Bean 已完全初始化并放入容器中 —— 现在可以被应用程序使用了。

8. **Container shutdown / bean destruction phase**（当 context 关闭时）：
   - `@PreDestroy` 注解的方法
   - `DisposableBean.destroy()`
   - 在 XML 或 `@Bean(destroyMethod = "...")` 中定义的自定义 `destroy-method`

### Summary Table – Spring Bean Lifecycle (现代 Spring 中最常见的顺序)

| 步骤 # | 阶段                               | 机制 / 注解 / 接口                                          | 是否对每个 Bean 运行？ | 典型用例                                      |
|-------|------------------------------------|-------------------------------------------------------------|----------------------|-----------------------------------------------|
| 1     | Instantiate                        | 构造函数调用                                                | 是                   | —                                             |
| 2     | Inject dependencies                | Setter / 构造函数 / 字段注入                                | 是                   | —                                             |
| 3     | Aware callbacks                    | `BeanNameAware`, `ApplicationContextAware` 等               | 是 (如果实现了)      | 访问 Bean 名称、工厂、Context                 |
| 4     | Before Initialization              | `BeanPostProcessor.postProcessBeforeInitialization()`       | 是                   | 在初始化前修改 Bean (AOP, validation…)        |
| 5     | Initialization                     | `@PostConstruct` → `afterPropertiesSet()` → `init-method`   | 是 (如果声明了)      | 开启连接、加载缓存、启动线程                  |
| 6     | After Initialization               | `BeanPostProcessor.postProcessAfterInitialization()`        | 是                   | 包装代理 (AOP, transactions, security)        |
| —     | In service (长期运行)              | —                                                           | —                    | 正常使用                                      |
| 7     | Destruction                        | `@PreDestroy` → `destroy()` → `destroy-method`              | 是 (如果声明了)      | 关闭连接、清理资源                            |

### 快速现代建议 (2025+)

大多数新的 Spring Boot / Spring 应用程序仅使用这些：

```java
@PostConstruct     // 代替 InitializingBean
@PreDestroy        // 代替 DisposableBean
```

……并依赖 Spring 内置的 `BeanPostProcessor`（特别是用于 AOP、`@Transactional`、`@ConfigurationProperties` 等）。

现在很少有开发者会亲自实现 `BeanPostProcessor` —— 库和 Spring Boot auto-configuration 通常会处理它。

**References:**

- <https://docs.spring.io/spring-framework/reference/core/beans/factory-lifecycle.html>
- <https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/postconstruct-and-predestroy-annotations.html>
