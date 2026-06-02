---
audio: false
generated: true
lang: en
layout: post
title: 'JDK 24: Key Features and Updates'
translated: false
type: note
---

### Introduction to JDK 24

Java Development Kit (JDK) 24 is a feature release of the Java SE (Standard Edition) Platform, officially released on March 18, 2025, as the Reference Implementation of version 24, specified by JSR 399 in the Java Community Process. It continues Oracle’s six-month release cadence, delivering a robust set of enhancements to improve developer productivity, performance, and security. JDK 24 includes 24 JDK Enhancement Proposals (JEPs), the highest number of features since the time-based release schedule began in 2018, making it a significant milestone in Java’s evolution. It serves as a stepping stone toward JDK 25, the next Long-Term Support (LTS) release scheduled for September 2025.[](https://www.infoworld.com/article/3491404/jdk-24-the-new-features-in-java-24.html)[](https://openjdk.org/projects/jdk/24/)[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)

### Long-Term Support (LTS) Status

JDK 24 is **not** a Long-Term Support (LTS) release. It is a short-term support release, receiving only six months of Premier-level support from Oracle, until September 2025, when it will be superseded by JDK 25. In contrast, LTS releases like JDK 21 (September 2023) and the upcoming JDK 25 (September 2025) receive at least five years of Premier support, making them preferred for enterprise stability. Oracle’s LTS cadence occurs every two years, with JDK 21 being the most recent LTS and JDK 25 set to be the next.[](https://www.infoworld.com/article/3491404/jdk-24-the-new-features-in-java-24.html)[](https://www.jrebel.com/blog/whats-new-java-24)[](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)

### Release and Stability

JDK 24 is a **stable, production-ready release**, having reached General Availability (GA) on March 18, 2025. Production-ready binaries are available from Oracle under the Oracle No-Fee Terms and Conditions (NFTC) and the GNU General Public License (GPLv2) for OpenJDK, with other vendors’ binaries following shortly. The release includes over 3,000 bug fixes and smaller enhancements beyond the 24 JEPs, ensuring stability for general use. However, as a non-LTS release, it is primarily aimed at developers eager to test new features rather than enterprises requiring long-term stability.[](https://openjdk.org/projects/jdk/24/)[](https://www.theregister.com/2025/03/18/oracle_jdk_24/)[](https://www.oracle.com/java/technologies/javase/24-relnote-issues.html)

### New Features in JDK 24

JDK 24 introduces 24 JEPs, categorized into core library enhancements, language improvements, security features, HotSpot JVM optimizations, and Java tools. Of these, 14 are permanent features, seven are preview features, two are experimental, and one is an incubator module. Below are some of the most notable features, with a focus on those relevant to developers and deployments:

1. **Stream Gatherers (JEP 485)** - Permanent
   - Enhances the Stream API by introducing the `Gatherer` interface, allowing developers to define custom intermediate operations for stream pipelines. This enables more flexible data transformations, complementing the existing `Collector` interface for terminal operations.
   - Example: Grouping words by length using `StreamGatherers.groupBy`.
   - Benefit: Simplifies complex stream processing for developers.[](https://www.azul.com/blog/six-jdk-24-features-you-should-know-about/)[](https://www.infoworld.com/article/3830643/the-most-relevant-new-features-in-jdk-24.html)

2. **Ahead-of-Time Class Loading & Linking (JEP 483)** - Experimental
   - Part of Project Leyden, this feature reduces Java application startup times by pre-loading and linking classes into a cache during a preparatory phase. The cache is reused at runtime, bypassing costly class loading steps.
   - Benefit: Improves performance for cloud and microservices applications.[](https://www.azul.com/blog/six-jdk-24-features-you-should-know-about/)[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)[](https://www.infoworld.com/article/3830643/the-most-relevant-new-features-in-jdk-24.html)

3. **Compact Object Headers (JEP 450)** - Experimental
   - Part of Project Lilliput, this reduces Java object header sizes from 96–128 bits to 64 bits on 64-bit architectures, decreasing heap usage and improving memory efficiency.
   - Benefit: Reduces memory footprint and enhances data locality for better performance.[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)[](https://www.happycoders.eu/java/java-24-features/)

4. **Generational Shenandoah Garbage Collector (JEP 404)** - Permanent
   - Transitions the Shenandoah GC’s generational mode from experimental to a product feature, improving throughput, load-spike resilience, and memory utilization by dividing objects into young and old generations.
   - Benefit: Enhances performance for demanding workloads.[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)[](https://www.infoworld.com/article/3846172/jdk-25-the-new-features-in-java-25.html)

5. **Module Import Declarations (JEP 494)** - Second Preview
   - Simplifies modular programming by allowing direct import of all packages exported by a module without requiring a `module-info.java` file (e.g., `import module java.sql;`).
   - Benefit: Reduces overhead for lightweight applications and scripting, aiding beginners and rapid prototyping.[](https://codefarm0.medium.com/java-24-features-a-deep-dive-into-whats-coming-81e77382b39c)[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)

6. **Flexible Constructor Bodies (JEP 492)** - Third Preview
   - Allows statements in constructors before `super()` or `this()` calls, enabling field initialization logic to be placed more naturally without auxiliary methods.
   - Benefit: Improves code reliability and readability, especially for subclassing.[](https://www.oracle.com/java/technologies/javase/24-relnote-issues.html)[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)

7. **Key Derivation Function (KDF) API (JEP 487)** - Preview
   - Introduces an API for cryptographic key derivation functions like HMAC-based Extract-and-Expand and Argon2, supporting secure password hashing and interaction with cryptographic hardware.
   - Benefit: Enhances security for applications requiring advanced cryptography.[](https://www.jrebel.com/blog/whats-new-java-24)[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)

8. **Permanently Disable the Security Manager (JEP 486)** - Permanent
   - Removes the Security Manager, deprecated in JDK 17, as it is no longer the primary means of securing Java applications (replaced by container-based sandboxing).
   - Note: Applications relying on the Security Manager may require architectural changes.[](https://www.azul.com/blog/six-jdk-24-features-you-should-know-about/)[](https://www.infoworld.com/article/3830643/the-most-relevant-new-features-in-jdk-24.html)

9. **Late Barrier Expansion for G1 Garbage Collector (JEP 464)** - Permanent
   - Simplifies G1 GC’s barrier implementation by moving expansion later in the compilation pipeline, reducing compilation time and improving maintainability.
   - Benefit: Enhances performance for applications using G1 GC.[](https://www.infoworld.com/article/3491404/jdk-24-the-new-features-in-java-24.html)[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)

10. **Quantum-Resistant Cryptography (JEP 452, 453)** - Preview
    - Introduces Module-Lattice-Based Key Encapsulation Mechanism (ML-KEM) and Digital Signature Algorithm (ML-DSA) to protect against quantum computing attacks.
    - Benefit: Future-proofs Java applications for post-quantum security.[](https://www.infoworld.com/article/3491404/jdk-24-the-new-features-in-java-24.html)[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)

11. **Scoped Values (JEP 480)** - Fourth Preview
    - Enables sharing immutable data within and across threads more safely than thread-local variables, improving concurrency handling.
    - Benefit: Simplifies reasoning about concurrent code.[](https://www.jrebel.com/blog/whats-new-java-24)

12. **Deprecate 32-bit x86 Port (JEP 501)** - Permanent
    - Deprecates the 32-bit x86 port for removal in JDK 25, with the architecture-agnostic Zero port as the alternative for 32-bit systems.
    - Benefit: Reduces maintenance overhead, focusing on modern architectures.[](https://www.infoworld.com/article/3491404/jdk-24-the-new-features-in-java-24.html)[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)

13. **Vector API (JEP 489)** - Ninth Incubator
    - Continues to refine the Vector API for SIMD programming, with enhancements to cross-lane and arithmetic operations.
    - Benefit: Improves performance for compute-intensive applications.[](https://www.infoq.com/news/2025/02/java-24-so-far/)

14. **Linking Run-Time Images without JMODs (JEP 493)** - Permanent
    - Allows the `jlink` tool to create custom run-time images without JMOD files, reducing JDK size by ~25%.
    - Benefit: Enhances deployment efficiency for custom Java runtimes.[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)

### Additional Notes

- **Preview and Experimental Features**: Many features (e.g., Scoped Values, KDF API) are in preview or experimental stages, allowing developers to test and provide feedback before they become permanent in JDK 25 or later. These may change before finalization.[](https://www.jrebel.com/blog/whats-new-java-24)[](https://www.infoq.com/news/2025/02/java-24-so-far/)
- **Project Integration**: JDK 24 introduces elements of OpenJDK Projects like Leyden (startup optimization), Lilliput (memory efficiency), and Panama (native interoperability), laying groundwork for future enhancements.[](https://bell-sw.com/blog/an-overview-of-jdk-24-features/)
- **Security and Deprecation**: Features like the removal of the Security Manager and deprecation of the 32-bit x86 port reflect Oracle’s focus on modernizing Java by phasing out outdated components.[](https://www.azul.com/blog/six-jdk-24-features-you-should-know-about/)[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)

### Conclusion

JDK 24 is a stable, feature-rich release that advances Java’s performance, developer productivity, and security. While not an LTS release, its 24 JEPs offer significant improvements, many of which will be finalized in the upcoming LTS release, JDK 25. Developers can leverage features like Stream Gatherers and Module Import Declarations for immediate productivity gains, while experimental features like Compact Object Headers and Ahead-of-Time Class Loading signal Java’s ongoing optimization for modern workloads. For enterprise use, sticking with LTS releases like JDK 21 or awaiting JDK 25 is recommended due to their extended support.[](https://www.infoworld.com/article/3491404/jdk-24-the-new-features-in-java-24.html)[](https://www.jrebel.com/blog/whats-new-java-24)[](https://www.infoworld.com/article/3830643/the-most-relevant-new-features-in-jdk-24.html)

For more details, visit:

- [Oracle JDK 24 Release Notes](https://www.oracle.com)[](https://www.oracle.com/java/technologies/javase/24-relnote-issues.html)
- [OpenJDK JDK 24](https://openjdk.org)[](https://openjdk.org/projects/jdk/24/)
- [JavaOne 2025 Conference](https://www.oracle.com/javaone) for feature highlights[](https://www.oracle.com/news/announcement/oracle-releases-java-24-2025-03-18/)
