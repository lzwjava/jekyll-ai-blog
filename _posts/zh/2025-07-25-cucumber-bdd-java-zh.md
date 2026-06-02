---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java开发者Cucumber行为驱动开发指南
translated: true
type: note
---

这是一份实用的端到端 **Cucumber** 指南——它是什么、团队为何使用它，以及如何在 Java 中高效使用它（另附 JS/Python 用户的快速说明）。

---

# Cucumber 是什么（与不是什么）

* **Cucumber** 是一个 **BDD（行为驱动开发）** 测试框架。它允许你用纯文本语言（Gherkin）描述行为，并将这些语句绑定到可执行代码（步骤定义）。
* 当你希望产品、QA 和工程团队达成**共同理解**，并需要**活文档**同时作为测试时，它非常理想。
* 它**并非**单元测试框架（JUnit/TestNG/Jest/PyTest）的替代品。它通过关注**业务级验收测试**来补充它们。

---

# 核心组件

**1) Gherkin（纯文本规范）**

* 写在 `.feature` 文件中。
* 关键词：`Feature`、`Scenario`、`Given/When/Then/And/But`、`Background`、`Scenario Outline` + `Examples`、`@tags`（以及新版本 Gherkin 中可选的 `Rule`）。
* 自然语言风格；支持多语言环境。

**2) 步骤定义（代码）**

* 通过 **Cucumber 表达式**（或正则表达式）将 Gherkin 步骤绑定到代码。
* 可以调用页面对象、API 客户端、服务、数据库助手等。

**3) 运行器**

* 启动 Cucumber，通过胶水路径、配置和标签发现功能和步骤。
* 在 JVM 上，通常通过 **JUnit**（4 或 5）或 **TestNG** 运行。

**4) 报告**

* 生成 HTML/JSON/JUnit XML；与 CI 仪表板和 **Allure** 等工具集成。

---

# 最小示例（Java, Maven）

**pom.xml（关键部分）**

```xml
<dependencies>
  <!-- JUnit 5 -->
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.2</version>
    <scope>test</scope>
  </dependency>

  <!-- Cucumber JVM + JUnit Platform -->
  <dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-java</artifactId>
    <version>7.18.1</version>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-junit-platform-engine</artifactId>
    <version>7.18.1</version>
    <scope>test</scope>
  </dependency>
</dependencies>

<build>
  <plugins>
    <plugin>
      <artifactId>maven-surefire-plugin</artifactId>
      <version>3.2.5</version>
      <configuration>
        <!-- 如果需要，按标签运行、并行运行等 -->
      </configuration>
    </plugin>
  </plugins>
</build>
```

**项目布局**

```
src
 └─ test
     ├─ java
     │   └─ com/example/steps/...
     └─ resources
         └─ features/...
```

**功能文件 (`src/test/resources/features/login.feature`)**

```gherkin
Feature: 登录功能
  作为一名注册用户
  我希望能够登录
  以便我可以访问我的账户

  Background:
    Given 应用程序正在运行

  @smoke
  Scenario: 成功登录
    Given 我在登录页面
    When 我使用用户名 "alice" 和密码 "secret" 登录
    Then 我应该看到 "Welcome, alice"

  Scenario Outline: 登录失败
    Given 我在登录页面
    When 我使用用户名 "<user>" 和密码 "<pass>" 登录
    Then 我应该看到 "Invalid credentials"
    Examples:
      | user  | pass     |
      | alice | wrong    |
      | bob   | invalid  |
```

**步骤定义（Java, Cucumber 表达式）**

```java
package com.example.steps;

import io.cucumber.java.en.*;
import static org.junit.jupiter.api.Assertions.*;

public class LoginSteps {
  private String page;
  private String message;

  @Given("the application is running")
  public void app_running() {
    // 启动测试应用 / 启动服务器 / 重置状态
  }

  @Given("I am on the login page")
  public void i_am_on_the_login_page() {
    page = "login";
  }

  @When("I sign in with username {string} and password {string}")
  public void i_sign_in(String user, String pass) {
    // 调用 UI 或 API；此处模拟：
    if ("alice".equals(user) && "secret".equals(pass)) {
      message = "Welcome, alice";
    } else {
      message = "Invalid credentials";
    }
  }

  @Then("I should see {string}")
  public void i_should_see(String expected) {
    assertEquals(expected, message);
  }
}
```

**JUnit 5 运行器（通过引擎发现）**

```java
// 使用 JUnit Platform 时不需要显式的运行器类。
// 如果需要标签过滤，创建一个测试套件：
import org.junit.platform.suite.api.*;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = "cucumber.glue", value = "com.example.steps")
@ConfigurationParameter(key = "cucumber.plugin", value = "pretty, html:target/cucumber.html, json:target/cucumber.json")
@ExcludeTags("wip") // 示例
public class RunCucumberTest {}
```

运行：

```bash
mvn -q -Dtest=RunCucumberTest test
```

---

# 日常使用的 Gherkin 要点

* **Background**：每个场景的通用设置（例如，“Given 我已登录”）。
* **Scenario Outline + Examples**：无需复制粘贴步骤的数据驱动测试。
* **Doc Strings**：步骤中的多行负载（例如，JSON 主体）。
* **Data Tables**：将步骤中的表格转换为对象或映射。
* **Tags**：为 CI 流水线切片测试套件（`@smoke`、`@api`、`@slow`）。
* **Rule**（可选）：按业务规则对场景进行分组以提高可读性。

---

# Cucumber 表达式（比正则表达式更友好）

* 占位符如 `{string}`、`{int}`、`{word}`、`{float}`。
* **自定义参数类型**允许你解析领域对象：

```java
import io.cucumber.java.ParameterType;

public class ParameterTypes {
  @ParameterType("USD|CNY|EUR")
  public Currency currency(String code) { return Currency.getInstance(code); }
}
```

然后使用：`When I pay 100 {currency}`。

---

# 钩子与测试生命周期

* JVM/JS/Ruby 变体中的 `@Before`、`@After`、`@BeforeStep`、`@AfterStep`。
* 使用钩子进行**清理设置/拆卸**、失败时截图、数据库重置等。
* 对于依赖注入，使用 **Spring** (cucumber-spring) 或 **PicoContainer** 来共享状态：

  * 使用 Spring Boot 时，将步骤类注解为 bean；根据需要使`@SpringBootTest` 进行装配和测试切片。

---

# 你可能需要的集成

* **Web UI**：Selenium/WebDriver、Playwright。封装在**页面对象**中并从步骤调用。
* **API**：REST Assured/HTTP 客户端；使用 JSON 断言进行验证。
* **DB**：Flyway/Liquibase 用于模式管理，测试数据加载器，嵌入式数据库。
* **Mocking**：WireMock/Testcontainers 用于外部系统。
* **报告**：内置 HTML/JSON；**Allure** 用于丰富的时间线和附件。
* **并行**：JUnit Platform（或在旧版本堆栈中使用带有 TestNG 的 `cucumber-jvm-parallel-plugin`）。保持场景隔离；避免共享可变状态。

---

# CI/CD 与扩展

* **基于标签的流水线**：在 PR 上运行 `@smoke`，每日运行 `@regression`，定时运行 `@slow`。
* **跨代理按文件或标签分片**以提高速度。
* **制品**：发布 HTML/JSON/Allure 以及截图/视频（UI）。
* **不稳定测试**：找出根本原因——不要通过“重试直到变绿”来逃避问题。

---

# 良好实践（经过实战检验）

* Gherkin 中**保持统一语调**：保持步骤措辞一致；避免 UI 细节描述（“点击蓝色按钮”）——关注**意图**（“提交凭据”）。
* **薄步骤，厚助手**：步骤代码应委托给页面对象/服务；将逻辑排除在步骤之外。
* **稳定的测试数据**：通过 API/数据库固定装置播种；避免与类生产的随机性耦合。
* **快速、独立的场景**：没有顺序假设；每个场景清理状态。
* **限制套件规模**：将 Cucumber 保留用于**业务行为**；将单元测试保留在 JUnit/TestNG/Jest 中以处理低级细节。

---

# 要避免的反模式

* 将 Cucumber 视为更漂亮的单元测试运行器。
* 过度使用 `And` 和冗长的过程序列（命令式、脆弱）。
* 在步骤措辞中耦合到 CSS 选择器或易变的 UI 细节。
* 隐藏每个场景实际所需内容的庞大 Background。

---

# 其他语言的快速说明

**JavaScript/TypeScript**

* 使用 **`@cucumber/cucumber`**。
* 典型脚本：

  ```bash
  npm i -D @cucumber/cucumber
  npx cucumber-js --require steps/**/*.ts --publish-quiet
  ```

* 与 **Playwright** 和 **Allure** 良好配合。

**Python**

* 使用 **behave**（类 Cucumber）或 **pytest-bdd**。
* 结构和概念相同：功能 + 步骤 + 固定装置。

**Ruby**

* 原始的 Cucumber 实现；习惯用法与 JVM 和 JS 版本类似。

---

# 何时选择 Cucumber

* 你需要非工程师也能读懂的**活文档**。
* 验收标准需要是**可执行的**并且**可追溯**到发布版本。
* 跨职能团队在实现**之前**就行为达成一致（BDD 三人组）。

如果团队不维护 Gherkin，或者测试纯粹是技术性的，而单元/集成测试已经提供了清晰度，则跳过它（或谨慎使用）。

---

如果你告诉我你的技术栈（Spring/Quarkus？REST/UI？部署/CI 方式？），我可以为你勾勒一个可立即运行的 Cucumber 骨架，包括 Maven/Gradle 配置、推荐的插件以及适合你设置的示例流水线。
