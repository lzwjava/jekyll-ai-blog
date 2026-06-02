---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 关于 JDK 17 的冷门观点
translated: true
type: note
---

问题：关于 JDK 17 有哪些不受欢迎的观点？

回答：

尽管 JDK 17 被广泛称赞为一个稳定的长期支持（LTS）版本，其密封类、记录和文本块等特性减少了冗余，但它也引发了一些开发人员的逆向观点。这些观点通常源于与更新版本（如 JDK 21 或 25）的比较，或对 Java 生态系统更广泛的不满。根据 Reddit 和 X（前身为 Twitter）等论坛的讨论，以下是一些不受欢迎的观点：

- **JDK 17 对于新项目来说已经过时，坚持使用像它这样的 LTS 版本会阻碍创新。**
  一些人认为，LTS 模型助长了自满情绪，使团队多年来局限于旧技术，而那些非 LTS 版本则提供了更快的性能提升和功能（例如，JDK 21 中的虚拟线程）。一位开发人员呼吁彻底放弃 LTS：“没有 LTS。只需坚持使用最新版本，每 6 个月升级一次……并免费获得性能和功能。”这种观点颠覆了 JDK 17 将“稳定性”作为卖点的说法，将其视为 Java 发展的障碍。

- **JDK 17 的性能改进不足以证明从 JDK 8 或 11 升级是合理的。**
  批评者指出，尽管 JDK 17 提供了更好的垃圾回收并减少了与 JDK 8 过时运行时相比的 Full GC 暂停，但对于许多工作负载来说，这些增益是渐进的——尤其是如果你没有利用新的 API。一项分析指出，旧版本中的 G1“停留在只使用一个线程的旧版本”，但 JDK 17 在紧密的部署中仍需要大约 25% 的更多 RAM 来避免 OOM 错误。一个不受欢迎的变调：“大多数关于 Java 的抱怨，除了可能的最大内存使用量，都只是应对之词”，这暗示 JDK 17 的 JVM 是一流但被低估的。

- **JDK 17 更严格的封装和移除使其对遗留代码来说弊大于利。**
  强制执行强封装（从 JDK 16/17 左右开始）破坏了依赖内部 API 的库，而像安全管理器（后来完全移除）这样的弃用功能则强制进行痛苦的迁移。从 JDK 11 升级到 17 对大多数人来说是“顺利的”，但对于 SOAP 客户端或 Jakarta EE 应用程序来说，却是兼容性问题的“地狱”。一个逆向角度：这种“私有即私有”的严格性是矫枉过正，惩罚了巧妙的（如果不可移植的）代码，却没有明确的升级指南。

- **像记录和密封类这样的功能给一个已经冗长的语言增加了不必要的仪式。**
  即使 JDK 17 在可用性方面有所改进（例如，通过记录提供简洁的数据类），批评者也认为与 Python 或 Groovy 相比，Java 仍然臃肿——文本块有助于字符串，但 switch 表达式仍然感觉笨拙。更广泛的生态系统抱怨也渗透进来：“JVM 语言……感觉过时和缓慢”，没有用于结构体的栈分配，并且并发选项（Threads vs. Executors）一团糟。一个不受欢迎的观点：src/main/java 样板结构“提高了小项目的门槛，加深了 JVM 沉重感的认知。”

这些观点是小众的——JDK 17 因其成熟度和现代化的平衡而拥有很高的采用率——但它们突出了 Java 社区中关于平衡稳定性与进步的持续争论。

参考文献：

- [r/java: How was your experience upgrading to JDK25?](https://www.reddit.com/r/java/comments/1ot1bqw/how_was_your_experience_upgrading_to_jdk25/)
- [How much faster is Java 17? | Hacker News](https://news.ycombinator.com/item?id=28540099)
- [r/java: Are there breaking changes between 17 and 21?](https://www.reddit.com/r/java/comments/1e01kc6/are_there_breaking_changes_between_17_and_21/)
- [Although Java 17 has appeared, why do most companies still use Java 11 or even Java 8? - Quora](https://www.quora.com/Although-Java-17-has-appeared-why-do-most-companies-still-use-Java-11-or-even-Java-8)
- [r/java: What are the differences between Java 8 and Java 17?](https://www.reddit.com/r/java/comments/12fowwd/what_are_the_differences_between_java_8_and_java/)
- [5 best Java 17 features that developers will love | TheServerSide](https://www.theserverside.com/tip/5-best-Java-17-features-that-developers-will-love)
- [Unpopular opinion but Java is actually a great language... (X post)](https://x.com/sampullara/status/1963843375431344277)
- [all JVM languages (Java or Kotlin) are honestly such a pain... (X post)](https://x.com/mrousavy/status/1993405762303840665)
- [Unpopular opinion: the defacto standard src/main/java... (X post)](https://x.com/relizarov/status/1305414701552209921)
