---
audio: false
generated: true
lang: zh
layout: post
title: 获取Spring应用上下文
translated: true
type: note
---

要使用 Spring 的 `ApplicationContextAware` 接口在普通 Java 对象（如 Kafka 消费者）中访问 `ApplicationContext`，需要一种桥接 Spring 托管 Bean 与普通对象的方法。具体操作如下：

### 通用方法
`ApplicationContextAware` 接口允许 Spring 托管的 Bean 自动从 Spring 接收 `ApplicationContext`。通过此接口，可使未受 Spring 管理的普通 Java 对象（即非 Spring 容器创建的 Bean）也能获取上下文。

#### 访问 ApplicationContext 的步骤
1. **创建 Spring 托管的辅助类**：
   定义一个实现 `ApplicationContextAware` 接口并由 Spring 管理的类（例如使用 `@Component` 注解）。该类将在 Spring 应用启动时接收 `ApplicationContext`。

   ```java
   import org.springframework.context.ApplicationContext;
   import org.springframework.context.ApplicationContextAware;
   import org.springframework.stereotype.Component;

   @Component
   public class ApplicationContextProvider implements ApplicationContextAware {
       private static ApplicationContext context;

       @Override
       public void setApplicationContext(ApplicationContext applicationContext) {
           context = applicationContext;
       }

       public static ApplicationContext getApplicationContext() {
           return context;
       }
   }
   ```

   - `@Component` 确保 Spring 管理该 Bean
   - `setApplicationContext` 由 Spring 调用以注入 `ApplicationContext`
   - 静态变量 `context` 和获取方法支持全局访问

2. **在普通 Java 对象中访问上下文**：
   在普通 Java 对象（如手动创建的 Kafka 消费者）中，通过辅助类获取 `ApplicationContext` 并用于获取 Spring 托管的 Bean。

   ```java
   public class MyKafkaConsumer {
       public void processMessage() {
           ApplicationContext context = ApplicationContextProvider.getApplicationContext();
           SomeService service = context.getBean(SomeService.class);
           // 按需使用服务或其他 Bean
       }
   }
   ```

   - 此方式有效是因为 `ApplicationContextProvider` 在启动时由 Spring 初始化，使上下文可通过静态方式获取

3. **替代方案：显式传递上下文**：
   若普通 Java 对象由 Spring 托管的 Bean 创建，可将 `ApplicationContext` 自动注入该 Bean，再通过构造函数或 setter 传递给普通对象。

   ```java
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.context.ApplicationContext;
   import org.springframework.stereotype.Component;

   @Component
   public class KafkaConsumerCreator {
       @Autowired
       private ApplicationContext context;

       public MyKafkaConsumer createConsumer() {
           return new MyKafkaConsumer(context);
       }
   }

   public class MyKafkaConsumer {
       private final ApplicationContext context;

       public MyKafkaConsumer(ApplicationContext context) {
           this.context = context;
       }

       public void processMessage() {
           SomeService service = context.getBean(SomeService.class);
           // 使用服务
       }
   }
   ```

   - 此方法避免使用静态变量，使依赖关系显式化并提升可测试性

### Kafka 消费者专用方案
若使用 **Spring Kafka** 处理 Kafka 消费者，推荐将消费者直接集成到 Spring 生态中，而非作为普通 Java 对象处理。

#### 使用 `@KafkaListener`
将 Kafka 消费者定义为包含 `@KafkaListener` 方法的 Spring 托管 Bean，从而直接自动注入 `ApplicationContext` 或其他 Bean。

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class MyKafkaConsumer {
    @Autowired
    private ApplicationContext context;

    @Autowired
    private SomeService someService;

    @KafkaListener(topics = "my-topic")
    public void consume(String message) {
        // 直接使用 context 或 someService
        SomeService service = context.getBean(SomeService.class); // 按需获取
        someService.process(message);
    }
}
```

- Spring Kafka 管理消费者生命周期（包括线程和轮询）
- 自动注入在多数情况下无需手动获取上下文

#### 手动创建 Kafka 消费者
如需手动创建 `KafkaConsumer`（例如直接使用 Kafka 客户端库），应在 Spring 托管的 Bean 中创建，并按前述显式传递方式传入 `ApplicationContext`。

### 建议方案
- **对于 Kafka 消费者**：尽可能在 Spring 托管的 Bean 中使用 Spring Kafka 的 `@KafkaListener`。此方式能充分利用 Spring 与 Kafka 的集成，简化对 `ApplicationContext` 及其他 Bean 的访问
- **对于普通 Java 对象**：根据实际场景选择静态 `ApplicationContextProvider` 方案，或通过 Spring 托管 Bean 显式传递 `ApplicationContext`。在可行情况下，显式传递方案更受推荐，因其能避免静态状态并提升可测试性

通过以上方法，可根据具体配置有效运用 `ApplicationContextAware` 使 Spring 上下文对普通 Java 对象（包括 Kafka 消费者）可用。
