---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自由代理与JaCoCo代理对比
translated: true
type: note
---

在 WebSphere Liberty (WLP) 中，`ws-javaagent.jar` 是 IBM 自研的 Java 插桩代理。它主要用于运行时监控、诊断以及与应用程序性能管理（APM）、Health Center 或 Liberty 自有监控功能的集成。启用该代理后，Liberty 可自动收集性能分析、垃圾回收、线程及其他 JVM 级别的指标。

而 JaCoCo 的 `jacocoagent.jar` 则专用于**代码覆盖率检测**。其作用是在运行时对字节码进行插桩，使测试运行或应用执行能生成覆盖率数据（例如记录哪些类、方法和分支被执行过）。

两者的核心区别在于：

* **`ws-javaagent.jar`** → 面向 Liberty 及 IBM 工具链的通用监控、性能分析和诊断
* **`jacocoagent.jar`** → 独立于 Liberty 的测试/代码覆盖率报告生成

不应使用 Liberty 代理替代 JaCoCo 代理。若您的目标是**生成测试覆盖率报告**（用于 CI 流水线、SonarQube、Maven/Gradle 报告等），必须继续使用 **JaCoCo 代理**。Liberty 代理无法生成 JaCoCo 的 `.exec` 覆盖率文件。

但如有需要，您可以**同时运行这两个代理**——Java 支持多个 `-javaagent` 参数。例如：

```bash
-javaagent:/path/to/ws-javaagent.jar
-javaagent:/path/to/jacocoagent.jar=destfile=jacoco.exec,output=file
```

👉 简而言之：
使用 **`jacocoagent.jar`** 检测代码覆盖率
使用 **`ws-javaagent.jar`** 实现 Liberty 诊断/性能分析
二者功能不同，不可互相替代。

需要我进一步演示如何在 Liberty 服务器的 JVM 选项文件中同时配置这两个代理吗？
