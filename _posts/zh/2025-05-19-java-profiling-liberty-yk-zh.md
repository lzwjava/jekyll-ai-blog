---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用YourKit Java分析器进行Liberty性能剖析
translated: true
type: note
---

WebSphere Liberty 与 YourKit Java Profiler 的集成相当顺畅，因为 Liberty 本质上也是基于 JVM 的运行时环境。具体集成方式如下：

---

### 1. 集成原理

YourKit Java Profiler 无需 Liberty 专用插件，它通过附加到 Liberty 运行的 JVM 进程来实现分析。一旦附加成功，它便能拦截方法调用、内存分配、线程活动及其他运行时事件。
Liberty 运行在 OpenJ9（或 HotSpot）JVM 上，因此您可以通过在 Liberty 启动时添加 YourKit 代理来启用性能分析。

---

### 2. 附加 YourKit 代理

主要有两种方式：

* **启动时附加（推荐用于服务器）**
  将 YourKit 代理选项添加到 Liberty 的 `jvm.options` 文件中（位于 `<wlp_home>/usr/servers/<server_name>/`）。
  示例：

  ```
  -agentpath:/path/to/yourkit/bin/linux-x86-64/libyjpagent.so=port=10001,listen=all
  ```

  这样可在服务器启动时立即加载分析器代理。

* **按需（动态）附加**
  若 Liberty 已在运行，您可通过 YourKit 图形界面进行附加。它会扫描正在运行的 JVM 并允许您直接连接，无需重启服务器。此方式适用于生产环境调试，但需要具备相应权限（相同用户/JDK 的 tools.jar）。

---

### 3. Liberty 环境下的分析要点

在 Liberty 中进行分析时，建议：

* **按应用包进行过滤**，避免被 Liberty 内部代码干扰
* **使用调用树/热点视图** 分析缓慢的 Servlet、JAX-RS 端点或 CDI Bean
* **监控 JDBC 与线程池**——由于 Liberty 应用常依赖容器管理资源，YourKit 可追踪 JDBC 调用并测量等待时间
* **多应用处理**：若 Liberty 托管多个应用，使用 YourKit 的线程和类过滤器聚焦目标应用

---

### 4. 性能注意事项

* 分析操作必然产生开销。开发环境可使用完整 CPU/内存分析；生产环境建议改用*采样*模式而非插桩模式
* Liberty 的模块化类加载机制可能导致类名重复，YourKit 通常能处理此情况，但过滤时仍需注意
* 若使用 IBM JDK 运行 Liberty，请确保下载适用于 IBM J9/OpenJ9 的 YourKit 代理（而非仅限 HotSpot 版本）

---

### 5. 典型工作流程

1. 在开发机安装 YourKit
2. 修改 Liberty 的 `jvm.options` 文件配置代理路径
3. 启动 Liberty
4. 通过 YourKit 图形界面连接到 Liberty JVM（通过套接字或附加方式）
5. 分析端点性能、内存使用或线程锁情况
6. 保存快照用于离线分析

---

👉 是否需要为您提供 **OpenJ9**（Liberty 默认 JVM）与 YourKit 的**分步配置示例**？包含针对 CPU 与内存分析的 `jvm.options` 配置样本？
