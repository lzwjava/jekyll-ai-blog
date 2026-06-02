---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Opinions on JDK 17
translated: false
type: note
---

Question: What are some unpopular opinions about JDK 17?

Answer:

While JDK 17 is widely praised as a stable Long-Term Support (LTS) release with features like sealed classes, records, and text blocks that reduce verbosity, it has drawn some contrarian views from developers. These opinions often stem from comparisons to newer versions (like JDK 21 or 25) or broader frustrations with the Java ecosystem. Based on discussions in forums like Reddit and X (formerly Twitter), here are a few unpopular takes:

- **JDK 17 is already outdated for new projects, and sticking to LTS versions like it hinders innovation.**
  Some argue that the LTS model encourages complacency, locking teams into older tech for years while non-LTS releases deliver faster performance gains and features (e.g., virtual threads in JDK 21). One developer called for ditching LTS altogether: "No LTS. Just stick with the latest version, upgrade every 6 months... and get the performance and features for free." This view flips the script on JDK 17's "stability" as a selling point, seeing it as a barrier to Java's evolution.

- **The performance improvements in JDK 17 aren't revolutionary enough to justify the upgrade from JDK 8 or 11.**
  Critics point out that while JDK 17 offers better garbage collection and reduced Full GC pauses compared to JDK 8's antiquated runtime, the gains are incremental for many workloads—especially if you're not leveraging new APIs. One analysis noted that G1 in older versions is "stuck in an old version that uses just one thread," but JDK 17 still requires ~25% more RAM in tight deployments to avoid OOM errors. Unpopular twist: "Most complaints [about Java] besides potentially max memory usage is just cope," implying JDK 17's JVM is elite but underappreciated.

- **JDK 17's stricter encapsulation and removals make it more trouble than it's worth for legacy code.**
  The enforcement of strong encapsulation (starting around JDK 16/17) breaks libraries that relied on internal APIs, and deprecated features like the security manager (fully removed later) force painful migrations. Upgrading from JDK 11 to 17 is "smooth" for most, but for SOAP clients or Jakarta EE apps, it's a "hell" of compatibility issues. An contrarian angle: This "private means private" rigidity is overkill, punishing clever (if non-portable) code without clear upgrade guides.

- **Features like records and sealed classes add needless ceremony to an already verbose language.**
  Even with JDK 17's usability wins (e.g., concise data classes via records), detractors say Java remains bloated compared to Python or Groovy—text blocks help strings, but switch expressions still feel clunky. Broader ecosystem gripes bleed in: "JVM languages... feel outdated and slow," with no stack allocation for structs and a mess of concurrency options (Threads vs. Executors). Unpopular opinion: The src/main/java boilerplate structure "raises the barrier for small projects, entrenching the perception of JVM heavy-weightiness."

These views are niche—JDK 17's adoption is high for its balance of maturity and modernity—but they highlight ongoing debates in the Java community about balancing stability with progress.

References:

- [r/java: How was your experience upgrading to JDK25?](https://www.reddit.com/r/java/comments/1ot1bqw/how_was_your_experience_upgrading_to_jdk25/)
- [How much faster is Java 17? | Hacker News](https://news.ycombinator.com/item?id=28540099)
- [r/java: Are there breaking changes between 17 and 21?](https://www.reddit.com/r/java/comments/1e01kc6/are_there_breaking_changes_between_17_and_21/)
- [Although Java 17 has appeared, why do most companies still use Java 11 or even Java 8? - Quora](https://www.quora.com/Although-Java-17-has-appeared-why-do-most-companies-still-use-Java-11-or-even-Java-8)
- [r/java: What are the differences between Java 8 and Java 17?](https://www.reddit.com/r/java/comments/12fowwd/what_are_the_differences_between_java_8_and_java/)
- [5 best Java 17 features that developers will love | TheServerSide](https://www.theserverside.com/tip/5-best-Java-17-features-that-developers-will-love)
- [Unpopular opinion but Java is actually a great language... (X post)](https://x.com/sampullara/status/1963843375431344277)
- [all JVM languages (Java or Kotlin) are honestly such a pain... (X post)](https://x.com/mrousavy/status/1993405762303840665)
- [Unpopular opinion: the defacto standard src/main/java... (X post)](https://x.com/relizarov/status/1305414701552209921)
