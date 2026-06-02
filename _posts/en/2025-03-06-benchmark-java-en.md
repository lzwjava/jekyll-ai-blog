---
audio: false
generated: true
lang: en
layout: post
title: Benchmarking in Java
translated: false
type: note
---

The Java Microbenchmark Harness (JMH) is a powerful tool for building, running, and analyzing microbenchmarks in Java. It allows developers to measure the performance of their code in a controlled and repeatable way. Below is a comprehensive guide on how to use JMH effectively.

---

## 1. Set Up Your Project

To use JMH, you need to include it in your project. Here’s how to do it with Maven or Gradle:

### **Maven**

Add the following dependencies to your `pom.xml`:

```xml
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-core</artifactId>
    <version>1.36</version>
</dependency>
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-generator-annprocess</artifactId>
    <version>1.36</version>
    <scope>provided</scope>
</dependency>
```

### **Gradle**

Add these lines to your `build.gradle`:

```groovy
dependencies {
    implementation 'org.openjdk.jmh:jmh-core:1.36'
    annotationProcessor 'org.openjdk.jmh:jmh-generator-annprocess:1.36'
}
```

These dependencies provide the JMH core library and the annotation processor needed to generate benchmark code.

---

## 2. Write Your Benchmark

Create a Java class to define your benchmark. Use the `@Benchmark` annotation to mark the methods you want to measure. Here’s a simple example:

```java
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import java.util.concurrent.TimeUnit;

public class MyBenchmark {

    @Benchmark
    @BenchmarkMode(Mode.AverageTime)
    @OutputTimeUnit(TimeUnit.NANOSECONDS)
    public void testMethod() {
        // Code to benchmark
        int a = 1;
        int b = 2;
        int sum = a + b;
    }
}
```

- **`@Benchmark`**: Marks the method as a benchmark target.
- **`@BenchmarkMode`**: Specifies how to measure performance (e.g., `Mode.AverageTime` for average execution time).
- **`@OutputTimeUnit`**: Sets the time unit for the results (e.g., `TimeUnit.NANOSECONDS`).

---

## 3. Configure the Benchmark

You can customize your benchmark using additional JMH annotations:

- **`@Warmup`**: Defines the warm-up phase (e.g., `@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)`).
- **`@Measurement`**: Configures the measurement phase (e.g., `@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)`).
- **`@Fork`**: Specifies how many JVM forks to use (e.g., `@Fork(value = 1)` to run in one JVM instance).
- **`@State`**: Defines the scope of state objects (e.g., `@State(Scope.Thread)` for thread-local state).

Example with configuration:

```java
@State(Scope.Thread)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(1)
public class MyBenchmark {
    @Benchmark
    @BenchmarkMode(Mode.Throughput)
    @OutputTimeUnit(TimeUnit.SECONDS)
    public void testMethod() {
        // Code to benchmark
    }
}
```

---

## 4. Run the Benchmark

To execute your benchmark, you can use the JMH runner. Here’s how to do it with Maven:

### **Add the Maven Shade Plugin**

Include this in your `pom.xml` to create an executable JAR:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.2.4</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <finalName>benchmarks</finalName>
                        <transformers>
                            <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                <mainClass>org.openjdk.jmh.Main</mainClass>
                            </transformer>
                        </transformers>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### **Build and Run**

1. Build the JAR: `mvn clean package`
2. Run the benchmark: `java -jar target/benchmarks.jar`

JMH will execute the benchmarks and display the results in your terminal.

---

## 5. Analyze the Results

JMH outputs performance metrics based on your configuration. For example:

```
Benchmark              Mode  Cnt  Score   Error  Units
MyBenchmark.testMethod avgt    5  1.234 ± 0.012  ns/op
```

- **Mode**: The benchmark mode (e.g., `avgt` for average time).
- **Cnt**: Number of measurement iterations.
- **Score**: The measured performance (e.g., average time in nanoseconds per operation).
- **Error**: The margin of error.
- **Units**: The unit of measurement.

Use these results to evaluate and optimize your code’s performance.

---

## 6. Advanced Features

JMH offers additional tools for more complex scenarios:

### **Parameterization**

Test your code with different inputs using `@Param`:

```java
@State(Scope.Benchmark)
public class MyBenchmark {
    @Param({"1", "10", "100"})
    private int iterations;

    @Benchmark
    public void testMethod() {
        for (int i = 0; i < iterations; i++) {
            // Code to benchmark
        }
    }
}
```

### **Blackholes**

Prevent the JVM from optimizing away unused results with `Blackhole`:

```java
@Benchmark
public void testMethod(Blackhole bh) {
    int sum = 1 + 2;
    bh.consume(sum); // Prevents dead code elimination
}
```

---

## 7. Best Practices

- **Warm Up the JVM**: Always include a warm-up phase to ensure the JIT compiler optimizes your code before measurement.
- **Choose the Right Mode**: Use `Mode.AverageTime` for latency, `Mode.Throughput` for operations per second, etc.
- **Control the Environment**: Run benchmarks on a stable system to avoid interference from other processes.
- **Avoid Optimizations**: Use blackholes or other JMH features to prevent the JVM from eliminating code.

---

By following these steps, you can use `org.openjdk.jmh` to accurately measure and improve the performance of your Java code. Whether you’re testing simple operations or complex algorithms, JMH provides the tools you need for reliable benchmarking.
