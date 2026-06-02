---
audio: false
generated: true
lang: en
layout: post
title: Spotless vs. Checkstyle in Java
translated: false
type: note
---

You can use the **Spotless Maven Plugin** and the **Checkstyle Maven Plugin** together in a Java project, as they serve complementary purposes. However, whether you *need* both depends on your project's requirements. Below, I’ll explain how they can work together, their differences, and when you might choose one over the other.

### Key Differences Between Spotless and Checkstyle

| **Aspect**            | **Spotless**                                                                 | **Checkstyle**                                                              |
|-----------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Purpose**           | Automatically formats code to enforce a consistent style and fixes issues.   | Statically analyzes code to enforce coding standards and detect violations.  |
| **Action**            | Modifies code (e.g., fixes indentation, import order, removes unused imports). | Reports violations without modifying code; fails build if checks fail.      |
| **Configuration**     | Configures formatters like `palantir-java-format`, `google-java-format`, etc. | Uses a ruleset (e.g., Google or Sun checks) to define coding standards.      |
| **Output**            | Formatted source files (with `mvn spotless:apply`).                          | Reports (XML, HTML, or console) listing style violations.                   |
| **Use Case**          | Ensures code is consistently formatted before commits or builds.             | Enforces coding standards and catches issues like complexity or bad practices. |

### Using Spotless and Checkstyle Together

You can combine Spotless and Checkstyle to achieve both **automatic formatting** and **style enforcement**. Here’s how they complement each other:

1. **Spotless for Formatting**:
   - Spotless applies formatting rules (e.g., indentation, import order) using tools like `palantir-java-format`.
   - It ensures code is consistently formatted, reducing manual effort.
   - Example: Fixes 2-space vs. 4-space indentation, sorts imports, and removes unused imports.

2. **Checkstyle for Validation**:
   - Checkstyle enforces coding standards beyond formatting, such as method length, naming conventions, or complexity.
   - It catches issues that formatters might not address, like missing Javadoc or overly complex methods.
   - Example: Flags a method with too many parameters or enforces Javadoc on public methods.

3. **Workflow**:
   - Run Spotless first (`mvn spotless:apply`) to format the code.
   - Then run Checkstyle (`mvn checkstyle:check`) to verify compliance with additional rules.
   - This ensures code is both formatted and adheres to broader style guidelines.

### Example Configuration in `pom.xml`

Here’s how to configure both plugins in your `pom.xml`:

```xml
<build>
    <plugins>
        <!-- Spotless Plugin for Formatting -->
        <plugin>
            <groupId>com.diffplug.spotless</groupId>
            <artifactId>spotless-maven-plugin</artifactId>
            <version>2.43.0</version>
            <configuration>
                <java>
                    <includes>
                        <include>src/main/java/**/*.java</include>
                        <include>src/test/java/**/*.java</include>
                    </includes>
                    <palantirJavaFormat>
                        <version>2.53.0</version>
                        <style>GOOGLE</style> <!-- Use Google style -->
                    </palantirJavaFormat>
                    <indent>
                        <spacesPerTab>2</spacesPerTab> <!-- 2-space indentation -->
                    </indent>
                    <importOrder>
                        <order>java,javax,org,com,\\#</order>
                    </importOrder>
                    <removeUnusedImports/>
                    <trimTrailingWhitespace/>
                    <endWithNewline/>
                </java>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>apply</goal>
                    </goals>
                    <phase>validate</phase>
                </execution>
            </executions>
        </plugin>

        <!-- Checkstyle Plugin for Validation -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.4.0</version>
            <configuration>
                <configLocation>google_checks.xml</configLocation> <!-- Use Google style or custom XML -->
                <includeTestSourceDirectory>true</includeTestSourceDirectory>
                <failOnViolation>true</failOnViolation> <!-- Fail build on violations -->
                <consoleOutput>true</consoleOutput> <!-- Output violations to console -->
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <phase>validate</phase>
                </execution>
            </executions>
            <dependencies>
                <!-- Specify Checkstyle version -->
                <dependency>
                    <groupId>com.puppycrawl.tools</groupId>
                    <artifactId>checkstyle</artifactId>
                    <version>10.17.0</version>
                </dependency>
            </dependencies>
        </plugin>
    </plugins>
</build>
```

### Key Configuration Notes

1. **Shared Style Rules**:
   - To avoid conflicts, align Spotless and Checkstyle configurations. For example, use `palantirJavaFormat` with `style>GOOGLE` in Spotless and `google_checks.xml` in Checkstyle.
   - Download `google_checks.xml` from [Checkstyle’s GitHub](https://github.com/checkstyle/checkstyle/blob/master/src/main/resources/google_checks.xml) or create a custom ruleset.

2. **Execution Order**:
   - Run Spotless before Checkstyle in the `validate` phase to ensure code is formatted before validation.
   - Example: `mvn spotless:apply checkstyle:check`.

3. **Custom Checkstyle Rules**:
   - Customize `google_checks.xml` or create your own (e.g., `my_checks.xml`) to enforce specific rules, such as:
     ```xml
     <module name="Indentation">
         <property name="basicOffset" value="2"/>
         <property name="lineWrappingIndentation" value="4"/>
     </module>
     <module name="ImportOrder">
         <property name="groups" value="java,javax,org,com"/>
         <property name="ordered" value="true"/>
         <property name="separated" value="true"/>
     </module>
     ```

4. **Avoid Redundancy**:
   - If Spotless handles formatting (e.g., indentation, import order), disable overlapping Checkstyle rules to avoid duplicate checks. For example, disable Checkstyle’s `Indentation` module if Spotless enforces indentation:
     ```xml
     <module name="Indentation">
         <property name="severity" value="ignore"/>
     </module>
     ```

### When to Use One vs. Both

- **Use Spotless Alone**:
  - If you only need consistent code formatting (e.g., indentation, import order, whitespace).
  - Ideal for teams that want automated formatting without strict style enforcement.
  - Example: Small projects or teams with IDE-based formatting.

- **Use Checkstyle Alone**:
  - If you need to enforce coding standards (e.g., naming conventions, Javadoc, method complexity) without modifying code.
  - Suitable for projects where developers manually format code but need validation.

- **Use Both**:
  - For robust code quality: Spotless formats code automatically, and Checkstyle catches additional issues (e.g., missing Javadoc, complex methods).
  - Common in large teams or projects with strict coding standards.
  - Example: Enterprise projects or open-source repositories requiring consistent style and quality checks.

### Practical Considerations

- **Performance**: Running both plugins increases build time. Use `spotless:check` (instead of `apply`) and `checkstyle:check` in CI pipelines to validate without modifying code.
- **IDE Integration**:
  - Spotless: Use the Spotless Gradle/Maven tasks or IDE plugins (e.g., `palantir-java-format` for IntelliJ).
  - Checkstyle: Use the Checkstyle-IDEA plugin for IntelliJ or Eclipse Checkstyle plugin, configured with the same `google_checks.xml`.
- **CI/CD**: Configure both plugins in your CI pipeline (e.g., Jenkins, GitHub Actions) to enforce formatting and style checks on pull requests.
  ```yaml
  # Example GitHub Actions workflow
  name: CI
  on: [pull_request]
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up JDK 17
          uses: actions/setup-java@v3
          with: { java-version: '17' }
        - name: Run Spotless and Checkstyle
          run: mvn spotless:check checkstyle:check
  ```

### Potential Conflicts and Solutions

- **Overlapping Rules**: If Spotless formats code differently from Checkstyle’s rules (e.g., 2-space vs. 4-space indentation), builds may fail. Solution: Align configurations (e.g., use `GOOGLE` style for both).
- **Build Failures**: Checkstyle’s `failOnViolation` can break builds if Spotless hasn’t run. Solution: Ensure Spotless runs first or use `spotless:check` to validate formatting.
- **Team Adoption**: Developers may resist automatic formatting. Solution: Use `spotless:check` in CI and educate the team on IDE integration.

### Sources

- Spotless Documentation: [GitHub](https://github.com/diffplug/spotless/tree/main/plugin-maven)
- Checkstyle Maven Plugin: [Maven Site](https://maven.apache.org/plugins/maven-checkstyle-plugin/)
- Community discussions on Stack Overflow and GitHub issues

### Conclusion

Using Spotless and Checkstyle together is a powerful combination for maintaining code quality: Spotless ensures consistent formatting, while Checkstyle enforces broader coding standards. Configure them to align (e.g., same indentation and import order rules) and run them sequentially in your build process. If your project only needs formatting, Spotless alone may suffice; if you need strict validation, consider adding Checkstyle. Let me know if you need help with specific configurations or a sample `google_checks.xml` file!
