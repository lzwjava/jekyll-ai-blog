---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2024-2025 Java 后端趋势
translated: true
type: note
---

Question: 后端/Java 领域过去一年的重大新闻、趋势和热门项目是什么？

Answer:

## Java/后端领域的重大新闻、趋势与热门项目（2024–2025）

---

### 1. 🚀 Java 语言演进：JDK 24 & Java 25 LTS

Java 25 作为新的 LTS 版本，奠定了现代基线，提升了可读性、并发性和性能，同时框架标准化要求 Java 17+。

JDK 24/25 的关键语言改进：

- **Stream Gatherers** 已最终确定，支持自定义中间流操作
- **Scoped Values** —— `ThreadLocal` 的现代、内存高效替代品（在 Java 24 中最终确定）
- **Pattern Matching** 扩展支持 `switch` 和 `instanceof` 中的原始类型
- Structured Concurrency 在 Java 25 中进行了全面改进，使更安全的并发代码组合更接近最终确定

---

### 2. 🔀 Project Loom & Virtual Threads —— 数十年来最大的并发变革

Virtual threads 在 JDK 21 中成为永久特性，被视为近年来 Java 平台最令人兴奋的添加之一。

这一故事在 2024–2025 年继续强劲发展：

- Java 21 中存在的线程“pinning”问题——执行 synchronized 块的 virtual threads 会绑定到 carrier threads 并丧失其优势——已在 Java 24+ 中通过改进的 JVM 插桩得到解决。
- Project Loom 在 2024 年完成了 virtual threads 的工作，包括与 object monitors 的交互，消除了采用的主要障碍，结果在 JDK 24 中可见。
- Virtual threads 是 JVM 管理的轻量级线程——现在可以创建数百万个——它们减少或消除了针对 I/O 密集型工作负载使用复杂响应式框架（如 Reactor 或 RxJava）的需求。

---

### 3. 🤖 JVM 上的 AI —— 2025 年最热门趋势

Java 正在迅速成为严肃的 AI 平台：

**Spring AI 1.0 GA（2025 年 5 月）**
Spring AI 1.0 GA 带来了企业级功能，包括用于文档摄取的 ETL 框架（S3 到 MongoDB）、通过 Spring Boot Actuator 的全面可观测性，以及针对长对话的内存管理功能。它支持所有主要 AI 提供商——Anthropic、OpenAI、Microsoft、Amazon、Google 和 Ollama——并将 AI 响应直接映射到 POJO 的结构化输出。

**LangChain4j 1.0（2025 年 5 月）**
LangChain4j 作为一个对 Java 开发者感觉原生的框架构建，拥抱 Java 习惯用法，如强类型、注解驱动编程和编译时检查。它在广泛的 beta 测试后于 2025 年 5 月稳定为 1.0 版本。到 2025 年，它将多模态模型和代理式多代理架构作为一流模式支持。

**新型 Agent 框架**
Embabel Agent Framework 和 Koog —— 分别由 Spring Framework 创始人 Rod Johnson 和 JetBrains 创建 —— 是 2025 年 Q2 引入的新的 JVM 开源代理平台，专为开发者构建和运行 AI 代理而设计。

**MCP Java SDK**
于 2024 年 12 月引入的 MCP Java SDK 使 Java 应用能够通过标准化接口与 AI 模型和工具交互，支持同步和异步通信模式。

---

### 4. 🌱 Spring Boot 4 & Spring Framework 7

Spring Boot 4 和 Spring Framework 7 于 2025 年 11 月发布，提供了 API 版本控制、弹性和来自 JSpecify 的空安全注解，同时改进了云兼容性、可观测性和 native image 支持。

Spring 团队现在正式推荐使用 Virtual Threads，整个 Spring 生态系统现在要求最低基线为 Java 17+。

---

### 5. ⚡ GraalVM Native Image & 云原生 Java

GraalVM 允许将 Java 应用预编译成 native 二进制文件，类似于 C/C++ 应用，从而实现更快的启动时间和更低的内存使用。这对于 serverless 和云环境尤为重要，其中冷启动延迟至关重要。

像 **Quarkus** 和 **Micronaut** 这样的框架是领先的云原生 Java 框架，与 GraalVM 紧密结合，实现亚秒级启动时间。Quarkus 强调构建时优化和通过 GraalVM 的 native 编译，与 virtual threads 形成协同效应——将响应式数据库驱动程序与 virtual threads 结合，实现非阻塞 I/O 和代码简洁性。

---

### 6. 🔧 Project Leyden —— 更快的 JVM 启动

Project Leyden 旨在改进 Java 的启动时间和峰值性能，于 2024 年引入了首批结果，包括 ahead-of-time (AOT) 类加载和链接——允许类在运行前被读取、解析和链接。前三个 Leyden 特性已在 Java 24 和 Java 25 中交付。

---

### 7. 🏢 Jakarta EE 11 & 企业 Java 进展

Jakarta EE 11 已稳定并广泛采用，Jakarta EE 12 的早期工作——特别是 Jakarta Query 规范——已在进行中，推动企业 Java 平台前进。

---

### 8. 🛠️ OpenRewrite —— 大规模遗留现代化

2025 年现代化浪潮涌现，组织优先更新遗留应用和过时的 Java 版本，OpenRewrite 已脱颖而出成为这项任务的主导自动化工具。它允许团队在大规模代码库中执行自动化重构（例如，从 Java 8 → 21、Spring Boot 2 → 3 的升级）。

---

### 9. 📈 更广泛的后端趋势

- **Microservices + Kubernetes** 仍占主导地位，主要框架为 Spring Boot、Quarkus 和 Micronaut
- **Observability**（OpenTelemetry、Micrometer）现在是企业 Java 应用中的默认期望
- **Reactive programming** 仍在使用，但面临 virtual threads 的挑战，后者为 I/O 密集型场景提供更简单的代码
- O'Reilly 报告称，Prompt Engineering 内容消费激增 456%，生成式 AI 学习上升 289%，反映了 AI 如何深刻改变后端开发者焦点，即使在 Java 社区内。

---

### Summary Table

| 领域 | 关键新闻 |
|---|---|
| Language | Java 24/25 released, virtual threads improved, Stream Gatherers finalized |
| Concurrency | Pinning bug fixed in JDK 24, Structured Concurrency maturing |
| AI/LLM | Spring AI 1.0, LangChain4j 1.0, Embabel, Koog, MCP SDK |
| Frameworks | Spring Boot 4 / Spring Framework 7 released |
| Performance | GraalVM native image, Project Leyden AOT, Project Loom |
| Enterprise | Jakarta EE 11 stable, OpenRewrite for modernization |

References:

- [InfoQ Java Trends Report 2025](https://www.infoq.com/articles/java-trends-report-2025/)
- [Spring AI and LangChain4j Deep Dive - Java Code Geeks](https://www.javacodegeeks.com/2026/01/building-ai-powered-applications-with-spring-ai-and-langchain4j.html)
- [Project Loom Virtual Threads - Java Code Geeks](https://www.javacodegeeks.com/2025/12/project-looms-virtual-threads-rethinking-concurrency-in-java.html)
- [Java 24 and Beyond - Medium](https://medium.com/@mohanbabudoddapaneni/java-24-and-beyond-virtual-threads-graalvm-and-the-future-of-cloud-native-java-43288df43536)
- [Java Trends Signal a Shift Amid AI Surge - ADTmag](https://adtmag.com/articles/2025/01/07/java-trends-signal-a-shift.aspx)
- [JVM Weekly - Java Plans for 2025](https://www.jvm-weekly.com/p/glancing-into-the-future-java-plans)
- [Inside Java - Project Loom Tag](https://inside.java/tag/loom)
