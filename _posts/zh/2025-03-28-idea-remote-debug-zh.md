---
audio: false
generated: true
lang: zh
layout: post
title: IntelliJ IDEA 内置远程调试功能
translated: true
type: note
---

要将 IntelliJ IDEA 连接到通过 `server debug default` 启动的 WebSphere Liberty 服务器的调试端口（无需使用 WebSphere Liberty 插件），您可以利用 IntelliJ IDEA 内置的远程调试功能。此方法之所以有效，是因为 WebSphere Liberty 在调试模式下启动时会暴露一个调试端口（默认为 7777），任何 JVM 调试器（包括 IntelliJ IDEA）都可以附加到该端口。以下是实现此目标的详细步骤：

---

### 步骤 1：在调试模式下启动 WebSphere Liberty 服务器
当您运行 `server debug default`（假设 "default" 是您的服务器名称；如果不同，请替换为实际的服务器名称）时，WebSphere Liberty 会启用调试功能启动。默认情况下，此命令将服务器配置为在端口 **7777** 上监听调试连接。

- **命令**：
  ```bash
  server debug default
  ```
- **作用**：此命令在调试模式下启动 "default" 服务器，自动启用 JVM 调试选项（例如 `-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=7777`）。
- **验证**：运行命令后，检查服务器控制台输出或日志（例如 `messages.log`），确认服务器正在调试端口上监听。查找指示调试端口的消息（通常为 7777，除非被覆盖或不可用）。

---

### 步骤 2：确认调试端口
WebSphere Liberty 的默认调试端口是 **7777**。但如果该端口已被使用或已自定义：
- 检查服务器启动后的控制台输出。可能会显示类似“正在端口 7777 上监听调试器连接”的消息。
- 如果端口不同（例如，由于冲突分配了随机端口），请记下实际端口号以在 IntelliJ IDEA 中使用。

在本指南中，除非您的设置另有指示，否则我们将假设默认端口为 **7777**。

---

### 步骤 3：在 IntelliJ IDEA 中配置远程调试
IntelliJ IDEA 的远程调试功能允许您连接到服务器的 JVM，而无需特定的 WebSphere 插件。以下是设置方法：

1. **打开运行/调试配置**：
   - 在 IntelliJ IDEA 中，转到顶部菜单并选择 **运行 > 编辑配置**。

2. **添加新的远程调试配置**：
   - 点击左上角的 **+** 按钮（或“添加新配置”）。
   - 从列表中选择 **Remote JVM Debug**（根据您的 IntelliJ 版本，可能仅显示“Remote”）。

3. **设置配置详细信息**：
   - **名称**：指定一个有意义的名称，例如“WebSphere Liberty Debug”。
   - **主机**：设置为 `localhost`（假设服务器与 IntelliJ IDEA 在同一台机器上运行；如果是远程服务器，请使用服务器的 IP 地址）。
   - **端口**：设置为 `7777`（如果调试端口不同，则使用实际端口）。
   - **传输**：确保设置为 **Socket**。
   - **调试器模式**：选择 **Attach**（这会告诉 IntelliJ 连接到已运行的 JVM）。
   - 除非需要特定的 JVM 选项，否则保留其他设置（如“远程 JVM 的命令行参数”）为默认值。

4. **保存配置**：
   - 点击 **应用**，然后点击 **确定** 保存。

---

### 步骤 4：开始调试
在服务器以调试模式运行且配置设置完成后：
- 转到 **运行 > 调试**（或点击调试图标）并选择您的新配置（例如“WebSphere Liberty Debug”）。
- IntelliJ IDEA 将尝试附加到指定主机和端口上的服务器 JVM。
- 如果成功，您将在调试窗口中看到类似“已连接到目标 VM，地址：'localhost:7777'”的消息。

---

### 步骤 5：调试您的应用程序
- **设置断点**：在源代码中，点击行号旁边的装订线以在希望执行暂停的位置添加断点。
- **触发执行**：与您的应用程序交互（例如，向服务器发送请求）以命中断点。
- **调试**：一旦断点被命中，使用 IntelliJ 的调试工具（单步跳过、单步进入、恢复等）来检查变量并控制执行。

---

### 附加说明
- **本地与远程服务器**：如果 WebSphere Liberty 在不同的机器上运行，请在远程调试配置中将 `localhost` 替换为服务器的 IP 地址。确保调试端口（例如 7777）是开放的且未被防火墙阻止。
- **端口冲突**：如果服务器启动时端口 7777 不可用，WebSphere Liberty 可能会选择一个随机端口。检查服务器输出以确认端口，并相应更新 IntelliJ 配置。
- **无需插件**：此方法使用 IntelliJ IDEA 的标准远程调试功能，因此不需要 WebSphere Liberty 插件。

---

### 总结
通过使用 `server debug default` 启动您的 WebSphere Liberty 服务器（默认在端口 7777 上启用调试）并在 IntelliJ IDEA 中配置远程调试设置，您可以在没有 WebSphere Liberty 插件的情况下连接到服务器的调试端口。这使您能够在 IntelliJ IDEA 中直接获得完整的调试功能——断点、变量检查和逐步执行。

---

在没有专用 Liberty Tools 插件的情况下，在 IntelliJ IDEA 中运行和调试 WebSphere Liberty 应用程序，可以通过手动设置 Liberty 运行时并为 IntelliJ IDEA 配置远程调试和外部工具执行来实现。与使用集成插件相比，这种方法需要一些手动步骤，但它提供了开发和排查 Liberty 应用程序问题所需的功能。

以下是该过程的分解：

**1. 获取并安装 WebSphere Liberty 运行时：**

由于没有插件为您管理运行时，您需要手动下载并安装 WebSphere Liberty 运行时。您可以从 IBM 官方网站获取运行时，或者如果您使用 Maven 或 Gradle 管理项目，也可以通过这些工具的其他分发方法获取。

通常，手动安装涉及下载 ZIP 或 JAR 文件并将其解压缩到系统上的某个目录。该目录将成为您的 Liberty 安装主目录（`<LIBERTY_HOME>`）。

**2. 为调试配置 Liberty 服务器：**

要调试您的应用程序，您需要启用调试功能启动 Liberty 服务器。这通过在服务器启动时添加特定的 JVM 选项来实现。这些选项告诉 Java 虚拟机（JVM）在特定端口上监听调试器连接。

在您的 Liberty 服务器配置目录（`<LIBERTY_HOME>/usr/servers/<your_server_name>/`）中找到 `jvm.options` 文件。如果此文件不存在，您可以创建它。将以下行添加到 `jvm.options` 文件中：

```
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005
```

  * `-agentlib:jdwp`：加载 Java 调试线协议（JDWP）库。
  * `transport=dt_socket`：指定调试器将使用套接字连接。
  * `server=y`：指示 JVM 将作为服务器，监听调试器连接。
  * `suspend=n`：指定 JVM 在启动前不应等待调试器连接。如果您需要调试在服务器启动期间运行的代码，可以将其更改为 `suspend=y`。
  * `address=5005`：设置调试器将连接的端口号。您可以将其更改为任何可用端口。

**3. 配置 IntelliJ IDEA 以运行 Liberty：**

您可以使用 IntelliJ IDEA 的“外部工具”配置从 IDE 内部启动您的 Liberty 服务器。

  * 转到 `文件` > `设置`（或在 macOS 上为 `IntelliJ IDEA` > `偏好设置`）。
  * 导航到 `工具` > `外部工具`。
  * 点击 `+` 图标添加新的外部工具。
  * 使用以下详细信息配置该工具：
      * **名称**：指定一个描述性名称，例如“启动 Liberty 服务器”。
      * **程序**：浏览到 Liberty 服务器脚本。通常在 Linux/macOS 上为 `<LIBERTY_HOME>/bin/server`，在 Windows 上为 `<LIBERTY_HOME>\bin\server.bat`。
      * **参数**：添加启动特定服务器实例的参数。通常是 `start <your_server_name>`，其中 `<your_server_name>` 是 `<LIBERTY_HOME>/usr/servers/` 中您的服务器目录的名称。
      * **工作目录**：将其设置为 `<LIBERTY_HOME>/bin`。

现在，您可以通过转到 `工具` > `外部工具` 并选择您刚刚配置的工具来启动 Liberty 服务器。

**4. 为远程调试配置 IntelliJ IDEA：**

要调试在手动启动的 Liberty 服务器上运行的应用程序，您将使用 IntelliJ IDEA 的“Remote JVM Debug”配置。

  * 转到 `运行` > `编辑配置`。
  * 点击 `+` 图标并选择 `Remote JVM Debug`。
  * 配置设置：
      * **名称**：指定一个描述性名称，例如“调试 Liberty 服务器”。
      * **调试器模式**：选择 `Attach to remote JVM`。
      * **主机**：输入 `localhost`（如果运行 Liberty 的机器不在本地，则输入其 IP 地址）。
      * **端口**：输入您在 `jvm.options` 文件中配置的端口号（例如 `5005`）。
      * **使用模块类路径**：选择 IntelliJ IDEA 项目中包含您的 Liberty 应用程序代码的模块。这有助于 IntelliJ IDEA 将运行中的代码映射到您的源文件以进行调试。

**5. 运行和调试：**

1.  使用您在 IntelliJ IDEA 中创建的“外部工具”配置启动 Liberty 服务器。
2.  等待服务器启动并指示它正在配置的端口上监听调试器（您应该在服务器控制台输出中看到一条消息）。
3.  在 IntelliJ IDEA 中的应用程序代码内设置断点。
4.  转到 `运行` > `调试` 并选择您创建的“调试 Liberty 服务器”配置。

IntelliJ IDEA 将尝试连接到指定端口上运行的 Liberty 服务器。一旦连接，您就可以使用 IntelliJ IDEA 的所有调试功能，例如逐步执行代码、检查变量和评估表达式。

通过遵循这些步骤，您可以在 IntelliJ IDEA 中有效地运行和调试您的 WebSphere Liberty 应用程序，而无需依赖专用的 Liberty Tools 插件，从而直接控制服务器生命周期和调试过程。
