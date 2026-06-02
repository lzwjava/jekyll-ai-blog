---
audio: false
generated: true
lang: zh
layout: post
title: 升级遗留代码库至新版JDK
translated: true
type: note
---

将大型代码库（数万行代码）从 JDK 8 和 Spring 5.2.2 升级到较新的 JDK（如 11、17 或 21）需要周密规划，特别是考虑到项目中使用了 IBM DB2 JCC 驱动、深度依赖 Spring 框架且需部署至 WebSphere Liberty。以下将详细阐述关键考量因素，包括兼容性、潜在破坏性变更、迁移步骤和建议方案。鉴于您提及可同步升级 Spring，我将涵盖可能需要或有益于升级 Spring 的场景。

### JDK 升级通用考量
- **向后兼容性与破坏性变更**：Java 虽注重向后兼容，但从 JDK 8 升级仍可能引发问题：
  - **移除/废弃的 API**：JDK 9+ 移除了内部 API（如 `sun.misc.Unsafe` 和部分 `sun.*` 包）。若代码（或依赖库）使用了这些 API，需采用替代方案（如第三方库的 `Unsafe` 替代方案或 Java 的 `VarHandle`）。
  - **模块系统（JPMS，JDK 9 引入）**：封装了内部 API，可能导致“非法访问”错误。可临时使用 `--add-opens` 或 `--add-exports` 参数，但最终需重构以实现模块化。
  - **垃圾回收机制变更**：JDK 9 后默认 GC 从 Parallel 改为 G1，后续版本（如 11+）进一步优化（如 Shenandoah 或 ZGC）。需针对内存密集型组件测试性能影响。
  - **其他变更**：更强的封装性、移除了 Applet/浏览器插件支持、安全管理器更新（17 版本废弃，21 版本移除）以及语言特性（如 14+ 的 record、17 的密封类、21 的虚拟线程）。这些多为增强性变更，但若大量使用反射则可能需要代码调整。
  - 从 8 到 11：中度变更（如移除了 Java EE 模块 JAXB，需手动添加依赖）。
  - 从 11 到 17：变更较少，主要是模式匹配等增强功能。
  - 从 17 到 21：几乎无破坏性变更，主要为 switch 模式匹配（21）等新特性。
- **渐进式迁移**：避免直接升级至 21，建议分阶段（如 8 → 11 → 17 → 21）以隔离问题。可使用 OpenRewrite 或 jdeps 等工具扫描兼容性问题。
- **测试与工具链**：
  - 在新 JDK 上运行全面测试（单元、集成、负载测试）。可使用 Maven/Gradle 插件（如 `maven-enforcer-plugin`）确保兼容性。
  - 更新构建工具：确保 Maven/Gradle 支持新 JDK（多数工具已支持，但需验证 Surefire 等插件）。
  - 多版本测试：使用 Docker 或 CI/CD（如 GitHub Actions）进行多 JDK 版本测试。
- **依赖项与第三方库**：扫描所有第三方库的兼容性，可使用 `mvn dependency:tree` 或 OWASP Dependency-Check 等工具。
- **性能与安全**：新版 JDK 提供更优性能（如 17+ 的更快启动速度）、安全修复和长期支持（LTS：11 支持至 2026 年，17 至 2029 年，21 至 2031 年以后）。
- **大型代码库工作量评估**：对于重度使用 Spring 的项目，需重点关注 Spring 管理的组件（如 Bean、AOP）。应为重构预留时间（例如每个主版本升级需 1-2 周，具体取决于代码规模）。

### 各目标 JDK 版本的特殊考量
#### 升级至 JDK 11
- **优势**：LTS 版本稳定性高；更接近 JDK 8，变更较少。虽临近生命周期终点（2026 年），但仍有广泛支持。
- **劣势**：缺少虚拟线程（21）和改进版 GC（17+）等现代特性。
- **Spring 兼容性**：Spring 5.2.2 支持 JDK 11，但建议升级至 Spring 5.3.x（5.x 最新系列）以获得更好的 JDK 11/17 支持和错误修复。无需对 Spring 进行重大变更。
- **DB2 JCC 驱动**：兼容近期驱动版本（如 4.x+）。早期驱动与 OpenJDK 11 存在兼容问题，建议更新至最新版本（从 IBM 官网获取）并测试连接。
- **WebSphere Liberty**：完全兼容（Liberty 支持 JDK 8/11/17/21）。
- **JDK 8 到 11 的关键变更**：
  - 为移除的模块添加依赖（如 JAXB 需添加 `javax.xml.bind:jaxb-api`）。
  - 修复非法反射访问（常见于旧版库）。
  - 迁移步骤：更新构建文件（如 Maven 的 `<java.version>11</java.version>`），重新编译并运行测试。参考 Oracle 的 JDK 11 迁移指南进行逐步检查。
- **工作量**：低至中度；若无内部 API 使用，代码变更极少。

#### 升级至 JDK 17
- **优势**：当前 LTS 版本，采用率高；包含文本块、record、增强 switch 等特性。性能优于 JDK 11。
- **劣势**：SecurityManager 已废弃（若使用需规划替代方案）。部分库可能需要更新。
- **Spring 兼容性**：Spring 5.3.x 完全支持 JDK 17（已通过 LTS 版本测试）。从 5.2.2 升级至 5.3.x 可实现最佳兼容性——Spring 自身无破坏性变更。
- **DB2 JCC 驱动**：新版驱动（如 JCC 4.29+ for DB2 11.5）明确支持。IBM 文档确认 JDK 17 运行时支持；需测试 SQLJ 增强功能。
- **WebSphere Liberty**：完全兼容。
- **JDK 11 到 17 的关键变更**：
  - 更强的封装性；对废弃功能发出更多警告。
  - 新增 API（如 `java.net.http` 用于 HTTP/2 客户端）可优化代码，但非强制要求。
  - 迁移步骤：在完成 JDK 11 迁移后，切换至 17 进行构建。使用迁移指南检查 Applet/CORBA 移除情况（若适用）。
- **工作量**：中度；基于 JDK 11 迁移成果推进。

#### 升级至 JDK 21
- **优势**：最新 LTS 版本，具备前沿特性（如用于并发的虚拟线程、序列化集合）。最适合长期规划。
- **劣势**：需升级 Spring（详见下文）；极旧库可能存在兼容问题。
- **Spring 兼容性**：Spring 5.x 不官方支持 JDK 21（最高支持 JDK 17）。必须升级至 Spring 6.1+（要求 JDK 17+ 基准）。此为重大变更：
  - **Jakarta EE 迁移**：Spring 6 从 Java EE（javax.*）切换至 Jakarta EE 9+（jakarta.*）。需修改导入（如 `javax.servlet` → `jakarta.servlet`）、更新配置并重构所有 EE 相关代码（如 JPA、Servlets、JMS）。
  - **破坏性变更**：移除废弃 API（如旧事务管理器）；支持 AOT 编译；需更新 Hibernate（至 6.1+）等依赖。
  - **迁移指南**：遵循 Spring 官方指南：先升级至 Spring 5.3.x，再升级至 6.0/6.1。使用 OpenRewrite 等工具自动完成 javax → jakarta 转换。对于大型代码库，可能涉及数百处变更——建议分模块测试。
  - 若使用 Spring Boot（根据 Spring 使用情况推断），Boot 3.x 与 Spring 6 和 JDK 17+ 对齐。
- **DB2 JCC 驱动**：通过向后兼容性支持 JDK 17，兼容性有保障；建议更新至最新驱动（如 4.32+）并验证。
- **WebSphere Liberty**：完全兼容（最高支持 JDK 24）。
- **JDK 17 到 21 的关键变更**：
  - SecurityManager 已移除；若使用需替换为替代方案。
  - 字符串模板（预览功能）等新特性不会破坏现有代码。
  - 迁移步骤：先基于 JDK 17 构建，再切换至 21。17 到 21 无重大故意破坏性变更。
- **工作量**：若升级 Spring 则为高度；否则与 17 相似。

### 项目特殊考量
- **IBM DB2 JCC 库**：确保驱动版本与 DB2 发行版匹配（如 DB2 11.5 需使用 JCC 4.29+）。测试 JDBC 连接、SQLJ 及自定义查询——新版 JDK 可能暴露字符集或时区问题。
- **WebSphere Liberty 部署**：无阻碍；Liberty 对 JDK 兼容性灵活。若需处理模块问题，可更新 server.xml 中的 JVM 参数（如 `--add-opens`）。建议尽早测试部署。
- **大型代码库与 Spring 使用**：优先采用模块化升级（如先升级核心服务）。若 Spring 深度集成（如 MVC、Data、Security），需审计 5.2.2 中已废弃的功能。升级 Spring 可带来更好的 AOT 和可观测性，但会增加成本。
- **风险与缓解**：不兼容可能导致停机；需制定回滚计划。若使用商业版 DB2/Liberty，应预留供应商支持预算。
- **成本**：时间成本（完整迁移需数周至数月）、潜在许可成本（如 Oracle 商业版 JDK）及新特性培训成本。

### 建议方案
- **推荐路径**：从 JDK 11 或 17 开始，同时保持/升级至 Spring 5.3.x——对代码库风险较低。仅当需要 JDK 21 特性（如虚拟线程）且愿意升级至 Spring 6（因 Jakarta 变更可能耗费大量精力）时，再升级至 21。
- **后续步骤**：
  1. 使用 jdeps/jlink 扫描代码问题。
  2. 建立专门分支进行迁移测试。
  3. 参考官方指南：Oracle JDK 迁移指南、Spring 版本维基、IBM DB2 JDBC 下载、Liberty Java 支持文档。
  4. 若升级至 Spring 6，遵循 Jakarta 变更的迁移指南。

若您能提供更多细节（如具体 Spring 模块或 DB2 版本），我可进一步细化建议。
