---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: JDK 11 Migration Pains and Criticisms
translated: false
type: note
---

Question: What are some unpopular opinions about JDK 11?

Answer:

JDK 11, released in 2018 as the first long-term support (LTS) version after JDK 8 under Oracle's faster release cadence, introduced significant changes like the removal of Java EE and CORBA modules, stronger module system enforcement, and licensing shifts. While praised for performance improvements and stability, it has sparked several unpopular opinions, often rooted in migration pains, ecosystem friction, and perceived over-engineering. Here are some notable ones drawn from developer discussions:

- **JDK 11's module system is a solution in search of a problem that created bigger headaches for everyone else.** Critics argue that the Java Platform Module System (JPMS), fully enforced in JDK 11, addressed niche issues like large binaries for a few large-scale users but burdened the entire ecosystem with introspection barriers, library incompatibilities, and verbose configuration—without delivering widespread benefits for most projects.

- **Upgrading to JDK 11 is a nightmare due to outdated dependencies and non-portable libraries, making it feel like a step backward from JDK 8's simplicity.** Many developers report spending days or weeks fixing issues with tools like Groovy (which relied on internal JDK hacks) or parsing errors in version detection code, blaming the transition for unjustly tarnishing the module system's reputation despite it not being the root cause.

- **Oracle's licensing changes for JDK 11 were a predatory "trap" that scared off adopters and eroded trust in Java's openness.** The shift to commercial licensing for production use (while development remained free) led to widespread FUD, with some suggesting it pushed users toward alternatives like Kotlin or even non-JVM languages, despite OpenJDK being a viable free path.

- **JDK 11 isn't truly "long-term support" if it locks you into a version that's already showing its age compared to bleeding-edge releases.** With the six-month release cycle, sticking to LTS like JDK 11 feels restrictive for accessing modern features (e.g., better GC or HTTP clients), and some prefer upgrading every six months to avoid stagnation, calling LTS a crutch for risk-averse enterprises.

- **The removal of Java EE modules in JDK 11 was a shortsighted gutting of useful tools, forcing unnecessary rewrites for distributed systems devs.** Dropping CORBA and other EE components slimmed the JDK but alienated developers building heterogeneous apps, who now juggle external dependencies or switch to non-JDK stacks, viewing it as Oracle prioritizing bloat reduction over practical utility.

These opinions highlight the tension between Java's evolution and its massive legacy codebase, though many teams successfully migrated and appreciate JDK 11's garbage collection tweaks and security fixes in hindsight.

References:

- [The Impossible Java 11](https://www.reddit.com/r/java/comments/o09unw/the_impossible_java_11/)
- [JDK 11: Pitfalls for the Unwary](https://medium.com/@speakjava/jdk-11-pitfalls-for-the-unwary-e08d864065c1)
- [Java 11 sucks big time](https://www.reddit.com/r/java/comments/9vmk0w/java_11_sucks_big_time/)
- [Do not fall into Oracle's Java 11 trap](https://www.reddit.com/r/programming/comments/9j25je/do_not_fall_into_oracles_java_11_trap/)
- [No one upgrading to java 11?](https://www.reddit.com/r/java/comments/9ow41b/no_one_upgrading_to_java_11/)
- [What is the point of all these new Java versions when Java 8 is all that seems to be supported by most apps?](https://www.reddit.com/r/java/comments/mu4sar/what_is_the_point_of_all_these_new_java_versions/)
- [A Year with Java 11 in Production!](https://www.infoq.com/presentations/java-11-production-story/)
