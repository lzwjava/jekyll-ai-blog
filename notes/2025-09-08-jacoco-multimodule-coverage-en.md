---
audio: false
date: 2025-09-08
generated: true
image: false
lang: en
layout: post
title: JaCoCo Multi-Module Coverage Reporting Strategy
translated: false
type: note
---

Of course. Your analysis is spot on, especially regarding the complexities of JaCoCo with external integration tests. Running the build twice is definitely not ideal.

The strategy you're looking for involves centralizing the test execution and then aggregating the results. You're very close, and the `aggregate` goal is indeed the right tool, but it needs to be applied in a specific way for this scenario.

Here’s the recommended strategy: **Generate one coverage file (`.exec`) in your web application module, and then use a separate, dedicated reporting module to create a single, aggregated report for all relevant modules.**

This approach is clean, scalable, and avoids redundant builds.

-----

## The Core Concept

When your `PlaygroundWeb` application runs on Jetty with the JaCoCo agent, the agent instruments **all classes loaded by the application's classloader**. This includes classes from `PlaygroundWeb` itself *and* all its dependencies, like `PlaygroundUtils.jar`.

Therefore, the single `jacoco-it.exec` file generated during the `PlaygroundWeb` build already contains the coverage data for **both modules**. The challenge is simply to point the JaCoCo reporting tool to the source code of all the modules it needs to build the final HTML report.

-----

## A Scalable Strategy in 4 Steps

Here is a step-by-step guide to refactor your project for clean, aggregated coverage reporting.

### Step 1: Create a Dedicated Reporting Module

First, create a new module exclusively for aggregation. This is a Maven best practice that keeps concerns separate.

1.  In your root `pom.xml` (`PlaygroundLib`), add the new module:
    ```xml
    <modules>
        <module>PlaygroundUtils</module>
        <module>PlaygroundWeb</module>
        <module>PlaygroundReports</module> </modules>
    ```
2.  Create a new directory `PlaygroundReports` at the root with its own `pom.xml`.

Your new project structure will look like this:

```
.
├── PlaygroundReports
│   └── pom.xml
├── PlaygroundUtils
│   └── pom.xml
├── PlaygroundWeb
│   └── pom.xml
└── pom.xml
```

### Step 2: Configure the Reporting Module's `pom.xml`

This new `pom.xml` is where the magic happens. It will depend on all the modules you want in the report and will run the `report-aggregate` goal.

**`PlaygroundReports/pom.xml`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.lzw</groupId>
        <artifactId>PlaygroundLib</artifactId>
        <version>1.0</version>
    </parent>
    <artifactId>PlaygroundReports</artifactId>
    <packaging>pom</packaging>
    <name>PlaygroundReports</name>

    <dependencies>
        <dependency>
            <groupId>com.lzw</groupId>
            <artifactId>PlaygroundWeb</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId>com.lzw</groupId>
            <artifactId>PlaygroundUtils</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <id>aggregate-report</id>
                        <phase>verify</phase>
                        <goals>
                            <goal>report-aggregate</goal>
                        </goals>
                        <configuration>
                            <dataFiles>
                                <dataFile>${project.basedir}/../PlaygroundWeb/target/jacoco-it.exec</dataFile>
                            </dataFiles>
                            <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate</outputDirectory>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### Step 3: Simplify the `PlaygroundWeb` Module

Your `PlaygroundWeb` module is now only responsible for **generating the coverage data**, not for reporting on it. You can remove the `jacoco:report` execution from its `pom.xml`.

**`PlaygroundWeb/pom.xml` (changes only):**

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
            <configuration>
                <propertyName>jacoco.it.agent</propertyName>
                <destFile>${project.build.directory}/jacoco-it.exec</destFile>
            </configuration>
        </execution>
        </executions>
</plugin>

<plugin>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>start-jetty</id>
            <phase>pre-integration-test</phase>
            <goals>
                <goal>start</goal>
            </goals>
            <configuration>
                <daemon>true</daemon>
                <jvmArgs>
                    ${jacoco.it.agent}
                </jvmArgs>
                </configuration>
        </execution>
        </executions>
</plugin>
```

*Note*: I've slightly modified the `prepare-agent` configuration to use a property (`jacoco.it.agent`) and then reference that in the `jetty-maven-plugin`. This is a robust way to pass the agent string. The previous configuration in your `pom.xml` was also fine, but this makes the intent clearer.

### Step 4: Clean Up `PlaygroundUtils`

The `PlaygroundUtils` module needs no JaCoCo plugin configuration for integration tests. Its code is covered via `PlaygroundWeb`, and the reporting is handled by `PlaygroundReports`. You can remove any JaCoCo-related properties or plugins from its `pom.xml`.

-----

## How This Solves the Problem

1.  **Single Build:** You run `mvn clean verify` from the root directory just once.
2.  **Correct Lifecycle:**
      * Maven builds `PlaygroundUtils`.
      * Maven builds `PlaygroundWeb`, starts Jetty with the JaCoCo agent, runs your Python tests (which hit code in both modules), stops Jetty, and produces `PlaygroundWeb/target/jacoco-it.exec`.
      * Maven builds `PlaygroundReports`. In the `verify` phase, the `report-aggregate` goal runs. It finds the `.exec` file from `PlaygroundWeb` and, because of the dependencies, it knows where to find the source code for both `PlaygroundWeb` and `PlaygroundUtils`.
      * It generates a **single, unified HTML report** with coverage for both modules.
3.  **Scalability:** If you add ten more library modules, you just add them as dependencies to the `PlaygroundReports/pom.xml`. The core logic doesn't change. This is the clean, scalable solution you were looking for.
