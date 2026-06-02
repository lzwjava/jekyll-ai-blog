---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Karate DSL API 测试指南
translated: true
type: note
---


**问题：** 什么是 Karate DSL——顶级推荐的 API testing framework 的全面介绍？

---

**回答：**

## 什么是 Karate DSL？

Karate 是一个开源工具，它将 API testing、mocks、performance testing 和 UI automation 结合到一个单一的统一框架中。由 Peter Thomas 创建，已成为最广泛采用的 API testing 解决方案之一。由 550+ 家公司使用，包括 Fortune 500 中的 76 家，每月下载量超过 200 万。

---

## 为什么 Karate 与众不同

Karate framework 遵循 Cucumber 风格，使用 BDD 方法编写程序。语法易于非程序员理解，并且它是唯一将 API automation 和 performance testing 结合到单一独立工具中的 API testing 工具。

与 Postman、Mocha 或 Chai 不同，Karate 不需要深厚的编码知识——它由 Peter Thomas 开发，由于其简单性和强大功能，在软件测试社区中获得了广泛采用。

Karate 用户通常在为单个 endpoint 编写测试时节省 80% 的时间，使用 60% 更少的代码，并且测试执行更快，并无缝集成到现有基础设施中。

---

## 核心特性

关键特性包括：

- 原生支持 JSON 和 XML 的优雅 DSL 语法，包括 JsonPath 和 XPath 表达式
- 无需 Java Beans 或 helper code 来表示 payloads 和 HTTP endpoints
- 测试超级易读——scenario 数据可以内联表示，使用人类友好的 JSON、XML 或 Cucumber Scenario Outline 表格
- 全面的 assertion 能力——失败时清楚报告哪个数据元素和路径不符合预期
- 多线程并行执行，这对于 integration 和 end-to-end 测试来说是巨大的时间节省器
- 内置与 Cucumber 兼容的测试报告，包括内联的 HTTP request 和 response logs

Karate 还支持通过重用 Karate test suites 作为 Gatling performance tests 来节省大量努力，这些测试在负载下深入验证服务器响应是否准确。

---

## 无需 Java Step Definitions 的 BDD 语法

Karate 支持标准的 Given–When–Then 关键字，但逻辑内置于其 DSL 中——无需 Java step definitions。

典型的 Karate 测试如下所示：

```gherkin
Feature: Simple API test example
  Scenario: Get user details
    Given url 'https://api.example.com'
    And path 'users', userId
    When method GET
    Then status 200
    And match response.name == 'John Doe'
    And match response.email contains '@example.com'
```

这取自 Karate documentation，展示了测试的干净和可读性。

---

## 项目结构

典型的 Karate 项目结构如下所示：

```
src/test/java
  +-- karate-config.js
  +-- logback-test.xml
  +-- some-reusable.feature
  \-- animals
      +-- AnimalsTest.java
      +-- cats
      |   +-- cats-post.feature
      |   +-- cats-get.feature
      \-- dogs
          +-- dog-crud.feature
          \-- DogsRunner.java
```

---

## `karate-config.js` 文件

启动时，Karate 期望 classpath 上存在名为 `karate-config.js` 的文件，并包含一个 JavaScript 函数。此文件是创建全局作用域变量的地方。Karate 在执行任何 scenario 之前读取此文件。

`karate-config.js` 文件允许您为测试设置全局配置，例如 base URLs、authentication credentials 或自定义函数。它集中化配置设置，促进测试的一致性，尤其适用于管理多个 test scenarios 共享的 variables、headers 和 endpoints。

---

## `.feature` 文件结构

Karate feature file 包含三个核心部分：`Feature`、`Background` 和 `Scenario`。feature 文件包含被测试内容的高级描述、可选的 `Background` 块（用于每个 scenario 之前运行的共享设置），以及单个 `Scenario` 块，每个代表一个测试。

---

## 数据驱动测试

Karate DSL 支持数据驱动测试，允许使用多个数据集测试 APIs。这对于使用各种输入值测试同一 API 特别有用。

内置支持读取 YAML 甚至 CSV 文件，这些文件可以直接用于数据驱动测试。

---

## 使用 Gatling 进行性能测试

Karate DSL 与 Gatling framework 有很好的集成，用于 performance 和 load testing。您只需负责将 load model 定义为 Scala class，相同的 feature files 即可成为您的 performance suites。

---

## 报告

运行测试后，Karate DSL 生成 HTML reports，提供测试结果的全面洞察。这些报告包括测试 scenarios、step outcomes 以及测试期间遇到的任何失败的详细信息。

---

## 设置（Maven Dependency）

要将 Karate 添加到 Maven 项目中，请在 `pom.xml` 中添加以下内容：

```xml
<dependency>
  <groupId>com.intuit.karate</groupId>
  <artifactId>karate-junit5</artifactId>
  <version>1.0.0</version>
  <scope>test</scope>
</dependency>
```

---

## 总结表格

| 特性 | Karate DSL |
|---|---|
| 语言 | Gherkin-style DSL（无需 Java） |
| API 测试 | ✅ 内置 HTTP client |
| Mocking | ✅ 内置 API mocks |
| 性能测试 | ✅ 通过 Gatling 集成 |
| UI 测试 | ✅ 支持 |
| 并行执行 | ✅ 原生支持 |
| 数据驱动 | ✅ CSV、YAML、JSON、Examples |
| 报告 | ✅ 自动生成 HTML reports |
| CI/CD 集成 | ✅ Maven、Gradle、JUnit 5 |

---

**参考资料：**

- [Karate Labs Official Site](https://www.karatelabs.io/)
- [Karate GitHub Repository](https://github.com/karatelabs/karate)
- [Karate Official Docs](https://docs.karatelabs.io/)
- [Karate Framework Tutorial – SoftwareTestingHelp](https://www.softwaretestinghelp.com/api-testing-with-karate-framework/)
- [Karate DSL Framework Overview – Perficient](https://blogs.perficient.com/2023/09/28/karate-dsl-framework-overview/)
- [Mastering API Testing with Karate DSL – Medium](https://medium.com/@sujit.code90/mastering-api-testing-with-karate-dsl-c2005d8ae588)
- [File Structure and Best Practices in Karate DSL – Perficient](https://blogs.perficient.com/2025/07/16/technical-deep-dive-file-structure-and-best-practices-in-karate-dsl/)
- [REST API Testing with Karate – Baeldung](https://www.baeldung.com/karate-rest-api-testing)
- [Introduction to Karate, Project Setup – Kloia](https://www.kloia.com/blog/step-1-introduction-to-karate-project-setup-hello-world)
