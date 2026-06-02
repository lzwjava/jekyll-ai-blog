---
audio: false
generated: true
lang: en
layout: post
title: Scheduling Tasks In Spring
translated: false
type: note
---

Scheduling tasks in Spring is a common requirement for automating repetitive jobs, such as sending emails, generating reports, or performing system maintenance. Spring provides a powerful and easy-to-use task scheduling feature through its `@Scheduled` annotation and the Spring Task Scheduler. Below, I’ll walk you through the steps to set it up and explain the key concepts.

### 1. **Enable Scheduling in Your Spring Application**

To use scheduling, you need to enable it in your Spring application. This is done by adding the `@EnableScheduling` annotation to a configuration class.

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

@Configuration
@EnableScheduling
public class SchedulerConfig {
    // Configuration class can be empty unless you need custom scheduler settings
}
```

This tells Spring to look for methods annotated with `@Scheduled` and execute them according to their defined schedules.

---

### 2. **Create a Task to Schedule**

You can define a method in any Spring-managed bean (like a `@Component` or `@Service`) and annotate it with `@Scheduled`. Here’s an example:

```java
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class MyScheduledTasks {

    // Runs every 5 seconds
    @Scheduled(fixedRate = 5000)
    public void performTask() {
        System.out.println("Task executed at: " + System.currentTimeMillis());
    }
}
```

In this example:

- `@Component` makes the class a Spring bean.
- `@Scheduled(fixedRate = 5000)` runs the method every 5 seconds (5000 milliseconds).

---

### 3. **Types of Scheduling Options**

Spring offers several ways to define when a task should run:

#### a) **Fixed Rate**

- Executes the task at a fixed interval, regardless of how long the task takes.
- Example: `@Scheduled(fixedRate = 5000)` (every 5 seconds).

#### b) **Fixed Delay**

- Executes the task with a fixed delay between the end of one execution and the start of the next.
- Example: `@Scheduled(fixedDelay = 5000)` (5 seconds after the previous task finishes).

#### c) **Cron Expression**

- Uses a cron-like syntax for more complex schedules (e.g., "every weekday at 9 AM").
- Example: `@Scheduled(cron = "0 0 9 * * MON-FRI")`.

#### d) **Initial Delay**

- Delays the first execution of the task. Combine with `fixedRate` or `fixedDelay`.
- Example: `@Scheduled(fixedRate = 5000, initialDelay = 10000)` (starts after 10 seconds, then runs every 5 seconds).

---

### 4. **Cron Syntax Basics**

If you use cron, here’s a quick reference:

- Format: `second minute hour day-of-month month day-of-week`
- Example: `@Scheduled(cron = "0 15 10 * * ?")` (runs at 10:15 AM every day).

| Field         | Allowed Values       |
|---------------|----------------------|
| Second        | 0-59                |
| Minute        | 0-59                |
| Hour          | 0-23                |
| Day of Month  | 1-31                |
| Month         | 1-12 or JAN-DEC     |
| Day of Week   | 0-7 or SUN-SAT (0 or 7 is Sunday) |

Special characters like `*` (all), `,` (list), `-` (range), `/` (increment) can be used.

---

### 5. **Dependencies**

If you’re using Spring Boot, the scheduling feature is included by default in the `spring-boot-starter` dependency. For a non-Boot Spring project, ensure you have:

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>6.1.3</version> <!-- Use the latest version -->
</dependency>
```

---

### 6. **Full Example with Spring Boot**

Here’s a complete Spring Boot example:

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
        System.out.println("Running every 5 seconds: " + System.currentTimeMillis());
    }

    @Scheduled(cron = "0 */1 * * * *")
    public void runEveryMinute() {
        System.out.println("Running every minute: " + System.currentTimeMillis());
    }
}
```

---

### 7. **Customizing the Scheduler (Optional)**

By default, Spring uses a single-threaded scheduler. If you need concurrent task execution, you can configure a custom `TaskScheduler`:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

@Configuration
public class SchedulerConfig {

    @Bean
    public ThreadPoolTaskScheduler taskScheduler() {
        ThreadPoolTaskScheduler scheduler = new ThreadPoolTaskScheduler();
        scheduler.setPoolSize(10); // Number of threads
        scheduler.setThreadNamePrefix("my-scheduler-");
        return scheduler;
    }
}
```

This allows multiple tasks to run in parallel.

---

### 8. **Testing Your Scheduled Tasks**

- Run your application and check the console logs to verify the tasks are executing as expected.
- Use shorter intervals (e.g., every 2 seconds) during testing to see results quickly.
