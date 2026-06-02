---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Spring Bean 初始化与销毁生命周期
translated: true
type: note
---

**Question:** Spring 中的 Disposable Bean 和 Initialization Bean 是什么？

**Answer:**

在 Spring Framework 中，这两个概念是指 **lifecycle callback methods**（生命周期回调方法），它们允许你在 bean 生命周期的特定时间点运行自定义代码：

| Concept              | Correct Spring Term              | When it is called                              | Main annotation          | Interface                     | Typical usage examples                              |
|----------------------|----------------------------------|------------------------------------------------|---------------------------|-------------------------------|------------------------------------------------------|
| Initialization Bean  | Bean initialization method       | 依赖注入完成后且 bean 创建之后（但在正式投入使用前） | `@PostConstruct`          | `InitializingBean`            | 设置默认值、加载配置、开启连接、校验状态 |
| Disposable Bean      | Bean destruction method          | 当容器关闭时（或 bean 从 context 中移除时） | `@PreDestroy`             | `DisposableBean`              | 关闭数据库连接、释放文件、停止线程、清理资源 |

### 最常用且推荐的方式 (Modern Spring)

```java
@Component
public class MyService {

    @PostConstruct
    public void init() {
        // 在 bean 创建和依赖注入完成后执行一次
        System.out.println("Initializing MyService...");
        // 例如：预热缓存、开启连接池等
    }

    @PreDestroy
    public void cleanup() {
        // 在 ApplicationContext 关闭时执行
        System.out.println("Cleaning up MyService...");
        // 例如：关闭连接、刷新缓冲区、停止后台任务
    }
}
```

### 传统风格 (依然有效，但现在较少使用)

```java
@Component
public class LegacyService
    implements InitializingBean, DisposableBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        // 等同于 @PostConstruct
    }

    @Override
    public void destroy() throws Exception {
        // 等同于 @PreDestroy
    }
}
```

### 完整的 Spring Bean Lifecycle (简化版)

1. 实例化 bean (Instantiate bean)
2. 属性填充 (Populate properties / Dependency Injection)
3. **BeanNameAware / BeanFactoryAware / ApplicationContextAware** 回调
4. **@PostConstruct** 或 `afterPropertiesSet()`
5. Bean 就绪并投入使用
6. (经过很长时间 – bean 被使用)
7. 容器开始关闭 (Container shutdown)
8. **@PreDestroy** 或 `destroy()`
9. Bean 被销毁

### 快速对比表 – 该使用哪种方式？

| Style                | Recommended in 2024–2025? | Pros                              | Cons                                 | Most common in new code? |
|----------------------|----------------------------|------------------------------------|--------------------------------------|---------------------------|
| `@PostConstruct` / `@PreDestroy` | 是 – 强烈推荐 | 代码整洁、无需实现接口、Jakarta EE 标准 | 在绝大多数情况下没有缺点 | 是 |
| `InitializingBean` / `DisposableBean` | 否 (Legacy) | 旧的 Spring 项目仍在使用 | 强制要求实现接口 | 否 |
| `@Bean(initMethod=…, destroyMethod=…)` | 有时 | 当你无法修改类源代码时很有用 | 较为繁琐、字符串配置容易出错 | 偶尔 |

**针对新代码 (2025+) 的结论：**

使用 **`@PostConstruct`** 进行初始化，使用 **`@PreDestroy`** 进行清理 —— 它们是最简洁、应用最广泛且框架无关（framework-agnostic）的方法。

**References:**

- https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/postconstruct-and-predestroy-annotations.html
- https://docs.spring.io/spring-framework/reference/core/beans/factory-lifecycle.html
