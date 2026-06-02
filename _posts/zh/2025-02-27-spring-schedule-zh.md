---
audio: false
generated: true
lang: zh
layout: post
title: Spring任务调度指南
translated: true
type: note
---

在 Spring 中调度任务是实现自动化重复作业（如发送邮件、生成报告或执行系统维护）的常见需求。Spring 通过 `@Scheduled` 注解和 Spring 任务调度器提供了强大易用的任务调度功能。下面我将逐步介绍配置方法并解释关键概念。

### 1. **在 Spring 应用中启用调度功能**
要使用调度功能，您需要在 Spring 应用中通过配置类添加 `@EnableScheduling` 注解。

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

@Configuration
@EnableScheduling
public class SchedulerConfig {
    // 除非需要自定义调度器设置，否则配置类可保持为空
}
```

这会指示 Spring 查找带有 `@Scheduled` 注解的方法，并按定义的计划执行它们。

---

### 2. **创建待调度任务**
您可以在任何 Spring 管理的 Bean（如 `@Component` 或 `@Service`）中定义方法，并用 `@Scheduled` 进行注解。示例如下：

```java
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class MyScheduledTasks {

    // 每 5 秒执行一次
    @Scheduled(fixedRate = 5000)
    public void performTask() {
        System.out.println("任务执行时间: " + System.currentTimeMillis());
    }
}
```

此示例中：
- `@Component` 将类声明为 Spring Bean
- `@Scheduled(fixedRate = 5000)` 使方法每 5 秒（5000 毫秒）运行一次

---

### 3. **调度类型选项**
Spring 提供多种定义任务执行时间的方式：

#### a) **固定频率**
- 以固定间隔执行任务，无论任务执行耗时
- 示例：`@Scheduled(fixedRate = 5000)`（每 5 秒）

#### b) **固定延迟**
- 在上次执行完成后，延迟固定时间再执行下一次
- 示例：`@Scheduled(fixedDelay = 5000)`（上次任务结束后 5 秒）

#### c) **Cron 表达式**
- 使用类 Cron 语法实现复杂调度（如"工作日早上 9 点"）
- 示例：`@Scheduled(cron = "0 0 9 * * MON-FRI")`

#### d) **初始延迟**
- 延迟任务的首次执行。可与 `fixedRate` 或 `fixedDelay` 组合使用
- 示例：`@Scheduled(fixedRate = 5000, initialDelay = 10000)`（10 秒后开始，之后每 5 秒执行）

---

### 4. **Cron 语法基础**
使用 cron 时的快速参考：
- 格式：`秒 分 时 日 月 周`
- 示例：`@Scheduled(cron = "0 15 10 * * ?")`（每日 10:15 AM 执行）

| 字段          | 允许值              |
|---------------|---------------------|
| 秒           | 0-59               |
| 分           | 0-59               |
| 时           | 0-23               |
| 日           | 1-31               |
| 月           | 1-12 或 JAN-DEC    |
| 周           | 0-7 或 SUN-SAT（0 和 7 均为周日） |

可使用特殊字符：`*`（所有值）、`,`（列表）、`-`（范围）、`/`（增量）

---

### 5. **依赖配置**
若使用 Spring Boot，调度功能已默认包含在 `spring-boot-starter` 依赖中。非 Boot 的 Spring 项目需确保包含：

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>6.1.3</version> <!-- 使用最新版本 -->
</dependency>
```

---

### 6. **Spring Boot 完整示例**
完整 Spring Boot 示例：

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@SpringBootApplication
@EnableScheduling
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@Component
class ScheduledTasks {

    @Scheduled(fixedRate = 5000)
    public void runEveryFiveSeconds() {
        System.out.println("每 5 秒执行: " + System.currentTimeMillis());
    }

    @Scheduled(cron = "0 */1 * * * *")
    public void runEveryMinute() {
        System.out.println("每分钟执行: " + System.currentTimeMillis());
    }
}
```

---

### 7. **自定义调度器（可选）**
默认情况下 Spring 使用单线程调度器。如需并发执行任务，可配置自定义 `TaskScheduler`：

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

@Configuration
public class SchedulerConfig {

    @Bean
    public ThreadPoolTaskScheduler taskScheduler() {
        ThreadPoolTaskScheduler scheduler = new ThreadPoolTaskScheduler();
        scheduler.setPoolSize(10); // 线程数量
        scheduler.setThreadNamePrefix("my-scheduler-");
        return scheduler;
    }
}
```

这样可实现多个任务并行执行。

---

### 8. **测试调度任务**
- 运行应用并查看控制台日志验证任务按预期执行
- 测试阶段可使用较短间隔（如每 2 秒）快速查看效果
