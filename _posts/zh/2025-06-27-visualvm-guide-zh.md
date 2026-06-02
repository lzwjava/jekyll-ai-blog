---
audio: false
generated: true
lang: zh
layout: post
title: VisualVM全面指南：Java性能分析与监控
translated: true
type: note
---

# VisualVM 全面指南

VisualVM 是一款功能强大的开源 Java 性能分析和监控工具，它提供了图形化界面用于分析 Java 应用程序的性能。该工具随 Java 开发工具包（JDK）一起提供，特别适用于诊断性能问题、内存泄漏和线程相关问题。本指南涵盖 VisualVM 的功能特性、设置安装、使用方法以及面向开发人员和系统管理员的最佳实践。

## 目录
1. [什么是 VisualVM？](#什么是-visualvm)
2. [VisualVM 主要特性](#visualvm-主要特性)
3. [系统要求](#系统要求)
4. [安装 VisualVM](#安装-visualvm)
5. [启动 VisualVM](#启动-visualvm)
6. [连接 Java 应用程序](#连接-java-应用程序)
7. [使用 VisualVM 进行监控和分析](#使用-visualvm-进行监控和分析)
   - [概览选项卡](#概览选项卡)
   - [监控选项卡](#监控选项卡)
   - [线程选项卡](#线程选项卡)
   - [采样器](#采样器)
   - [分析器](#分析器)
   - [堆转储分析](#堆转储分析)
   - [线程转储分析](#线程转储分析)
   - [MBeans](#mbeans)
8. [远程监控](#远程监控)
9. [通过插件扩展 VisualVM](#通过插件扩展-visualvm)
10. [最佳实践](#最佳实践)
11. [常见问题排查](#常见问题排查)
12. [其他资源](#其他资源)

## 什么是 VisualVM？

VisualVM 是一款基于 Java 的工具，它将多个 JDK 实用程序（如 `jstack`、`jmap` 和 `jconsole`）集成到一个单一、用户友好的界面中。它允许开发人员实时监控 Java 应用程序，分析 CPU 和内存使用情况，分析堆转储并管理线程。VisualVM 对于识别本地和远程 Java 应用程序中的性能瓶颈、内存泄漏和线程问题特别有价值。

VisualVM 最初由 Sun Microsystems 开发，现已成为 Oracle JDK 的一部分，并作为一个开源项目积极维护。它支持在 JDK 6 及更高版本上运行的 Java 应用程序。

## VisualVM 主要特性

- **实时监控**：跟踪 CPU 使用率、内存消耗、线程活动和垃圾回收。
- **性能分析**：提供 CPU 和内存分析，以识别性能瓶颈和内存分配模式。
- **堆转储分析**：允许检查内存内容以诊断内存泄漏。
- **线程转储分析**：帮助分析线程状态并检测死锁。
- **MBean 管理**：提供对 Java 管理扩展（JMX）的访问，用于监控和管理应用程序。
- **远程监控**：支持监控在远程机器上运行的 Java 应用程序。
- **可扩展性**：支持插件以扩展功能，例如与特定框架集成或附加分析工具。
- **轻量级且易于使用**：设置简单，具有直观的图形界面。

## 系统要求

使用 VisualVM 需确保满足以下条件：
- **操作系统**：Windows、macOS、Linux 或任何支持 JVM 的操作系统。
- **Java 版本**：JDK 6 或更高版本（VisualVM 随 JDK 8 及更高版本捆绑提供）。
- **内存**：至少 512 MB 空闲 RAM 用于轻量级监控；1 GB 或更多用于堆转储分析。
- **磁盘空间**：约 50 MB 用于 VisualVM 安装。
- **权限**：某些功能可能需要管理员权限（例如，访问系统进程）。

## 安装 VisualVM

VisualVM 包含在 Oracle JDK 8 及更高版本中，位于 JDK 安装目录的 `bin` 目录下（`jvisualvm` 可执行文件）。或者，您也可以将其作为独立应用程序下载：

1. **从 JDK 获取**：
   - 如果您安装了 JDK 8 或更高版本，VisualVM 已位于 `JAVA_HOME/bin` 目录中，名为 `jvisualvm`。
   - 运行 `jvisualvm` 可执行文件以启动该工具。

2. **独立下载**：
   - 访问 [VisualVM 网站](https://visualvm.github.io/) 下载最新的独立版本。
   - 将 ZIP 文件解压缩到您选择的目录。
   - 运行 `visualvm` 可执行文件（例如，在 Windows 上为 `visualvm.exe`）。

3. **验证安装**：
   - 确保 `JRE_HOME` 或 `JAVA_HOME` 环境变量指向兼容的 JDK/JRE。
   - 通过启动 VisualVM 进行测试。

## 启动 VisualVM

启动 VisualVM：
- **在 Windows 上**：双击 JDK 的 `bin` 文件夹或独立安装目录中的 `jvisualvm.exe`。
- **在 macOS/Linux 上**：在终端中运行 `bin` 目录下的 `./jvisualvm`。
- VisualVM 界面将打开，在左侧面板显示本地 Java 应用程序列表。

## 连接 Java 应用程序

VisualVM 可以监控本地和远程的 Java 应用程序。

### 本地应用程序
- 启动后，VisualVM 会自动检测本地机器上运行的 Java 应用程序。
- 双击左侧面板中的应用程序以打开其监控仪表板。
- 如果某个应用程序未列出，请确保它正在兼容的 JVM 下运行。

### 远程应用程序
要监控远程 Java 应用程序：
1. 通过添加 JVM 参数（例如 `-Dcom.sun.management.jmxremote`）在远程应用程序上启用 JMX。
2. 在 VisualVM 中，转到 **文件 > 添加 JMX 连接**。
3. 输入远程主机的 IP 地址和端口（例如 `主机名:端口`）。
4. 如果启用了身份验证，请提供凭据。
5. 连接并监控应用程序。

**注意**：对于安全连接，请根据需要配置 SSL 和身份验证（参见[远程监控](#远程监控)）。

## 使用 VisualVM 进行监控和分析

VisualVM 提供了多个选项卡和工具来分析 Java 应用程序。以下是每个功能的详细说明。

### 概览选项卡
- 显示有关应用程序的一般信息，包括：
  - JVM 参数
  - 系统属性
  - 应用程序类路径
  - PID（进程 ID）
- 用于验证应用程序的配置。

### 监控选项卡
- 提供以下内容的实时图表：
  - **CPU 使用率**：跟踪应用程序和系统的 CPU 使用率。
  - **堆内存**：监控堆使用情况（Eden、老年代、永久代/元空间）和垃圾回收活动。
  - **类**：显示已加载类的数量。
  - **线程**：显示活动线程和守护线程的数量。
- 允许手动触发垃圾回收或堆转储。

### 线程选项卡
- 可视化线程状态（运行中、休眠、等待等）随时间的变化。
- 提供线程转储功能以捕获所有线程的当前状态。
- 有助于识别死锁、阻塞线程或过度使用线程。

### 采样器
- 提供轻量级的 CPU 和内存采样以进行性能分析。
- **CPU 采样**：
  - 捕获方法级别的执行时间。
  - 识别消耗最多 CPU 时间的热点方法。
- **内存采样**：
  - 跟踪对象分配和内存使用情况。
  - 帮助识别消耗过多内存的对象。
- 采样比性能分析的开销更低，但提供的数据详细程度较低。

### 分析器
- 提供深入的 CPU 和内存分析。
- **CPU 分析**：
  - 测量方法的执行时间。
  - 在方法级别识别性能瓶颈。
- **内存分析**：
  - 跟踪对象分配和引用。
  - 通过识别意外持久存在的对象来帮助检测内存泄漏。
- **注意**：性能分析比采样的开销更高，可能会减慢应用程序速度。

### 堆转储分析
- 堆转储是应用程序内存的快照。
- 生成堆转储：
  1. 转到 **监控** 选项卡。
  2. 点击 **堆转储**。
  3. 将转储保存到 `.hprof` 文件或直接在 VisualVM 中分析。
- 功能：
  - 查看类实例、大小和引用。
  - 识别内存使用量高的对象。
  - 通过分析对象保留路径检测内存泄漏。
- 使用 **OQL（对象查询语言）** 控制台进行高级堆查询。

### 线程转储分析
- 捕获特定时刻所有线程的状态。
- 生成线程转储：
  1. 转到 **线程** 选项卡。
  2. 点击 **线程转储**。
  3. 在 VisualVM 中分析转储或导出以供外部工具使用。
- 有助于诊断：
  - 死锁
  - 阻塞线程
  - 线程争用问题

### MBeans
- 访问 JMX MBeans 以管理和监控应用程序。
- 功能：
  - 查看和修改 MBean 属性。
  - 调用 MBean 操作。
  - 监控 MBean 通知。
- 对于具有自定义 JMX 检测的应用程序非常有用。

## 远程监控

要监控远程 Java 应用程序：
1. **配置远程 JVM**：
   - 将以下 JVM 参数添加到远程应用程序：
     ```bash
     -Dcom.sun.management.jmxremote
     -Dcom.sun.management.jmxremote.port=<端口>
     -Dcom.sun.management.jmxremote.ssl=false
     -Dcom.sun.management.jmxremote.authenticate=false
     ```
   - 对于安全连接，启用 SSL 和身份验证：
     ```bash
     -Dcom.sun.management.jmxremote.ssl=true
     -Dcom.sun.management.jmxremote.authenticate=true
     -Dcom.sun.management.jmxremote.password.file=<密码文件>
     ```
2. **设置 VisualVM**：
   - 在 VisualVM 中使用远程主机的 IP 和端口添加 JMX 连接。
   - 如果需要，请提供凭据。
3. **防火墙配置**：
   - 确保 JMX 端口在远程主机上开放。
   - 如果需要，使用 SSH 隧道进行安全的远程访问：
     ```bash
     ssh -L <本地端口>:<远程主机>:<远程端口> 用户@远程主机
     ```

## 通过插件扩展 VisualVM

VisualVM 支持插件以增强其功能：
1. **安装插件**：
   - 转到 **工具 > 插件**。
   - 在插件中心浏览可用插件（例如，Visual GC、BTrace、JConsole 插件）。
   - 安装并重新启动 VisualVM。
2. **常用插件**：
   - **Visual GC**：可视化垃圾回收活动。
   - **BTrace**：为 Java 应用程序提供动态跟踪。
   - **JConsole 插件**：添加 JConsole 兼容功能。
3. **自定义插件**：
   - 从 VisualVM 网站或第三方来源下载插件。
   - 将插件文件放入 `plugins` 目录并重新启动 VisualVM。

## 最佳实践

- **从采样开始**：在进行性能分析之前使用采样，以最小化性能影响。
- **限制分析范围**：分析特定的包或类以减少开销。
- **定期堆转储**：为长时间运行的应用程序安排定期堆转储，以跟踪内存趋势。
- **监控垃圾回收**：使用 Visual GC 插件分析 GC 性能。
- **保护远程连接**：始终对远程监控使用 SSL 和身份验证。
- **保存快照**：保存堆和线程转储以供后续分析或协作。
- **使用 OQL 进行高级分析**：学习 OQL 以进行高效的堆转储查询。
- **监控资源使用情况**：确保 VisualVM 有足够的内存来处理大型堆转储。

## 常见问题排查

- **未检测到应用程序**：
  - 确保应用程序在兼容的 JVM 上运行。
  - 检查 JVM 是否配置为允许 JMX 连接。
- **性能分析期间开销过高**：
  - 切换到采样以降低开销。
  - 分析特定的类或方法。
- **远程监控连接问题**：
  - 验证 JMX 端口和防火墙设置。
  - 使用 `telnet <主机> <端口>` 测试连接性。
- **VisualVM 中出现 OutOfMemoryError**：
  - 通过编辑 `visualvm.conf` 文件增加 VisualVM 的堆大小：
    ```bash
    -J-Xmx<内存大小>m
    ```
- **堆转储分析缓慢**：
  - 使用具有更多 RAM 的机器。
  - 过滤类以缩小分析范围。

## 其他资源

- **官方网站**：[visualvm.github.io](https://visualvm.github.io/)
- **文档**：[VisualVM 文档](https://visualvm.github.io/documentation.html)
- **教程**：
  - Oracle 的 [VisualVM 指南](https://www.oracle.com/java/technologies/visualvm.html)
  - [使用 VisualVM 进行 Java 性能调优](https://www.baeldung.com/java-visualvm)
- **社区**：
  - [VisualVM GitHub Issues](https://github.com/visualvm/visualvm.github.io/issues)
  - [Stack Overflow VisualVM 标签](https://stackoverflow.com/questions/tagged/visualvm)
