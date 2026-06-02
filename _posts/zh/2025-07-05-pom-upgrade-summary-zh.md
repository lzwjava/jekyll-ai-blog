---
audio: false
generated: true
lang: zh
layout: post
title: 升级Maven依赖与插件
translated: true
type: note
---

以下是您 `pom.xml` 中可升级的版本列表，以及截至 2025 年 7 月 5 日的最新可用版本：

**依赖项：**

* `org.junit.jupiter:junit-jupiter-api`
  * 当前版本：`5.9.2`
  * 最新稳定版：`5.13.2`（发布于 2025 年 6 月 24 日）
  * 最新预览版：`6.0.0-M1`（发布于 2025 年 6 月 27 日）- 如需使用里程碑版本请考虑
* `org.junit.jupiter:junit-jupiter-engine`
  * 当前版本：`5.9.2`
  * 最新稳定版：`5.13.2`（发布于 2025 年 6 月 24 日）
  * 最新预览版：`6.0.0-M1`（发布于 2025 年 6 月 27 日）- 如需使用里程碑版本请考虑

**插件：**

* `org.apache.maven.plugins:maven-compiler-plugin`
  * 当前版本：`3.13.0`
  * 最新版本：`3.14.0`（发布于 2025 年 2 月 17 日）
* `org.apache.maven.plugins:maven-jar-plugin`
  * 当前版本：`3.4.2`
  * 最新版本：`3.4.2`（未发现更新的稳定版本。最后发布于 2024 年 6 月 16 日，当前时间为 2025 年 7 月 5 日，因此仍是最新版本）
* `com.diffplug.spotless:spotless-maven-plugin`
  * 当前版本：`2.44.5`
  * 最新版本：`2.44.5`（未发现更新的稳定版本。最后发布于 2025 年 5 月 28 日，因此仍是最新版本）
* `org.apache.maven.plugins:maven-checkstyle-plugin`
  * 当前版本：`3.6.0`
  * 最新版本：`3.6.0`（未发现更新的稳定版本。最后发布于 2024 年 10 月 22 日，因此仍是最新版本）
  * **注意：** 插件配置中的 `checkstyle` 依赖可更新：
    * 当前版本：`10.25.0`
    * 最新版本：`10.26.1`（发布于 2025 年 6 月 29 日）
* `org.apache.maven.plugins:maven-surefire-plugin`
  * 当前版本：`3.0.0-M7`
  * 最新稳定版：`3.5.3`（发布于 2025 年 3 月 27 日）- 这是从里程碑版本的重要跨越
* `org.codehaus.mojo:exec-maven-plugin`
  * 当前版本：`3.5.1`
  * 最新版本：`3.5.1`（未发现更新的稳定版本。最后发布于 2025 年 5 月 27 日，因此仍是最新版本）

**升级摘要：**

* **JUnit Jupiter API：** 5.9.2 → 5.13.2（或 6.0.0-M1）
* **JUnit Jupiter Engine：** 5.9.2 → 5.13.2（或 6.0.0-M1）
* **Maven Compiler Plugin：** 3.13.0 → 3.14.0
* **Checkstyle（插件内依赖）：** 10.25.0 → 10.26.1
* **Maven Surefire Plugin：** 3.0.0-M7 → 3.5.3

**升级前重要注意事项：**

* **破坏性变更：** 请务必检查每个待升级组件的发布说明。主版本升级（如 JUnit 5 到 6，或 Surefire 3.0.0-M7 到 3.5.3）可能引入需要代码修改的破坏性变更
* **兼容性：** 确保新版本与您使用的 Java 版本（当前为 JDK 21）及项目中其他依赖项保持兼容
* **测试：** 升级后请进行全面测试，确保所有功能仍按预期正常运行
