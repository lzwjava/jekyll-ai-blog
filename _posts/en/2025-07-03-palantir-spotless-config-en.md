---
audio: false
generated: true
lang: en
layout: post
title: Configure Palantir Java Format with Spotless
translated: false
type: note
---

To configure the **Palantir Java Format** with the **Spotless Maven Plugin** in a `pom.xml` file, you need to set up the plugin to use `palantirJavaFormat` and specify formatting options such as tabspace, indentation, import order, and other settings. Below is a detailed guide on how to configure these settings and the available options based on the Spotless plugin and Palantir Java Format.

### Adding Spotless Maven Plugin with Palantir Java Format

Include the Spotless Maven Plugin in your `pom.xml` and configure it to use `palantirJavaFormat`. Here's a basic setup with common configurations for tabspace, indentation, import order, and other options:

```xml
<plugin>
    <groupId>com.diffplug.spotless</groupId>
    <artifactId>spotless-maven-plugin</artifactId>
    <version>2.43.0</version> <!-- Use the latest version -->
    <configuration>
        <java>
            <!-- Specify files to format (optional, defaults to all .java files) -->
            <includes>
                <include>src/main/java/**/*.java</include>
                <include>src/test/java/**/*.java</include>
            </includes>
            <!-- Palantir Java Format -->
            <palantirJavaFormat>
                <version>2.53.0</version> <!-- Specify desired version -->
                <style>GOOGLE</style> <!-- Options: GOOGLE, AOSP, or PALANTIR -->
                <formatJavadoc>true</formatJavadoc> <!-- Optional: Format Javadoc -->
            </palantirJavaFormat>
            <!-- Indentation settings -->
            <indent>
                <tabs>true</tabs> <!-- Use tabs instead of spaces -->
                <spacesPerTab>4</spacesPerTab> <!-- Number of spaces per tab -->
            </indent>
            <!-- Import order configuration -->
            <importOrder>
                <order>java,javax,org,com,\\#</order> <!-- Custom import order -->
            </importOrder>
            <!-- Remove unused imports -->
            <removeUnusedImports/>
            <!-- Other optional settings -->
            <trimTrailingWhitespace/>
            <endWithNewline/>
            <toggleOffOn/> <!-- Enable spotless:off and spotless:on tags -->
        </java>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>apply</goal> <!-- Automatically format code -->
            </goals>
            <phase>validate</phase> <!-- Run during validate phase -->
        </execution>
    </executions>
</plugin>
```

### Explanation of Configuration Options

Here’s a breakdown of the key configuration options for the `java` section in Spotless with `palantirJavaFormat`, focusing on tabspace, indentation, import order, and other relevant settings:

#### 1. **Palantir Java Format (`<palantirJavaFormat>`)**

- **`<version>`**: Specifies the version of `palantir-java-format` to use. Check the latest version on [Maven Repository](https://mvnrepository.com/artifact/com.palantir.java-format/palantir-java-format) or [GitHub](https://github.com/palantir/palantir-java-format/releases). Example: `<version>2.53.0</version>`.
- **`<style>`**: Defines the formatting style. Options are:
  - `GOOGLE`: Uses Google Java Style (2-space indentation, 100-character line limit).
  - `AOSP`: Uses Android Open Source Project style (4-space indentation, 100-character line limit).
  - `PALANTIR`: Uses Palantir’s style (4-space indentation, 120-character line limit, lambda-friendly formatting).[](https://github.com/palantir/palantir-java-format)
- **`<formatJavadoc>`**: Boolean to enable/disable Javadoc formatting (requires Palantir Java Format version ≥ 2.39.0). Example: `<formatJavadoc>true</formatJavadoc>`.[](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)
- **Custom Group Artifact**: Rarely needed, but you can specify a custom group and artifact for the formatter. Example: `<groupArtifact>com.palantir.java-format:palantir-java-format</groupArtifact>`.

#### 2. **Indentation (`<indent>`)**

- **`<tabs>`**: Boolean to use tabs (`true`) or spaces (`false`) for indentation. Example: `<tabs>true</tabs>`.[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<spacesPerTab>`**: Number of spaces per tab (used when `<tabs>` is `false` or for mixed indentation). Common values are `2` or `4`. Example: `<spacesPerTab>4</spacesPerTab>`.[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
  - **Note**: Palantir Java Format’s style (e.g., `GOOGLE`, `AOSP`, `PALANTIR`) may influence indentation behavior. For example, `GOOGLE` defaults to 2 spaces, while `AOSP` and `PALANTIR` use 4 spaces. The `<indent>` settings in Spotless can override or complement these defaults, but ensure consistency to avoid conflicts.[](https://stackoverflow.com/questions/50027892/override-google-java-format-with-spotless-maven-plugin)

#### 3. **Import Order (`<importOrder>`)**

- **`<order>`**: Specifies the order of import groups, separated by commas. Use `\\#` for static imports and an empty string (`""`) for unspecified imports. Example: `<order>java,javax,org,com,\\#</order>` sorts imports starting with `java`, then `javax`, etc., with static imports last.[](https://stackoverflow.com/questions/71339562/spotless-java-google-format-vs-intellij-import-file)
- **`<file>`**: Alternatively, specify a file containing the import order. Example: `<file>${project.basedir}/eclipse.importorder</file>`. The file format matches Eclipse’s import order configuration (e.g., `java|javax|org|com|\\#`).[](https://stackoverflow.com/questions/71339562/spotless-java-google-format-vs-intellij-import-file)
  - Example file content:
    ```
    #sort
    java
    javax
    org
    com
    \#
    ```

#### 4. **Other Useful Settings**

- **`<removeUnusedImports>`**: Removes unused imports. Optionally, specify the engine:
  - Default: Uses `google-java-format` for removal.
  - Alternative: `<engine>cleanthat-javaparser-unnecessaryimport</engine>` for JDK8+ compatibility with newer Java features (e.g., Java 17).[](https://stackoverflow.com/questions/77126927/spotless-eclipse-formatter-java-17-error-on-string-literals-removing-unu)
- **`<trimTrailingWhitespace>`**: Removes trailing whitespace from lines. Example: `<trimTrailingWhitespace/>`.[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<endWithNewline>`**: Ensures files end with a newline. Example: `<endWithNewline/>`.[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<toggleOffOn>`**: Enables `// spotless:off` and `// spotless:on` comments to exclude sections of code from formatting. Example: `<toggleOffOn/>`.[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<licenseHeader>`**: Adds a license header to files. Example:
  ```xml
  <licenseHeader>
      <content>/* (C) $YEAR */</content>
  </licenseHeader>
  ```
  You can also use a file: `<file>${project.basedir}/license.txt</file>`.[](https://www.baeldung.com/java-maven-spotless-plugin)
- **`<formatAnnotations>`**: Ensures type annotations are on the same line as the fields they describe. Example: `<formatAnnotations/>`.[](https://www.baeldung.com/java-maven-spotless-plugin)
- **`<ratchetFrom>`**: Limits formatting to files changed relative to a Git branch (e.g., `origin/main`). Example: `<ratchetFrom>origin/main</ratchetFrom>`.[](https://github.com/diffplug/spotless/blob/main/plugin-maven/README.md)

#### 5. **POM-Specific Formatting (`<pom>`)**

To format the `pom.xml` file itself, use the `<pom>` section with `sortPom`:
```xml
<pom>
    <sortPom>
        <nrOfIndentSpace>2</nrOfIndentSpace> <!-- Indentation for POM -->
        <predefinedSortOrder>recommended_2008_06</predefinedSortOrder> <!-- Standard POM order -->
        <sortDependencies>groupId,artifactId</sortDependencies> <!-- Sort dependencies -->
        <sortPlugins>groupId,artifactId</sortPlugins> <!-- Sort plugins -->
        <endWithNewline>true</endWithNewline>
    </sortPom>
</pom>
```
- **Options for `sortPom`**:
  - `<nrOfIndentSpace>`: Number of spaces for indentation (e.g., `2` or `4`).
  - `<predefinedSortOrder>`: Options like `recommended_2008_06` or `custom_1` for element order.[](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)
  - `<sortDependencies>`: Sort by `groupId`, `artifactId`, or other criteria.
  - `<sortPlugins>`: Sort plugins similarly.
  - `<endWithNewline>`: Ensure POM ends with a newline.
  - `<expandEmptyElements>`: Expand empty XML tags (e.g., `<tag></tag>` vs `<tag/>`).[](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)

### Running Spotless

- **Check formatting**: `mvn spotless:check` – Validates code against the configured rules, failing the build if violations are found.
- **Apply formatting**: `mvn spotless:apply` – Automatically formats code to comply with the rules.

### Notes and Best Practices

- **Consistency with IDE**: To align IntelliJ or Eclipse with Spotless, install the `palantir-java-format` IntelliJ plugin or use an Eclipse formatter XML file. For IntelliJ, import a compatible style file (e.g., `intellij-java-google-style.xml` for Google style) or configure manually to match Palantir settings.[](https://plugins.jetbrains.com/plugin/13180-palantir-java-format)
- **Version Compatibility**: Ensure the `palantir-java-format` version supports your Java version. For Java 17+, use a recent version (e.g., 2.53.0). Some features like pattern matching may have limited support.[](https://www.reddit.com/r/java/comments/1g8zu8c/codestyle_and_formatters/)
- **Custom Formatting**: For advanced customization, use an Eclipse formatter XML file with `<eclipse>` instead of `<palantirJavaFormat>`:
  ```xml
  <eclipse>
      <file>${project.basedir}/custom-style.xml</file>
  </eclipse>
  ```
  Example `custom-style.xml`:
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <profiles version="21">
      <profile kind="CodeFormatterProfile" name="custom" version="21">
          <setting id="org.eclipse.jdt.core.formatter.tabulation.char" value="space"/>
          <setting id="org.eclipse.jdt.core.formatter.indentation.size" value="4"/>
          <setting id="org.eclipse.jdt.core.formatter.tabulation.size" value="4"/>
      </profile>
  </profiles>
  ```
  [](https://www.baeldung.com/java-maven-spotless-plugin)
- **Limitations**: Palantir Java Format is less configurable than Eclipse’s formatter but is designed for consistency and modern Java features (e.g., lambdas). It may not handle all edge cases (e.g., deeply nested lambdas).[](https://www.reddit.com/r/java/comments/18z151f/strict_code_formatter/)

### Available Options Summary

| **Option**                  | **Description**                                                                 | **Example Values**                              |
|-----------------------------|---------------------------------------------------------------------------------|------------------------------------------------|
| `<palantirJavaFormat>`      | Configures Palantir Java Format.                                                | `<version>2.53.0</version>`, `<style>PALANTIR</style>` |
| `<indent>`                  | Sets indentation style (tabs or spaces) and size.                               | `<tabs>true</tabs>`, `<spacesPerTab>4</spacesPerTab>` |
| `<importOrder>`             | Defines import group order or uses a file.                                      | `<order>java,javax,org,com,\\#</order>`        |
| `<removeUnusedImports>`     | Removes unused imports, with optional engine.                                   | `<engine>cleanthat-javaparser-unnecessaryimport</engine>` |
| `<trimTrailingWhitespace>`  | Removes trailing whitespace.                                                   | `<trimTrailingWhitespace/>`                    |
| `<endWithNewline>`         | Ensures files end with a newline.                                              | `<endWithNewline/>`                           |
| `<toggleOffOn>`            | Enables `spotless:off`/`spotless:on` tags.                                     | `<toggleOffOn/>`                              |
| `<licenseHeader>`          | Adds a license header.                                                         | `<content>/* (C) $YEAR */</content>`           |
| `<formatAnnotations>`       | Formats annotations to be on the same line as fields.                          | `<formatAnnotations/>`                         |
| `<sortPom>`                | Formats `pom.xml` with sorting and indentation.                                | `<nrOfIndentSpace>2</nrOfIndentSpace>`        |

### Sources

- Spotless Maven Plugin Documentation: [GitHub](https://github.com/diffplug/spotless/tree/main/plugin-maven)[](https://github.com/diffplug/spotless/blob/main/plugin-maven/README.md)
- Palantir Java Format: [GitHub](https://github.com/palantir/palantir-java-format)[](https://github.com/palantir/palantir-java-format)
- Stack Overflow and community examples for Spotless configuration[](https://stackoverflow.com/questions/50027892/override-google-java-format-with-spotless-maven-plugin)[](https://stackoverflow.com/questions/71339562/spotless-java-google-format-vs-intellij-import-file)[](https://stackoverflow.com/questions/77126927/spotless-eclipse-formatter-java-17-error-on-string-literals-removing-unu)

This configuration ensures consistent code formatting with Palantir Java Format, tailored to your preferences for tabspace, indentation, and import order. Let me know if you need further clarification or additional options!
