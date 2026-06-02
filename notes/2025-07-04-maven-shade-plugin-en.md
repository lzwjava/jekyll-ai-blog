---
audio: false
generated: true
lang: en
layout: post
title: 'Maven Shade Plugin: Create Uber-JARs'
translated: false
type: note
---

The `maven-shade-plugin` is a Maven plugin used to create an "uber-JAR" (a single, self-contained JAR file) by combining a project’s compiled code with its dependencies. It’s commonly used in Java projects to package an application and all its required libraries into one executable JAR file, simplifying distribution and deployment.

### Key Details:
- **Group ID**: `org.apache.maven.plugins` (indicates it’s an official Apache Maven plugin).
- **Artifact ID**: `maven-shade-plugin` (the specific plugin name).
- **Purpose**:
  - **Shading**: Relocates (renames) packages of dependencies to avoid class conflicts (e.g., when multiple libraries use different versions of the same class).
  - **Packaging**: Bundles dependencies into the final JAR, making it standalone.
  - **Resource Transformation**: Can modify resources (e.g., merge configuration files like `MANIFEST.MF`).
- **Common Use Cases**:
  - Creating executable JARs for command-line applications.
  - Resolving classpath conflicts in projects with multiple dependencies.
  - Simplifying deployment for applications like Spark or Hadoop jobs.
- **How It Works**:
  - Configured in the `pom.xml` file under the `<plugins>` section.
  - During the build process (typically in the `package` phase), it combines classes and resources, optionally relocates packages, and produces the final JAR.
- **Example Configuration** in `pom.xml`:
  ```xml
  <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-shade-plugin</artifactId>
      <version>3.5.0</version> <!-- Use the latest version -->
      <executions>
          <execution>
              <phase>package</phase>
              <goals>
                  <goal>shade</goal>
              </goals>
              <configuration>
                  <transformers>
                      <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                          <mainClass>com.example.Main</mainClass>
                      </transformer>
                  </transformers>
              </configuration>
          </execution>
      </executions>
  </plugin>
  ```
  This example specifies the main class for an executable JAR and runs the plugin during the `package` phase.

- **Key Features**:
  - **Dependency Inclusion**: Embeds dependencies into the JAR.
  - **Package Relocation**: Renames packages to avoid conflicts (e.g., `com.google.common` to `shaded.com.google.common`).
  - **Resource Filtering**: Merges or transforms resource files.
  - **Executable JAR**: Adds manifest entries to make the JAR executable with `java -jar`.

### When to Use:
- When you need a single JAR for easy distribution.
- When dealing with dependency conflicts (e.g., different versions of the same library).
- For deploying applications to environments where external dependencies are hard to manage.

If you have a specific question about its configuration or use case, let me know!
