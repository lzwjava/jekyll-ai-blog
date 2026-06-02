---
audio: false
generated: true
lang: en
layout: post
title: Application Metrics in Java
translated: false
type: note
---

The `com.yammer.metrics` library, originally developed by Yammer, is now part of the **Dropwizard Metrics** library. It provides a robust way to collect and report application metrics in Java, helping you monitor performance aspects like request counts, response times, and more. Below is a guide on how to use it effectively.

---

### Step 1: Add the Dependency

Since `com.yammer.metrics` has evolved into Dropwizard Metrics, you should use the Dropwizard Metrics library. If you're using Maven, add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>io.dropwizard.metrics</groupId>
    <artifactId>metrics-core</artifactId>
    <version>4.2.0</version> <!-- Use the latest version available -->
</dependency>
```

Depending on your needs, you might also want additional modules, such as:

- `metrics-jvm` for JVM-related metrics.
- `metrics-httpclient` for HTTP client metrics.
- `metrics-jersey` for integration with the Jersey web framework.

Check the [Dropwizard Metrics documentation](https://metrics.dropwizard.io/) for the latest version and available modules.

---

### Step 2: Create a Metric Registry

The `MetricRegistry` is the central place where all metrics are stored. You typically create one instance for your application:

```java
import com.codahale.metrics.MetricRegistry;

public class MyApplication {
    public static void main(String[] args) {
        MetricRegistry registry = new MetricRegistry();
    }
}
```

---

### Step 3: Use Different Types of Metrics

Dropwizard Metrics supports several types of metrics, each suited to different monitoring needs:

#### **Counters**

Counters are used to track values that can increase or decrease (e.g., number of requests processed).

```java
import com.codahale.metrics.Counter;

Counter counter = registry.counter("requests.processed");
counter.inc();  // Increment by 1
counter.inc(5); // Increment by 5
counter.dec();  // Decrement by 1
```

#### **Gauges**

Gauges provide a snapshot of a value at a specific moment (e.g., current queue size). You define a gauge by implementing the `Gauge` interface:

```java
import com.codahale.metrics.Gauge;

registry.register("queue.size", new Gauge<Integer>() {
    @Override
    public Integer getValue() {
        return someQueue.size(); // Replace with your logic
    }
});
```

#### **Histograms**

Histograms track the statistical distribution of values (e.g., request sizes):

```java
import com.codahale.metrics.Histogram;

Histogram histogram = registry.histogram("request.sizes");
histogram.update(150); // Record a value
```

#### **Meters**

Meters measure the rate of events (e.g., requests per second):

```java
import com.codahale.metrics.Meter;

Meter meter = registry.meter("requests.rate");
meter.mark(); // Record an event
```

#### **Timers**

Timers measure both the rate and duration of events (e.g., request processing time):

```java
import com.codahale.metrics.Timer;

Timer timer = registry.timer("request.duration");
Timer.Context context = timer.time();
try {
    // Simulate some work
    Thread.sleep(100);
} finally {
    context.stop(); // Record the duration
}
```

---

### Step 4: Report Metrics

To make metrics useful, you need to report them somewhere. Dropwizard Metrics supports various reporters, such as console, JMX, or Graphite. Here’s an example of a console reporter that logs metrics every 10 seconds:

```java
import com.codahale.metrics.ConsoleReporter;
import java.util.concurrent.TimeUnit;

ConsoleReporter reporter = ConsoleReporter.forRegistry(registry)
    .convertRatesTo(TimeUnit.SECONDS)
    .convertDurationsTo(TimeUnit.MILLISECONDS)
    .build();
reporter.start(10, TimeUnit.SECONDS); // Report every 10 seconds
```

For production use, consider integrating with systems like Graphite or exposing metrics via JMX.

---

### Step 5: Integrate with Frameworks (Optional)

If you’re using a web framework like Jersey, you can use the `metrics-jersey` module to automatically instrument your endpoints. Additionally, annotations like `@Timed` or `@Counted` can simplify metric collection:

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

Add the `metrics-jersey` dependency and configure it with your Jersey application to enable this feature.

---

### Best Practices

- **Naming Conventions**: Use a hierarchical naming scheme for clarity (e.g., `com.example.myapp.requests.total`).
- **Performance**: Be cautious with the number and frequency of metrics, as excessive collection can impact performance.
- **Documentation**: Refer to the [Dropwizard Metrics documentation](https://metrics.dropwizard.io/) for up-to-date examples and advanced features.

---

### Example: Putting It All Together

Here’s a simple example combining several concepts:

```java
import com.codahale.metrics.*;
import java.util.concurrent.TimeUnit;

public class MetricsExample {
    public static void main(String[] args) throws InterruptedException {
        MetricRegistry registry = new MetricRegistry();

        // Create a counter
        Counter counter = registry.counter("example.counter");
        counter.inc();

        // Create a timer
        Timer timer = registry.timer("example.timer");
        Timer.Context context = timer.time();
        Thread.sleep(100); // Simulate work
        context.stop();

        // Start a console reporter
        ConsoleReporter reporter = ConsoleReporter.forRegistry(registry)
            .convertRatesTo(TimeUnit.SECONDS)
            .convertDurationsTo(TimeUnit.MILLISECONDS)
            .build();
        reporter.start(1, TimeUnit.SECONDS);

        // Keep the program running to see reports
        Thread.sleep(5000);
    }
}
```

This code tracks a counter and a timer, reporting results to the console every second.

---

### Final Notes

The `com.yammer.metrics` library has evolved into Dropwizard Metrics, so always use the latest version from the `io.dropwizard.metrics` group. If you’re starting a new project, you might also explore modern alternatives like Micrometer, but Dropwizard Metrics remains a solid choice for many Java applications. For more details, check the official documentation!
