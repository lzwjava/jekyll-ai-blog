---
audio: false
generated: true
lang: zh
layout: post
title: Java代码规范工具对比：Spotless与Checkstyle
translated: true
type: note
---

你可以在 Java 项目中同时使用 **Spotless Maven 插件**和 **Checkstyle Maven 插件**，因为它们的功能互为补充。但是否*需要*同时使用两者，取决于项目的具体要求。下面我将解释它们如何协同工作、它们的区别以及何时选择其中之一。

### Spotless 与 Checkstyle 的主要区别

| **方面**            | **Spotless**                                                                 | **Checkstyle**                                                              |
|-----------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **目的**           | 自动格式化代码以强制执行一致的样式并修复问题。   | 静态分析代码以强制执行编码标准并检测违规。  |
| **操作**            | 修改代码（例如，修复缩进、导入顺序，移除未使用的导入）。 | 报告违规而不修改代码；如果检查失败则构建失败。      |
| **配置**     | 配置格式化工具，如 `palantir-java-format`、`google-java-format` 等。 | 使用规则集（例如 Google 或 Sun 检查）定义编码标准。      |
| **输出**            | 格式化后的源文件（使用 `mvn spotless:apply`）。                          | 报告（XML、HTML 或控制台），列出样式违规。                   |
| **使用场景**          | 确保在提交或构建前代码格式一致。             | 强制执行编码标准并捕获如复杂度或不良实践等问题。 |

### 同时使用 Spotless 和 Checkstyle

你可以结合使用 Spotless 和 Checkstyle，以实现**自动格式化**和**样式强制执行**。以下是它们如何互补：

1. **Spotless 用于格式化**：
   - Spotless 使用如 `palantir-java-format` 等工具应用格式化规则（例如缩进、导入顺序）。
   - 它确保代码格式一致，减少手动操作。
   - 示例：修复 2 空格与 4 空格缩进、排序导入、移除未使用的导入。

2. **Checkstyle 用于验证**：
   - Checkstyle 强制执行格式化之外的编码标准，如方法长度、命名约定或复杂度。
   - 它捕获格式化工具可能无法处理的问题，如缺少 Javadoc 或过于复杂的方法。
   - 示例：标记参数过多的方法或强制要求公共方法必须有 Javadoc。

3. **工作流程**：
   - 首先运行 Spotless（`mvn spotless:apply`）格式化代码。
   - 然后运行 Checkstyle（`mvn checkstyle:check`）验证是否符合附加规则。
   - 这确保代码既格式规范又符合更广泛的样式指南。

### `pom.xml` 中的配置示例

以下是如何在 `pom.xml` 中配置这两个插件：

```xml
<build>
    <plugins>
        <!-- Spotless Plugin for Formatting -->
        <plugin>
            <groupId>com.diffplug.spotless</groupId>
            <artifactId>spotless-maven-plugin</artifactId>
            <version>2.43.0</version>
            <configuration>
                <java>
                    <includes>
                        <include>src/main/java/**/*.java</include>
                        <include>src/test/java/**/*.java</include>
                    </includes>
                    <palantirJavaFormat>
                        <version>2.53.0</version>
                        <style>GOOGLE</style> <!-- Use Google style -->
                    </palantirJavaFormat>
                    <indent>
                        <spacesPerTab>2</spacesPerTab> <!-- 2-space indentation -->
                    </indent>
                    <importOrder>
                        <order>java,javax,org,com,\\#</order>
                    </importOrder>
                    <removeUnusedImports/>
                    <trimTrailingWhitespace/>
                    <endWithNewline/>
                </java>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>apply</goal>
                    </goals>
                    <phase>validate</phase>
                </execution>
            </executions>
        </plugin>

        <!-- Checkstyle Plugin for Validation -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.4.0</version>
            <configuration>
                <configLocation>google_checks.xml</configLocation> <!-- Use Google style or custom XML -->
                <includeTestSourceDirectory>true</includeTestSourceDirectory>
                <failOnViolation>true</failOnViolation> <!-- Fail build on violations -->
                <consoleOutput>true</consoleOutput> <!-- Output violations to console -->
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <phase>validate</phase>
                </execution>
            </executions>
            <dependencies>
                <!-- Specify Checkstyle version -->
                <dependency>
                    <groupId>com.puppycrawl.tools</groupId>
                    <artifactId>checkstyle</artifactId>
                    <version>10.17.0</version>
                </dependency>
            </dependencies>
        </plugin>
    </plugins>
</build>
```

### 关键配置说明

1. **共享样式规则**：
   - 为避免冲突，对齐 Spotless 和 Checkstyle 的配置。例如，在 Spotless 中使用 `palantirJavaFormat` 并设置 `style>GOOGLE`，在 Checkstyle 中使用 `google_checks.xml`。
   - 从 [Checkstyle 的 GitHub](https://github.com/checkstyle/checkstyle/blob/master/src/main/resources/google_checks.xml) 下载 `google_checks.xml` 或创建自定义规则集。

2. **执行顺序**：
   - 在 `validate` 阶段先运行 Spotless，再运行 Checkstyle，确保在验证前代码已格式化。
   - 示例：`mvn spotless:apply checkstyle:check`。

3. **自定义 Checkstyle 规则**：
   - 自定义 `google_checks.xml` 或创建自己的规则集（例如 `my_checks.xml`）以强制执行特定规则，如：

     ```xml
     <module name="Indentation">
         <property name="basicOffset" value="2"/>
         <property name="lineWrappingIndentation" value="4"/>
     </module>
     <module name="ImportOrder">
         <property name="groups" value="java,javax,org,com"/>
         <property name="ordered" value="true"/>
         <property name="separated" value="true"/>
     </module>
     ```

4. **避免冗余**：
   - 如果 Spotless 处理了格式化（例如缩进、导入顺序），禁用 Checkstyle 中重叠的规则以避免重复检查。例如，如果 Spotless 强制执行缩进，则禁用 Checkstyle 的 `Indentation` 模块：

     ```xml
     <module name="Indentation">
         <property name="severity" value="ignore"/>
     </module>
     ```

### 何时使用其中之一或两者

- **仅使用 Spotless**：
  - 如果只需要一致的代码格式化（例如缩进、导入顺序、空格）。
  - 适合希望自动格式化而不需要严格样式强制执行的团队。
  - 示例：小型项目或使用 IDE 格式化的团队。

- **仅使用 Checkstyle**：
  - 如果需要强制执行编码标准（例如命名约定、Javadoc、方法复杂度）而不修改代码。
  - 适用于开发人员手动格式化代码但需要验证的项目。

- **同时使用两者**：
  - 用于健壮的代码质量：Spotless 自动格式化代码，Checkstyle 捕获附加问题（例如缺少 Javadoc、复杂方法）。
  - 常见于大型团队或需要严格编码标准的项目。
  - 示例：企业项目或需要一致样式和质量检查的开源仓库。

### 实际考虑

- **性能**：运行两个插件会增加构建时间。在 CI 管道中使用 `spotless:check`（而非 `apply`）和 `checkstyle:check` 来验证而不修改代码。
- **IDE 集成**：
  - Spotless：使用 Spotless Gradle/Maven 任务或 IDE 插件（例如 IntelliJ 的 `palantir-java-format`）。
  - Checkstyle：使用 IntelliJ 的 Checkstyle-IDEA 插件或 Eclipse Checkstyle 插件，配置相同的 `google_checks.xml`。
- **CI/CD**：在 CI 管道（例如 Jenkins、GitHub Actions）中配置两个插件，以在拉取请求上强制执行格式化和样式检查。

  ```yaml
  # Example GitHub Actions workflow
  name: CI
  on: [pull_request]
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up JDK 17
          uses: actions/setup-java@v3
          with: { java-version: '17' }
        - name: Run Spotless and Checkstyle
          run: mvn spotless:check checkstyle:check
  ```

### 潜在冲突及解决方案

- **重叠规则**：如果 Spotless 格式化代码的方式与 Checkstyle 规则不同（例如 2 空格与 4 空格缩进），构建可能失败。解决方案：对齐配置（例如两者都使用 `GOOGLE` 样式）。
- **构建失败**：如果 Spotless 未运行，Checkstyle 的 `failOnViolation` 可能导致构建中断。解决方案：确保 Spotless 先运行或使用 `spotless:check` 验证格式化。
- **团队接受度**：开发人员可能抵制自动格式化。解决方案：在 CI 中使用 `spotless:check` 并教育团队使用 IDE 集成。

### 来源

- Spotless 文档：[GitHub](https://github.com/diffplug/spotless/tree/main/plugin-maven)
- Checkstyle Maven 插件：[Maven 站点](https://maven.apache.org/plugins/maven-checkstyle-plugin/)
- Stack Overflow 和 GitHub issues 上的社区讨论

### 结论

同时使用 Spotless 和 Checkstyle 是维护代码质量的强大组合：Spotless 确保一致的格式化，而 Checkstyle 强制执行更广泛的编码标准。配置它们以对齐（例如相同的缩进和导入顺序规则）并在构建过程中顺序运行它们。如果你的项目仅需要格式化，仅使用 Spotless 可能足够；如果需要严格验证，考虑添加 Checkstyle。如果你需要特定配置或示例 `google_checks.xml` 文件的帮助，请告诉我！
