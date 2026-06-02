---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: JavaCC 源码与类文件位置
translated: true
type: note
---

### JavaCC 概述

JavaCC（Java 编译器编译器）是一个能够从语法规范文件（.jj 文件）生成 Java 源代码（例如解析器类）的工具。它**不会**直接将代码编译成字节码（.class 文件）——这部分工作由标准 Java 编译器（如 `javac`）处理。如果您以编程方式使用 JavaCC（例如在 IDE 或运行时环境中）来生成和编译动态代码，其输出位置取决于您的配置方式。我将基于 JavaCC 的标准行为和常见使用模式逐步说明。

### JavaCC 生成源文件的位置

- **默认输出位置**：JavaCC 将生成的 `.java` 文件输出到**当前工作目录**（如果未指定，则输出到名为 "output" 的子目录）。您可以通过命令行选项（如 `-OUTPUT_DIRECTORY=<路径>`）或在代码中通过 `JavaCCOptions` 类以编程方式覆盖此设置。
- **命令行使用示例**：

  ```
  javacc -OUTPUT_DIRECTORY=/路径/到/生成文件 MyGrammar.jj
  ```

  这将在 `/路径/到/生成文件` 中创建 `.java` 文件（例如 `Token`、`Parser`、`ParseException`）。
- **编程方式使用**：如果您在 Java 应用程序内部调用 JavaCC（例如使用 `org.javacc.JavaCC.main()` 或类似的 API），您可以设置选项来指定输出路径。这些源文件只是普通的 `.java` 文件，需要进一步编译。

这与官方 JavaCC 文档（例如来自 SourceForge 上的传统 JavaCC 项目或基于 Maven 的发行版）一致，其中说明生成的类作为源代码输出到指定目录，而不是字节码。

### 如果编译生成的代码，编译后的类文件存储位置

JavaCC 本身不会编译成 `.class` 文件——您必须手动执行此操作或在代码中自动化此过程。接下来会发生以下情况：

- **手动编译**：对生成的 `.java` 文件使用 `javac`：

  ```
  javac -d /路径/到/类文件 MyGeneratedParser.java
  ```

  - `-d` 标志指定 `.class` 文件的输出目录，通常是 `classes/` 文件夹或项目的构建目标目录（例如 Maven/Gradle 中的 `target/classes/`）。
  - 常见位置：根据您的构建系统（例如 Ant、Maven），可能是 `bin/`、`build/classes/` 或 `target/classes/`。

- **代码中的动态编译**：如果您在运行时使用 JavaCC 为动态代码生成解析器（例如用于脚本解释或即时解析），您通常会：
  1. 以编程方式生成 `.java` 文件（例如写入临时目录，如 `System.getProperty("java.io.tmpdir")`）。
  2. 使用 Java 编译器 API（`javax.tools.JavaCompiler`）或像 Janino 这样的库编译它们。
     - 示例：将编译输出设置为自定义目录，例如 `new File("generated/classes")`。
     - 编译后的 `.class` 文件存储在该目录中。在运行时，使用自定义 ClassLoader 从那里或内存缓冲区加载它们。
  - **JVM 默认设置**：如果没有自定义路径，类文件可能会根据构建工具默认输出到 `target/classes`，或者根据编译任务中指定的任何目录输出。

- **常见动态场景**：
  - **内存编译**：像编译器 API 这样的库允许在不写入磁盘的情况下编译，通过 `ClassLoader.defineClass()` 将字节码存储在内存中。不会发生物理存储。
  - **临时存储**：如果生成的代码被编译并持久化，通常会输出到类 Unix 系统上的 `/tmp/` 或临时文件夹。对于生产应用程序，请使用项目文件系统中的专用 `generated/` 或 `cache/` 目录。
  - **框架**：像 ANTLR（JavaCC 的替代品）或自定义运行器这样的工具可能会自动化此过程，将类存储在 RAM 或类路径文件夹中（例如 `CLASSPATH` 条目）。

### 关键考虑因素和最佳实践

- **运行时安全性**：动态编译代码存在风险（例如安全问题）。确保用户生成的语法经过沙箱处理。
- **构建工具集成**：如果使用 Maven 或 Gradle，JavaCC 插件（例如 `javacc-maven-plugin`）会将源文件输出到 `target/generated-sources/javacc/`，编译后的类文件输出到 `target/classes/`，这些可以在您的 `pom.xml` 或 `build.gradle` 中配置。
- **调试**：如果编译失败，请检查 JavaCC 的错误输出或日志。生成的文件通常存储在您的应用程序运行的位置，而不是全局位置。
- **文档证据**：根据 JavaCC 的官方指南（javacc.github.io 或传统文档），输出是基于目录的，编译后处理由用户管理。GitHub 仓库中的实际示例（例如搜索 JavaCC 使用情况）显示了自定义输出目录，如 `src/main/generated/`。

如果这与您的设置不匹配（例如特定的框架或 IDE），请提供更多详细信息，如您的代码片段或环境，我可以进一步优化答案！
