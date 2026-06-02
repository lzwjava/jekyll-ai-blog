---
audio: false
generated: true
lang: en
layout: post
title: Build Helper Maven Plugin
translated: false
type: note
---

The `builder-helper-maven-plugin`, now known as the **Build Helper Maven Plugin**, is a versatile tool designed to assist with various tasks in the Maven build lifecycle. Originally hosted under Codehaus, it is now maintained by MojoHaus, though its Maven coordinates still use the `org.codehaus.mojo` group ID. This plugin provides a set of goals to help with operations such as adding extra source directories, attaching additional artifacts, parsing version information, and more. Below, I’ll guide you through how to use this plugin in your Maven project.

### What is Maven?

Before diving into the plugin, let’s set the context. Maven is a widely-used build automation tool primarily for Java projects. It simplifies and standardizes the build process by managing dependencies, compiling code, packaging applications, and more, all configured through a central file called `pom.xml`.

### Step 1: Include the Plugin in Your `pom.xml`

To use the Build Helper Maven Plugin, you need to add it to your Maven project’s `pom.xml` file within the `<build><plugins>` section. Here’s how to do it:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>build-helper-maven-plugin</artifactId>
            <version>3.6.0</version>
            <!-- Executions for specific goals will be added here -->
        </plugin>
    </plugins>
</build>
```

- **Group ID**: `org.codehaus.mojo` (reflecting its origins, even though it’s now under MojoHaus).
- **Artifact ID**: `build-helper-maven-plugin`.
- **Version**: As of my last update, `3.6.0` is the latest version, but you should check [Maven Central](https://mvnrepository.com/artifact/org.codehaus.mojo/build-helper-maven-plugin) for the most recent release.

This declaration makes the plugin available in your project, but it won’t do anything until you configure specific goals.

### Step 2: Configure Executions for Specific Goals

The Build Helper Maven Plugin offers multiple goals, each designed for a particular task. You configure these goals by adding `<executions>` blocks within the plugin declaration, specifying when they should run (via a Maven lifecycle phase) and how they should behave.

Here are some commonly used goals and their purposes:

- **`add-source`**: Adds additional source directories to your project.
- **`add-test-source`**: Adds additional test source directories.
- **`add-resource`**: Adds additional resource directories.
- **`attach-artifact`**: Attaches extra artifacts (e.g., files) to your project for installation and deployment.
- **`parse-version`**: Parses the project’s version and sets properties (e.g., major, minor, incremental versions).

Each goal requires its own configuration, which you define within an `<execution>` block.

### Step 3: Example – Adding an Extra Source Directory

A frequent use case for this plugin is adding an extra source directory, since Maven typically supports only one by default (`src/main/java`). Here’s how to configure the `add-source` goal to include an additional source directory:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>build-helper-maven-plugin</artifactId>
            <version>3.6.0</version>
            <executions>
                <execution>
                    <id>add-source</id>
                    <phase>generate-sources</phase>
                    <goals>
                        <goal>add-source</goal>
                    </goals>
                    <configuration>
                        <sources>
                            <source>path/to/your/extra/source/directory</source>
                        </sources>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

- **`<id>`**: A unique identifier for this execution (e.g., `add-source`).
- **`<phase>`**: The Maven lifecycle phase when the goal runs (e.g., `generate-sources` ensures the directory is added early in the build).
- **`<goals>`**: Specifies the goal to execute (`add-source` in this case).
- **`<configuration>`**: Defines the extra source directory (replace `path/to/your/extra/source/directory` with your actual path, e.g., `src/main/generated`).

When you run a Maven command like `mvn compile`, Maven will include this additional directory as a source folder.

### Additional Notes

- **Version Compatibility**: Since version 3.0.0, the plugin requires Maven 3 or higher. If you’re using an older Maven version, you’ll need to use plugin version 1.12 or earlier.
- **Multiple Goals**: You can define multiple `<execution>` blocks within the same plugin to run different goals. For example, you could add both source and test source directories by including executions for `add-source` and `add-test-source`.
- **Running the Plugin**: Once configured, running a Maven command (e.g., `mvn clean install`) will trigger the plugin’s goals during the specified phases.

### Further Resources

For more details and examples of other goals, check the [official usage page](https://www.mojohaus.org/build-helper-maven-plugin/usage.html). This page provides comprehensive documentation and sample configurations for all available goals.

### Final Thoughts

The Build Helper Maven Plugin is a powerful addition to your Maven toolkit, especially for projects requiring non-standard build configurations. By including it in your `pom.xml` and configuring the appropriate goals, you can tailor your build process to meet specific needs. While it originated under Codehaus, its current home is MojoHaus, and it remains a reliable choice for enhancing Maven builds.
