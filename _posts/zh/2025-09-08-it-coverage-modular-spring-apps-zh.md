---
audio: false
date: 2025-09-08
generated: true
image: false
lang: zh
layout: post
title: 模块化Spring应用的IT覆盖方案
translated: true
type: note
---

### 当前配置总体评估

您当前的配置对于这类小型多模块项目来说非常稳健，特别是已经实现了核心流程：将 JaCoCo 代理附加到 Jetty、通过 Exec 插件运行外部 Python 集成测试，并在 `PlaygroundWeb` 模块中生成报告。这能捕获通过 Python `unittest` 测试的 API 端点的运行时覆盖率，正是 Spring Web 应用集成测试（IT）覆盖率所需的关键能力。

核心优势：

- **模块化与阶段绑定**：使用 Maven 阶段（`pre-integration-test` 启动 Jetty、`integration-test` 运行 Python 测试、`post-integration-test` 停止服务、`verify` 生成报告）确保了可靠性和可重复性
- **代理附加机制**：Jetty 的 JVM 参数（`-javaagent:...`）正确实现了运行时检测，将覆盖率数据捕获到 `jacoco.it.exec`
- **外部测试集成**：Exec 插件完美处理 Python 测试，将测试代码保留在仓库根目录（`${project.parent.basedir}/tests`）使其与 Java 模块解耦
- **避免不必要的重复**：不在 `PlaygroundUtils`（无控制器模块）中运行 Jetty/Python，提升了效率

已识别的挑战：

- **库模块（如 `PlaygroundUtils`）的覆盖率**：由于工具类代码在 `PlaygroundWeb` 的 JVM 中运行（作为 WAR 依赖），它会被检测并出现在 `PlaygroundWeb` 的 `jacoco.it.exec` 中。但您的报告是模块特定的，因此除非聚合或包含，否则 `PlaygroundUtils` 的覆盖率不可见
- **JaCoCo 的非自包含特性**：与 Checkstyle/Spotless（仅分析源码/静态产物）不同，JaCoCo 需要来自外部测试的运行时数据（`.exec` 文件）和代理附加。这使得在多模块场景中需要精细协调
- **聚合目标限制**：`jacoco:report-aggregate` 需要每个模块的 `.exec` 文件（如单元测试生成），但您的覆盖率纯粹来自单个模块的集成测试。强制聚合会导致库模块（如 `PlaygroundUtils`）生成空报告
- **扩展到 10+ 模块的挑战**：跨模块复制 Jetty/Python 设置会造成资源浪费（冗余服务器/测试）。通过复制 `.exec` 文件或重复运行等变通方案会增加维护负担和构建时间

您回退到每模块报告的方案很务实，但我们可以优化覆盖率包含机制而避免重复。

### 推荐策略

专注于**在运行应用的模块（此处为 `PlaygroundWeb`）生成单一综合的 IT 覆盖率报告**，同时**包含依赖模块（如 `PlaygroundUtils`）的覆盖率数据**。这避免了多次运行测试，并利用了所有代码在单一 JVM 中执行的事实。

为何选择此方案而非聚合？

- 聚合（`report-aggregate`）更适合跨模块的分布式单元测试覆盖率。对于来自单一运行时的 IT 覆盖率（您的情况），它过于复杂且不自然
- 统一报告提供应用覆盖率的整体视图，通常比孤立的每模块报告更有用（例如"整体覆盖率 80%，但工具层仅 60%"）
- 对于大型项目，通过将"应用模块"（WAR/EAR）作为覆盖率中心来扩展，引入依赖项

#### 针对 2 模块项目的分步实施

从小规模开始：在当前设置（1 个应用模块 + 1 个库模块）上应用此方案。测试通过后再扩展。

1. **保持 IT 执行仅在 `PlaygroundWeb`**：
   - 此处无需更改。Jetty 启动 WAR（内嵌 `PlaygroundUtils`），Python 测试调用端点，覆盖率捕获到 `${project.build.directory}/jacoco.it.exec`
   - 确认工具类代码被执行：如果 Python 测试调用了使用 `PlaygroundUtils` 类（如 `SystemUtils`）的端点，它们的覆盖率将出现在 `.exec` 文件中

2. **增强 `PlaygroundWeb` 中的 JaCoCo 报告以包含 `PlaygroundUtils`**：
   - 在 `report` 目标中使用 JaCoCo 的 `<additionalClassesDirectories>` 和 `<additionalSourceDirectories>`。这指示 JaCoCo 针对同一 `.exec` 文件扫描 `PlaygroundUtils` 的类/源码
   - 更新 `PlaygroundWeb` 的 POM（在 `jacoco-maven-plugin` 配置中）：

     ```xml
     <plugin>
         <groupId>org.jacoco</groupId>
         <artifactId>jacoco-maven-plugin</artifactId>
         <executions>
             <!-- 现有的 prepare-agent -->
             <execution>
                 <id>prepare-agent</id>
                 <goals>
                     <goal>prepare-agent</goal>
                 </goals>
             </execution>
             <!-- 增强的报告：包含工具模块 -->
             <execution>
                 <id>report-it</id>
                 <phase>verify</phase>
                 <goals>
                     <goal>report</goal>
                 </goals>
                 <configuration>
                     <dataFile>${jacoco.it.exec}</dataFile>
                     <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
                     <!-- 添加以下内容以包含 PlaygroundUtils 覆盖率 -->
                     <additionalClassesDirectories>
                         <directory>${project.parent.basedir}/PlaygroundUtils/target/classes</directory>
                     </additionalClassesDirectories>
                     <additionalSourceDirectories>
                         <directory>${project.parent.basedir}/PlaygroundUtils/src/main/java</directory>
                     </additionalSourceDirectories>
                 </configuration>
             </execution>
         </executions>
     </plugin>
     ```

   - 这会生成一个报告（在 `PlaygroundWeb/target/site/jacoco-it`），覆盖两个模块。您将看到按包/类的细分，包括来自 utils 的 `org.lzw`

3. **在 `PlaygroundUtils` 中禁用/移除 JaCoCo**：
   - 由于它没有自身的 IT，移除所有 JaCoCo 配置/属性（如 `<jacoco.it.exec>`、`<it.report.skip>`）。它不需要生成自己的报告——覆盖率在上游处理
   - 如果 utils 中有单元测试，保留单独的 `prepare-agent` + `report` 用于单元覆盖率（默认 `jacoco.exec`），但将其与 IT 隔离

4. **构建与验证**：
   - 从父项目运行 `mvn clean verify`
   - Jetty/Python 仅运行一次（在 `PlaygroundWeb` 中）
   - 检查 `PlaygroundWeb/target/site/jacoco-it/index.html`：应显示两个模块的类覆盖率
   - 如果 utils 覆盖率为 0%，请确保 Python 测试执行了这些类（例如添加通过端点触发 `SystemUtils` 的测试）

5. **可选：强制执行覆盖率阈值**：
   - 在 `PlaygroundWeb` 的 JaCoCo 插件中添加 `check` 执行，如果覆盖率低于阈值（如整体行覆盖率 70%）则使构建失败

     ```xml
     <execution>
         <id>check-it</id>
         <goals>
             <goal>check</goal>
         </goals>
         <configuration>
             <dataFile>${jacoco.it.exec}</dataFile>
             <rules>
                 <rule>
                     <element>BUNDLE</element>
                     <limits>
                         <limit>
                             <counter>LINE</counter>
                             <value>COVEREDRATIO</value>
                             <minimum>0.70</minimum>
                         </limit>
                     </limits>
                 </rule>
             </rules>
         </configuration>
     </execution>
     ```

#### 扩展到大型项目（如 10+ 模块）

对于 10+ 模块（如多个库 + 1-2 个应用/WAR 模块），扩展上述方案以避免复杂性：

- **在应用模块集中化 IT**：如果有一个主 WAR（如 `PlaygroundWeb`），将其设为"覆盖率中心"。为所有依赖库添加 `<additionalClassesDirectories>` 和 `<additionalSourceDirectories>`（例如通过循环或父 POM 中的属性列表）
  - 示例：在父属性中定义路径：

    ```xml
    <properties>
        <lib1.classes>${project.basedir}/Lib1/target/classes</lib1.classes>
        <lib1.sources>${project.basedir}/Lib1/src/main/java</lib1.sources>
        <!-- 为 10 个库重复定义 -->
    </properties>
    ```

  - 在 WAR 的 JaCoCo 报告配置中：动态引用它们

- **如果有多个应用/WAR**：创建专用的 IT 模块（如 `App1-IT`、`App2-IT`），这些模块依赖 WAR，配置 Jetty/Exec/JaCoCo，并仅包含相关依赖的类/源码。这保持了构建的模块化（例如 `mvn verify -pl App1-IT` 进行针对性覆盖率分析）

- **避免每模块 IT 重复**：绝不在库模块中运行 Jetty/Python——这是资源浪费。如果库需要隔离的 IT（罕见情况），为其提供独立的迷你服务器/测试套件

- **报告聚合（如需要）**：如果坚持需要独立的每模块报告：
  - 在应用模块中生成 `.exec` 文件
  - 在父项目的 `post-integration-test` 中使用 Maven 的 `dependency:copy` 或自定义脚本（通过 Exec 插件）将 `.exec` 复制到每个库的 `target/`（如作为 `jacoco-it.exec`）
  - 然后，在每个库中配置 `report` 使用该复制的文件
  - 但这更复杂——除非利益相关者要求每模块指标，否则推荐统一报告

- **扩展规模的工具提示**：
  - **Maven 配置集**：使用配置集（如 `-Pcoverage`）在开发构建中切换 IT/报告以提升速度
  - **CI 优化**：在 CI（如 GitHub Actions）中缓存 Maven 依赖项，仅当测试/端点变更时运行 IT
  - **JaCoCo 过于复杂时的替代方案**：考虑使用 SonarQube 进行聚合分析（它可摄取跨模块的 JaCoCo 数据）。或切换到 OpenClover 等运行时工具，但如果坚持中心化方案，JaCoCo 已足够
  - **测试验证**：在 Python 中添加冒烟测试以验证服务器启动（如轮询 `http://localhost:8080/health`）

此策略最小化运行次数（每个应用一次 Jetty/Python），清晰处理 JaCoCo 的依赖关系，且能无爆炸性扩展。如果您分享更多细节（如 utils 如何在端点中使用），我可以进一步优化 POM 片段。
