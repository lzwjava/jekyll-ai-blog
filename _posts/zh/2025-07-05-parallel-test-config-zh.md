---
audio: false
generated: true
lang: zh
layout: post
title: 配置Maven实现并行测试执行
translated: true
type: note
---

要在 Maven 项目中启用并行测试执行，特别是针对提供的 `MavenTest.java` 类，您可以配置 Maven Surefire 插件以并行运行测试。`MavenTest.java` 类使用 JUnit 4 的动态测试功能来执行针对不同问题的 Maven 命令，而您原始错误中的堆栈跟踪显示测试已在并行运行（由堆栈跟踪中的 `ForkJoinPool` 证明）。不过，您可以通过在 `pom.xml` 文件中配置 Surefire 插件来显式控制并行执行。下面，我将解释如何设置并行测试执行，并按要求处理 `-DParallel` 标志的使用。

### 并行执行的原因

您的测试输出显示堆栈跟踪中有 `ForkJoinPool`，表明 JUnit 或 Maven 已在为并行执行使用线程池。`MavenTest` 类使用 `@TestFactory` 和 `DynamicTest`，并且测试可能由于 JUnit 的默认行为或现有的 Surefire 配置而并行运行。现在的目标是显式配置并行执行，并允许通过命令行标志（如 `-DParallel`）进行控制。

### 配置并行测试执行的步骤

1. **更新 `pom.xml` 以配置 Maven Surefire 插件**：
   Maven Surefire 插件支持 JUnit 4.7+ 的并行测试执行（您的项目使用了与 `DynamicTest` 兼容的版本）。您可以指定并行级别（例如 `classes`、`methods` 或 `both`）和线程数。为了通过 `-DParallel` 进行控制，您可以使用 Maven 属性来切换或配置并行性。

   在 `pom.xml` 中添加或更新 Surefire 插件配置：

   ```xml
   <project>
       <!-- 其他配置 -->
       <properties>
           <!-- 除非指定，否则默认为不进行并行执行 -->
           <parallel.mode>none</parallel.mode>
           <thread.count>4</thread.count>
       </properties>
       <build>
           <plugins>
               <plugin>
                   <groupId>org.apache.maven.plugins</groupId>
                   <artifactId>maven-surefire-plugin</artifactId>
                   <version>3.5.3</version>
                   <configuration>
                       <parallel>${parallel.mode}</parallel>
                       <threadCount>${thread.count}</threadCount>
                       <perCoreThreadCount>false</perCoreThreadCount>
                       <!-- 可选：并行测试的超时设置 -->
                       <parallelTestsTimeoutInSeconds>10</parallelTestsTimeoutInSeconds>
                       <!-- 分叉配置以隔离测试 -->
                       <forkCount>1</forkCount>
                       <reuseForks>true</reuseForks>
                   </configuration>
               </plugin>
           </plugins>
       </build>
   </project>
   ```

   - **解释**：
     - `<parallel>`：指定并行级别。JUnit 4.7+ 的有效值为 `methods`、`classes`、`both`、`suites`、`suitesAndClasses`、`suitesAndMethods`、`classesAndMethods` 或 `all`。对于您的 `MavenTest` 类，`classes` 是合适的，因为每个 `DynamicTest` 代表一个问题，而您希望并行运行不同问题的测试。
     - `<threadCount>`：设置线程数（例如 `4` 表示四个并发测试）。您可以通过 `-Dthread.count=<number>` 覆盖此值。
     - `<perCoreThreadCount>false</perCoreThreadCount>`：确保 `threadCount` 是固定数字，不按 CPU 核心数缩放。
     - `<parallelTestsTimeoutInSeconds>`：设置并行测试的超时时间以防止挂起（与 `MavenTest.java` 中的 `TEST_TIMEOUT` 10 秒匹配）。
     - `<forkCount>1</forkCount>`：在单独的 JVM 进程中运行测试以隔离它们，减少共享状态问题。`<reuseForks>true</reuseForks>` 允许重用 JVM 以提高效率。
     - `<parallel.mode>` 和 `<thread.count>`：可以通过命令行标志覆盖的 Maven 属性（例如 `-Dparallel.mode=classes`）。

2. **使用 `-DParallel` 运行测试**：
   要使用 `-DParallel` 标志来控制并行执行，您可以将其映射到 `parallel.mode` 属性。例如，运行：

   ```bash
   mvn test -Dparallel.mode=classes -Dthread.count=4
   ```

   - 如果未指定 `-Dparallel.mode`，默认值（`none`）将禁用并行执行。
   - 您也可以使用更简单的标志，如 `-DParallel=true`，以使用预定义模式（例如 `classes`）启用并行性。为了支持这一点，更新 `pom.xml` 以解释 `-DParallel`：

   ```xml
   <project>
       <!-- 其他配置 -->
       <properties>
           <parallel.mode>${Parallel ? 'classes' : 'none'}</parallel.mode>
           <thread.count>4</thread.count>
       </properties>
       <build>
           <plugins>
               <plugin>
                   <groupId>org.apache.maven.plugins</groupId>
                   <artifactId>maven-surefire-plugin</artifactId>
                   <version>3.5.3</version>
                   <configuration>
                       <parallel>${parallel.mode}</parallel>
                       <threadCount>${thread.count}</threadCount>
                       <perCoreThreadCount>false</perCoreThreadCount>
                       <parallelTestsTimeoutInSeconds>10</parallelTestsTimeoutInSeconds>
                       <forkCount>1</forkCount>
                       <reuseForks>true</reuseForks>
                   </configuration>
               </plugin>
           </plugins>
       </build>
   </project>
   ```

   现在，您可以使用以下命令运行测试：

   ```bash
   mvn test -DParallel=true
   ```

   - `-DParallel=true`：启用并行执行，使用 `parallel=classes` 和 `threadCount=4`。
   - `-DParallel=false` 或省略 `-DParallel`：禁用并行执行（`parallel=none`）。
   - 您可以使用 `-Dthread.count=<number>` 覆盖线程数（例如 `-Dthread.count=8`）。

3. **确保线程安全**：
   您的 `MavenTest` 类并行执行 Maven 命令（`mvn exec:exec -Dproblem=<problem>`），这会生成单独的进程。由于每个进程都有自己的内存空间，这本质上是线程安全的，避免了共享状态问题。但是，请确保：
   - `com.lzw.solutions.uva.<problem>.Main` 类不共享可能导致冲突的资源（例如文件或数据库）。
   - 每个问题使用的输入/输出文件或资源（例如 `p10009` 的测试数据）是隔离的，以避免竞态条件。
   - 如果使用了共享资源，请考虑在特定测试类上使用 `@NotThreadSafe` 或同步对共享资源的访问。

4. **在并行执行中处理跳过列表**：
   您的 `MavenTest.java` 已经包含一个 `SKIP_PROBLEMS` 集合，用于跳过如 `p10009` 这样的问题。这与并行执行配合良好，因为跳过的测试在调度前就被排除了。请根据需要更新跳过列表：

   ```java
   private static final Set<String> SKIP_PROBLEMS = new HashSet<>(Arrays.asList(
       "p10009", // 由于 NumberFormatException 跳过 p10009
       "p10037"  // 在此处添加其他有问题的问题
   ));
   ```

5. **运行测试**：
   要使用跳过列表和 `-DParallel` 标志并行运行测试：

   ```bash
   mvn test -DParallel=true -Dthread.count=4
   ```

   - 这将最多同时运行四个问题测试，跳过 `p10009` 和 `SKIP_PROBLEMS` 中的任何其他问题。
   - 如果您想为调试禁用并行性：

     ```bash
     mvn test -DParallel=false
     ```

6. **处理 `p10009` 的 `NumberFormatException`**：
   `p10009` 中的 `NumberFormatException`（来自您的原始错误）表明正在解析一个 `null` 字符串。虽然跳过 `p10009` 避免了这个问题，但为了完整性，您可能希望修复它。检查 `com.lzw.solutions.uva.p10009.Main` 的第 17 行（`readInt` 方法）并添加空值检查：

   ```java
   public int readInt() {
       String input = readInput(); // 假设的输入读取方法
       if (input == null || input.trim().isEmpty()) {
           throw new IllegalArgumentException("输入不能为 null 或空");
       }
       return Integer.parseInt(input);
   }
   ```

   或者，在问题解决之前将 `p10009` 保留在跳过列表中。

### 关于并行执行的注意事项

- **性能**：对于您的 `MavenTest` 类，使用 `parallel=classes` 进行并行执行是合适的，因为每个 `DynamicTest` 代表一个不同的问题。与 `methods` 或 `both` 相比，这最小化了开销。
- **资源使用**：并行执行会增加 CPU 和内存使用量。监控您的系统以确保 `threadCount`（例如 `4`）不会使硬件过载。如果出现内存问题，请使用 `forkCount` 在单独的 JVM 中隔离测试。
- **超时**：`parallelTestsTimeoutInSeconds` 设置确保测试不会无限期挂起，与 `MavenTest.java` 中的 `TEST_TIMEOUT` 10 秒保持一致。
- **线程安全**：由于您的测试执行 `mvn exec:exec` 命令，这些命令在单独的进程中运行，因此线程安全问题较少。但是，请确保每个问题的测试输入/输出（例如文件）是隔离的。
- **调试**：如果测试在并行模式下意外失败，请按顺序运行它们（`-DParallel=false`）以隔离问题。

### 完整命令示例

要并行运行测试，跳过 `p10009`，使用四个线程：

```bash
mvn test -DParallel=true -Dthread.count=4
```

要调试特定问题（例如 `p10009`）而不使用并行性，请暂时将其从 `SKIP_PROBLEMS` 中移除并运行：

```bash
mvn test -DParallel=false -Dproblem=p10009
```

### 其他考虑事项

- **JUnit 4 限制**：您的项目使用 JUnit 4（基于 `org.junit.jupiter.api` 导入和 `DynamicTest`）。JUnit 4.7+ 通过 Surefire 支持并行执行，但 JUnit 5 提供了更灵活的并行化选项。如果您需要每个类的并行性或自定义策略等高级功能，请考虑升级到 JUnit 5。
- **Maven 版本**：确保您使用的是最新版本的 Maven（例如 3.9.10，如您的错误输出所示）和 Surefire（例如 3.5.3），以获得最佳的并行执行支持。
- **错误处理**：为了使测试更加健壮，考虑在 `runMavenExecTests` 中捕获异常（如之前的响应中所建议的），以记录失败而不停止测试套件：

   ```java
   @TestFactory
   Collection<DynamicTest> runMavenExecTests() {
       return PROBLEMS.stream()
               .map(problem -> DynamicTest.dynamicTest("测试问题: " + problem, () -> {
                   String command = String.format("mvn exec:exec -Dproblem=%s", problem);
                   System.out.println("为 " + problem + " 执行命令: " + command);
                   try {
                       Process process = Runtime.getRuntime().exec(command);
                       // ...（其余进程处理代码）
                       int exitCode = process.exitValue();
                       Assertions.assertTrue(
                               exitCode == 0,
                               "Maven 命令对问题失败: " + problem + "\n错误输出:\n" + errorOutput);
                   } catch (Exception e) {
                       System.err.println("问题 " + problem + " 的异常: " + e.getMessage());
                       // 可选地继续而不是失败
                   }
               }))
               .collect(Collectors.toList());
   }
   ```

此设置允许您使用 `-DParallel=true` 控制并行执行，跳过有问题的测试（如 `p10009`），并保持健壮的测试执行。如果您需要进一步定制，例如通过命令行参数动态跳过列表或高级 JUnit 5 配置，请告诉我！
