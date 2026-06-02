---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java社区争议观点
translated: true
type: note
---

问题：Java 编程社区中一些不受欢迎或有争议的观点是什么？

答：

以下是一些真正不受欢迎（通常会引发激烈争论）的观点，它们经常让 Java 开发者争论不休。这些观点被相当一部分少数派（或有时是沉默的大多数）所持有，但受到“官方”Java 正统派或社区中直言不讳的部分的强烈反对：

- **受检异常是失败的尝试，应该被废弃。**
  大多数经验丰富的 Java 开发者都悄悄地讨厌它们，并设法绕过它们（包装在 RuntimeException 中，声明通用的 `throws Exception` 等）。大声说出这个观点仍然会激怒许多老派人士，他们捍卫原始设计。

- **Lombok 是一种反模式，不应出现在严肃的代码库中。**
  尽管它非常流行，但一部分直言不讳的人坚持认为 @Data、@Builder 等创建了“魔法”，模糊了实际生成的代码，破坏了 IDE 调试，并增加了上手难度。

- **Spring Boot 臃肿、过于神奇，大多数应用程序应该只使用纯 Servlet 或最简框架（Micronaut、Quarkus、Helidon，甚至 Javalin）。**
  Spring Boot 在企业 Java 中占据主导地位，因此在许多公司中，将其批评为“XML 地狱，但使用注解和 starter-POMs”是异端。

- **Records (Java 14+)，尤其是“紧凑型构造函数”，让语言看起来像 Kotlin/脚本，并削弱了 Java 的冗长优势。**
  一些传统主义者确实不喜欢日益简洁的语法，希望 Java 保持明确的冗长。

- **Project Loom 的虚拟线程被过度炒作；大多数实际性能问题仍然存在于数据库/IO 层，而不是线程数量。**
  很多人喜欢 Loom，但也有人认为这种炒作忽略了虚拟线程上的阻塞 I/O 仍然是阻塞的，并且只会增加连接池压力。

- **Java 永远不应该添加 var（局部变量类型推断）。**
  即使在 Java 10 发布多年后，仍有数量惊人的开发者（尤其是在金融/企业领域）在他们的样式指南中禁止使用 `var`，并认为它不可读。

- **模块系统（JPMS / Jigsaw）是一个错误，几乎没有带来任何实际好处，却破坏了一半的生态系统。**
  非常普遍的私下观点；公开说出来仍然会被模块布道者大声呵斥。

- **Getter 和 Setter 大部分是无用的仪式；公共 final 字段 + withers（或 records）在 95% 的时间里更好。**
  这与长达数十年、至今仍在普遍教授的“始终封装”教条背道而驰。

- **对于真正的企业项目，Maven 在几乎所有方面都优于 Gradle（更好的依赖解析，更可预测，对公司更友好）。**
  Gradle 几年前赢得了人气竞赛，因此现在捍卫 Maven 是逆流而上。

- **Java 不再是顶级语言，大多数新项目应该选择 Kotlin、Go、Rust，甚至 TypeScript。**
  这在许多 Java 公司中是极致的禁忌，但随着 Java 在新开发者中逐渐失去心智份额，这种观点越来越多地被窃窃私语。

这些观点私下持有通常是职业安全的，但如果你在 Reddit、Stack Overflow 或 Java 会议上表达出来，可能会引发真实的争论。

参考资料：

- <https://www.reddit.com/r/java/comments/15×6×84/what_are_your_java_heresy_opinions/>
- <https://blog.softwaremill.com/java-controversies-that-never-die-2c3f5e8e9b8d>
- <https://twitter.com/lukaseder/status/1721518218360836520（受检异常的争论，从古至今持续不断）>
