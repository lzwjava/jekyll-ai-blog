---
audio: false
generated: true
lang: zh
layout: post
title: Java性能基准测试
translated: true
type: note
---

Java 微基准测试工具（JMH）是一个功能强大的工具，用于在 Java 中构建、运行和分析微基准测试。它允许开发人员以可控和可重复的方式测量代码性能。以下是如何有效使用 JMH 的完整指南。

---

## 1. 设置项目

要使用 JMH，您需要将其包含在项目中。以下是使用 Maven 或 Gradle 的方法：

### **Maven**
将以下依赖项添加到您的 `pom.xml` 中：

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
将以下行添加到您的 `build.gradle` 中：

```groovy
dependencies {
    implementation 'org.openjdk.jmh:jmh-core:1.36'
    annotationProcessor 'org.openjdk.jmh:jmh-generator-annprocess:1.36'
}
```

这些依赖项提供了 JMH 核心库以及生成基准测试代码所需的注解处理器。

---

## 2. 编写基准测试

创建一个 Java 类来定义您的基准测试。使用 `@Benchmark` 注解标记您要测量的方法。以下是一个简单示例：

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
        // 要基准测试的代码
        int a = 1;
        int b = 2;
        int sum = a + b;
    }
}
```

- **`@Benchmark`**：将方法标记为基准测试目标。
- **`@BenchmarkMode`**：指定性能测量方式（例如，`Mode.AverageTime` 表示平均执行时间）。
- **`@OutputTimeUnit`**：设置结果的时间单位（例如，`TimeUnit.NANOSECONDS`）。

---

## 3. 配置基准测试

您可以使用其他 JMH 注解来自定义基准测试：

- **`@Warmup`**：定义预热阶段（例如，`@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)`）。
- **`@Measurement`**：配置测量阶段（例如，`@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)`）。
- **`@Fork`**：指定要使用的 JVM 进程数（例如，`@Fork(value = 1)` 表示在一个 JVM 实例中运行）。
- **`@State`**：定义状态对象的作用域（例如，`@State(Scope.Thread)` 表示线程本地状态）。

带配置的示例：

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
        // 要基准测试的代码
    }
}
```

---

## 4. 运行基准测试

要执行基准测试，您可以使用 JMH 运行器。以下是使用 Maven 的方法：

### **添加 Maven Shade 插件**
在您的 `pom.xml` 中包含以下内容以创建可执行的 JAR：

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

### **构建和运行**
1. 构建 JAR：`mvn clean package`
2. 运行基准测试：`java -jar target/benchmarks.jar`

JMH 将执行基准测试并在终端中显示结果。

---

## 5. 分析结果

JMH 根据您的配置输出性能指标。例如：

```
Benchmark              Mode  Cnt  Score   Error  Units
MyBenchmark.testMethod avgt    5  1.234 ± 0.012  ns/op
```

- **Mode**：基准测试模式（例如，`avgt` 表示平均时间）。
- **Cnt**：测量迭代次数。
- **Score**：测量的性能（例如，每次操作的平均时间，单位为纳秒）。
- **Error**：误差范围。
- **Units**：测量单位。

使用这些结果来评估和优化代码性能。

---

## 6. 高级功能

JMH 提供了其他工具用于更复杂的场景：

### **参数化**
使用 `@Param` 测试不同输入的代码：

```java
@State(Scope.Benchmark)
public class MyBenchmark {
    @Param({"1", "10", "100"})
    private int iterations;

    @Benchmark
    public void testMethod() {
        for (int i = 0; i < iterations; i++) {
            // 要基准测试的代码
        }
    }
}
```

### **黑洞**
使用 `Blackhole` 防止 JVM 优化掉未使用的结果：

```java
@Benchmark
public void testMethod(Blackhole bh) {
    int sum = 1 + 2;
    bh.consume(sum); // 防止死代码消除
}
```

---

## 7. 最佳实践

- **预热 JVM**：始终包含预热阶段，以确保 JIT 编译器在测量前优化您的代码。
- **选择正确的模式**：使用 `Mode.AverageTime` 测量延迟，`Mode.Throughput` 测量每秒操作数等。
- **控制环境**：在稳定的系统上运行基准测试，以避免其他进程的干扰。
- **避免优化**：使用黑洞或其他 JMH 功能防止 JVM 消除代码。

---

通过遵循这些步骤，您可以使用 `org.openjdk.jmh` 准确测量和改进 Java 代码的性能。无论您是测试简单操作还是复杂算法，JMH 都提供了可靠的基准测试工具。
