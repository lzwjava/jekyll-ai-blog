---
audio: false
generated: true
lang: zh
layout: post
title: 在VSCode中配置Spring Boot的launch.json文件
translated: true
type: note
---

要为 Maven Spring Boot 项目在 Visual Studio Code (VSCode) 中配置 `launch.json` 文件，您需要设置一个启动配置，使 VSCode 能够使用其 Java 扩展来运行和调试您的应用程序。以下是帮助您完成此操作的逐步指南。

### 前提条件

在继续之前，请确保：

- 您已在 VSCode 中安装了 **Java Extension Pack**。此包包含必要的扩展，例如 Red Hat 的 "Debugger for Java" 和 "Language Support for Java"，它们为运行和调试 Java 应用程序（包括 Spring Boot 项目）提供支持。
- 您的 Spring Boot 项目是一个具有有效 `pom.xml` 文件的 Maven 项目。
- 项目有一个带有 `@SpringBootApplication` 注解的主类，该类包含用于启动应用程序的 `main` 方法。

### 配置 `launch.json` 的步骤

1. **定位主类**
   - 在典型的 Spring Boot 项目中，主类位于 `src/main/java` 目录中，并带有 `@SpringBootApplication` 注解。例如，它可能名为 `com.example.demo.DemoApplication`。
   - 在 VSCode 中打开您的项目，并确定此类的完全限定名称（例如 `com.example.demo.DemoApplication`）。

2. **确定项目名称**
   - Maven 项目中的项目名称对应于您的 `pom.xml` 文件中定义的 `artifactId`。
   - 打开您的 `pom.xml` 文件并查找 `<artifactId>` 标签。例如：

     ```xml
     <artifactId>demo</artifactId>
     ```

     这里，项目名称将是 `demo`。

3. **打开调试视图**
   - 在 VSCode 中，点击左侧边栏中的 **调试** 图标（或在 Mac 上按 `Cmd+Shift+D`）。
   - 点击“运行和调试”下拉菜单旁边的齿轮图标 ⚙️ 以配置启动设置。如果不存在 `launch.json`，VSCode 将提示您创建一个。

4. **创建或编辑 `launch.json`**
   - 如果提示选择环境，请选择 **Java**。这将在您项目的 `.vscode` 文件夹中生成一个基本的 `launch.json` 文件。
   - 打开 `launch.json` 文件。如果它已存在，您可以直接编辑它。

5. **添加启动配置**
   - 在 `launch.json` 的 `"configurations"` 数组中添加以下配置。将占位符替换为您项目的详细信息：

     ```json
     {
         "type": "java",
         "name": "启动 Spring Boot 应用",
         "request": "launch",
         "mainClass": "com.example.demo.DemoApplication",
         "projectName": "demo"
     }
     ```

     - **字段说明：**
       - `"type": "java"`：指定这是一个 Java 启动配置。
       - `"name": "启动 Spring Boot 应用"`：此配置的描述性名称，将出现在调试下拉菜单中。
       - `"request": "launch"`：指示 VSCode 应启动应用程序（而不是附加到现有进程）。
       - `"mainClass"`：您的 Spring Boot 主类的完全限定名称（例如 `com.example.demo.DemoApplication`）。
       - `"projectName"`：来自您的 `pom.xml` 的 `artifactId`（例如 `demo`），这有助于 VSCode 在多模块设置中定位项目。

   - 以下是包含此配置的完整 `launch.json` 文件示例：

     ```json
     {
         "version": "0.2.0",
         "configurations": [
             {
                 "type": "java",
                 "name": "启动 Spring Boot 应用",
                 "request": "launch",
                 "mainClass": "com.example.demo.DemoApplication",
                 "projectName": "demo"
             }
         ]
     }
     ```

6. **可选：添加 VM 参数或程序参数**
   - 如果您的应用程序需要其他设置（例如，激活 Spring 配置文件），您可以使用 `"vmArgs"` 或 `"args"` 添加它们：
     - 使用 Spring 配置文件的示例：

       ```json
       {
           "type": "java",
           "name": "使用配置文件启动 Spring Boot 应用",
           "request": "launch",
           "mainClass": "com.example.demo.DemoApplication",
           "projectName": "demo",
           "vmArgs": "-Dspring.profiles.active=dev"
       }
       ```

       这将 `spring.profiles.active` 属性设置为 `dev`。
     - 使用程序参数的示例：

       ```json
       "args": ["arg1", "arg2"]
       ```

7. **保存并运行**
   - 保存 `launch.json` 文件。
   - 返回调试视图，从下拉菜单中选择 **"启动 Spring Boot 应用"**，然后点击绿色播放按钮（或按 `F5`）。
   - VSCode 将使用 Maven 和 Java 扩展构建并运行您的 Spring Boot 应用程序。您应该在调试控制台中看到 Spring Boot 启动日志。

### 验证配置

- 如果您的 Spring Boot 应用程序是一个 Web 应用程序，请打开浏览器并导航到 `http://localhost:8080`（或在您的 `application.properties` 或 `application.yml` 文件中指定的端口）以确认它正在运行。
- 您还可以在代码中设置断点，并使用调试控件（暂停、单步跳过等）来调试您的应用程序。

### 注意事项

- VSCode 中的 Java 扩展会根据您的 `pom.xml` 自动处理类路径和构建过程，因此您通常不需要事先手动运行 `mvn clean install`。
- 如果您的项目是多模块 Maven 设置的一部分，请确保 `projectName` 与正确模块的 `artifactId` 匹配。
- 对于高级配置（例如，自定义工作目录或启动前任务），请参阅 [VSCode Java 调试文档](https://code.visualstudio.com/docs/java/java-debugging)。

通过此设置，您的 `launch.json` 应该已正确配置，以便在 VSCode 中运行和调试您的 Maven Spring Boot 项目！
