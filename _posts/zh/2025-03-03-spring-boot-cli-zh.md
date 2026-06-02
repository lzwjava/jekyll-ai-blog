---
audio: false
generated: true
lang: zh
layout: post
title: 如何使用Spring Boot CLI
translated: true
type: note
---

Spring Boot CLI（命令行界面）是一个功能强大的工具，允许您直接从命令行快速开发、测试和原型化 Spring Boot 应用程序。它特别适用于运行 Groovy 脚本而无需搭建完整的项目结构、生成新项目或试验 Spring Boot 功能。以下是关于如何有效安装和使用 Spring Boot CLI 的完整指南。

---

## 安装
在使用 Spring Boot CLI 之前，您需要先安装它。根据您的操作系统，主要有两种安装方法：

### 1. 使用 SDKMAN！（推荐用于基于 Unix 的系统，如 Linux 或 macOS）
SDKMAN! 是一个用于管理软件开发工具包的工具，可以轻松安装 Spring Boot CLI。

- **步骤 1：安装 SDKMAN!**
  打开终端并运行：
  ```bash
  curl -s "https://get.sdkman.io" | bash
  ```
  按照提示通过执行脚本来初始化 SDKMAN!：
  ```bash
  source "$HOME/.sdkman/bin/sdkman-init.sh"
  ```

- **步骤 2：安装 Spring Boot CLI**
  运行以下命令：
  ```bash
  sdk install springboot
  ```

### 2. 手动安装（适用于 Windows 或手动设置）
如果您使用的是 Windows 或偏好手动安装：
- 从 [Spring 官方网站](https://spring.io/projects/spring-boot) 下载 Spring Boot CLI ZIP 文件。
- 将 ZIP 文件解压缩到您选择的目录。
- 将解压文件夹中的 `bin` 目录添加到系统的 PATH 环境变量中。

### 验证安装
要确认 Spring Boot CLI 已正确安装，请在终端中运行以下命令：
```bash
spring --version
```
您应该会看到已安装的 Spring Boot CLI 版本（例如 `Spring CLI v3.3.0`）。如果此命令有效，说明您已准备好开始使用它！

---

## Spring Boot CLI 的主要使用方式
Spring Boot CLI 提供了多项功能，使其成为快速开发和原型设计的理想工具。以下是其主要使用方式：

### 1. 运行 Groovy 脚本
Spring Boot CLI 的一个突出特点是能够直接运行 Groovy 脚本，而无需完整的项目设置。这非常适合快速原型设计或试验 Spring Boot。

- **示例：创建一个简单的 Web 应用程序**
  创建一个名为 `hello.groovy` 的文件，内容如下：
  ```groovy
  @RestController
  class HelloController {
      @RequestMapping("/")
      String home() {
          "Hello, World!"
      }
  }
  ```

- **运行脚本**
  在终端中，导航到包含 `hello.groovy` 的目录并运行：
  ```bash
  spring run hello.groovy
  ```
  这将在端口 8080 上启动一个 Web 服务器。打开浏览器并访问 `http://localhost:8080`，您将看到显示 "Hello, World!"。

- **添加依赖项**
  您可以使用 `@Grab` 注解直接在脚本中包含依赖项。例如：
  ```groovy
  @Grab('org.springframework.boot:spring-boot-starter-data-jpa')
  @RestController
  class HelloController {
      @RequestMapping("/")
      String home() {
          "Hello, World!"
      }
  }
  ```
  这将在无需构建文件的情况下将 Spring Data JPA 添加到您的脚本中。

- **运行多个脚本**
  要运行当前目录中的所有 Groovy 脚本，请使用：
  ```bash
  spring run *.groovy
  ```

### 2. 创建新的 Spring Boot 项目
Spring Boot CLI 可以生成具有所需依赖项的新项目结构，从而在启动完整应用程序时节省时间。

- **示例：生成项目**
  运行以下命令以创建一个具有 Web 和 data-jpa 依赖项的新项目：
  ```bash
  spring init --dependencies=web,data-jpa my-project
  ```
  这将创建一个名为 `my-project` 的目录，其中包含一个配置了 Spring Web 和 Spring Data JPA 的 Spring Boot 应用程序。

- **自定义选项**
  您可以指定其他选项，例如：
  - 构建工具：`--build=maven` 或 `--build=gradle`
  - 语言：`--language=java`、`--language=groovy` 或 `--language=kotlin`
  - 打包方式：`--packaging=jar` 或 `--packaging=war`

  例如：
  ```bash
  spring init --dependencies=web --build=gradle --language=kotlin my-kotlin-project
  ```

### 3. 打包应用程序
Spring Boot CLI 允许您将脚本打包成可执行的 JAR 或 WAR 文件以便部署。

- **创建 JAR 文件**
  ```bash
  spring jar my-app.jar *.groovy
  ```
  这将当前目录中的所有 Groovy 脚本打包到 `my-app.jar` 中。

- **创建 WAR 文件**
  ```bash
  spring war my-app.war *.groovy
  ```
  这将生成一个适用于 Servlet 容器部署的 `my-app.war` 文件。

### 4. 运行测试
如果您有 Groovy 测试脚本，可以使用以下命令执行它们：
```bash
spring test *.groovy
```
这将运行当前目录中的所有测试脚本。

### 5. 使用交互式 Shell
要获得交互式体验，请启动 Spring Boot CLI shell：
```bash
spring shell
```
在 shell 中，您可以交互式地运行 `run`、`grab` 或 `jar` 等命令，这对于实验非常有用。

---

## 总结
Spring Boot CLI 是一个出色的工具，适用于希望从命令行快速高效地使用 Spring Boot 的开发者。以下是其使用要点：

1. **安装**：使用 SDKMAN!（`sdk install springboot`）或通过下载 ZIP 文件并更新 PATH 进行手动安装。
2. **运行 Groovy 脚本**：使用 `spring run <script.groovy>` 进行快速原型设计。
3. **创建新项目**：使用 `spring init --dependencies=<deps> <project-name>`。
4. **打包应用程序**：使用 `spring jar` 或 `spring war` 将应用程序打包成 JAR 或 WAR 文件。
5. **交互式实验**：使用 `spring shell`。

无论您是在原型化一个想法、学习 Spring Boot 还是自动化任务，Spring Boot CLI 都提供了一种轻量级且灵活的方式来开始，而无需完整的 IDE 或项目设置的开销。
