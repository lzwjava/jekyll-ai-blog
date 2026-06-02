---
audio: false
generated: true
lang: en
layout: post
title: Upgrading Legacy Codebase to Newer JDK
translated: false
type: note
---

Upgrading a large codebase (tens of thousands of lines) from JDK 8 and Spring 5.2.2 to a newer JDK like 11, 17, or 21 requires careful planning to minimize disruptions, especially given the use of IBM DB2 JCC drivers, heavy reliance on Spring, and deployment to WebSphere Liberty. Below, I'll outline key considerations, including compatibility, potential breaking changes, migration steps, and recommendations. Since you mentioned you can upgrade Spring as well, I'll cover scenarios where that might be necessary or beneficial.

### General Considerations for JDK Upgrade

- **Backward Compatibility and Breaking Changes**: Java aims for strong backward compatibility, but upgrades from JDK 8 introduce changes that could affect your code:
  - **Removed/Deprecated APIs**: JDK 9+ removed internal APIs like `sun.misc.Unsafe` and some `sun.*` packages. If your code (or dependencies) uses these, you'll need alternatives (e.g., via `Unsafe` alternatives in third-party libs or Java's `VarHandle`).
  - **Module System (JPMS from JDK 9)**: Encapsulates internal APIs, potentially causing "illegal access" errors. Use `--add-opens` or `--add-exports` flags temporarily, but aim to refactor for modularity.
  - **Garbage Collection Changes**: Default GC shifted from Parallel to G1 in JDK 9, and further tweaks in later versions (e.g., Shenandoah or ZGC in 11+). Test for performance impacts on memory-intensive parts.
  - **Other Changes**: Stronger encapsulation, removal of applet/browser plugin support, updates to security managers (deprecated in 17, removed in 21), and language features like records (14+), sealed classes (17), and virtual threads (21). These are mostly additive but could require code tweaks if using reflection heavily.
  - From 8 to 11: Moderate changes (e.g., no more Java EE modules like JAXB, which were removed in 9; add them as dependencies).
  - From 11 to 17: Fewer disruptions, mainly enhancements like better pattern matching.
  - From 17 to 21: Minimal breaking changes; mostly new features like pattern matching for switch (21) and no major removals.
- **Stepwise Migration**: Don't jump directly to 21. Upgrade incrementally (e.g., 8 → 11 → 17 → 21) to isolate issues. Use tools like OpenRewrite or jdeps to scan for incompatibilities.
- **Testing and Tooling**:
  - Run comprehensive tests (unit, integration, load) on the new JDK. Tools like Maven/Gradle plugins (e.g., `maven-enforcer-plugin`) can enforce compatibility.
  - Update build tools: Ensure Maven/Gradle supports the new JDK (most do, but verify plugins like Surefire).
  - Multi-version Testing: Use Docker or CI/CD (e.g., GitHub Actions) to test against multiple JDKs.
- **Dependencies and Libraries**: Scan all third-party libs for compatibility. Use tools like `mvn dependency:tree` or OWASP Dependency-Check.
- **Performance and Security**: Newer JDKs offer better performance (e.g., faster startup in 17+), security fixes, and long-term support (LTS: 11 until 2026, 17 until 2029, 21 until 2031+).
- **Effort for Large Codebase**: With heavy Spring usage, focus on Spring-managed components (e.g., beans, AOP). Budget time for refactoring (e.g., 1-2 weeks per major version jump, scaling with code size).

### Specific Considerations by Target JDK

#### Upgrading to JDK 11

- **Pros**: LTS with good stability; closer to JDK 8, so fewer changes. End-of-life approaching (2026), but still widely supported.
- **Cons**: Misses modern features like virtual threads (21) or improved GC (17+).
- **Spring Compatibility**: Spring 5.2.2 works on JDK 11, but upgrade to Spring 5.3.x (latest in 5.x line) for better JDK 11/17 support and bug fixes. No major Spring changes needed.
- **DB2 JCC Driver**: Compatible with recent driver versions (e.g., 4.x+). Some older drivers had issues with OpenJDK 11, so update to the latest (e.g., from IBM's site) and test connections.
- **WebSphere Liberty**: Fully supported (Liberty runs on JDK 8/11/17/21).
- **Key Changes from JDK 8**:
  - Add dependencies for removed modules (e.g., `javax.xml.bind:jaxb-api` for JAXB).
  - Fix any illegal reflective access (common in older libs).
  - How to Migrate: Update your build file (e.g., Maven `<java.version>11</java.version>`), recompile, and run tests. Use Oracle's JDK 11 Migration Guide for step-by-step checks.
- **Effort**: Low to medium; minimal code changes if no internal API usage.

#### Upgrading to JDK 17

- **Pros**: Current LTS with strong adoption; includes features like text blocks, records, and enhanced switch. Better performance than 11.
- **Cons**: SecurityManager deprecated (if used, plan removal). Some libs might need updates.
- **Spring Compatibility**: Spring 5.3.x fully supports JDK 17 (tested on LTS releases). Upgrade from 5.2.2 to 5.3.x for optimal compatibility—no breaking changes in Spring itself.
- **DB2 JCC Driver**: Explicitly supported in recent versions (e.g., JCC 4.29+ for DB2 11.5). IBM docs confirm JDK 17 runtime support; test for any SQLJ enhancements.
- **WebSphere Liberty**: Fully supported.
- **Key Changes from JDK 11**:
  - Stricter encapsulation; more warnings on deprecated features.
  - New APIs (e.g., `java.net.http` for HTTP/2 clients) can modernize code but aren't mandatory.
  - How to Migrate: After JDK 11, switch to 17 in builds. Use migration guides to check for applet/corba removals (if any).
- **Effort**: Medium; build on JDK 11 migration.

#### Upgrading to JDK 21

- **Pros**: Latest LTS with cutting-edge features (e.g., virtual threads for concurrency, sequenced collections). Best for future-proofing.
- **Cons**: Requires Spring upgrade (see below); potential issues with very old libs.
- **Spring Compatibility**: Spring 5.x does not officially support JDK 21 (max is JDK 17). You must upgrade to Spring 6.1+ (which requires JDK 17+ baseline). This is a major shift:
  - **Jakarta EE Migration**: Spring 6 switches from Java EE (javax.*) to Jakarta EE 9+ (jakarta.*). Change imports (e.g., `javax.servlet` → `jakarta.servlet`), update configs, and refactor any EE-related code (e.g., JPA, Servlets, JMS).
  - **Breaking Changes**: Removed deprecated APIs (e.g., old transaction managers); AOT compilation support; requires updating dependencies like Hibernate (to 6.1+).
  - **Migration Guide**: Follow Spring's official guide: Update to Spring 5.3.x first, then to 6.0/6.1. Use tools like OpenRewrite recipes for automated javax → jakarta swaps. For your large codebase, this could involve hundreds of changes—test in modules.
  - If using Spring Boot (implied by Spring usage), Boot 3.x aligns with Spring 6 and JDK 17+.
- **DB2 JCC Driver**: Compatible via backward compatibility with JDK 17 support; update to latest driver (e.g., 4.32+) and verify.
- **WebSphere Liberty**: Fully supported (up to JDK 24).
- **Key Changes from JDK 17**:
  - SecurityManager removed; if used, replace with alternatives.
  - New features like string templates (preview) won't break existing code.
  - How to Migrate: Build on JDK 17 first, then switch. No major deliberate breaking changes between 17 and 21.
- **Effort**: High if upgrading Spring; otherwise similar to 17.

### Additional Project-Specific Considerations

- **IBM DB2 JCC Library**: Ensure your driver version matches DB2 release (e.g., for DB2 11.5, use JCC 4.29+). Test JDBC connections, SQLJ, and any custom queries—newer JDKs might expose charset or timezone issues.
- **WebSphere Liberty Deployment**: No blockers; Liberty is flexible with JDKs. Update server.xml if needed for JVM args (e.g., `--add-opens` for module issues). Test deployments early.
- **Large Codebase and Spring Usage**: Prioritize modular upgrades (e.g., upgrade core services first). If Spring is deeply integrated (e.g., MVC, Data, Security), audit for deprecated features in 5.2.2. Upgrading Spring brings benefits like better AOT and observability but adds cost.
- **Risks and Mitigations**: Downtime from incompatibilities; mitigate with rollback plans. Budget for vendor support if using commercial DB2/Liberty.
- **Costs**: Time (weeks to months for full migration), potential licensing (e.g., commercial JDKs like Oracle's), and training on new features.

### Recommendations

- **Preferred Path**: Start with JDK 11 or 17 while keeping/upgrading to Spring 5.3.x—lower risk for your codebase. Go to 21 only if you need its features (e.g., virtual threads) and are willing to upgrade to Spring 6 (which could take significant effort due to Jakarta changes).
- **Next Steps**:
  1. Scan code with jdeps/jlink for issues.
  2. Set up a branch for migration testing.
  3. Consult official guides: Oracle JDK Migration Guide, Spring Versions Wiki, IBM DB2 JDBC Downloads, Liberty Java Support.
  4. If upgrading Spring to 6, follow the migration guide for Jakarta changes.

If you provide more details (e.g., specific Spring modules or DB2 version), I can refine this further.
