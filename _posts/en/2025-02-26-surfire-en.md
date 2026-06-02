---
audio: false
generated: true
lang: en
layout: post
title: Maven Surefire Plugin
translated: false
type: note
---

Below is an explanation of the **Maven Surefire Plugin**, which is a key component in Maven-based projects for running unit tests during the build process. This explanation covers its purpose, configuration, usage, and customization options.

---

## What is the Maven Surefire Plugin?

The **Maven Surefire Plugin** is a plugin in Apache Maven designed to execute unit tests during the build lifecycle. It integrates seamlessly with Maven’s `test` phase and is automatically triggered when you run commands like `mvn test`, `mvn package`, or `mvn install`. The plugin supports popular test frameworks such as JUnit (versions 3, 4, and 5) and TestNG, and it generates test reports to help developers assess test outcomes.

### Key Features
- Runs tests in a separate JVM process for isolation.
- Supports multiple test frameworks (JUnit, TestNG, etc.).
- Generates test reports in formats like XML and plain text.
- Offers flexibility to skip tests, run specific tests, or customize execution.

---

## Basic Setup in `pom.xml`

The Surefire Plugin is included by default in Maven’s build lifecycle, so you don’t need to configure it for basic use. However, you can explicitly declare it in your `pom.xml` file to specify a version or customize its behavior.

### Minimal Configuration
If you don’t add any configuration, Maven uses the plugin with default settings:
- Tests are located in `src/test/java`.
- Test files follow naming patterns like `**/*Test.java`, `**/Test*.java`, or `**/*Tests.java`.

### Explicit Declaration
To customize the plugin or ensure a specific version, add it to the `<build><plugins>` section of your `pom.xml`. Here’s an example:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M5</version> <!-- Use the latest version -->
        </plugin>
    </plugins>
</build>
```

---

## Running Tests with Surefire

The plugin is tied to the `test` phase of the Maven lifecycle. Here’s how to use it:

### Run All Tests
To execute all unit tests, run:

```
mvn test
```

### Run Tests in a Larger Build
Tests are automatically executed when you run commands that include the `test` phase, such as:

```
mvn package
mvn install
```

### Skip Tests
You can skip test execution using command-line flags:
- **Skip running tests**: `-DskipTests`
  ```
  mvn package -DskipTests
  ```
- **Skip test compilation and execution**: `-Dmaven.test.skip=true`
  ```
  mvn package -Dmaven.test.skip=true
  ```

---

## Customizing the Surefire Plugin

You can tailor the plugin’s behavior by adding a `<configuration>` section in the `pom.xml`. Here are some common customizations:

### Include or Exclude Specific Tests
Specify which tests to run or skip using patterns:
```xml
<configuration>
    <includes>
        <include>**/My*Test.java</include>
    </includes>
    <excludes>
        <exclude>**/SlowTest.java</exclude>
    </excludes>
</configuration>
```

### Run Tests in Parallel
Speed up execution by running tests concurrently:
```xml
<configuration>
    <parallel>methods</parallel>
    <threadCount>2</threadCount>
</configuration>
```
*Note*: Ensure your tests are thread-safe before enabling this.

### Pass System Properties
Set properties for the test JVM:
```xml
<configuration>
    <systemPropertyVariables>
        <propertyName>propertyValue</propertyName>
    </systemPropertyVariables>
</configuration>
```

### Generate Reports
By default, reports are saved in `target/surefire-reports`. For an HTML report, use the `maven-surefire-report-plugin`:
```xml
<reporting>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-report-plugin</artifactId>
            <version>3.0.0-M5</version>
        </plugin>
    </plugins>
</reporting>
```
Run `mvn surefire-report:report` to generate the HTML report.

---

## Handling Test Failures

### Fail the Build on Test Failure
By default, a failing test causes the build to fail. To ignore failures and continue:
```
mvn test -Dmaven.test.failure.ignore=true
```

### Rerun Failed Tests
Handle flaky tests by retrying failures:
```xml
<configuration>
    <rerunFailingTestsCount>2</rerunFailingTestsCount>
</configuration>
```
This reruns failed tests up to 2 times.

---

## Using Surefire with Test Frameworks

The plugin supports various test frameworks with minimal setup:

### JUnit 4
No extra configuration is needed; Surefire detects JUnit 4 tests automatically.

### JUnit 5
Add the JUnit 5 dependency:
```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.8.1</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```
Use Surefire version 2.22.0 or later for full support.

### TestNG
Add the TestNG dependency:
```xml
<dependencies>
    <dependency>
        <groupId>org.testng</groupId>
        <artifactId>testng</artifactId>
        <version>7.4.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```
Surefire will automatically run TestNG tests.

---

## Key Notes

- **Test Location**: Tests should be in `src/test/java`, with resources in `src/test/resources`.
- **Naming Conventions**: Default patterns include `**/*Test.java`, `**/Test*.java`, etc., but these can be customized.
- **Plugin Version**: Use a recent version (e.g., 3.0.0-M5) for the latest features and framework support.

---

## Summary

The **Maven Surefire Plugin** is essential for running unit tests in Maven projects. To use it:
1. Rely on its default behavior or declare it explicitly in `pom.xml` for customization.
2. Run tests with `mvn test` or as part of larger builds like `mvn package`.
3. Customize it with options like include/exclude patterns, parallel execution, or system properties.
4. Handle failures by skipping tests, ignoring them, or rerunning flaky ones.
5. Ensure compatibility with your test framework (JUnit, TestNG) by adding the right dependencies.

This plugin provides a robust and flexible way to manage unit testing in your Maven projects!
