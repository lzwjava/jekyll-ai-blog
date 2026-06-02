---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cucumber BDD Guide for Java Devs
translated: false
type: note
---

Here’s a practical, end-to-end introduction to **Cucumber**—what it is, why teams use it, and how to get productive with it in Java (plus quick notes for JS/Python users).

---

# What Cucumber is (and isn’t)

* **Cucumber** is a **BDD (Behavior-Driven Development)** test framework. It lets you describe behavior in plain language (Gherkin) and bind those sentences to executable code (step definitions).
* It’s ideal when you want **shared understanding** across product, QA, and engineering, and **living documentation** that doubles as tests.
* It is **not** a replacement for unit testing frameworks (JUnit/TestNG/Jest/PyTest). It complements them by focusing on **business-level acceptance tests**.

---

# Core pieces

**1) Gherkin (plain-text specs)**

* Written in `.feature` files.
* Keywords: `Feature`, `Scenario`, `Given/When/Then/And/But`, `Background`, `Scenario Outline` + `Examples`, `@tags`, (and optionally `Rule` in newer Gherkin).
* Natural-language style; supports many locales.

**2) Step Definitions (code)**

* Bind Gherkin steps to code via **Cucumber Expressions** (or regex).
* Can call page objects, API clients, services, DB helpers, etc.

**3) Runner**

* Starts Cucumber, discovers features/steps by glue paths, config, and tags.
* On the JVM, you typically run via **JUnit** (4 or 5) or **TestNG**.

**4) Reports**

* Generate HTML/JSON/JUnit XML; integrate with CI dashboards and tools like **Allure**.

---

# Minimal example (Java, Maven)

**pom.xml (key bits)**

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
        <!-- run by tag, parallel, etc., if needed -->
      </configuration>
    </plugin>
  </plugins>
</build>
```

**Project layout**

```
src
 └─ test
     ├─ java
     │   └─ com/example/steps/...
     └─ resources
         └─ features/...
```

**A feature file (`src/test/resources/features/login.feature`)**

```gherkin
Feature: Login
  As a registered user
  I want to sign in
  So that I can access my account

  Background:
    Given the application is running

  @smoke
  Scenario: Successful login
    Given I am on the login page
    When I sign in with username "alice" and password "secret"
    Then I should see "Welcome, alice"

  Scenario Outline: Failed login
    Given I am on the login page
    When I sign in with username "<user>" and password "<pass>"
    Then I should see "Invalid credentials"
    Examples:
      | user  | pass     |
      | alice | wrong    |
      | bob   | invalid  |
```

**Step definitions (Java, Cucumber Expressions)**

```java
package com.example.steps;

import io.cucumber.java.en.*;
import static org.junit.jupiter.api.Assertions.*;

public class LoginSteps {
  private String page;
  private String message;

  @Given("the application is running")
  public void app_running() {
    // bootstrap test app / start server / reset state
  }

  @Given("I am on the login page")
  public void i_am_on_the_login_page() {
    page = "login";
  }

  @When("I sign in with username {string} and password {string}")
  public void i_sign_in(String user, String pass) {
    // call UI or API; here fake it:
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

**JUnit 5 runner (discovery by engine)**

```java
// No explicit runner class needed with JUnit Platform.
// Create a test suite if you want tag filtering:
import org.junit.platform.suite.api.*;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = "cucumber.glue", value = "com.example.steps")
@ConfigurationParameter(key = "cucumber.plugin", value = "pretty, html:target/cucumber.html, json:target/cucumber.json")
@ExcludeTags("wip") // example
public class RunCucumberTest {}
```

Run:

```bash
mvn -q -Dtest=RunCucumberTest test
```

---

# Gherkin essentials you’ll use daily

* **Background**: common setup once per scenario (e.g., “Given I’m logged in”).
* **Scenario Outline + Examples**: data-driven tests without copy-pasting steps.
* **Doc Strings**: multiline payloads (e.g., JSON bodies) in steps.
* **Data Tables**: transform a step’s table into objects or maps.
* **Tags**: slice the suite (`@smoke`, `@api`, `@slow`) for CI pipelines.
* **Rule** (optional): group scenarios by a business rule for readability.

---

# Cucumber Expressions (friendlier than regex)

* Placeholders like `{string}`, `{int}`, `{word}`, `{float}`.
* **Custom parameter types** let you parse domain objects:

```java
import io.cucumber.java.ParameterType;

public class ParameterTypes {
  @ParameterType("USD|CNY|EUR")
  public Currency currency(String code) { return Currency.getInstance(code); }
}
```

Then use: `When I pay 100 {currency}`.

---

# Hooks & test lifecycle

* `@Before`, `@After`, `@BeforeStep`, `@AfterStep` in JVM/JS/Ruby variants.
* Use hooks for **clean setup/teardown**, screenshots on failure, DB resets, etc.
* For DI, use **Spring** (cucumber-spring) or **PicoContainer** to share state:

  * With Spring Boot, annotate step classes as beans; use `@SpringBootTest` for wiring and test slices as needed.

---

# Integrations you’ll likely want

* **Web UI**: Selenium/WebDriver, Playwright. Wrap in **Page Objects** and call from steps.
* **API**: REST Assured/HTTP clients; validate with JSON assertions.
* **DB**: Flyway/Liquibase for schema, test data loaders, embedded DBs.
* **Mocking**: WireMock/Testcontainers for external systems.
* **Reporting**: built-in HTML/JSON; **Allure** for rich timelines and attachments.
* **Parallel**: JUnit Platform (or the `cucumber-jvm-parallel-plugin` with TestNG in older stacks). Keep scenarios isolated; avoid shared mutable state.

---

# CI/CD & scaling

* **Tag-based pipelines**: run `@smoke` on PRs, daily `@regression`, cron `@slow`.
* **Shard by file or tag** across agents for speed.
* **Artifacts**: publish HTML/JSON/Allure and screenshots/videos (UI).
* **Flaky tests**: root cause them—don’t “retry to green” your way out.

---

# Good practices (battle-tested)

* **One voice** in Gherkin: keep step phrasing consistent; avoid UI chatter (“click the blue button”)—focus on **intent** (“submit credentials”).
* **Thin steps, thick helpers**: step code should delegate to page objects/services; keep logic out of steps.
* **Stable test data**: seed via APIs/DB fixtures; avoid coupling to production-like randomness.
* **Fast, independent scenarios**: no ordering assumptions; clean state per scenario.
* **Limit the suite size**: reserve Cucumber for **business behavior**; keep unit tests in JUnit/TestNG/Jest for low-level details.

---

# Anti-patterns to avoid

* Treating Cucumber as a prettier unit test runner.
* Overusing `And` with long procedural sequences (imperative, brittle).
* Coupling to CSS selectors or volatile UI details in step wording.
* Giant Backgrounds that hide what each scenario actually needs.

---

# Quick notes for other languages

**JavaScript/TypeScript**

* Use **`@cucumber/cucumber`**.
* Typical scripts:

  ```bash
  npm i -D @cucumber/cucumber
  npx cucumber-js --require steps/**/*.ts --publish-quiet
  ```
* Plays nicely with **Playwright** and **Allure**.

**Python**

* Use **behave** (Cucumber-like) or **pytest-bdd**.
* Structure and concepts are the same: features + steps + fixtures.

**Ruby**

* Original Cucumber implementation; idioms mirror the JVM and JS versions.

---

# When to choose Cucumber

* You want **living documentation** readable by non-engineers.
* Acceptance criteria need to be **executable** and **traceable** to releases.
* Cross-functional teams agree on behavior **before** implementation (BDD triads).

Skip it (or use sparingly) if the team won’t maintain Gherkin, or if tests are purely technical where unit/integration tests already deliver clarity.

---

If you tell me your stack (Spring/Quarkus? REST/UI? how you deploy/CI?), I can sketch a ready-to-run Cucumber skeleton with Maven/Gradle, recommended plugins, and a sample pipeline that fits your setup.
