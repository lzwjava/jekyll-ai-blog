---
audio: false
generated: true
lang: zh
layout: post
title: 在Windows上将YourKit性能分析工具集成至WebSphere Liberty
translated: true
type: note
---

在 Windows 系统上将 YourKit Java Profiler 与 WebSphere Liberty Server 结合使用，需要将 YourKit 代理集成到 WebSphere Liberty JVM 中并进行性能分析配置。以下是基于现有信息和 YourKit 与 WebSphere Liberty 集成最佳实践的设置步骤：

### 前置条件
- **YourKit Java Profiler**：在 Windows 计算机上完成安装。请从 [YourKit 官网](https://www.yourkit.com/) 下载并确保拥有有效的许可证或试用密钥。
- **WebSphere Liberty**：在 Windows 系统上完成安装并处于运行状态。确保对服务器配置文件拥有管理访问权限。
- **Java JDK**：WebSphere Liberty 使用 Java 运行时（IBM JDK 或 OpenJDK）。请确认 JDK 版本与 YourKit 兼容（YourKit 支持 Java 5 及更高版本，但请验证与您特定版本的兼容性）。
- **管理权限**：修改 WebSphere Liberty 配置文件需要管理权限。

### 分步指南

1. **安装 YourKit Java Profiler**
   - 从 [YourKit 官网](https://www.yourkit.com/download) 下载并安装 Windows 版 YourKit Java Profiler。
   - 记录安装目录，后续需要用到 YourKit 代理库路径（`yjpagent.dll`）。

2. **定位 YourKit 代理**
   - Windows 系统的 YourKit 代理通常位于：
     ```
     C:\Program Files\YourKit-Java-Profiler-<版本>\bin\win64\yjpagent.dll
     ```
     （如果运行的是 32 位 JVM，请使用 `win32` 替代 `win64`。）
   - 确保代理与 WebSphere Liberty 使用的 JVM 架构（32 位或 64 位）匹配。

3. **配置 WebSphere Liberty 使用 YourKit 代理**
   - **定位 `jvm.options` 文件**：
     - 导航至 WebSphere Liberty 服务器的配置目录，通常位于：
       ```
       <LIBERTY_INSTALL_DIR>\usr\servers\<服务器名称>\jvm.options
       ```
       请将 `<LIBERTY_INSTALL_DIR>` 替换为 WebSphere Liberty 安装路径（例如 `C:\wlp`），将 `<服务器名称>` 替换为您的服务器名称（例如 `defaultServer`）。
     - 如果 `jvm.options` 文件不存在，请在服务器目录中创建该文件。
   - **添加 YourKit 代理路径**：
     - 使用文本编辑器以管理权限打开 `jvm.options`。
     - 添加以下行以包含 YourKit 代理：
       ```
       -agentpath:C:\Program Files\YourKit-Java-Profiler-<版本>\bin\win64\yjpagent.dll=disablestacktelemetry,disableexceptiontelemetry,delay=10000,probe_disable=*,sessionname=WebSphereLiberty
       ```
       - 将 `<版本>` 替换为您的 YourKit 版本（例如 `2023.9`）。
       - 选项（`disablestacktelemetry`、`disableexceptiontelemetry`、`probe_disable=*`）通过禁用不必要的遥测来减少开销。`delay=10000` 确保代理在服务器初始化后启动，`sessionname=WebSphereLiberty` 用于标识分析会话。
       - 示例：
         ```
         -agentpath:C:\Program Files\YourKit-Java-Profiler-2023.9\bin\win64\yjpagent.dll=disablestacktelemetry,disableexceptiontelemetry,delay=10000,probe_disable=*,sessionname=WebSphereLiberty
         ```
   - **保存文件**：确保对 `jvm.options` 文件拥有写入权限。

4. **验证 JVM 兼容性**
   - WebSphere Liberty 通常使用 IBM JDK 或 OpenJDK。YourKit 与两者兼容，但如果遇到问题（例如某些 IBM JDK 案例中出现的 `NoSuchMethodError`），请在代理路径中添加 `probe_disable=*` 以禁用可能导致与 IBM JDK 冲突的探测。[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=8042)
   - 检查 Liberty 使用的 Java 版本：
     ```
     <LIBERTY_INSTALL_DIR>\java\bin\java -version
     ```
     确保 YourKit 支持该版本（旧版本支持 Java 5 或更高版本；现代版本支持 Java 8+）。

5. **启动 WebSphere Liberty**
   - 照常启动 WebSphere Liberty 服务器：
     ```
     <LIBERTY_INSTALL_DIR>\bin\server start <服务器名称>
     ```
     示例：
     ```
     C:\wlp\bin\server start defaultServer
     ```
   - 检查服务器日志（`<LIBERTY_INSTALL_DIR>\usr\servers\<服务器名称>\logs\console.log` 或 `messages.log`）中是否存在与 YourKit 代理相关的错误。
   - 在以下位置查找 YourKit 代理日志：
     ```
     %USERPROFILE%\.yjp\log\<会话名称>-<进程ID>.log
     ```
     示例：
     ```
     C:\Users\<您的用户名>\.yjp\log\WebSphereLiberty-<进程ID>.log
     ```
     日志应显示代理已加载并在端口上监听（默认：10001）：
     ```
     Profiler agent is listening on port 10001
     ```

6. **连接 YourKit Profiler 界面**
   - 在 Windows 计算机上启动 YourKit Java Profiler 界面。
   - 在 YourKit 界面中，选择 **Profile | Profile Local Java Server or Application** 或 **Profile | Profile Remote Java Server or Application**。
     - 对于本地分析（由于 YourKit 和 Liberty 位于同一台计算机），选择 **Profile Local Java Server or Application**。
     - 界面应自动检测到 WebSphere Liberty 进程（通过 `sessionname=WebSphereLiberty` 标识）。
   - 如果未自动检测到，请使用 **Profile Remote Java Server or Application**，选择 **Direct Connect**，并输入：
     - **主机**：`localhost`
     - **端口**：`10001`（或代理日志中指定的端口）。
   - 连接到服务器。界面将显示 CPU、内存和线程遥测数据。

7. **分析应用程序**
   - 使用 YourKit 界面进行以下操作：
     - **CPU 分析**：启用 CPU 采样或跟踪以识别性能瓶颈。为避免高负载系统开销过大，请勿启用 "Profile J2EE"。[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)
     - **内存分析**：通过按 Web 应用程序分组对象来分析堆使用情况并检测内存泄漏（适用于 Liberty 托管的应用程序）。[](https://www.yourkit.com/docs/java-profiler/latest/help/webapps.jsp)
     - **线程分析**：在 "Threads" 选项卡中检查死锁或冻结线程。[](https://www.yourkit.com/changes/)
   - 如需离线分析，可拍摄快照（文件 | 保存快照）。
   - 监控内存使用情况，因为分析可能会增加内存消耗。避免在无监控的情况下进行长时间分析会话。[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)

8. **故障排除**
   - **服务器无法启动或变得不可访问**：
     - 检查日志（`console.log`、`messages.log` 和 YourKit 代理日志）中是否存在 `OutOfMemoryError` 或 `NoSuchMethodError` 等错误。[](https://www.yourkit.com/forum/viewtopic.php?t=328)[](https://www.yourkit.com/forum/viewtopic.php?t=16205)
     - 确保 `-agentpath` 已添加到正确的 `jvm.options` 文件中，并且与用于启动 Liberty 的脚本匹配。[](https://www.yourkit.com/forum/viewtopic.php?t=16205)
     - 如果使用 IBM JDK，请尝试在代理路径中添加 `probe_disable=*` 以避免冲突。[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=8042)
   - **ClassNotFoundException**：
     - 如果看到 `java.lang.ClassNotFoundException` 等错误（例如对于 `java.util.ServiceLoader`），请确保 YourKit 代理版本与您的 JDK 兼容。对于旧的 IBM JDK（例如 Java 5），请使用 YourKit 8.0 或更早版本。[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=7149)
   - **无分析数据**：
     - 验证 YourKit 代理和界面版本是否匹配。版本不匹配可能导致连接问题。[](https://www.yourkit.com/forum/viewtopic.php?t=328)
     - 确保可通过浏览器访问服务器（例如，如果使用 SSL，则访问 `https://localhost:9443`）。如果无法访问，请检查防火墙设置或 SSL 配置。[](https://www.yourkit.com/forum/viewtopic.php?t=16205)
   - **日志文件问题**：
     - 如果在 `~/.yjp/log/` 中未创建 YourKit 日志，请确保进程对用户主目录拥有写入权限。[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=3219)
   - **性能影响**：
     - 分析可能会影响性能。在类生产环境中，请使用最小设置（例如禁用堆栈遥测）。[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)

9. **可选：使用 YourKit 集成向导**
   - YourKit 提供 Java 服务器集成向导以简化配置：
     - 启动 YourKit 界面并选择 **Profile | Profile Local Java Server or Application**。
     - 从支持的服务器列表中选择 **WebSphere Liberty**（如果未列出 Liberty，则选择 "Other Java application"）。
     - 按照向导生成必要的 `-agentpath` 设置并更新 `jvm.options`。确保对配置文件拥有写入权限。[](https://www.yourkit.com/docs/java-profiler/latest/help/java-server-integration-wizard.jsp)
   - 这对于确保路径和设置正确特别有用。

10. **停止分析**
    - 要禁用分析，请删除或注释掉 `jvm.options` 中的 `-agentpath` 行，然后重启服务器。
    - 或者，停止服务器：
      ```
      <LIBERTY_INSTALL_DIR>\bin\server stop <服务器名称>
      ```

### 补充说明
- **许可证**：服务器上的 YourKit 代理不需要许可证密钥；许可证在 YourKit 界面中应用。如果从另一台 Windows 计算机进行远程分析，请确保界面拥有有效的许可证。[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=11385)[](https://www.yourkit.com/forum/viewtopic.php?t=11385)
- **远程分析**：如果从其他计算机进行分析，请确保网络可连接到代理端口（默认：10001），并使用 **Profile Remote Java Server or Application** 选项，输入服务器的主机名/IP。
- **性能考虑**：分析可能会增加内存和 CPU 使用量。对于生产系统，请从最小分析选项（例如 CPU 采样）开始，并监控服务器运行状况。[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)
- **兼容性**：如果使用旧版 WebSphere Liberty 搭配 IBM JDK 1.4.2 或 1.5，可能需要旧版 YourKit（例如 Java 5 需使用 8.0 版）。[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=7149)[](https://stackoverflow.com/questions/61795/java-profiler-for-ibm-jvm-1-4-2-websphere-6-0-2)
- **文档**：请参考 YourKit 官方文档以获取详细的分析选项：[YourKit Java Profiler 帮助](https://www.yourkit.com/docs/java/help/)。[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)

### 配置示例
以下是示例 `jvm.options` 文件：
```
-Xmx4G
-Xms4G
-agentpath:C:\Program Files\YourKit-Java-Profiler-2023.9\bin\win64\yjpagent.dll=disablestacktelemetry,disableexceptiontelemetry,delay=10000,probe_disable=*,sessionname=WebSphereLiberty
```

### 测试设置
- 启动服务器后，访问您的应用程序（例如 `https://localhost:9443`）以确保其正在运行。
- 在 YourKit 界面中，验证是否显示遥测数据（CPU、内存、线程）。
- 如果出现问题，请检查 YourKit 代理日志和 Liberty 日志中的错误。

如果您遇到具体错误或需要某个步骤的进一步帮助，请告知我，我可以提供进一步协助！
