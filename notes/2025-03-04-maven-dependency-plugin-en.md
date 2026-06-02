---
audio: false
generated: true
lang: en
layout: post
title: Maven Dependency Plugin
type: note
---

The **Maven Dependency Plugin** is a powerful tool in Maven, a widely-used build automation tool for Java projects, that helps you manage and manipulate project dependencies. Dependencies in a Maven project are external libraries or modules declared in the `pom.xml` file, which Maven downloads from repositories and makes available during compilation, runtime, or testing. The Dependency Plugin extends this functionality by providing various goals (tasks) to analyze, copy, list, or otherwise handle these dependencies. Here's how you can use it effectively:

---

#### **1. Overview of Usage**
You can use the Maven Dependency Plugin in two primary ways:
- **Configure it in the `pom.xml` file**: This allows you to bind specific plugin goals to phases of the Maven build lifecycle (e.g., `package`, `install`) for automatic execution during the build process.
- **Run goals directly from the command line**: This is ideal for one-off tasks or when you don’t want to modify the `pom.xml`.

The plugin is identified by its coordinates: `groupId: org.apache.maven.plugins`, `artifactId: maven-dependency-plugin`. You’ll need to specify a version (e.g., `3.2.0`) when configuring it, though Maven can often resolve the latest version if omitted in command-line usage.

---

#### **2. Adding the Plugin to `pom.xml`**
To use the plugin as part of your build process, add it to the `<build><plugins>` section of your `pom.xml`. Here’s a basic example:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-dependency-plugin</artifactId>
            <version>3.2.0</version>
        </plugin>
    </plugins>
</build>
```

With this setup, you can configure specific goals to execute during the build lifecycle by adding `<executions>` blocks.

---

#### **3. Common Goals and How to Use Them**
The plugin provides several goals for managing dependencies. Below are some of the most commonly used ones, along with examples of how to use them:

##### **a. `copy-dependencies`**
- **Purpose**: Copies project dependencies to a specified directory (e.g., for packaging into a `lib` folder).
- **Configured in `pom.xml`**:
  Bind this goal to the `package` phase to copy dependencies during `mvn package`:

  ```xml
  <build>
      <plugins>
          <plugin>
              <groupId>org.apache.maven.plugins</groupId>
              <artifactId>maven-dependency-plugin</artifactId>
              <version>3.2.0</version>
              <executions>
                  <execution>
                      <id>copy-dependencies</id>
                      <phase>package</phase>
                      <goals>
                          <goal>copy-dependencies</goal>
                      </goals>
                      <configuration>
                          <outputDirectory>${project.build.directory}/lib</outputDirectory>
                          <includeScope>runtime</includeScope>
                      </configuration>
                  </execution>
              </executions>
          </plugin>
      </plugins>
  </build>
  ```

  - `${project.build.directory}/lib` resolves to `target/lib` in your project.
  - `<includeScope>runtime</includeScope>` limits copying to dependencies with `compile` and `runtime` scopes, excluding `test` and `provided`.

- **Command Line**:
  Run it directly without modifying `pom.xml`:

  ```bash
  mvn dependency:copy-dependencies -DoutputDirectory=lib
  ```

##### **b. `tree`**
- **Purpose**: Displays the dependency tree, showing all direct and transitive dependencies and their versions. This is useful for identifying version conflicts.
- **Command Line**:
  Simply run:

  ```bash
  mvn dependency:tree
  ```

  This outputs a hierarchical view of dependencies to the console.
- **Configured in `pom.xml`** (optional):
  If you want this to run during a build phase (e.g., `verify`), configure it similarly to `copy-dependencies`.

##### **c. `analyze`**
- **Purpose**: Analyzes dependencies to identify issues, such as:
  - Used but undeclared dependencies.
  - Declared but unused dependencies.
- **Command Line**:
  Run:

  ```bash
  mvn dependency:analyze
  ```

  This generates a report in the console.
- **Note**: This goal may require additional configuration for complex projects to refine its analysis.

##### **d. `list`**
- **Purpose**: Lists all resolved dependencies of the project.
- **Command Line**:
  Run:

  ```bash
  mvn dependency:list
  ```

  This provides a flat list of dependencies, useful for quick reference.

##### **e. `unpack`**
- **Purpose**: Extracts the contents of a specific dependency (e.g., a JAR file) to a directory.
- **Command Line**:
  Example to unpack a specific artifact:

  ```bash
  mvn dependency:unpack -Dartifact=groupId:artifactId:version -DoutputDirectory=target/unpacked
  ```

  Replace `groupId:artifactId:version` with the coordinates of the dependency (e.g., `org.apache.commons:commons-lang3:3.12.0`).

##### **f. `purge-local-repository`**
- **Purpose**: Removes specified dependencies from your local Maven repository (`~/.m2/repository`), forcing a fresh download from remote repositories.
- **Command Line**:
  Run:

  ```bash
  mvn dependency:purge-local-repository
  ```

  This is helpful for troubleshooting corrupted dependency files.

---

#### **4. Customization Options**
Many goals support configuration parameters to tailor their behavior:
- **`outputDirectory`**: Specifies where to copy or unpack files (e.g., `target/lib`).
- **`includeScope` or `excludeScope`**: Filters dependencies by scope (e.g., `runtime`, `test`).
- **`artifact`**: Targets a specific dependency for goals like `unpack`.

These can be set in the `<configuration>` section of the `pom.xml` or passed as command-line arguments with `-D` (e.g., `-DincludeScope=runtime`).

---

#### **5. Practical Examples**
- **Scenario 1: Packaging a Standalone Application**
  Use `copy-dependencies` to gather all runtime dependencies into a `lib` folder:

  ```bash
  mvn dependency:copy-dependencies -DoutputDirectory=lib -DincludeScope=runtime
  ```

- **Scenario 2: Debugging Dependency Conflicts**
  Run `dependency:tree` to inspect transitive dependencies:

  ```bash
  mvn dependency:tree
  ```

  If you spot multiple versions of a library (e.g., `commons-logging`), resolve the conflict by adding a `<dependencyManagement>` section in `pom.xml`.

- **Scenario 3: Extracting Resources**
  Unpack a dependency to access its contents:

  ```bash
  mvn dependency:unpack -Dartifact=org.example:my-lib:1.0.0 -DoutputDirectory=target/resources
  ```

---

#### **6. Summary**
To use the Maven Dependency Plugin:
- Add it to your `pom.xml` with specific goals and configurations if you want it integrated into your build process.
- Run goals like `copy-dependencies`, `tree`, `analyze`, `list`, or `unpack` directly from the command line for ad-hoc tasks.
- Customize behavior with configuration options to suit your project’s needs.

This plugin is a versatile tool for managing dependencies beyond simple declaration, making it invaluable for building, debugging, and distributing Maven projects.
