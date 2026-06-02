---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 混合式Java开发策略
translated: true
type: note
---

简短总结：对于大型Java代码库，**混合方案**效果最佳。将**VS Code**作为AI优先的操作平台（Claude Code + Copilot = 更快的迭代和样板代码处理），同时保留**IntelliJ IDEA**用于"精密手术"（深度重构、代码检查、高级Spring/Gradle/Maven向导）。您不必固守单一选择。🙂

我的思考框架如下——无需表格，直击核心：

### VS Code的闪光点

* **AI工作流**：Copilot的内联补全在VS Code中表现最佳，Claude Code的仓库级推理也更为迅捷。非常适合编写服务、测试、映射器、SQL和快速重设计
* **轻量模块化**：按需装配扩展。在大型单体仓库中冷启动和内存占用更友好
* **跳转功能+LSP**：配合Java扩展，"转到定义/实现"、类型层次结构、调用层次结构和符号搜索足以满足日常需求

推荐扩展（按ID搜索）：

* `vscjava.vscode-java-pack`（包含以下多数扩展）
* `redhat.java`（Java语言支持）
* `vscjava.vscode-java-debug` / `vscjava.vscode-java-test`
* `vscjava.vscode-maven` / `vscjava.vscode-gradle`
* `vscjava.vscode-spring-boot-dashboard` + `vscjava.vscode-spring-initializr`
* `sonarsource.sonarlint-vscode`（静态检查）
* `streetsidesoftware.code-spell-checker`（在JavaDocs中意外实用）
* Claude Code + GitHub Copilot

大型项目性能优化（放入`.vscode/settings.json`）：

```json
{
  "java.maxConcurrentBuilds": 4,
  "java.jdt.ls.vmargs": "-Xms512m -Xmx4g -XX:+UseG1GC -XX:+UseStringDeduplication",
  "java.errors.incompleteClasspath.severity": "ignore",
  "java.referencesCodeLens.enabled": false,
  "java.implementationsCodeLens.enabled": false,
  "files.watcherExclude": {
    "**/target/**": true,
    "**/.gradle/**": true,
    "**/node_modules/**": true
  }
}
```

实用技巧：

* 使用**Gradle**或**Maven**导入（尽量避免混合构建）
* 启用**Spring Boot仪表板**进行多服务运行/调试
* 让Claude/Copilot起草类和测试，但要用**SonarLint**和单元测试作为安全护栏

### IntelliJ IDEA的持续优势

* **重构深度与精度**：跨大型层次结构的重命名/移动/提取，泛型密集型API、Lombok、XML配置，甚至Spring Bean装配——IDEA的语义模型难以超越
* **代码检查与快速修复**：内置代码检查（及结构化搜索/替换）能发现比大多数VS Code设置更细微的代码异味
* **UML与导航优化**：数据流向追踪、依赖关系图和高级搜索范围在复杂领域中节省时间

实用模式：

* 在VS Code中使用Claude/Copilot进行**探索+脚手架搭建+重复编辑**
* 需要**非简单重构**时（如拆分核心模块、跨40个模块修改API合约、迁移Spring配置），在IDEA中打开同一仓库，完成索引后安全重构，推送后返回VS Code

### 关于"Codex"

OpenAI旧的**Codex**模型早已停用。当前主要使用**GitHub Copilot**（底层由OpenAI驱动）和**Claude Code**。可将"Codex"视为历史产物——现有技术栈应为**Copilot + Claude Code**

### VS Code中的静态分析与质量保障

* **SonarLint**在VS Code中提供近似IDEA的体验；可搭配CI流水线中的SonarQube/SonarCloud质量门禁
* 通过Gradle/Maven插件集成**SpotBugs**和**Checkstyle**，确保质量检查在CI中运行（不限于本地）
* 使用**JUnit**测试探索器和**Coverage Gutters**扩展保持紧密的红绿循环

### Spring/企业级特性支持

* VS Code的**Spring工具集**适用于运行/调试、执行器端点和属性提示。遇到复杂自动配置或元注解时，IDEA的解析仍然更可靠——当注解显得"神秘"时可切换使用
* 对于**Gradle**多模块大型项目：保持守护进程+并行构建，考虑使用复合构建限制工作区大小

### 可扩展的AI工作流

* **Copilot内联补全**用于输入时的微调
* **Claude Code**对话用于仓库级推理（"如果修改`LedgerPosting`的构造函数会有什么副作用？"/"起草PR用resilience4j替换自定义重试逻辑"）
* 要求模型生成**重构计划+检查清单**；然后通过可评审的小提交应用更改
* **对模型输出进行测试**：要求AI生成的PR必须包含单元/集成测试变更

### 那么...应该以哪个为主？

* 如果日常工作以**编码+迭代+大量AI辅助**为主 → 当前选择**VS Code**作为主要编辑器体验更佳
* 如果日常工作以**架构设计+大型重构+调试框架边界问题**为主 → 保留**IntelliJ**应对这些场景
* 许多资深工程师会两者兼顾。这并非低效，而是根据风险级别使用合适工具

如果需要，我可以为您量身定制：
- 针对单体仓库的**VS Code Java启动套件**（extensions.json、settings.json、推荐任务/启动配置）
- 用于"调用重型机械"场景的IDEA快捷检查清单
