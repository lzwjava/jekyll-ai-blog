---
audio: false
generated: true
lang: en
layout: post
title: 'Guide to Micrometers: Tools and Observability'
translated: false
type: note
---

This comprehensive guide covers two distinct topics: **Micrometers (the measuring tool)** and **Micrometer (the observability facade for Java applications, particularly Spring Boot), focusing on tracing solutions.**

Let's break them down:

-----

## Part 1: Comprehensive Guide about Micrometers (Measuring Tool)

A micrometer, often called a micrometer screw gauge, is a precision measuring instrument used to obtain highly accurate measurements of small distances, typically in the range of thousandths of an inch or hundredths of a millimeter. It's widely used in engineering, machining, manufacturing, and scientific fields where precise dimensions are critical.

### 1\. What is a Micrometer?

At its core, a micrometer utilizes a precisely machined screw mechanism to translate rotational motion into linear movement. This allows for fine adjustments and accurate readings of an object's dimensions by clamping it between a stationary anvil and a movable spindle.

### 2\. Key Components of a Micrometer

* **Frame:** The C-shaped main body that holds all other components. It provides stability and needs to be handled carefully to avoid thermal expansion errors.
* **Anvil:** The stationary measuring face against which the object is placed.
* **Spindle:** The movable measuring face that moves towards or away from the anvil when the thimble is rotated.
* **Sleeve (or Barrel):** The fixed part of the micrometer that houses the main linear scale, displaying whole numbers and half increments (e.g., in inches or millimeters).
* **Thimble:** The rotating part that moves the spindle and has a finely graduated scale for more precise readings.
* **Ratchet Stop:** Located at the end of the thimble, it ensures consistent measuring pressure by slipping when the correct force is applied, preventing overtightening and distortion of the workpiece.
* **Lock Nut (or Lock Lever):** Used to lock the spindle in place once a measurement has been taken, preventing accidental movement and preserving the reading.

### 3\. Types of Micrometers

Micrometers come in various types, each designed for specific measurement tasks:

* **Outside Micrometer (External Micrometer):** The most common type, used for measuring external dimensions like the diameter of a shaft or the thickness of a plate.
* **Inside Micrometer (Internal Micrometer):** Used for measuring internal dimensions, such as the diameter of a bore or hole. They often have different designs, like tubular or jaw-type micrometers.
* **Depth Micrometer:** Used to measure the depth of holes, slots, or steps.
* **Screw Thread Micrometer:** Designed to measure the pitch diameter of screw threads.
* **Ball Micrometer:** Features ball-shaped anvils/spindles for measuring the thickness of curved surfaces or specific features like tube walls.
* **Disk Micrometer:** Has flat, disc-shaped measuring faces for measuring thin materials, paper, or gear teeth.
* **Digital Micrometer:** Features an electronic display for direct digital readings, eliminating parallax error and making readings easier.
* **Analog Micrometer:** Requires manual reading of scales on the sleeve and thimble.
* **Vernier Micrometer:** Includes an additional vernier scale for even higher precision, allowing readings beyond the thimble's main graduations.

### 4\. How to Read a Micrometer (Analog/Imperial Example)

While specific readings vary between imperial (inches) and metric (millimeters) and analog/digital, the general principle for analog micrometers is:

1. **Read the Sleeve Scale (Main Scale):**
      * **Whole Inches:** Note the largest whole inch mark visible.
      * **Tenths of an Inch (0.100"):** Each numbered line on the sleeve represents 0.100 inches.
      * **Twenty-five Thousandths (0.025"):** Each unnumbered line between the tenths marks represents 0.025 inches.
2. **Read the Thimble Scale:**
      * The thimble has 25 graduations, with each mark representing 0.001 inches.
      * Read the line on the thimble that aligns with the index line on the sleeve.
3. **Combine the Readings:** Add the values from the sleeve (whole inches, tenths, and twenty-five thousandths) and the thimble (thousandths) to get the final measurement.

**Example (Imperial):**

* Sleeve:
  * Say you see "1" (for 1.000")
  * Then 3 lines after the "1" (3 x 0.100" = 0.300")
  * And 2 lines below the main line (2 x 0.025" = 0.050")
  * Total from Sleeve: 1.000 + 0.300 + 0.050 = 1.350"
* Thimble:
  * The 15th mark on the thimble aligns with the index line (0.015")
* **Total Reading:** 1.350" + 0.015" = **1.365"**

### 5\. Proper Usage and Best Practices

* **Cleanliness:** Always ensure the measuring faces (anvil and spindle) are clean and free of dust, oil, or debris.
* **Zeroing:** Before use, always "zero" the micrometer. Close the measuring faces gently using the ratchet stop until they touch. The reading should be 0.000 (or the starting range, e.g., 25-50mm). If not, adjust the micrometer for zero error. Digital micrometers usually have a reset button.
* **Temperature:** Handle the micrometer by its insulated frame or wear gloves, as body heat can cause thermal expansion and affect accuracy, especially for larger micrometers. Allow both the tool and the object to reach room temperature.
* **Consistent Pressure:** Always use the ratchet stop to apply consistent and appropriate measuring pressure. Overtightening can distort the object or the micrometer.
* **Object Positioning:** Position the object squarely between the anvil and spindle to avoid skewed readings.
* **Multiple Measurements:** For critical dimensions, take several measurements at different points on the object to account for variations.
* **Storage:** Store micrometers in their protective cases to prevent damage.
* **Calibration:** Regularly check and calibrate micrometers against known standards (e.g., gauge blocks) to ensure their accuracy.

-----

## Part 2: Micrometer as a Tracing Solution for Spring Java Projects

In the context of Spring Java projects, "Micrometer" refers to an **application observability facade** that provides a vendor-neutral API for instrumenting JVM-based applications. It allows you to collect and export various telemetry data, including metrics, logging, and **distributed tracing**.

Micrometer Tracing is the successor to Spring Cloud Sleuth and is designed to provide insight into complex distributed systems by tracking requests across multiple services.

### 1\. What is Distributed Tracing?

In a microservices architecture, a single user request often traverses multiple services. Distributed tracing allows you to:

* **Track the flow:** See the complete path a request takes through your system.
* **Identify bottlenecks:** Pinpoint which service or operation is causing latency.
* **Understand dependencies:** Visualize the interactions between different services.
* **Simplify debugging:** Correlate logs with specific requests, making troubleshooting much easier.

A distributed trace is composed of **spans**. A **span** represents a single operation or unit of work within a trace (e.g., an HTTP request to a service, a database query, a method execution). Spans have a unique ID, a start and end time, and can include tags (key-value pairs) and events for additional metadata. Spans are organized hierarchically, with parent-child relationships, forming a trace.

### 2\. Micrometer Tracing in Spring Boot 3.x+

Spring Boot 3.x+ deeply integrates with Micrometer's Observation API and Micrometer Tracing, making it significantly easier to implement distributed tracing.

#### 2.1. Core Concepts

* **Observation API:** Micrometer's unified API for instrumenting your code, capable of producing metrics, traces, and logs from a single instrumentation point.
* **Micrometer Tracing:** A facade over popular tracer libraries like OpenTelemetry and OpenZipkin Brave. It handles the lifecycle of spans, context propagation, and reporting to tracing backends.
* **Tracer Bridges:** Micrometer Tracing provides "bridges" to connect its API to specific tracing implementations (e.g., `micrometer-tracing-bridge-otel` for OpenTelemetry, `micrometer-tracing-bridge-brave` for OpenZipkin Brave).
* **Reporters/Exporters:** These components send the collected trace data to a tracing backend (e.g., Zipkin, Jaeger, Grafana Tempo).

#### 2.2. Setting Up Micrometer Tracing in a Spring Boot Java Project

Here's a step-by-step guide:

**Step 1: Add Dependencies**

You need `spring-boot-starter-actuator` for observability features, a Micrometer Tracing bridge, and a reporter/exporter for your chosen tracing backend.

**Example with OpenTelemetry and Zipkin (common choice):**

In your `pom.xml` (Maven):

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>

    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-observation</artifactId>
    </dependency>

    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-tracing-bridge-otel</artifactId>
    </dependency>

    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-exporter-zipkin</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
</dependencies>
```

**Step 2: Configure Tracing Properties**

In `application.properties` or `application.yml`, you can configure tracing behavior.

```properties
# Enable tracing (usually true by default with actuator and tracing dependencies)
management.tracing.enabled=true

# Configure sampling probability (1.0 = 100% of requests are traced)
# Default is often 0.1 (10%), set to 1.0 for development/testing
management.tracing.sampling.probability=1.0

# Configure Zipkin base URL (if using Zipkin)
spring.zipkin.base-url=http://localhost:9411
```

**Step 3: Run a Tracing Backend (e.g., Zipkin)**

You need a tracing server to collect and visualize your traces. Zipkin is a popular choice for local development.

You can run Zipkin via Docker:

```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

Once running, you can access the Zipkin UI at `http://localhost:9411`.

**Step 4: Automatic Instrumentation (Spring Boot Magic\!)**

For many common components in Spring Boot (like `RestController` endpoints, `RestTemplate`, `WebClient`, `JdbcTemplate`, Kafka listeners/producers, etc.), Micrometer Tracing provides **automatic instrumentation**. This means you often don't need to write any explicit tracing code for basic request tracing to work.

Spring Boot ensures that:

* Incoming HTTP requests automatically create a new trace or continue an existing one if trace headers are present.
* Outgoing requests made with auto-configured `RestTemplateBuilder`, `RestClient.Builder`, or `WebClient.Builder` propagate the trace context to downstream services.
* Log statements automatically include `traceId` and `spanId` (if you configure your logging pattern).

**Example Logging Pattern (in `application.properties`):**

```properties
logging.pattern.level=%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}] %c{1.}:%M:%L - %m%n
```

This pattern will inject the `traceId` and `spanId` into your log lines, making it easy to correlate logs with a specific trace.

**Step 5: Manual Instrumentation (for custom logic)**

While auto-instrumentation covers a lot, you'll often want to trace specific business logic or critical operations within your application. You can do this using:

* **`@Observed` Annotation (Recommended for Spring Boot 3.x+):**
    This annotation is part of the Micrometer Observation API and is the preferred way to create observations (which can produce both metrics and traces).

    ```java
    import io.micrometer.observation.annotation.Observed;
    import org.springframework.stereotype.Service;

    @Service
    public class MyService {

        @Observed(name = "myService.processData", contextualName = "processing-data")
        public String processData(String input) {
            // ... your business logic ...
            System.out.println("Processing data: " + input);
            return "Processed: " + input;
        }
    }
    ```

    The `name` attribute defines the name for the observation (which becomes the metric name and trace span name). `contextualName` provides a more human-readable name for the span in tracing tools.

* **Programmatic API (for more control):**
    You can directly use the `ObservationRegistry` and `Tracer` beans provided by Spring Boot.

    ```java
    import io.micrometer.observation.Observation;
    import io.micrometer.observation.ObservationRegistry;
    import org.springframework.stereotype.Service;

    @Service
    public class AnotherService {

        private final ObservationRegistry observationRegistry;

        public AnotherService(ObservationRegistry observationRegistry) {
            this.observationRegistry = observationRegistry;
        }

        public String performComplexOperation(String id) {
            return Observation.createNotStarted("complex.operation", observationRegistry)
                    .lowCardinalityKeyValue("operation.id", id) // Add a tag
                    .observe(() -> {
                        // ... complex logic here ...
                        try {
                            Thread.sleep(100); // Simulate work
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        }
                        return "Completed complex operation for " + id;
                    });
        }
    }
    ```

    Here, `observe()` wraps the code block, and `lowCardinalityKeyValue` adds a tag to the span.

### 3\. Distributed Tracing in Microservices

When you have multiple Spring Boot services, Micrometer Tracing facilitates context propagation automatically for `RestTemplate`, `WebClient`, and other instrumented clients. This means that the `traceId` and `spanId` are passed in HTTP headers between services (e.g., `traceparent` header for W3C Trace Context).

When a request comes into a downstream service, Micrometer Tracing detects these headers and continues the existing trace, creating new spans that are children of the parent span from the calling service. This forms the complete end-to-end trace.

### 4\. Visualizing Traces

Once your application is instrumented and sending traces to a backend like Zipkin (or Jaeger, Lightstep, etc.), you can:

1. **Access the UI:** Go to the tracing backend's web UI (e.g., `http://localhost:9411` for Zipkin).
2. **Find Traces:** Use filters (service name, span name, trace ID) to find specific traces.
3. **Analyze Trace Details:** Click on a trace to see its timeline, individual spans, their durations, tags, and events.
4. **Dependency Graph:** Most tracing backends can visualize the service dependencies based on the collected traces.

### 5\. Best Practices for Micrometer Tracing

* **Name Your Spans Meaningfully:** Use clear, concise, and low-cardinality names for your spans (e.g., "userService.getUser", "productService.updateStock"). Avoid including highly dynamic data in span names.
* **Use Tags for Detail (High Cardinality Data):** Instead of putting dynamic data in span names, use tags (key-value pairs) for additional context. For example, `userId`, `orderId`, `customerType`. Be mindful of **high cardinality** tags, as they can significantly increase storage costs and query times in your tracing backend. Use them judiciously.
* **Keep Spans Granular but Not Excessive:** Create spans for significant operations, but avoid creating too many tiny spans, as this can add overhead. Aim for a balance that provides sufficient visibility without overwhelming the system.
* **Propagate Context:** Ensure that trace context is properly propagated across service boundaries. Spring Boot's auto-configuration handles this for common scenarios, but be aware when using custom clients or asynchronous operations.
* **Sampling:** For high-traffic production environments, consider using sampling strategies to reduce the volume of trace data sent to your backend. Spring Boot allows configuring `management.tracing.sampling.probability`.
* **Correlate Logs:** Leverage the `traceId` and `spanId` injected into logs for easier debugging and correlation of application behavior with specific requests.
* **Monitor Your Tracing Backend:** Ensure your tracing backend (e.g., Zipkin server) has sufficient resources to handle the incoming trace volume.
* **Integrate with Other Observability Tools:** Tracing is one part of observability. Combine it with metrics (also via Micrometer) and structured logging for a holistic view of your application's health and performance.

By following these guidelines, you can effectively leverage Micrometer Tracing to gain deep insights into your Spring Boot applications, especially in distributed environments.
