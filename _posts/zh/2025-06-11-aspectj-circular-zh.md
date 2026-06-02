---
audio: false
generated: true
lang: zh
layout: post
title: 使用AspectJ解决循环依赖问题
translated: true
type: note
---

在你的场景中，循环依赖的出现是因为 `BlogConfig`、`BlogCore` 和 `BlogWeb` 相互引用，形成了依赖循环。此外，如果 `BlogCore`（或可能是 `BlogWeb`）中的 AspectJ `LoggingAspect` 应用于跨模块的方法（包括依赖于 `BlogCore` 的 `BlogConfig`），则可能会加剧此问题。让我们分解问题，并提供一个解决方案，以在保持 AspectJ 功能完整的同时解决循环依赖。

### 问题分析

1. **模块依赖**：
   - `BlogCore` 依赖于 `BlogConfig`。
   - `BlogWeb` 依赖于 `BlogCore` 和 `BlogConfig`。
   - `BlogConfig` 依赖于 `BlogCore`（这导致了循环依赖：`BlogCore` ↔ `BlogConfig`）。
   - `BlogWeb` 对这两个模块的依赖可能会引入循环依赖。

2. **AspectJ LoggingAspect**：
   - `BlogCore`（或 `BlogWeb`）中的 `LoggingAspect` 使用了宽泛的切点（`execution(* *(..))`），该切点应用于应用程序上下文中的所有方法执行，包括 `BlogConfig`、`BlogCore` 和 `BlogWeb` 中的方法。
   - 如果 `LoggingAspect` 位于 `BlogCore` 中并织入到 `BlogConfig`，而 `BlogConfig` 又依赖于 `BlogCore`，则 AspectJ 的织入过程可能会在初始化期间使循环依赖问题复杂化。

3. **循环依赖的影响**：
   - 在 Maven 或 Gradle 等构建系统中，模块之间的循环依赖可能导致编译或运行时问题（例如，如果使用 Spring，可能会出现 `BeanCurrentlyInCreationException`，或类加载问题）。
   - 如果 `BlogConfig` 和 `BlogCore` 中的类相互依赖且未完全初始化，AspectJ 的编译时或加载时织入可能会失败或产生意外行为。

### 解决方案

要解决循环依赖并确保 AspectJ 的 `LoggingAspect` 正常工作，请按照以下步骤操作：

#### 1. 打破循环依赖

主要问题是 `BlogCore` ↔ `BlogConfig` 的依赖关系。要解决此问题，可以将导致 `BlogConfig` 依赖于 `BlogCore` 的共享功能或配置提取到一个新模块中，或重构依赖关系。

**选项 A：引入新模块（`BlogCommon`）**

- 创建一个新模块 `BlogCommon`，用于存放 `BlogCore` 和 `BlogConfig` 都需要共享的接口、配置或工具。
- 将 `BlogConfig` 所依赖的 `BlogCore` 部分（例如接口、常量或共享服务）移动到 `BlogCommon`。
- 更新依赖关系：
  - `BlogConfig` 依赖于 `BlogCommon`。
  - `BlogCore` 依赖于 `BlogCommon` 和 `BlogConfig`。
  - `BlogWeb` 依赖于 `BlogCore` 和 `BlogConfig`。

**依赖结构示例**：

```
BlogCommon ← BlogConfig ← BlogCore ← BlogWeb
```

**实现**：

- 在 `BlogCommon` 中定义接口或共享组件。例如：

  ```java
  // BlogCommon 模块
  public interface BlogService {
      void performAction();
  }
  ```

- 在 `BlogCore` 中实现接口：

  ```java
  // BlogCore 模块
  public class BlogCoreService implements BlogService {
      public void performAction() { /* 逻辑 */ }
  }
  ```

- 在 `BlogConfig` 中使用来自 `BlogCommon` 的接口：

  ```java
  // BlogConfig 模块
  import com.example.blogcommon.BlogService;
  public class BlogConfiguration {
      private final BlogService blogService;
      public BlogConfiguration(BlogService blogService) {
          this.blogService = blogService;
      }
  }
  ```

- 在 `BlogWeb` 中根据需要同时使用这两个模块。

通过确保 `BlogConfig` 不再直接依赖于 `BlogCore`，可以消除循环依赖。

**选项 B：使用依赖注入实现控制反转（IoC）**

- 如果使用 Spring 等框架，重构 `BlogConfig`，使其依赖于 `BlogCore` 中定义的抽象（接口），而不是具体类。
- 使用依赖注入在运行时将 `BlogCore` 的实现提供给 `BlogConfig`，从而避免编译时的循环依赖。
- 示例：

  ```java
  // BlogCore 模块
  public interface BlogService {
      void performAction();
  }
  @Component
  public class BlogCoreService implements BlogService {
      public void performAction() { /* 逻辑 */ }
  }

  // BlogConfig 模块
  @Configuration
  public class BlogConfiguration {
      private final BlogService blogService;
      public BlogConfiguration(BlogService blogService) {
          this.blogService = blogService;
      }
  }
  ```

- Spring 的 IoC 容器在运行时解析依赖关系，从而打破编译时的循环依赖。

#### 2. 调整 AspectJ 配置

`LoggingAspect` 的宽泛切点（`execution(* *(..))`）可能会应用于所有模块，包括 `BlogConfig`，这可能会使初始化过程复杂化。为了使切面更易于管理并避免织入问题：

- **缩小切点范围**：将切面限制在特定的包或模块中，以避免将其应用于 `BlogConfig` 或其他基础设施代码。

  ```java
  import org.aspectj.lang.JoinPoint;
  import org.aspectj.lang.annotation.After;
  import org.aspectj.lang.annotation.Aspect;
  import java.util.Arrays;

  @Aspect
  public class LoggingAspect {
      @After("execution(* com.example.blogcore..*(..)) || execution(* com.example.blogweb..*(..))")
      public void logAfter(JoinPoint joinPoint) {
          System.out.println("方法已执行: " + joinPoint.getSignature());
          System.out.println("参数: " + Arrays.toString(joinPoint.getArgs()));
      }
  }
  ```

  此切点仅应用于 `BlogCore`（`com.example.blogcore`）和 `BlogWeb`（`com.example.blogweb`）中的方法，排除了 `BlogConfig`。

- **将切面移动到单独的模块**：为避免模块初始化期间的织入问题，将 `LoggingAspect` 放置在一个新模块（例如 `BlogAspects`）中，该模块依赖于 `BlogCore` 和 `BlogWeb`，但不依赖于 `BlogConfig`。
  - 依赖结构：

    ```
    BlogCommon ← BlogConfig ← BlogCore ← BlogWeb
                       ↑          ↑
                       └─ BlogAspects ─┘
    ```

  - 更新构建配置（例如 Maven/Gradle），以确保 `BlogAspects` 在 `BlogCore` 和 `BlogWeb` 之后织入。

- **使用加载时织入（LTW）**：如果编译时织入由于循环依赖而导致问题，可以切换到使用 AspectJ 的加载时织入。在应用程序中配置 LTW（例如通过 Spring 的 `@EnableLoadTimeWeaving` 或 `aop.xml` 文件），以将切面的应用延迟到运行时，即在类加载之后。

#### 3. 更新构建配置

确保构建工具（Maven、Gradle 等）反映新的模块结构并正确解析依赖关系。

**Maven 示例**：

```xml
<!-- BlogCommon/pom.xml -->
<dependencies>
    <!-- 无依赖 -->
</dependencies>

<!-- BlogConfig/pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogCommon</artifactId>
        <version>1.0</version>
    </dependency>
</dependencies>

<!-- BlogCore/pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogCommon</artifactId>
        <version>1.0</version>
    </dependency>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogConfig</artifactId>
        <version>1.0</version>
    </dependency>
</dependencies>

<!-- BlogWeb/pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogCore</artifactId>
        <version>1.0</version>
    </dependency>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogConfig</artifactId>
        <version>1.0</version>
    </dependency>
</dependencies>

<!-- BlogAspects/pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogCore</artifactId>
        <version>1.0</version>
    </dependency>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>BlogWeb</artifactId>
        <version>1.0</version>
    </dependency>
    <dependency>
        <groupId>org.aspectj</groupId>
        <artifactId>aspectjrt</artifactId>
        <version>1.9.7</version>
    </dependency>
</dependencies>
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>aspectj-maven-plugin</artifactId>
            <version>1.14.0</version>
            <executions>
                <execution>
                    <goals>
                        <goal>compile</goal>
                        <goal>test-compile</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**Gradle 示例**：

```groovy
// BlogCommon/build.gradle
dependencies {
    // 无依赖
}

// BlogConfig/build.gradle
dependencies {
    implementation project(':BlogCommon')
}

// BlogCore/build.gradle
dependencies {
    implementation project(':BlogCommon')
    implementation project(':BlogConfig')
}

// BlogWeb/build.gradle
dependencies {
    implementation project(':BlogCore')
    implementation project(':BlogConfig')
}

// BlogAspects/build.gradle
plugins {
    id 'java'
    id 'io.freefair.aspectj.post-compile-weaving' version '6.5.1'
}
dependencies {
    implementation project(':BlogCore')
    implementation project(':BlogWeb')
    implementation 'org.aspectj:aspectjrt:1.9.7'
}
```

#### 4. 测试应用程序

- 通过构建和运行应用程序来验证循环依赖是否已解决。
- 确保 `LoggingAspect` 记录 `BlogCore` 和 `BlogWeb` 中的方法执行，但不记录 `BlogConfig` 中的方法执行（除非明确需要）。
- 如果使用 Spring，检查在上下文初始化期间是否出现 `BeanCurrentlyInCreationException` 或类似错误。
- 测试 AspectJ 织入，以确认日志出现在正确的方法中。

#### 5. 其他提示

- **使用依赖分析工具**：使用 Maven 的 `mvn dependency:tree` 或 Gradle 的 `dependencies` 任务来检测任何剩余的循环依赖。
- **考虑切面的粒度**：如果仅需要为特定服务记录日志，可以进一步优化切点以针对特定类或方法（例如 `execution(* com.example.blogcore.service.*.*(..))`）。
- **避免对配置模块使用 AspectJ**：通常，避免将切面应用于配置或基础设施代码（如 `BlogConfig`），以减少复杂性。

### 最终依赖结构

重构后：

```
BlogCommon → BlogConfig → BlogCore → BlogWeb
   ↑                        ↑
   └────── BlogAspects ─────┘
```

### 为什么此方案有效

- **打破循环**：将共享依赖移动到 `BlogCommon` 或使用 IoC 确保 `BlogConfig` 不依赖于 `BlogCore`，从而消除循环依赖。
- **隔离切面**：将 `LoggingAspect` 放置在单独的模块（`BlogAspects`）中或缩小其切点范围，可以防止织入问题，并使切面逻辑独立于依赖链。
- **构建配置**：正确的构建工具设置确保模块按正确的顺序编译和织入。

这种方法在保持 AspectJ 日志功能的同时，确保了清晰、可维护的模块结构。如果您有关于设置的更多详细信息（例如 Spring 的使用、导致循环的具体类），我可以进一步优化解决方案！
