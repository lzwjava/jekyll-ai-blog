---
audio: false
generated: true
lang: zh
layout: post
title: 开发提示
translated: true
type: note
---

以下是与您提及主题相关的各类开发工程师任务常用提示词：**在 Visual Studio Code 中使用 GitHub Copilot**、**在 Visual Studio Code 中调试 Spring Boot 应用程序**、**IBM Db2 数据库中的锁定机制**、**在 VSCode 中配置 Spring Boot 的 launch.json** 以及 **为 WebSphere Liberty 指定 JDK**。这些提示词遵循常见模式，例如配置路径、启用详细输出，并涉及调试、优化和安全等编程的不同方面。它们设计灵活，可根据具体需求进行调整。

---

### 在 Visual Studio Code 中使用 GitHub Copilot
这些提示词帮助您在 Visual Studio Code (VSCode) 中利用 GitHub Copilot 进行编码、调试和理解任务：

- **代码生成**
  - "生成一个计算数字阶乘的 Python 函数。"
  - "创建一个包含用户名和密码字段的 React 登录组件。"

- **代码重构**
  - "重构此代码，使用 async/await 替代 Promise。"
  - "将这个大型函数拆分为更小、可复用的辅助函数。"

- **理解代码**
  - "解释这段代码的作用：[粘贴代码片段]。"
  - "这个变量在程序上下文中的用途是什么？"

- **调试辅助**
  - "针对此错误建议修复方案：[粘贴错误信息]。"
  - "如何添加日志记录来追踪此函数的执行流程？"

---

### 在 Visual Studio Code 中调试 Spring Boot 应用程序
这些提示词专注于在 VSCode 中设置和排查 Spring Boot 应用程序的调试问题：

- **设置调试**
  - "如何在 VSCode 中设置 launch.json 来调试 Spring Boot 应用程序？"
  - "展示如何在 VSCode 中的 Spring Boot 控制器内添加断点。"

- **问题排查**
  - "为什么我的 Spring Boot 应用在 VSCode 的调试模式下启动失败？"
  - "调试 Spring Boot 应用时如何检查变量值？"

- **详细输出**
  - "如何在 Spring Boot 调试会话中启用详细日志记录？"
  - "展示如何在 VSCode 中为异常配置详细堆栈跟踪。"

- **高级调试**
  - "如何在 VSCode 中对 Spring Boot 应用使用条件断点？"
  - "调试多线程 Spring Boot 应用的最佳方式是什么？"

---

### IBM Db2 数据库中的锁定机制
这些提示词帮助您理解和管理 IBM Db2 中的锁定机制：

- **理解锁定**
  - "IBM Db2 中有哪些不同的锁类型？"
  - "Db2 如何处理行级锁与表级锁？"

- **管理锁**
  - "如何检查 IBM Db2 数据库中的活动锁？"
  - "在 Db2 中可以采取哪些步骤防止锁争用？"

- **问题排查**
  - "如何识别和解决 IBM Db2 中的死锁？"
  - "为什么我的 Db2 查询在等待锁，如何解决？"

- **详细输出**
  - "如何在 Db2 日志中启用详细的锁信息？"
  - "展示如何配置 Db2 输出锁等待详情。"

---

### 在 VSCode 中配置 Spring Boot 的 launch.json
这些提示词协助设置和排查 VSCode 中 Spring Boot 应用程序的 `launch.json` 文件：

- **基础配置**
  - "提供 VSCode 中 Spring Boot 应用的基础 launch.json 示例。"
  - "如何在 launch.json 中为 Spring Boot 项目设置主类？"

- **路径配置**
  - "如何在 launch.json 中配置 Spring Boot 调试的 JDK 路径？"
  - "展示如何在 launch.json 中指定项目路径。"

- **高级配置**
  - "如何在 launch.json 中添加调试用的环境变量？"
  - "在 VSCode 中远程调试 Spring Boot 应用的设置是什么？"

- **问题排查**
  - "为什么 VSCode 提示 '找不到主类'，尽管我的 launch.json 配置正确？"
  - "如何修复 launch.json 中的 '调试器未附加' 问题？"

---

### 为 WebSphere Liberty 指定 JDK
这些提示词帮助配置和排查 WebSphere Liberty 的 JDK：

- **路径配置**
  - "如何在环境中设置 WebSphere Liberty 的 JDK 路径？"
  - "展示如何将 WebSphere Liberty 更新至使用 JDK 11。"

- **问题排查**
  - "为什么 WebSphere Liberty 未检测到我安装的 JDK？"
  - "如何检查 WebSphere Liberty 正在使用的 JDK 版本？"

- **详细输出**
  - "如何在 WebSphere Liberty 中启用详细的 JDK 日志记录？"
  - "哪个命令可以显示 Liberty 中的详细 JDK 启动信息？"

- **最佳实践**
  - "WebSphere Liberty 推荐使用哪些 JDK 版本？"
  - "如何确保我的应用在 Liberty 中使用正确的 JDK？"

---

### 通用编程提示模式
这些提示词涵盖跨编程任务的常见模式，例如配置、详细输出以及其他方面如优化和安全：

- **路径配置**
  - "如何在 [环境] 中配置 [工具/库] 的路径？"
  - "展示如何设置 [应用/框架] 的类路径。"

- **详细输出**
  - "如何为 [工具/应用] 启用详细日志记录？"
  - "如何从 [命令/进程] 获取详细输出？"

- **调试**
  - "建议调试此问题的步骤：[描述问题]。"
  - "如何在 [语言/框架] 中追踪执行流程？"

- **性能优化**
  - "如何优化此代码以加快执行速度？"
  - "在 [应用] 中减少内存使用的方法有哪些？"

- **安全**
  - "如何保护 [应用/组件] 免受 [漏洞] 影响？"
  - "[技术] 的安全最佳实践是什么？"

---

这些提示词实用、可复用，并针对您指定的任务量身定制。您可以通过添加具体细节（例如错误信息、代码片段或工具版本）来调整它们，以适应项目需求。无论您是用 GitHub Copilot 编码、调试 Spring Boot、管理 Db2 锁、配置 VSCode，还是设置 WebSphere Liberty，这些提示词都将帮助简化开发工作流程。
