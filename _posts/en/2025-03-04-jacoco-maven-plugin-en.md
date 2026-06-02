---
audio: false
generated: true
lang: en
layout: post
title: JaCoCo Maven Plugin
translated: false
type: note
---

Here’s a step-by-step guide on **how to use the JaCoCo Maven plugin** to measure code coverage in a Maven-based Java project. JaCoCo (Java Code Coverage) is a tool that integrates with Maven to track how much of your code is exercised by tests, typically unit tests. By adding and configuring the JaCoCo Maven plugin in your project, you can generate detailed coverage reports during the build process.

---

### **Steps to Use the JaCoCo Maven Plugin**

#### **1. Add the JaCoCo Maven Plugin to Your `pom.xml`**

To use the JaCoCo Maven plugin, you need to include it in the `<build><plugins>` section of your project’s `pom.xml` file. Below is a basic configuration that sets up the plugin:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.12</version> <!-- Use the latest version available -->
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>verify</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

- **`groupId`, `artifactId`, and `version`**: These identify the JaCoCo Maven plugin. Replace `0.8.12` with the latest version available on [Maven Central Repository](https://mvnrepository.com/artifact/org.jacoco/jacoco-maven-plugin).
- **`<executions>`**: This section configures when and how the plugin runs during the Maven build lifecycle:
  - **`<goal>prepare-agent</goal>`**: Prepares the JaCoCo agent to collect coverage data during test execution. By default, it binds to an early phase (like `initialize`) and doesn’t require an explicit phase unless customized.
  - **`<goal>report</goal>`**: Generates the coverage report after tests have run. It’s bound to the `verify` phase here, which occurs after the `test` phase, ensuring all test data is available.

#### **2. Ensure Tests Are Configured**

The JaCoCo plugin works by analyzing test execution, typically unit tests run by the Maven Surefire Plugin. In most Maven projects, Surefire is included by default and runs tests located in `src/test/java`. No additional configuration is needed unless your tests are non-standard. Verify that:

- You have unit tests written (e.g., using JUnit or TestNG).
- The Surefire plugin is present (it’s inherited from the default Maven parent POM in most cases).

If you need to explicitly configure Surefire, it might look like this:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.5.0</version> <!-- Use the latest version -->
</plugin>
```

The `prepare-agent` goal sets up the JaCoCo agent by modifying the `argLine` property, which Surefire uses to run tests with coverage tracking enabled.

#### **3. Run the Maven Build**

To generate the coverage report, execute the following command in your project directory:

```bash
mvn verify
```

- **`mvn verify`**: This runs all phases up to `verify`, including `compile`, `test`, and `verify`. The JaCoCo plugin will:
  1. Prepare the agent before tests run.
  2. Collect coverage data during the `test` phase (when Surefire executes tests).
  3. Generate the report during the `verify` phase.

Alternatively, if you only want to run tests without proceeding to `verify`, use:

```bash
mvn test
```

However, since the `report` goal is bound to `verify` in this configuration, you’ll need to run `mvn verify` to see the report. If you prefer the report to generate during `mvn test`, you can change the `<phase>` for the `report` execution to `test`, though `verify` is a common convention.

#### **4. View the Coverage Report**

After running `mvn verify`, JaCoCo generates an HTML report by default. You can find it at:

```
target/site/jacoco/index.html
```

- Open this file in a web browser to view a detailed breakdown of code coverage, including percentages for packages, classes, methods, and lines.
- The report also includes XML and CSV formats in the same directory (`jacoco.xml` and `jacoco.csv`), useful for integration with tools like CI systems.

---

### **Optional Customizations**

For more advanced use cases, you can tweak the plugin configuration:

- **Exclude Classes or Packages**:
  To exclude certain code from coverage analysis (e.g., generated code), add a `<configuration>` section:

  ```xml
  <configuration>
      <excludes>
          <exclude>**/generated/**/*</exclude>
      </excludes>
  </configuration>
  ```

  Place this inside the `<plugin>` tag, above `<executions>`.

- **Enforce Coverage Thresholds**:
  To fail the build if coverage falls below a threshold, add the `check` goal:

  ```xml
  <execution>
      <id>check</id>
      <phase>verify</phase>
      <goals>
          <goal>check</goal>
      </goals>
      <configuration>
          <rules>
              <rule>
                  <element>BUNDLE</element>
                  <limits>
                      <limit>
                          <counter>LINE</counter>
                          <value>COVEREDRATIO</value>
                          <minimum>0.80</minimum> <!-- 80% line coverage -->
                      </limit>
                  </limits>
              </rule>
          </rules>
      </configuration>
  </execution>
  ```

- **Change Report Output Directory**:
  To customize the report location, add:

  ```xml
  <configuration>
      <destFile>${project.build.directory}/custom-jacoco.exec</destFile>
      <dataFile>${project.build.directory}/custom-jacoco.exec</dataFile>
      <outputDirectory>${project.build.directory}/custom-reports</outputDirectory>
  </configuration>
  ```

---

### **Summary**

To use the JaCoCo Maven plugin:

1. Add the plugin to your `pom.xml` with `prepare-agent` and `report` goals.
2. Ensure your project has tests configured (typically via Surefire).
3. Run `mvn verify` to generate the coverage report.
4. Check the report at `target/site/jacoco/index.html`.

This setup provides a straightforward way to integrate code coverage into your Maven build process, helping you assess the effectiveness of your tests. For the latest plugin version or advanced configurations, refer to the [official JaCoCo documentation](https://www.jacoco.org/jacoco/trunk/doc/maven.html).
