---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: JDK 11迁移的痛点与批评
translated: true
type: note
---

问题：关于 JDK 11 有哪些不受欢迎的观点？

回答：

JDK 11 于 2018 年发布，是 Oracle 快速发布节奏下继 JDK 8 之后的第一个长期支持（LTS）版本，引入了 significant changes，例如移除了 Java EE 和 CORBA 模块、更强的模块系统强制执行和许可变更。虽然其性能改进和稳定性受到赞扬，但也引发了一些不受欢迎的观点，这些观点通常源于迁移难题、生态系统摩擦和被认为的过度设计。以下是一些来自开发者讨论的 noteworthy 观点：

- **JDK 11 的模块系统是为了解决一个并未普遍存在的问题而生，反而给所有人带来了更大的麻烦。** 批评者认为，在 JDK 11 中完全强制执行的 Java Platform Module System (JPMS) 解决了少数大型用户面临的二进制文件过大等利基问题，但却给整个生态系统带来了内部反射障碍、库不兼容和冗长的配置——而没有为大多数项目带来广泛的 benefits。

- **由于过时的 dependencies 和不可移植的 libraries，升级到 JDK 11 是一场噩梦，让人感觉比 JDK 8 的 Simplicity 倒退了一步。** 许多开发者报告称，花费数天或数周来修复 Groovy 等工具（依赖于内部 JDK hacks）的问题或版本检测代码中的解析错误，他们将这种过渡归咎于不公正地玷污了模块系统的 repution，尽管它并非根本原因。

- **Oracle 对 JDK 11 的许可变更是一个 predatory 的“陷阱”，吓跑了 adopter 并侵蚀了对 Java 开放性的信任。** 生产用途的商业许可（而开发仍然免费）转向导致了普遍的 FUD，一些人认为这推动用户转向 Kotlin 甚至 non-JVM 语言等 alternatives，尽管 OpenJDK 是一条可行的免费途径。

- **如果 JDK 11 将你锁定在一个与 bleeding-edge 版本相比已经过时的版本中，那么它就不是真正的“长期支持”。** 随着 six-month 发布周期，坚持使用 JDK 11 这样的 LTS 版本在访问现代 features（例如，更好的 GC 或 HTTP clients）方面感觉受到 restrict，一些人更喜欢每 six months 升级一次以避免 stagnation，称 LTS 是 risk-averse 企业的拐杖。

- **JDK 11 中移除 Java EE 模块是一个 shortsighted 的有用工具的 gutting，迫使分布式系统开发者进行不必要的 rewrites。** 移除 CORBA 和其他 EE 组件使得 JDK 变得 slim，但疏远了构建 heterogeneous 应用程序的开发者，他们现在需要 juggling external dependencies 或切换到 non-JDK stacks，认为 Oracle 是将 bloat reduction 置于 practical utility 之上。

这些观点突显了 Java 的 evolution 与其 massive 的 legacy codebase 之间的 tension，尽管许多团队成功迁移并事后感谢 JDK 11 的垃圾 collection tweaks 和 security fixes。

References:
- [The Impossible Java 11](https://www.reddit.com/r/java/comments/o09unw/the_impossible_java_11/)
- [JDK 11: Pitfalls for the Unwary](https://medium.com/@speakjava/jdk-11-pitfalls-for-the-unwary-e08d864065c1)
- [Java 11 sucks big time](https://www.reddit.com/r/java/comments/9vmk0w/java_11_sucks_big_time/)
- [Do not fall into Oracle's Java 11 trap](https://www.reddit.com/r/programming/comments/9j25je/do_not_fall_into_oracles_java_11_trap/)
- [No one upgrading to java 11?](https://www.reddit.com/r/java/comments/9ow41b/no_one_upgrading_to_java_11/)
- [What is the point of all these new Java versions when Java 8 is all that seems to be supported by most apps?](https://www.reddit.com/r/java/comments/mu4sar/what_is_the_point_of_all_these_new_java_versions/)
- [A Year with Java 11 in Production!](https://www.infoq.com/presentations/java-11-production-story/)
