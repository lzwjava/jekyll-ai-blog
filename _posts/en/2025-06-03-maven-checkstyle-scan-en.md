---
audio: false
generated: true
lang: en
layout: post
title: 'Maven Checkstyle: Continue Scanning'
translated: false
type: note
---

To make `mvn checkstyle:check` continue scanning all modules without failing early on violations, you need to configure the Checkstyle Maven plugin to disable the `failOnViolation` option. By default, `failOnViolation` is set to `true`, causing the build to stop as soon as violations are found. Setting it to `false` allows the scan to complete across all modules, reporting all violations without halting the build.

### Solution
Update your `pom.xml` to configure the Checkstyle plugin as follows:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-checkstyle-plugin</artifactId>
      <version>3.3.1</version> <!-- Use the latest version -->
      <configuration>
        <failOnViolation>false</failOnViolation>
        <logViolationsToConsole>true</logViolationsToConsole> <!-- Optional: Logs violations to console -->
      </configuration>
      <executions>
        <execution>
          <id>checkstyle</id>
          <phase>validate</phase> <!-- Or your preferred phase -->
          <goals>
            <goal>check</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

### Explanation
- **`<failOnViolation>false</failOnViolation>`**: This setting prevents the build from failing when Checkstyle violations are detected, allowing the scan to continue across all modules.
- **`<logViolationsToConsole>true</logViolationsToConsole>`**: (Optional) Ensures violations are printed to the console for visibility, even if the build doesn’t fail.
- **Execution Phase**: The `<phase>validate</phase>` binds the Checkstyle check to the `validate` phase of the Maven lifecycle. Adjust the phase (e.g., `compile`, `verify`) if you want it to run at a different stage.

### Running the Command
Run the command again:
```bash
mvn checkstyle:check
```
With `failOnViolation` set to `false`, Maven will scan all modules, report all violations, and complete the build without stopping early.

### Notes
- Ensure you’re using a recent version of the `maven-checkstyle-plugin` (e.g., 3.3.1 as shown). Check for the latest version on Maven Central if needed.
- If you’re working in a multi-module project, this configuration applies to all modules unless overridden in a child `pom.xml`.
- To generate a report of violations, consider running `mvn checkstyle:checkstyle` instead, which produces an HTML report without failing the build by default.

If you have specific requirements (e.g., custom Checkstyle rules or a different setup), let me know, and I can tailor the solution further!
