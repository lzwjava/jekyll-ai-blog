---
audio: false
generated: true
lang: zh
layout: post
title: 使用Eclipse
translated: true
type: note
---

### 核心要点

- Eclipse 似乎能够有效配合 IBM Websphere Liberty、Spring、Spring Boot 和 Maven 使用，但需要进行特定配置。
- 研究表明，在 Eclipse 中安装 Spring Tool Suite (STS) 和 IBM Liberty Developer Tools 插件可以增强功能。
- 现有证据倾向于使用 STS 或 Spring Initializr 创建 Spring Boot 项目，然后配置其用于 Websphere Liberty 部署。

### 设置 Eclipse

首先，从 [Eclipse 下载页面](https://www.eclipse.org/downloads/packages/release/2024-06/r/eclipse-ide-enterprise-java-and-web-developers) 下载并安装 "Eclipse IDE for Enterprise Java and Web Developers"。确保已安装 JDK 17 或更高版本，您可以在终端中运行 `java -version` 来验证。

### 配置 Spring 和 Spring Boot

在 Eclipse 中通过 Help -> Eclipse Marketplace 安装 Spring Tool Suite (STS) 插件，搜索 "Spring Tools" 并安装相应版本。这将增强 Spring 和 Spring Boot 开发功能。您可以直接在 Eclipse 中通过 File -> New -> Spring Starter Project 创建新的 Spring Boot 项目，选择 Maven 作为构建工具并添加必要的依赖项（如 Spring Web）。

### 集成 IBM Websphere Liberty

通过 Eclipse Marketplace 搜索 "IBM Liberty Developer Tools" 并按照安装提示安装 IBM Liberty Developer Tools。通过 Window -> Preferences -> Servers -> Runtime Environments 设置 Websphere Liberty 服务器，添加新的 Websphere Liberty 运行时，并通过 File -> New -> Other -> Server 创建服务器实例。确保服务器的 server.xml 包含 `<feature>springBoot-2.0</feature>` 以支持 Spring Boot，如 [Open Liberty 文档](https://openliberty.io/docs/latest/deploy-spring-boot.html) 中所述。

### 部署应用程序

修改您的 Spring Boot 应用程序，使其扩展 `SpringBootServletInitializer` 而不是使用启动嵌入式服务器的主方法，通过在 pom.xml 中设置 `<packaging>war</packaging>` 将其打包为 WAR 文件。通过右键单击项目，选择 "Run As -> Run on Server" 并选择您的 Liberty 服务器进行部署。这确保应用程序在 Liberty 的 Web 容器上运行。

---

### 调研说明：使用 Eclipse 与 IBM Websphere Liberty、Spring、Spring Boot 和 Maven 的完整指南

本指南提供了在 Eclipse 中有效使用 IBM Websphere Liberty、Spring、Spring Boot 和 Maven 的详细步骤，专为在这些生态系统中工作的开发人员量身定制。该过程涉及设置 Eclipse、安装必要的插件、创建和配置项目以及部署应用程序，重点关注集成和最佳实践（截至 2025 年 2 月 27 日）。

#### Eclipse 设置与先决条件

Eclipse 是一个强大的 Java 开发 IDE，特别适用于企业应用程序。对于此设置，请从 [Eclipse 下载页面](https://www.eclipse.org/downloads/packages/release/2024-06/r/eclipse-ide-enterprise-java-and-web-developers) 下载 "Eclipse IDE for Enterprise Java and Web Developers" 2024-06 版本。确保您的系统安装了 JDK 17 或更高版本，您可以在终端中运行 `java -version` 进行检查。此版本确保与现代 Spring 和 Liberty 功能的兼容性。

#### 安装基本插件

为了增强 Eclipse 的 Spring 和 Spring Boot 开发功能，请安装 Spring Tool Suite (STS)，这是 Spring 工具的下一个代。通过 Help -> Eclipse Marketplace 访问，搜索 "Spring Tools"，并安装标记为 "Spring Tools (aka Spring IDE and Spring Tool Suite)" 的条目。该插件在 [Spring Tools](https://spring.io/tools/) 中有详细说明，为基于 Spring 的应用程序提供一流的支持，并与 Eclipse 无缝集成，提供项目创建和调试等功能。

对于 IBM Websphere Liberty 集成，请安装 IBM Liberty Developer Tools，同样可以通过 Eclipse Marketplace 搜索 "IBM Liberty Developer Tools" 获得。该插件在 [IBM Liberty Developer Tools](https://marketplace.eclipse.org/content/ibm-liberty-developer-tools) 中注明已针对 Eclipse 2024-06 进行测试，支持构建和部署 Java EE 应用程序到 Liberty，并向后兼容至 2019-12 版本。

#### 创建 Spring Boot 项目

在安装了 STS 的 Eclipse 中，有两种主要方法可以创建 Spring Boot 项目：

1. **使用 Spring Initializr**：访问 [Spring Initializr](https://start.spring.io/)，选择 Maven 作为构建工具，选择项目元数据（Group、Artifact 等），并添加依赖项（如 Spring Web）。将项目生成为 ZIP 文件，解压缩，然后通过 File -> Import -> Existing Maven Project 导入到 Eclipse 中，选择解压缩后的文件夹。

2. **直接使用 STS**：打开 Eclipse，转到 File -> New -> Other，展开 Spring Boot，然后选择 "Spring Starter Project"。按照向导操作，确保选择 Maven 作为类型，并选择依赖项。如 [使用 Eclipse 和 Maven 创建 Spring Boot 项目](https://www.springboottutorial.com/creating-spring-boot-project-with-eclipse-and-maven) 中所述，此方法因其与 Eclipse 工作区的集成而受到青睐。

两种方法都确保创建基于 Maven 的项目，这对于使用 Spring Boot 进行依赖管理至关重要。

#### 配置 Websphere Liberty 部署

要部署到 Websphere Liberty，需要修改您的 Spring Boot 应用程序，使其在 Liberty 的 Web 容器上运行，而不是启动嵌入式服务器。这包括：

- 确保主应用程序类扩展 `SpringBootServletInitializer`。例如：

  ```java
  @SpringBootApplication
  public class MyApplication extends SpringBootServletInitializer {
      // 无主方法；Liberty 处理启动
  }
  ```

- 更新 pom.xml 以打包为 WAR 文件，添加：

  ```xml
  <packaging>war</packaging>
  ```

  这对于传统的 servlet 容器部署是必要的，如 [部署 Spring Boot 应用程序](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment.html#deployment.servlet) 中所述。

Websphere Liberty，特别是其开源变体 Open Liberty，支持具有特定功能的 Spring Boot 应用程序。确保 Liberty 服务器的 server.xml 包含 `<feature>springBoot-2.0</feature>` 以支持 Spring Boot 2.x，如 [Open Liberty 文档](https://openliberty.io/docs/latest/deploy-spring-boot.html) 中所述。此配置禁用嵌入式 Web 容器，转而利用 Liberty 的容器。

#### 在 Eclipse 中设置和配置 Websphere Liberty 服务器

安装 IBM Liberty Developer Tools 后，设置 Liberty 服务器：

- 导航到 Window -> Preferences -> Servers -> Runtime Environments，单击 "Add"，然后选择 "WebSphere Application Server Liberty"。按照向导定位您的 Liberty 安装目录，通常位于类似 `<Liberty_Root>/wlp` 的目录中，如 [Liberty 和 Eclipse](https://www.ibm.com/cloud/blog/liberty-and-eclipse-installing-dev-environment-p9) 中所述。

- 通过 File -> New -> Other -> Server 创建新的服务器实例，选择 "WebSphere Application Server Liberty" 和您配置的运行时。命名服务器并根据需要调整设置。

- 编辑服务器的 server.xml（可通过 Servers 视图访问）以包含必要的功能。对于 Spring Boot，添加：

  ```xml
  <featureManager>
      <feature>springBoot-2.0</feature>
      <!-- 其他功能，如用于 Web 支持的 servlet-3.1 -->
  </featureManager>
  ```

此设置由 [IBM WebSphere Liberty](https://www.ibm.com/docs/en/was-liberty/base?topic=liberty-overview) 支持，确保与 Spring Boot 应用程序的兼容性。

#### 部署和运行应用程序

要部署，请在 Project Explorer 中右键单击您的项目，选择 "Run As -> Run on Server"，选择您的 Liberty 服务器，然后单击 Finish。Eclipse 会将 WAR 文件部署到 Liberty 服务器，您可以在 Console 视图中监视日志。确保在 server.xml 中正确设置应用程序上下文根（通常在 `<webApplication>` 标签下），以便通过适当的 URL 访问您的应用程序，例如 `http://localhost:9080/yourapp`。

对于调试，请使用 Debug 透视图，根据需要设置断点，利用 Liberty 对远程调试的支持，如 [使用 Eclipse 和 Liberty 进行调试](https://stackoverflow.com/questions/41428156/how-to-debug-web-service-with-eclipse-websphere-liberty) 中所述。

#### 其他注意事项

- **打包选项**：虽然 WAR 是 servlet 容器的标准，但 Open Liberty 也支持 JAR 部署，如 [配置和部署 Spring Boot 到 Open Liberty](https://openliberty.io/docs/latest/deploy-spring-boot.html) 中所示。对于 JAR，请确保应用程序配置为不启动嵌入式服务器，这可能需要额外的 Liberty 功能或配置。
- **Maven 集成**：使用 Maven 进行依赖管理，确保包含 `liberty-maven-plugin` 以实现自动化部署，如 [IBM Liberty Maven 插件](https://github.com/WASdev/ci.maven#liberty-maven-plugin) 中所述。
- **故障排除**：如果出现问题，请检查 Liberty 服务器实例下 `logs` 目录中的服务器日志，并确保 Liberty 版本与 Spring Boot 之间的兼容性，例如 Liberty 8.5.5.9 或更高版本支持可运行 JAR，根据 [Stack Overflow 讨论](https://stackoverflow.com/questions/36132791/how-to-use-websphere-liberty-in-spring-boot-application)。

这种全面的设置确保有效使用 Eclipse 来开发和部署在 IBM Websphere Liberty 上运行的 Spring Boot 应用程序，并利用 Maven 进行构建管理。

#### 表格：部署选项比较

| 部署类型 | 优点                                      | 缺点                                      | 配置说明                          |
|-----------------|-------------------------------------------|-------------------------------------------|----------------------------------------------|
| WAR 文件        | 适用于 servlet 容器的标准，广泛支持 | 需要扩展 `SpringBootServletInitializer` | 在 pom.xml 中设置 `<packaging>war</packaging>`  |
| JAR 文件        | 开发更简单，Open Liberty 支持 | 可能需要额外的 Liberty 功能   | 确保不启动嵌入式服务器，使用 springBoot 功能 |

此表格源自 [Open Liberty 文档](https://openliberty.io/docs/latest/deploy-spring-boot.html)，有助于根据项目需求选择合适的部署策略。

### 关键引用

- [使用 Eclipse 和 Maven 创建 Spring Boot 项目，分步指南](https://www.springboottutorial.com/creating-spring-boot-project-with-eclipse-and-maven)
- [IBM Liberty Developer Tools，用于 Java EE 应用程序的 Eclipse 插件](https://marketplace.eclipse.org/content/ibm-liberty-developer-tools)
- [Open Liberty 文档，部署 Spring Boot 应用程序](https://openliberty.io/docs/latest/deploy-spring-boot.html)
- [Spring Tools，用于 Spring 开发的下一代工具](https://spring.io/tools/)
- [Eclipse 下载，企业级 Java 开发包](https://www.eclipse.org/downloads/packages/release/2024-06/r/eclipse-ide-enterprise-java-and-web-developers)
- [Liberty 和 Eclipse，安装开发环境](https://www.ibm.com/cloud/blog/liberty-and-eclipse-installing-dev-environment-p9)
- [部署 Spring Boot 应用程序，Spring Boot 参考](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment.html#deployment.servlet)
