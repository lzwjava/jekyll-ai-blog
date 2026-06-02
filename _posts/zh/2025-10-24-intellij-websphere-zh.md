---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: IntelliJ IDEA WebSphere 开发指南
translated: true
type: note
---

### 使用 IntelliJ IDEA 进行 IBM WebSphere Application Server (WAS) 开发

IntelliJ IDEA 是开发面向 IBM WebSphere Application Server (WAS) 的 Java EE 应用程序的可靠选择。它支持 WAS 遵循的 Java EE 标准，并提供了出色的工具用于构建、部署和调试企业级应用程序。虽然 Eclipse 通过 IBM 工具具有更多原生 WAS 集成功能，但 IntelliJ 经过适当配置后也能良好工作。下面我将介绍基础知识、远程调试（是的，你可以附加到 WAS JVM）以及其他技巧。

#### 1. 在 IntelliJ 中设置 WAS 开发环境
- **安装必要插件**：
  - 进入 **文件 > 设置 > 插件**，在 JetBrains 市场中搜索 "WebSphere Server"。安装该插件以获得更好的本地服务器管理功能（例如从 IntelliJ 启动/停止 WAS）。此插件非捆绑提供，属于可选但推荐用于本地开发。
  - 确保已启用 Java EE 和 Jakarta EE 插件（通常已预安装）。

- **创建项目**：
  - 新建 **Java 企业版** 项目（或导入现有项目）。
  - 选择 **Web 应用程序** 原型，并配置为 Java EE（例如根据你的 WAS 版本如 9.x 选择版本 8 或 9）。
  - 如需 WAS 特定库，请添加依赖（例如通过 Maven/Gradle：用于 JSP 支持的 `com.ibm.websphere.appserver.api:jsp-2.3`）。

- **配置本地 WAS 服务器（可选，用于本地运行）**：
  - 进入 **运行 > 编辑配置 > + > WebSphere Server > 本地**。
  - 指向你的本地 WAS 安装目录（例如 `/opt/IBM/WebSphere/AppServer`）。
  - 设置服务器名称、JRE（如果 WAS 捆绑了 IBM JDK 则使用它）和部署选项（例如用于热重载的展开式 WAR）。
  - 对于部署：在 **部署** 选项卡中，添加你的构件（例如 WAR 文件）并设置上下文路径。

此设置允许你直接从 IntelliJ 运行/部署以进行本地测试。

#### 2. 远程调试：将 IntelliJ 附加到 WAS JVM
是的，你完全可以将 IntelliJ 调试器附加到远程 WAS JVM。这是通过 JDWP（Java 调试线协议）进行的标准 Java 远程调试。它适用于本地和远程 WAS 实例——将服务器视为“远程 JVM”。

**步骤 1：在 WAS 服务器上启用调试**
- **通过管理控制台（推荐用于类生产环境设置）**：
  - 登录 WAS 管理控制台（例如 `https://your-host:9043/ibm/console`）。
  - 导航至 **服务器 > 服务器类型 > WebSphere Application Servers > [你的服务器] > 调试服务**。
  - 勾选 **在服务器启动时启用服务**。
  - 设置 **JVM 调试端口**（默认为 7777；选择未使用的端口如 8000 以避免冲突）。
  - 保存并重启服务器。

- **通过 server.xml（用于独立或快速编辑）**：
  - 编辑 `$WAS_HOME/profiles/[配置文件]/config/cells/[单元]/nodes/[节点]/servers/[服务器]/server.xml`。
  - 在 `<processDefinitions>` 下的 `<jvmEntries>` 部分，添加或更新：
    ```
    <jvmEntries xmi:id="..." debugMode="true">
      <debugArgs>-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000</debugArgs>
    </jvmEntries>
    ```
    - `suspend=n` 正常启动服务器（使用 `suspend=y` 可在启动时暂停）。
    - 将 `8000` 替换为你的端口。
  - 保存，然后重启服务器：`./startServer.sh [服务器名称]`（或通过控制台）。

- 验证：检查服务器日志中是否有 "JDWP: transport=dt_socket, address=*:8000" 或类似内容。

**步骤 2：在 IntelliJ 中配置远程调试**
- 进入 **运行 > 编辑配置 > + > 远程 JVM 调试**。
- 为其命名（例如 "WAS 远程调试"）。
- 将 **调试器模式** 设置为 "附加到远程 JVM"。
- **主机**：你的 WAS 服务器 IP/主机名（例如本地用 `localhost`，远程用 `192.168.1.100`）。
- **端口**：JVM 调试端口（例如 8000）。
- 可选地，如果你的项目有特定库，设置 **使用模块类路径**。
- 应用并关闭。

**步骤 3：附加并调试**
- 在代码中设置断点（例如在 servlet 或 EJB 中）。
- 将你的应用程序部署到 WAS（通过管理控制台或 wsadmin 脚本手动部署）。
- 运行调试配置（**运行 > 调试 'WAS 远程调试'**）。
- 触发你的应用程序（例如通过 HTTP 请求）。IntelliJ 将附加，执行将在断点处暂停。
- 常见问题：防火墙阻塞端口、JDK 版本不匹配（在 IntelliJ 中使用 WAS 的 IBM JDK）或配置更改后服务器未重启。

这适用于 WAS 7+（包括 Liberty 版本）。对于远程服务器，确保网络可访问调试端口。

#### 3. 高效 WAS 开发的其他技巧
- **热部署/热交换**：为了更快迭代，以“展开式”WAR（解压的）形式部署。WAS 支持 JSP 和某些类的热重载，但对于完整热交换（无需重启的代码更改），请使用 JRebel 插件（付费）或 DCEVM + HotSwapAgent（免费，但需测试与 WAS 的 IBM JDK 的兼容性）。

- **构建工具**：使用 Maven 或 Gradle 管理依赖。将 WAS 运行时库添加为 provided 范围以避免类路径臃肿：
  ```
  <dependency>
    <groupId>com.ibm.websphere.appserver.runtime</groupId>
    <artifactId>shared</artifactId>
    <version>9.0.5</version>
    <scope>provided</scope>
  </dependency>
  ```
  运行 `mvn clean package` 并通过管理控制台部署 WAR。

- **日志记录和分析**：集成 SLF4J/Logback 用于应用程序日志。对于性能分析，使用 VisualVM 或 YourKit（像调试一样远程附加）。WAS 的 PMI（性能监控基础设施）很棒——在管理控制台中启用它以获取指标。

- **测试**：使用 Arquillian 针对远程 WAS 进行集成测试。或者嵌入 Open Liberty（WAS 兼容）用于本地单元测试而无需完整 WAS。

- **版本特定说明**：对于 WAS 9.x+，利用 IntelliJ 中的 Jakarta EE 迁移工具。如果使用 WAS Liberty（以微配置文件为中心），Liberty Tools 插件会添加具有自动重载功能的开发模式。

- **常见陷阱**：
  - 类路径问题：确保 IntelliJ 的项目 SDK 与 WAS 的 JDK 匹配。
  - 安全性：远程调试会暴露端口——仅在开发/受信任网络中使用。
  - 插件限制：WebSphere 插件功能基础；对于高级功能，考虑 IBM 的 Rational Application Developer（但因其 UX 而坚持使用 IntelliJ）。

这应该能让你顺利上手。如果你使用的是特定 WAS 版本，请分享详细信息以获得更有针对性的建议。

#### 参考资料
- [运行/调试配置：WebSphere Server | IntelliJ IDEA](https://www.jetbrains.com/help/idea/run-debug-configuration-websphere-server.html)
- [在 IntelliJ Idea 中配置 WebSphere 远程服务器调试](https://stackoverflow.com/questions/33013860/websphere-remote-server-debug-configuration-in-intellij-idea)
- [使用 Eclipse / Intellij IDEA 调试在 IBM Websphere 上运行的代码](https://davanum.wordpress.com/2009/11/20/debug-code-running-on-ibm-websphere-using-eclipse-intellij-idea/)
- [调试应用程序 - IBM](https://www.ibm.com/docs/en/was/9.0.5?topic=applications-debugging)
- [使用 IntelliJ IDEA 进行远程调试 | Baeldung](https://www.baeldung.com/intellij-remote-debugging)
