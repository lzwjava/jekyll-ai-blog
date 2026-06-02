---
audio: false
generated: true
lang: zh
layout: post
title: Java应用性能指标详解
translated: true
type: note
---

`com.yammer.metrics` 库最初由 Yammer 开发，现已成为 **Dropwizard Metrics** 库的组成部分。它提供了强大的 Java 应用指标采集与报告功能，可帮助您监控请求数、响应时间等性能指标。以下是高效使用该库的指南。

---

### 步骤 1：添加依赖
由于 `com.yammer.metrics` 已演进为 Dropwizard Metrics，您应使用 Dropwizard Metrics 库。若使用 Maven，请在 `pom.xml` 中添加以下依赖：

```xml
<dependency>
    <groupId>io.dropwizard.metrics</groupId>
    <artifactId>metrics-core</artifactId>
    <version>4.2.0</version> <!-- 请使用最新可用版本 -->
</dependency>
```

根据需求，您可能还需要添加其他模块：
- `metrics-jvm`：用于 JVM 相关指标
- `metrics-httpclient`：用于 HTTP 客户端指标
- `metrics-jersey`：用于 Jersey Web 框架集成

请查阅 [Dropwizard Metrics 文档](https://metrics.dropwizard.io/)获取最新版本和可用模块信息。

---

### 步骤 2：创建指标注册表
`MetricRegistry` 是存储所有指标的中央容器，通常为应用创建单个实例：

```java
import com.codahale.metrics.MetricRegistry;

public class MyApplication {
    public static void main(String[] args) {
        MetricRegistry registry = new MetricRegistry();
    }
}
```

---

### 步骤 3：使用不同类型的指标
Dropwizard Metrics 支持多种指标类型，分别适用于不同监控场景：

#### **计数器**
计数器用于追踪可增减的数值（如已处理请求数）：

```java
import com.codahale.metrics.Counter;

Counter counter = registry.counter("requests.processed");
counter.inc();  // 增加 1
counter.inc(5); // 增加 5
counter.dec();  // 减少 1
```

#### **测量器**
测量器提供特定时刻的数值快照（如当前队列大小）。通过实现 `Gauge` 接口定义测量器：

```java
import com.codahale.metrics.Gauge;

registry.register("queue.size", new Gauge<Integer>() {
    @Override
    public Integer getValue() {
        return someQueue.size(); // 替换为实际逻辑
    }
});
```

#### **直方图**
直方图追踪数值的统计分布（如请求大小）：

```java
import com.codahale.metrics.Histogram;

Histogram histogram = registry.histogram("request.sizes");
histogram.update(150); // 记录数值
```

#### **计量器**
计量器测量事件发生率（如每秒请求数）：

```java
import com.codahale.metrics.Meter;

Meter meter = registry.meter("requests.rate");
meter.mark(); // 记录事件
```

#### **计时器**
计时器同时测量事件的发生率与持续时间（如请求处理时间）：

```java
import com.codahale.metrics.Timer;

Timer timer = registry.timer("request.duration");
Timer.Context context = timer.time();
try {
    // 模拟业务处理
    Thread.sleep(100);
} finally {
    context.stop(); // 记录持续时间
}
```

---

### 步骤 4：报告指标
为使指标产生价值，需将其报告至特定目标。Dropwizard Metrics 支持控制台、JMX、Graphite 等多种报告器。以下示例创建每 10 秒记录指标的控制台报告器：

```java
import com.codahale.metrics.ConsoleReporter;
import java.util.concurrent.TimeUnit;

ConsoleReporter reporter = ConsoleReporter.forRegistry(registry)
    .convertRatesTo(TimeUnit.SECONDS)
    .convertDurationsTo(TimeUnit.MILLISECONDS)
    .build();
reporter.start(10, TimeUnit.SECONDS); // 每 10 秒报告一次
```

生产环境中建议集成 Graphite 等系统或通过 JMX 暴露指标。

---

### 步骤 5：与框架集成（可选）
若使用 Jersey 等 Web 框架，可通过 `metrics-jersey` 模块自动检测端点。此外，`@Timed` 或 `@Counted` 等注解能简化指标采集：

```java
import com.codahale.metrics.annotation.Timed;

@Path("/example")
public class ExampleResource {
    @GET
    @Timed
    public String getExample() {
        return "Hello, world!";
    }
}
```

添加 `metrics-jersey` 依赖并在 Jersey 应用中配置即可启用此功能。

---

### 最佳实践
- **命名规范**：采用层次化命名方案（如 `com.example.myapp.requests.total`）提升可读性
- **性能考量**：注意指标数量与采集频率，过度采集可能影响性能
- **文档参考**：查阅 [Dropwizard Metrics 文档](https://metrics.dropwizard.io/)获取最新示例和高级功能

---

### 示例：完整实践
以下示例整合了多个概念：

```java
import com.codahale.metrics.*;
import java.util.concurrent.TimeUnit;

public class MetricsExample {
    public static void main(String[] args) throws InterruptedException {
        MetricRegistry registry = new MetricRegistry();

        // 创建计数器
        Counter counter = registry.counter("example.counter");
        counter.inc();

        // 创建计时器
        Timer timer = registry.timer("example.timer");
        Timer.Context context = timer.time();
        Thread.sleep(100); // 模拟业务处理
        context.stop();

        // 启动控制台报告器
        ConsoleReporter reporter = ConsoleReporter.forRegistry(registry)
            .convertRatesTo(TimeUnit.SECONDS)
            .convertDurationsTo(TimeUnit.MILLISECONDS)
            .build();
        reporter.start(1, TimeUnit.SECONDS);

        // 保持程序运行以查看报告
        Thread.sleep(5000);
    }
}
```

此代码追踪计数器与计时器，每秒向控制台报告结果。

---

### 重要说明
`com.yammer.metrics` 库已演进为 Dropwizard Metrics，请始终使用 `io.dropwizard.metrics` 组的最新版本。对于新项目，也可考虑 Micrometer 等现代替代方案，但 Dropwizard Metrics 仍是许多 Java 应用的可靠选择。更多细节请参阅官方文档！
