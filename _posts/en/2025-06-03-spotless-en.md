---
audio: false
generated: true
lang: en
layout: post
title: Using Spotless to Format Code
translated: false
type: note
---

There is no `mvn checkstyle:format` command in the Maven Checkstyle Plugin. The plugin is primarily designed for checking code against a Checkstyle configuration and reporting violations, not for automatically formatting code. However, you can achieve code formatting based on a Checkstyle configuration using other tools like Spotless or the Maven Formatter Plugin, which can be configured to align with your Checkstyle rules.

Below, I’ll explain how to format code based on your Checkstyle configuration using the **Spotless Maven Plugin**, as it’s a popular choice for this purpose and can integrate with Checkstyle rules.

### Solution: Using Spotless with Checkstyle Configuration

The Spotless Maven Plugin can format Java code according to a Checkstyle configuration file (e.g., `checkstyle.xml`). Here’s how to set it up:

#### 1. Add Spotless to Your `pom.xml`
Add the Spotless plugin to your `pom.xml` and configure it to use your Checkstyle configuration file.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.diffplug.spotless</groupId>
      <artifactId>spotless-maven-plugin</artifactId>
      <version>2.43.0</version> <!-- Use the latest version -->
      <configuration>
        <java>
          <!-- Point to your Checkstyle configuration file -->
          <googleJavaFormat>
            <version>1.22.0</version> <!-- Optional: Use a specific version -->
            <style>GOOGLE</style> <!-- Or AOSP, or omit for default -->
          </googleJavaFormat>
          <formatAnnotations>
            <!-- Use Checkstyle configuration for formatting -->
            <checkstyle>
              <file>${project.basedir}/checkstyle.xml</file> <!-- Path to your Checkstyle config -->
              <version>10.17.0</version> <!-- Match your Checkstyle version -->
            </checkstyle>
          </formatAnnotations>
        </java>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>apply</goal> <!-- Automatically formats the code -->
          </goals>
          <phase>process-sources</phase> <!-- Optional: Bind to a phase -->
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

#### 2. Ensure Your Checkstyle Configuration Exists
Make sure you have a `checkstyle.xml` file in your project (e.g., in the root directory or a subdirectory). This file defines the coding standards (e.g., indentation, whitespace, etc.) that Spotless will use to format your code. If you’re using a standard like Google Java Format, you can reference it, or use a custom Checkstyle configuration tailored to your project.

Example `checkstyle.xml` snippet for basic formatting rules:
```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN" "https://checkstyle.sourceforge.io/dtds/configuration_1_3.dtd">
<module name="Checker">
  <module name="TreeWalker">
    <module name="Indentation">
      <property name="basicOffset" value="2"/>
      <property name="braceAdjustment" value="0"/>
    </module>
  </module>
</module>
```

#### 3. Run Spotless to Format Code
To format your code based on the Checkstyle configuration, run:
```bash
mvn spotless:apply
```

This command will format all Java files in your project according to the rules defined in your Checkstyle configuration and any additional formatting settings (e.g., Google Java Format).

#### 4. Verify Formatting with Checkstyle
After formatting, you can run `mvn checkstyle:check` to verify that the formatted code complies with your Checkstyle rules. If you followed the previous advice to set `<failOnViolation>false</failOnViolation>`, it will report any remaining violations without stopping the build.

### Alternative: Maven Formatter Plugin
If you prefer not to use Spotless, you can use the **Maven Formatter Plugin**, which also supports formatting based on rules but is less commonly used with Checkstyle configurations directly. Here’s a basic setup:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>net.revelc.code.formatter</groupId>
      <artifactId>formatter-maven-plugin</artifactId>
      <version>2.23.0</version> <!-- Use the latest version -->
      <configuration>
        <configFile>${project.basedir}/checkstyle.xml</configFile> <!-- Path to Checkstyle config -->
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>format</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

Run the formatting with:
```bash
mvn formatter:format
```

### Notes
- **No Direct Checkstyle Format Command**: The Checkstyle Maven Plugin does not provide a `format` goal. Tools like Spotless or the Formatter Plugin are needed to apply formatting based on Checkstyle rules.
- **Checkstyle Version Compatibility**: Ensure the Checkstyle version specified in Spotless (or Formatter) matches the version used in your Checkstyle plugin to avoid rule mismatches.
- **Custom Checkstyle Rules**: Your `checkstyle.xml` must include formatting-related rules (e.g., `Indentation`, `WhitespaceAround`, etc.) for Spotless to apply them correctly.
- **Multi-Module Projects**: In a multi-module Maven project, you can place the Spotless/Formatter configuration in the parent `pom.xml` to apply it across all modules, or configure it per module as needed.
- **Check After Formatting**: Always run `mvn checkstyle:check` after formatting to confirm compliance, especially if you have non-formatting rules (e.g., method length, complexity) in your Checkstyle configuration.

If you don’t have a `checkstyle.xml` or need help creating one, let me know, and I can provide a sample or guide you further! Also, if you prefer a different tool or have specific formatting requirements, please share, and I’ll adjust the solution.
