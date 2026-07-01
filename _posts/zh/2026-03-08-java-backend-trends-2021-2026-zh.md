---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java 后端趋势 2021–2026 详解
translated: true
type: note
---

问题：过去 5 年（2021–2026）Java/后端开发领域最大的新闻、趋势和热门项目是什么？

回答：

## Java & Backend：5 年历程 (2021–2026)

以下是 Java 和后端开发领域最重要的变化的逐年全面分解。

---

## 🗓️ 2021 — 云原生觉醒之年

**Java 17 LTS 发布**
JDK 17 于 2021 年 9 月发布，成为切换到新的 6 个月发布节奏后的第二个长期支持 (LTS) 版本。它包括 `switch` 的模式匹配（预览）和 sealed classes。

**Spring Boot 仍是王者，但挑战者崛起**
Spring Boot 主导市场，但有一个明显的弱点：对 native executables 的支持乏力——应用使用的内存更多，启动速度比 Quarkus 慢。Spring Boot 3 带有 GraalVM native 支持还需要一年时间。

Quarkus 2.0 于 2021 年 6 月发布，推动了 Red Hat 的愿景：一个专为容器和 Kubernetes 设计的 Java 框架，针对 GraalVM 优化，将 Java 字节码编译成 native 二进制文件。

**容器成为主流**
到 2023 年（反映从 2021 年开始的趋势），向 New Relic 报告的 Java 应用中 70% 运行在容器中——这标志着容器化在 Java 生态系统中根深蒂固。

**JDK 供应商格局动荡**
2020 年，Oracle 是最受欢迎的 JDK 供应商，市场份额约 75%。在 JDK 11 引入更严格的许可后，人们逐年明显、稳步转向远离 Oracle 二进制文件。

---

## 🗓️ 2022 — Spring Boot 3、Jakarta EE 重生与 Native Java

**十年以来最大的 Spring 发布**
VMware 发布了 Spring Framework 6 和 Spring Boot 3，这是 Spring 生态系统的新一代。Spring Framework 6 需要 Java 17 和 Jakarta EE 9，并通过 Micrometer 嵌入 observability，包括 tracing 和 metrics。Spring Boot 3 的头条功能是通过 GraalVM Native Image 的静态 ahead-of-time (AOT) 编译内置支持创建 native executables。

**`javax.*` → `jakarta.*` 命名空间迁移**
Jakarta EE 9 将 Java 命名空间从 `javax.*` 更改为 `jakarta.*`，要求所有导入 Jakarta EE 类型的现有 Spring 和 Spring Boot 应用进行更改。Spring Boot Migrator 项目专门创建，用于自动化从 Spring Boot 2.7 到 3.0 的升级。

**云原生 Java 框架增长**
到 2023 年初，Quarkus 和 Micronaut 已成为新框架中的明显赢家，两者在两年内绝对数量和相对市场份额均翻倍。Spring Boot 保持对 Jakarta EE 的 5:1 领先，但 Quarkus 已牢固确立为第 3 名。

---

## 🗓️ 2023 — Java 21 LTS：近年来最大发布

**Java 21 — 里程碑 LTS**
Oracle 于 2023 年 9 月发布了 Java 21，这是 Java 的重大里程碑， notable 改进包括 virtual threads 正式 GA、record patterns、`switch` 的模式匹配以及 sequenced collections。发布后六个月内，1.4% 的应用已使用 Java 21——相比 Java 17 在相同时间框架内的 0.37%，采用率高出 287%。

**Virtual Threads 正式 GA (Project Loom)**
这可以说是十年中最具深远影响的 Java 特性——virtual threads 成为生产就绪功能，使 JVM 上无需复杂 reactive programming 即可启用数百万轻量级线程。

**Quarkus 3.0 发布**
Quarkus 3.0 于 2023 年 5 月发布，Jakarta EE 命名空间迁移完成。更新需要 2.x 用户付出大量努力。Quarkus 1.0 于 2019 年底推出，这在短短三年内实现了代际跃升。

**快速 JVM 启动成为优先事项**
“Fast JVM Startup”概念在 Java 社区中成为公认类别。主要方法分为两类：CRaC (Coordinated Restore at Checkpoint)，由 Azul 和 BellSoft 在其 OpenJDK 发行版中实现；以及 GraalVM native image 编译，已进入 Early Adopters 阶段。

**采用快照**
2023 年，Java 11 保持生产份额首位，超过 56% 的应用（2022 年为 48%）。Java 17 的采用率同比增长 430%，从不到 1% 增长到超过 9%，与 Java 11 早期采用缓慢形成鲜明对比。

---

## 🗓️ 2024 — AI 进入 JVM 且生产成熟

**Java 22 & 23 发布**
Java 23 于 2024 年 9 月发布，Spring Boot 3.3 伴随其后——structured concurrency 进入预览、`primitives` 的模式匹配预览，六个月节奏继续提供增量质量改进。

**Java 17 成为新基线**
到 2024 年，35% 的应用运行 Java 17——一年内增长近 300%——各框架统一将 Java 17 作为最低版本。Eclipse Adoptium 年同比增长 50%，市场份额达 18%，作为 vendor-neutral JDK。

**GraalVM 成熟：GraalPy & GraalWasm**
GraalPy 和 GraalWasm 与 GraalVM for JDK 23 一起进入“Early Adopters”和稳定生产类别。这些项目使 JVM 上可执行 Python 和 WebAssembly，将 GraalVM 扩展超出单纯 native image 生成。

**Jakarta EE 11 开发中**
Jakarta EE 11 计划于 2024 年底 GA 发布，正在积极开发 16 个规范，包括 Jakarta Security 4.0、Jakarta Validation 3.1 和新的 Jakarta Data 1.0 规范。

**CRaC (快速启动) 进入 Early Adopters**
Coordinated Restore at Checkpoint (CRaC) 在 2024 年进入 Early Adopters 类别，Azul 和 BellSoft 在其 OpenJDK 下游发行版中实现，无需 GraalVM native 编译即可实现 JVM 启动时间大幅改进。

**MCP Java SDK 推出**
MCP Java SDK 于 2024 年 12 月推出，使 Java 应用通过标准化接口与 AI 模型和工具交互，支持同步和异步通信模式。

---

## 🗓️ 2025 — AI 赋能的 Java 时代

**Java 24 & 25 LTS 发布**
Java 25 于 2025 年作为新 LTS 发布，Spring Boot 4.0 和 AI 集成成为标准。时代框架转变：2021 年，核心 Java 知识足以应对面试；到 2026 年，virtual threads、records、模式匹配和 AI 集成成为新基线期望。

**Java 24 中修复 Virtual Thread Pinning Bug**
长期问题——执行 `synchronized` 块的 virtual threads 会“pin”到 carrier threads 并丧失性能优势——在 JDK 24 中解决，消除了 virtual threads 广泛采用的最后主要障碍。

**Spring AI 1.0 & LangChain4j 1.0 正式 GA**
Spring AI 1.0 于 2025 年 5 月发布，提供 `ChatClient` 接口支持二十个 AI 模型的多模态输入、Advisors API 作为注入检索数据和对话记忆的拦截器链，以及对 Model Context Protocol (MCP) 的完全支持。

**Spring Boot 4 & Spring Framework 7**
备受期待的 Spring Boot 4.0 和 Spring Framework 7.0 GA 发布于 2025 年 11 月，提供 API versioning、resilience 和来自 JSpecify 的 null-safe 注解。

**新型 JVM Agent 框架**
Embabel Agent Framework 和 Koog——分别由 Spring Framework 创始人 Rod Johnson 和 JetBrains 创建——是 2025 年 Q2 推出的新开源 agent 平台，专为开发者在 Java 中原生构建和运行 AI agents 设计。

**Project Leyden：AOT 类加载**
Project Leyden 的前三个特性——旨在改进 Java 启动时间和峰值性能时间——于 2025 年随 Java 24 和 Java 25 发布，第四个特性计划用于 Java 26。

---

## 📊 5 年总结：关键宏观趋势

| Theme | 2021 | 2026 |
| --- | --- | --- |
| **LTS Baseline** | Java 11 主导 | 处处要求 Java 17+，Java 21/25 快速增长 |
| **Concurrency** | 线程池 + reactive | Virtual Threads (Project Loom) 成为新默认 |
| **Native/Cloud** | Quarkus/Micronaut 细分市场 | GraalVM native + Spring Boot 4 主流 |
| **AI Integration** | 非 Java 关注点 | Spring AI、LangChain4j、agent 框架一流 |
| **Startup Time** | 分钟级忽略 | CRaC、Leyden、GraalVM native 竞争 |
| **Frameworks** | Spring Boot 单片 | Spring Boot 4 + Quarkus + Micronaut 均可行 |
| **Enterprise Java** | Java EE 衰退 | Jakarta EE 11 稳定，EE 12 进行中 |
| **JDK Vendors** | Oracle ~75% | Oracle ~21%，Adoptium/Amazon/Azul 分享市场 |

参考文献：

- [Java Version History - Wikipedia](https://en.wikipedia.org/wiki/Java_version_history)
- [InfoQ Java Trends Report 2025](https://www.infoq.com/articles/java-trends-report-2025/)
- [InfoQ Java Trends Report 2024](https://www.infoq.com/articles/java-trends-report-2024/)
- [InfoQ Java Trends Report 2023](https://www.infoq.com/articles/java-trends-report-2023/)
- [2024 State of the Java Ecosystem - New Relic](https://newrelic.com/resources/report/2024-state-of-the-java-ecosystem)
- [2023 State of the Java Ecosystem - New Relic](https://newrelic.com/resources/report/2023-state-of-the-java-ecosystem)
- [Spring Boot 3 and Spring Framework 6 Launch - InfoQ](https://www.infoq.com/news/2022/11/spring-6-spring-boot-3-launch/)
- [Quarkus 3.0 Released - DevClass](https://devclass.com/2023/05/09/despite-extremely-disruptive-jakarta-ee-change-red-hat-releases-the-quarkus-3-0-container-optimized-framework/)
- [Java Developer Roadmap 2026 - DEV Community](https://dev.to/dbc2201/the-java-developers-roadmap-for-2026-from-first-program-to-production-ready-professional-41ng)
