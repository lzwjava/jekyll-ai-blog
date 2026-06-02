---
audio: false
generated: true
lang: zh
layout: post
title: 测微计指南：工具与可观测性
translated: true
type: note
---

本综合指南涵盖两个截然不同的主题：**千分尺（测量工具）** 和 **Micrometer（Java应用，特别是Spring Boot的可观测性门面，聚焦于追踪解决方案）**。

让我们分别进行解析：

-----

## 第一部分：关于千分尺（测量工具）的全面指南

千分尺，常称为螺旋测微器，是一种精密测量仪器，用于获取微小距离的高精度测量结果，通常测量范围在千分之一英寸或百分之一毫米级别。它广泛应用于工程、机械加工、制造和科学领域，这些领域对精确尺寸至关重要。

### 1. 什么是千分尺？

千分尺的核心是利用精密加工的螺旋机构将旋转运动转化为直线移动。这允许通过将物体夹在固定的测砧和可移动的测杆之间，进行精细调整并精确读取物体的尺寸。

### 2. 千分尺的关键部件：

  * **尺架：** C形的主体，用于固定所有其他部件。它提供稳定性，需要小心操作以避免热膨胀误差。
  * **测砧：** 固定的测量面，物体紧靠此面放置。
  * **测杆：** 可移动的测量面，当旋转套筒时，它朝向或远离测砧移动。
  * **固定套筒：** 千分尺的固定部分，包含主直线刻度，显示整数和半增量（例如，以英寸或毫米为单位）。
  * **微分筒：** 旋转部件，用于移动测杆，并带有一个精细分度的刻度用于更精确的读数。
  * **棘轮停止器：** 位于微分筒末端，通过在施加正确力时打滑来确保一致的测量压力，防止过度拧紧和工件变形。
  * **锁紧装置：** 用于在取得测量读数后锁定测杆位置，防止意外移动并保留读数。

### 3. 千分尺的类型：

千分尺有多种类型，每种设计用于特定的测量任务：

  * **外径千分尺：** 最常见的类型，用于测量外部尺寸，如轴径或板厚。
  * **内径千分尺：** 用于测量内部尺寸，如孔径或内孔直径。它们通常有不同的设计，如管式或爪式千分尺。
  * **深度千分尺：** 用于测量孔、槽或台阶的深度。
  * **螺纹千分尺：** 设计用于测量螺纹的中径。
  * **点接触千分尺：** 具有球形测砧/测杆，用于测量曲面厚度或特定特征（如管壁）。
  * **盘式千分尺：** 具有扁平的盘形测量面，用于测量薄材料、纸张或齿轮齿。
  * **数显千分尺：** 具有电子显示屏，可直接读取数字读数，消除了视差误差，使读数更容易。
  * **模拟千分尺：** 需要手动读取固定套筒和微分筒上的刻度。
  * **游标千分尺：** 包含一个额外的游标刻度，可实现更高的精度，允许读取超出微分筒主刻度的读数。

### 4. 如何读取千分尺（模拟/英制示例）：

虽然具体读数在英制（英寸）和公制（毫米）以及模拟/数显之间有所不同，但模拟千分尺的一般原理是：

1.  **读取固定套筒刻度（主刻度）：**
      * **整数英寸：** 注意可见的最大整数英寸标记。
      * **十分之一英寸：** 固定套筒上的每个数字线代表 0.100 英寸。
      * **二十五分之一英寸：** 十分之一标记之间的每个未编号线代表 0.025 英寸。
2.  **读取微分筒刻度：**
      * 微分筒有 25 个分度，每个标记代表 0.001 英寸。
      * 读取微分筒上与固定套筒基准线对齐的线。
3.  **合并读数：** 将固定套筒（整数英寸、十分之一和二十五分之一英寸）和微分筒（千分之一英寸）的值相加，得到最终测量值。

**示例（英制）：**

  * 固定套筒：
      * 假设您看到 "1"（表示 1.000"）
      * 然后在 "1" 之后有 3 条线（3 x 0.100" = 0.300"）
      * 并且在主线下方有 2 条线（2 x 0.025" = 0.050"）
      * 固定套筒总计：1.000 + 0.300 + 0.050 = 1.350"
  * 微分筒：
      * 微分筒上的第 15 个标记与基准线对齐（0.015"）
  * **总读数：** 1.350" + 0.015" = **1.365"**

### 5. 正确使用和最佳实践：

  * **清洁度：** 始终确保测量面（测砧和测杆）清洁，无灰尘、油污或碎屑。
  * **归零：** 使用前，务必"归零"千分尺。使用棘轮停止器轻轻合上测量面直到它们接触。读数应为 0.000（或起始范围，例如 25-50mm）。如果不是，调整千分尺的零误差。数显千分尺通常有复位按钮。
  * **温度：** 通过绝缘框架手持千分尺或戴手套，因为体温会导致热膨胀并影响精度，尤其是对于较大的千分尺。让工具和物体都达到室温。
  * **一致的压力：** 始终使用棘轮停止器施加一致且适当的测量压力。过度拧紧会使物体或千分尺变形。
  * **物体定位：** 将物体垂直放置在测砧和测杆之间，以避免读数偏差。
  * **多次测量：** 对于关键尺寸，在物体的不同点进行多次测量以考虑变化。
  * **存储：** 将千分尺存放在保护盒中以防损坏。
  * **校准：** 定期对照已知标准（例如，量块）检查和校准千分尺，以确保其准确性。

-----

## 第二部分：Micrometer 作为 Spring Java 项目的追踪解决方案

在 Spring Java 项目的上下文中，"Micrometer" 指的是一个**应用可观测性门面**，它提供了一个供应商中立的 API 用于检测基于 JVM 的应用程序。它允许您收集和导出各种遥测数据，包括指标、日志记录和**分布式追踪**。

Micrometer Tracing 是 Spring Cloud Sleuth 的后继者，旨在通过跨多个服务追踪请求来洞察复杂的分布式系统。

### 1. 什么是分布式追踪？

在微服务架构中，单个用户请求通常遍历多个服务。分布式追踪允许您：

  * **追踪流程：** 查看请求在系统中经过的完整路径。
  * **识别瓶颈：** 精确定位哪个服务或操作导致延迟。
  * **理解依赖关系：** 可视化不同服务之间的交互。
  * **简化调试：** 将日志与特定请求关联起来，使故障排除更加容易。

分布式追踪由 **Span** 组成。一个 **Span** 代表追踪中的一个单独操作或工作单元（例如，向服务发起的 HTTP 请求、数据库查询、方法执行）。Span 具有唯一的 ID、开始和结束时间，并且可以包含用于附加元数据的标签（键值对）和事件。Span 按层次结构组织，具有父子关系，形成一个追踪。

### 2. Spring Boot 3.x+ 中的 Micrometer Tracing

Spring Boot 3.x+ 深度集成了 Micrometer 的 Observation API 和 Micrometer Tracing，使得实现分布式追踪变得非常容易。

#### 2.1. 核心概念：

  * **Observation API：** Micrometer 的统一 API，用于检测您的代码，能够从单个检测点生成指标、追踪和日志。
  * **Micrometer Tracing：** 流行追踪器库（如 OpenTelemetry 和 OpenZipkin Brave）之上的门面。它处理 Span 的生命周期、上下文传播以及向追踪后端的报告。
  * **追踪器桥接：** Micrometer Tracing 提供"桥接"将其 API 连接到特定的追踪实现（例如，`micrometer-tracing-bridge-otel` 用于 OpenTelemetry，`micrometer-tracing-bridge-brave` 用于 OpenZipkin Brave）。
  * **报告器/导出器：** 这些组件将收集的追踪数据发送到追踪后端（例如，Zipkin、Jaeger、Grafana Tempo）。

#### 2.2. 在 Spring Boot Java 项目中设置 Micrometer Tracing：

以下是分步指南：

**步骤 1：添加依赖项**

您需要 `spring-boot-starter-actuator` 用于可观测性功能、一个 Micrometer Tracing 桥接器以及用于您选择的追踪后端的报告器/导出器。

**使用 OpenTelemetry 和 Zipkin 的示例（常见选择）：**

在您的 `pom.xml` (Maven) 中：

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

**步骤 2：配置追踪属性**

在 `application.properties` 或 `application.yml` 中，您可以配置追踪行为。

```properties
# 启用追踪（通常在有 actuator 和 tracing 依赖项时默认为 true）
management.tracing.enabled=true

# 配置采样概率 (1.0 = 100% 的请求被追踪)
# 默认通常是 0.1 (10%)，在开发/测试时可设置为 1.0
management.tracing.sampling.probability=1.0

# 配置 Zipkin 基础 URL（如果使用 Zipkin）
spring.zipkin.base-url=http://localhost:9411
```

**步骤 3：运行追踪后端（例如，Zipkin）**

您需要一个追踪服务器来收集和可视化您的追踪。Zipkin 是本地开发的热门选择。

您可以通过 Docker 运行 Zipkin：

```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

运行后，您可以在 `http://localhost:9411` 访问 Zipkin UI。

**步骤 4：自动检测（Spring Boot 的魔力！）**

对于 Spring Boot 中的许多常见组件（如 `RestController` 端点、`RestTemplate`、`WebClient`、`JdbcTemplate`、Kafka 监听器/生产者等），Micrometer Tracing 提供了**自动检测**。这意味着对于基本的请求追踪，您通常不需要编写任何显式的追踪代码即可工作。

Spring Boot 确保：

  * 传入的 HTTP 请求会自动创建一个新的追踪，或者如果存在追踪头信息，则继续现有的追踪。
  * 使用自动配置的 `RestTemplateBuilder`、`RestClient.Builder` 或 `WebClient.Builder` 发出的传出请求会将追踪上下文传播到下游服务。
  * 日志语句自动包含 `traceId` 和 `spanId`（如果您配置了日志模式）。

**日志模式示例（在 `application.properties` 中）：**

```properties
logging.pattern.level=%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}] %c{1.}:%M:%L - %m%n
```

此模式将把 `traceId` 和 `spanId` 注入到您的日志行中，使得将日志与特定追踪关联起来变得容易。

**步骤 5：手动检测（用于自定义逻辑）**

虽然自动检测涵盖了很多场景，但您通常希望追踪应用程序内的特定业务逻辑或关键操作。您可以使用以下方法实现：

  * **`@Observed` 注解（Spring Boot 3.x+ 推荐）：**
    此注解是 Micrometer Observation API 的一部分，是创建观测（可以同时生成指标和追踪）的首选方式。

    ```java
    import io.micrometer.observation.annotation.Observed;
    import org.springframework.stereotype.Service;

    @Service
    public class MyService {

        @Observed(name = "myService.processData", contextualName = "processing-data")
        public String processData(String input) {
            // ... 您的业务逻辑 ...
            System.out.println("Processing data: " + input);
            return "Processed: " + input;
        }
    }
    ```

    `name` 属性定义了观测的名称（该名称将成为指标名称和追踪 Span 名称）。`contextualName` 为追踪工具中的 Span 提供了更易读的名称。

  * **编程式 API（用于更多控制）：**
    您可以直接使用 Spring Boot 提供的 `ObservationRegistry` 和 `Tracer` Bean。

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
                    .lowCardinalityKeyValue("operation.id", id) // 添加一个标签
                    .observe(() -> {
                        // ... 复杂逻辑在这里 ...
                        try {
                            Thread.sleep(100); // 模拟工作
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        }
                        return "Completed complex operation for " + id;
                    });
        }
    }
    ```

    这里，`observe()` 包装了代码块，`lowCardinalityKeyValue` 向 Span 添加了一个标签。

### 3. 微服务中的分布式追踪：

当您有多个 Spring Boot 服务时，Micrometer Tracing 为 `RestTemplate`、`WebClient` 和其他已检测的客户端自动促进上下文传播。这意味着 `traceId` 和 `spanId` 通过 HTTP 头在服务之间传递（例如，用于 W3C Trace Context 的 `traceparent` 头）。

当请求进入下游服务时，Micrometer Tracing 检测到这些头信息并继续现有的追踪，创建新的 Span，这些 Span 是调用服务父 Span 的子级。这就形成了完整的端到端追踪。

### 4. 可视化追踪：

一旦您的应用程序被检测并开始向诸如 Zipkin（或 Jaeger、Lightstep 等）的后端发送追踪，您可以：

1.  **访问 UI：** 转到追踪后端的 Web UI（例如，Zipkin 的 `http://localhost:9411`）。
2.  **查找追踪：** 使用过滤器（服务名称、Span 名称、追踪 ID）来查找特定的追踪。
3.  **分析追踪详情：** 点击一个追踪以查看其时间线、各个 Span、它们的持续时间、标签和事件。
4.  **依赖关系图：** 大多数追踪后端可以根据收集到的追踪可视化服务依赖关系。

### 5. Micrometer Tracing 的最佳实践：

  * **有意义地命名您的 Span：** 为您的 Span 使用清晰、简洁且低基数的名称（例如，"userService.getUser", "productService.updateStock"）。避免在 Span 名称中包含高度动态的数据。
  * **使用标签记录详细信息（高基数数据）：** 不要将动态数据放在 Span 名称中，而是使用标签（键值对）来提供额外的上下文。例如，`userId`、`orderId`、`customerType`。注意**高基数**标签，因为它们会显著增加追踪后端的存储成本和查询时间。请谨慎使用。
  * **保持 Span 粒度但不过度：** 为重要的操作创建 Span，但避免创建过多的小 Span，因为这会增加开销。力求在提供足够可见性和不使系统不堪重负之间取得平衡。
  * **传播上下文：** 确保追踪上下文在跨服务边界时得到正确传播。Spring Boot 的自动配置处理了常见场景，但在使用自定义客户端或异步操作时需要注意。
  * **采样：** 对于高流量的生产环境，考虑使用采样策略来减少发送到后端的追踪数据量。Spring Boot 允许配置 `management.tracing.sampling.probability`。
  * **关联日志：** 利用注入到日志中的 `traceId` 和 `spanId`，以便更轻松地调试应用程序行为并将其与特定请求关联起来。
  * **监控您的追踪后端：** 确保您的追踪后端（例如，Zipkin 服务器）有足够的资源来处理传入的追踪量。
  * **与其他可观测性工具集成：** 追踪是可观测性的一部分。将其与指标（也通过 Micrometer）和结构化日志记录结合起来，以全面了解应用程序的运行状况和性能。

通过遵循这些指南，您可以有效地利用 Micrometer Tracing 来深入了解您的 Spring Boot 应用程序，尤其是在分布式环境中。
