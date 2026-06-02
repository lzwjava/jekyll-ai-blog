---
audio: false
generated: true
lang: zh
layout: post
title: JDK 24：核心特性与更新详解
translated: true
type: note
---

### JDK 24 简介

Java开发工具包（JDK）24是Java SE（标准版）平台的功能版本，于2025年3月18日正式发布，作为Java社区进程中JSR 399指定的第24版参考实现。它延续了Oracle每六个月发布一次的节奏，提供了一系列强大的增强功能，以提高开发人员的工作效率、性能和安全性。JDK 24包含了24个JDK增强提案（JEP），这是自2018年基于时间的发布计划开始以来功能数量最多的一次，使其成为Java演进的重要里程碑。它是通往JDK 25（下一个长期支持版本，计划于2025年9月发布）的垫脚石。

### 长期支持（LTS）状态

JDK 24**不是**长期支持（LTS）版本。它是一个短期支持版本，仅获得Oracle六个月的Premier级别支持，直到2025年9月被JDK 25取代。相比之下，LTS版本（如JDK 21（2023年9月发布）和即将发布的JDK 25（2025年9月发布））至少获得五年的Premier支持，这使它们成为企业稳定性的首选。Oracle的LTS发布节奏每两年一次，JDK 21是最近的LTS版本，JDK 25将是下一个LTS版本。

### 发布与稳定性

JDK 24是一个**稳定的、生产就绪的版本**，已于2025年3月18日达到通用可用性（GA）。生产就绪的二进制文件可从Oracle根据Oracle免费条款和条件（NFTC）以及OpenJDK的GNU通用公共许可证（GPLv2）获取，其他供应商的二进制文件也将很快跟进。该版本除了24个JEP外，还包括超过3000个错误修复和较小的增强功能，确保了通用使用的稳定性。然而，作为一个非LTS版本，它主要面向渴望测试新功能的开发人员，而不是需要长期稳定性的企业。

### JDK 24 的新功能

JDK 24引入了24个JEP，分为核心库增强、语言改进、安全功能、HotSpot JVM优化和Java工具。其中，14个是永久功能，七个是预览功能，两个是实验性功能，一个是孵化器模块。以下是一些最值得注意的功能，重点关注与开发人员和部署相关的功能：

1.  **Stream Gatherers (JEP 485)** - 永久功能
    - 通过引入`Gatherer`接口增强Stream API，允许开发人员为流管道定义自定义中间操作。这使得数据转换更加灵活，补充了用于终端操作的现有`Collector`接口。
    - 示例：使用`StreamGatherers.groupBy`按长度对单词进行分组。
    - 好处：简化了开发人员的复杂流处理。

2.  **Ahead-of-Time Class Loading & Linking (JEP 483)** - 实验性功能
    - 作为Project Leyden的一部分，此功能通过在准备阶段将类预加载和链接到缓存中，减少了Java应用程序的启动时间。缓存在运行时被重用，绕过了昂贵的类加载步骤。
    - 好处：提高了云和微服务应用程序的性能。

3.  **Compact Object Headers (JEP 450)** - 实验性功能
    - 作为Project Lilliput的一部分，这将64位架构上的Java对象头大小从96-128位减少到64位，降低了堆使用量并提高了内存效率。
    - 好处：减少了内存占用并增强了数据局部性以提高性能。

4.  **Generational Shenandoah Garbage Collector (JEP 404)** - 永久功能
    - 将Shenandoah GC的分代模式从实验性功能过渡为产品功能，通过将对象分为年轻代和老年代来提高吞吐量、负载峰值恢复能力和内存利用率。
    - 好处：增强了要求苛刻工作负载的性能。

5.  **Module Import Declarations (JEP 494)** - 第二次预览
    - 简化模块化编程，允许直接导入模块导出的所有包，而无需`module-info.java`文件（例如，`import module java.sql;`）。
    - 好处：减少了轻量级应用程序和脚本的开销，有助于初学者和快速原型设计。

6.  **Flexible Constructor Bodies (JEP 492)** - 第三次预览
    - 允许在`super()`或`this()`调用之前的构造函数中放置语句，使得字段初始化逻辑可以更自然地放置，而无需辅助方法。
    - 好处：提高了代码的可靠性和可读性，特别是在子类化方面。

7.  **Key Derivation Function (KDF) API (JEP 487)** - 预览功能
    - 引入了用于加密密钥派生函数（如基于HMAC的提取和扩展以及Argon2）的API，支持安全密码哈希和与加密硬件的交互。
    - 好处：增强了需要高级加密技术的应用程序的安全性。

8.  **Permanently Disable the Security Manager (JEP 486)** - 永久功能
    - 移除了在JDK 17中已弃用的Security Manager，因为它不再是保护Java应用程序的主要手段（已被基于容器的沙箱取代）。
    - 注意：依赖Security Manager的应用程序可能需要进行架构更改。

9.  **Late Barrier Expansion for G1 Garbage Collector (JEP 464)** - 永久功能
    - 通过将屏障扩展移至编译管道的后期来简化G1 GC的屏障实现，从而减少编译时间并提高可维护性。
    - 好处：提高了使用G1 GC的应用程序的性能。

10. **Quantum-Resistant Cryptography (JEP 452, 453)** - 预览功能
    - 引入了基于模块格子的密钥封装机制（ML-KEM）和数字签名算法（ML-DSA），以防范量子计算攻击。
    - 好处：为Java应用程序的后量子安全做好了未来准备。

11. **Scoped Values (JEP 480)** - 第四次预览
    - 使得在线程内部和跨线程之间共享不可变数据比线程局部变量更安全，改进了并发处理。
    - 好处：简化了对并发代码的理解。

12. **Deprecate 32-bit x86 Port (JEP 501)** - 永久功能
    - 弃用32位x86端口，计划在JDK 25中移除，并使用与架构无关的Zero端口作为32位系统的替代方案。
    - 好处：减少了维护开销，专注于现代架构。

13. **Vector API (JEP 489)** - 第九次孵化器
    - 继续完善用于SIMD编程的Vector API，增强了跨通道和算术操作。
    - 好处：提高了计算密集型应用程序的性能。

14. **Linking Run-Time Images without JMODs (JEP 493)** - 永久功能
    - 允许`jlink`工具在没有JMOD文件的情况下创建自定义运行时映像，将JDK大小减少约25%。
    - 好处：提高了自定义Java运行时的部署效率。

### 补充说明

-   **预览和实验性功能**：许多功能（例如，Scoped Values、KDF API）处于预览或实验阶段，允许开发人员在它们成为JDK 25或更高版本的永久功能之前进行测试和提供反馈。这些功能在最终确定之前可能会发生变化。
-   **项目集成**：JDK 24引入了OpenJDK项目的元素，如Leyden（启动优化）、Lilliput（内存效率）和Panama（原生互操作性），为未来的增强奠定了基础。
-   **安全性和弃用**：诸如移除Security Manager和弃用32位x86端口等功能反映了Oracle通过逐步淘汰过时组件来现代化Java的关注点。

### 结论

JDK 24是一个稳定、功能丰富的版本，提升了Java的性能、开发人员生产力和安全性。虽然它不是LTS版本，但其24个JEP提供了显著的改进，其中许多将在即将发布的LTS版本JDK 25中最终确定。开发人员可以利用诸如Stream Gatherers和Module Import Declarations等功能来获得即时生产力提升，而像Compact Object Headers和Ahead-of-Time Class Loading这样的实验性功能则标志着Java正在持续优化以适应现代工作负载。对于企业使用，建议坚持使用LTS版本（如JDK 21）或等待JDK 25，因为它们提供更长的支持期。

有关更多详细信息，请访问：
-   [Oracle JDK 24 发布说明](https://www.oracle.com/java/technologies/javase/24-relnote-issues.html)
-   [OpenJDK JDK 24](https://openjdk.org/projects/jdk/24/)
-   [JavaOne 2025 会议](https://www.oracle.com/javaone) 了解功能亮点
