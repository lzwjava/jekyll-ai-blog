---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maven Surefire Plugin Unit Testing Guide
translated: false
type: note
---

The **Maven Surefire Plugin** is the plugin that runs your unit tests during the **test** phase of a Maven build lifecycle. It’s one of the most commonly used Maven plugins because nearly every project needs automated testing integrated into its build.

---

## What It Is

* **Name**: `maven-surefire-plugin`
* **Purpose**: Executes tests written with frameworks like JUnit (3, 4, 5), TestNG, etc.
* **Phase**: Tied to the `test` phase of Maven’s default lifecycle.
* **Output**: Generates test reports (by default in `target/surefire-reports`).

---

## How It Works

1. When you run `mvn test` or `mvn package`, Maven invokes the Surefire plugin.
2. It scans your `src/test/java` directory for test classes.
3. By default, it looks for files matching naming conventions like:

   * `*Test.java`
   * `Test*.java`
   * `*Tests.java`
   * `*TestCase.java`
4. Executes them in an isolated classloader.
5. Writes results to `target/surefire-reports` (plain text, XML, and sometimes HTML via reporting plugins).

---

## Basic Usage

You can configure it in your `pom.xml`:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <version>3.2.5</version> <!-- use latest stable -->
    </plugin>
  </plugins>
</build>
```

After this, just run:

```bash
mvn test
```

---

## Common Configurations

* **Include/exclude patterns**:

```xml
<configuration>
  <includes>
    <include>**/*MyTest.java</include>
  </includes>
  <excludes>
    <exclude>**/IntegrationTest.java</exclude>
  </excludes>
</configuration>
```

* **System properties**:

```xml
<configuration>
  <systemPropertyVariables>
    <env>dev</env>
  </systemPropertyVariables>
</configuration>
```

* **Parallel test execution**:

```xml
<configuration>
  <forkCount>2</forkCount>
  <reuseForks>true</reuseForks>
  <parallel>classes</parallel>
</configuration>
```

This runs tests in multiple JVM forks or threads.

---

## When to Use It

* Anytime you want to integrate **unit testing** into your Maven lifecycle.
* To separate **unit tests (Surefire)** from **integration tests (Failsafe plugin)**:

  * Surefire → unit tests (`mvn test`)
  * Failsafe → integration tests (`mvn verify`)

---

✅ **In short**: `maven-surefire-plugin` is your go-to plugin for unit test execution in Maven projects. You configure it in `pom.xml`, run with `mvn test`, and review reports in `target/surefire-reports`.

---

Do you want me to also explain the **difference between Surefire and Failsafe** (since they’re often confused)?
