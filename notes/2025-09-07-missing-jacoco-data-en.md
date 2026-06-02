---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Resolving Missing JaCoCo Execution Data File
translated: false
type: note
---

To generate the JaCoCo execution data file, often referred to as a **'.exec' file**, you need to run your tests with the JaCoCo agent attached. The log message "Skipping JaCoCo execution due to missing execution data file" indicates that the `report` goal was executed without the `prepare-agent` goal having been successfully run first.

-----

### Step 1: Configure the JaCoCo Maven Plugin

First, make sure your `pom.xml` file has the JaCoCo Maven plugin properly configured. It should look something like this:

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.12</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

The **`prepare-agent`** goal is crucial as it sets up the JaCoCo runtime agent. This agent instruments your code during the test run to collect coverage data.

-----

### Step 2: Run the Tests

After configuring the plugin, run your Maven build. The typical command to run tests and generate the report is:

`mvn clean install`

When you run this command, Maven executes the `prepare-agent` goal first, which attaches the JaCoCo agent to the JVM. Then, when the `test` phase runs, the agent records the code coverage data and saves it to a file, typically located at **`target/jacoco.exec`**. The `report` goal is then executed, which reads this `.exec` file and generates the final HTML or XML reports.

If you're still facing issues, check the following:

* **Project Structure**: Ensure your tests are located in the standard Maven directory `src/test/java`.
* **Test Failures**: If your tests are failing, the build might stop before the `.exec` file can be generated. Resolve any test failures first.
* **Version Mismatch**: Make sure the JaCoCo plugin version is compatible with your Maven and Java versions.
