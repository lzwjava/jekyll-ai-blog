---
audio: false
generated: true
lang: zh
layout: post
title: 使用Spotless配置Palantir Java代码格式化
translated: true
type: note
---

要在 `pom.xml` 文件中配置 **Palantir Java Format** 与 **Spotless Maven 插件**，您需要设置插件以使用 `palantirJavaFormat` 并指定格式化选项，如制表符空间、缩进、导入顺序和其他设置。以下是基于 Spotless 插件和 Palantir Java Format 配置这些设置及可用选项的详细指南。

### 添加带有 Palantir Java Format 的 Spotless Maven 插件

在您的 `pom.xml` 中包含 Spotless Maven 插件，并将其配置为使用 `palantirJavaFormat`。以下是一个基本设置，包含制表符空间、缩进、导入顺序和其他选项的常见配置：

```xml
<plugin>
    <groupId>com.diffplug.spotless</groupId>
    <artifactId>spotless-maven-plugin</artifactId>
    <version>2.43.0</version> <!-- 使用最新版本 -->
    <configuration>
        <java>
            <!-- 指定要格式化的文件（可选，默认为所有 .java 文件） -->
            <includes>
                <include>src/main/java/**/*.java</include>
                <include>src/test/java/**/*.java</include>
            </includes>
            <!-- Palantir Java Format -->
            <palantirJavaFormat>
                <version>2.53.0</version> <!-- 指定所需版本 -->
                <style>GOOGLE</style> <!-- 选项：GOOGLE、AOSP 或 PALANTIR -->
                <formatJavadoc>true</formatJavadoc> <!-- 可选：格式化 Javadoc -->
            </palantirJavaFormat>
            <!-- 缩进设置 -->
            <indent>
                <tabs>true</tabs> <!-- 使用制表符而非空格 -->
                <spacesPerTab>4</spacesPerTab> <!-- 每个制表符的空格数 -->
            </indent>
            <!-- 导入顺序配置 -->
            <importOrder>
                <order>java,javax,org,com,\\#</order> <!-- 自定义导入顺序 -->
            </importOrder>
            <!-- 移除未使用的导入 -->
            <removeUnusedImports/>
            <!-- 其他可选设置 -->
            <trimTrailingWhitespace/>
            <endWithNewline/>
            <toggleOffOn/> <!-- 启用 spotless:off 和 spotless:on 标签 -->
        </java>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>apply</goal> <!-- 自动格式化代码 -->
            </goals>
            <phase>validate</phase> <!-- 在验证阶段运行 -->
        </execution>
    </executions>
</plugin>
```

### 配置选项说明

以下是 Spotless 中 `java` 部分与 `palantirJavaFormat` 配合使用时关键配置选项的细分，重点关注制表符空间、缩进、导入顺序和其他相关设置：

#### 1. **Palantir Java Format (`<palantirJavaFormat>`)**

- **`<version>`**：指定要使用的 `palantir-java-format` 版本。在 [Maven Repository](https://mvnrepository.com/artifact/com.palantir.java-format/palantir-java-format) 或 [GitHub](https://github.com/palantir/palantir-java-format/releases) 上检查最新版本。示例：`<version>2.53.0</version>`。
- **`<style>`**：定义格式化样式。选项包括：
  - `GOOGLE`：使用 Google Java 风格（2 空格缩进，100 字符行限制）。
  - `AOSP`：使用 Android 开源项目风格（4 空格缩进，100 字符行限制）。
  - `PALANTIR`：使用 Palantir 风格（4 空格缩进，120 字符行限制，支持 Lambda 友好格式化）。[](https://github.com/palantir/palantir-java-format)
- **`<formatJavadoc>`**：布尔值，启用/禁用 Javadoc 格式化（需要 Palantir Java Format 版本 ≥ 2.39.0）。示例：`<formatJavadoc>true</formatJavadoc>`。[](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)
- **自定义 Group Artifact**：很少需要，但您可以指定格式化程序的自定义 group 和 artifact。示例：`<groupArtifact>com.palantir.java-format:palantir-java-format</groupArtifact>`。

#### 2. **缩进 (`<indent>`)**

- **`<tabs>`**：布尔值，使用制表符 (`true`) 或空格 (`false`) 进行缩进。示例：`<tabs>true</tabs>`。[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<spacesPerTab>`**：每个制表符的空格数（当 `<tabs>` 为 `false` 或用于混合缩进时使用）。常用值为 `2` 或 `4`。示例：`<spacesPerTab>4</spacesPerTab>`。[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
  - **注意**：Palantir Java Format 的样式（例如 `GOOGLE`、`AOSP`、`PALANTIR`）可能会影响缩进行为。例如，`GOOGLE` 默认为 2 个空格，而 `AOSP` 和 `PALANTIR` 使用 4 个空格。Spotless 中的 `<indent>` 设置可以覆盖或补充这些默认值，但请确保一致性以避免冲突。[](https://stackoverflow.com/questions/50027892/override-google-java-format-with-spotless-maven-plugin)

#### 3. **导入顺序 (`<importOrder>`)**

- **`<order>`**：指定导入组的顺序，以逗号分隔。使用 `\\#` 表示静态导入，空字符串 (`""`) 表示未指定的导入。示例：`<order>java,javax,org,com,\\#</order>` 会先排序以 `java` 开头的导入，然后是 `javax` 等，最后是静态导入。[](https://stackoverflow.com/questions/71339562/spotless-java-google-format-vs-intellij-import-file)
- **`<file>`**：或者，指定一个包含导入顺序的文件。示例：`<file>${project.basedir}/eclipse.importorder</file>`。文件格式与 Eclipse 的导入顺序配置匹配（例如 `java|javax|org|com|\\#`）。[](https://stackoverflow.com/questions/71339562/spotless-java-google-format-vs-intellij-import-file)
  - 示例文件内容：

    ```
    #sort
    java
    javax
    org
    com
    \#
    ```

#### 4. **其他有用设置**

- **`<removeUnusedImports>`**：移除未使用的导入。可选地指定引擎：
  - 默认：使用 `google-java-format` 进行移除。
  - 替代方案：`<engine>cleanthat-javaparser-unnecessaryimport</engine>` 以获得 JDK8+ 兼容性并支持新的 Java 特性（例如 Java 17）。[](https://stackoverflow.com/questions/77126927/spotless-eclipse-formatter-java-17-error-on-string-literals-removing-unu)
- **`<trimTrailingWhitespace>`**：移除行尾的空白字符。示例：`<trimTrailingWhitespace/>`。[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<endWithNewline>`**：确保文件以换行符结尾。示例：`<endWithNewline/>`。[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<toggleOffOn>`**：启用 `// spotless:off` 和 `// spotless:on` 注释，以排除代码段的格式化。示例：`<toggleOffOn/>`。[](https://dev.to/ankityadav33/standardize-code-formatting-with-spotless-2bdh)
- **`<licenseHeader>`**：向文件添加许可证头。示例：

  ```xml
  <licenseHeader>
      <content>/* (C) $YEAR */</content>
  </licenseHeader>
  ```

  您也可以使用文件：`<file>${project.basedir}/license.txt</file>`。[](https://www.baeldung.com/java-maven-spotless-plugin)
- **`<formatAnnotations>`**：确保类型注解与它们描述的字段位于同一行。示例：`<formatAnnotations/>`。[](https://www.baeldung.com/java-maven-spotless-plugin)
- **`<ratchetFrom>`**：将格式化限制为相对于 Git 分支（例如 `origin/main`）更改的文件。示例：`<ratchetFrom>origin/main</ratchetFrom>`。[](https://github.com/diffplug/spotless/blob/main/plugin-maven/README.md)

#### 5. **POM 特定格式化 (`<pom>`)**

要格式化 `pom.xml` 文件本身，请使用带有 `sortPom` 的 `<pom>` 部分：

```xml
<pom>
    <sortPom>
        <nrOfIndentSpace>2</nrOfIndentSpace> <!-- POM 的缩进 -->
        <predefinedSortOrder>recommended_2008_06</predefinedSortOrder> <!-- 标准 POM 顺序 -->
        <sortDependencies>groupId,artifactId</sortDependencies> <!-- 对依赖项排序 -->
        <sortPlugins>groupId,artifactId</sortPlugins> <!-- 对插件排序 -->
        <endWithNewline>true</endWithNewline>
    </sortPom>
</pom>
```

- **`sortPom` 的选项**：
  - `<nrOfIndentSpace>`：缩进的空格数（例如 `2` 或 `4`）。
  - `<predefinedSortOrder>`：元素顺序的选项，如 `recommended_2008_06` 或 `custom_1`。[](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)
  - `<sortDependencies>`：按 `groupId`、`artifactId` 或其他条件排序。
  - `<sortPlugins>`：类似地对插件排序。
  - `<endWithNewline>`：确保 POM 以换行符结尾。
  - `<expandEmptyElements>`：展开空的 XML 标签（例如 `<tag></tag>` 与 `<tag/>`）。[](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)

### 运行 Spotless

- **检查格式化**：`mvn spotless:check` – 根据配置的规则验证代码，如果发现违规则构建失败。
- **应用格式化**：`mvn spotless:apply` – 自动格式化代码以符合规则。

### 注意事项与最佳实践

- **与 IDE 保持一致**：要使 IntelliJ 或 Eclipse 与 Spotless 对齐，请安装 `palantir-java-format` IntelliJ 插件或使用 Eclipse 格式化程序 XML 文件。对于 IntelliJ，导入兼容的样式文件（例如，Google 风格的 `intellij-java-google-style.xml`）或手动配置以匹配 Palantir 设置。[](https://plugins.jetbrains.com/plugin/13180-palantir-java-format)
- **版本兼容性**：确保 `palantir-java-format` 版本支持您的 Java 版本。对于 Java 17+，请使用较新的版本（例如 2.53.0）。某些特性（如模式匹配）可能支持有限。[](https://www.reddit.com/r/java/comments/1g8zu8c/codestyle_and_formatters/)
- **自定义格式化**：对于高级自定义，请使用带有 `<eclipse>` 的 Eclipse 格式化程序 XML 文件，而不是 `<palantirJavaFormat>`：

  ```xml
  <eclipse>
      <file>${project.basedir}/custom-style.xml</file>
  </eclipse>
  ```

  示例 `custom-style.xml`：

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
- **限制**：Palantir Java Format 的可配置性不如 Eclipse 的格式化程序，但旨在实现一致性和支持现代 Java 特性（例如 Lambda）。它可能无法处理所有边缘情况（例如深度嵌套的 Lambda）。[](https://www.reddit.com/r/java/comments/18z151f/strict_code_formatter/)

### 可用选项摘要

| **选项**                  | **描述**                                                                 | **示例值**                              |
|-----------------------------|-------------------------------------------------------------------------|----------------------------------------|
| `<palantirJavaFormat>`      | 配置 Palantir Java Format。                                              | `<version>2.53.0</version>`, `<style>PALANTIR</style>` |
| `<indent>`                  | 设置缩进样式（制表符或空格）和大小。                                       | `<tabs>true</tabs>`, `<spacesPerTab>4</spacesPerTab>` |
| `<importOrder>`             | 定义导入组顺序或使用文件。                                                 | `<order>java,javax,org,com,\\#</order>`        |
| `<removeUnusedImports>`     | 移除未使用的导入，带有可选引擎。                                           | `<engine>cleanthat-javaparser-unnecessaryimport</engine>` |
| `<trimTrailingWhitespace>`  | 移除行尾空白字符。                                                       | `<trimTrailingWhitespace/>`                    |
| `<endWithNewline>`         | 确保文件以换行符结尾。                                                   | `<endWithNewline/>`                           |
| `<toggleOffOn>`            | 启用 `spotless:off`/`spotless:on` 标签。                                | `<toggleOffOn/>`                              |
| `<licenseHeader>`          | 添加许可证头。                                                           | `<content>/* (C) $YEAR */</content>`           |
| `<formatAnnotations>`       | 将注解格式化为与字段位于同一行。                                          | `<formatAnnotations/>`                         |
| `<sortPom>`                | 使用排序和缩进格式化 `pom.xml`。                                         | `<nrOfIndentSpace>2</nrOfIndentSpace>`        |

### 来源

- Spotless Maven 插件文档：[GitHub](https://github.com/diffplug/spotless/tree/main/plugin-maven)[](https://github.com/diffplug/spotless/blob/main/plugin-maven/README.md)
- Palantir Java Format：[GitHub](https://github.com/palantir/palantir-java-format)[](https://github.com/palantir/palantir-java-format)
- Stack Overflow 和社区关于 Spotless 配置的示例[](https://stackoverflow.com/questions/50027892/override-google-java-format-with-spotless-maven-plugin)[](https://stackoverflow.com/questions/71339562/spotless-java-google-format-vs-intellij-import-file)[](https://stackoverflow.com/questions/77126927/spotless-eclipse-formatter-java-17-error-on-string-literals-removing-unu)

此配置确保使用 Palantir Java Format 实现一致的代码格式化，并根据您对制表符空间、缩进和导入顺序的偏好进行定制。如果您需要进一步说明或其他选项，请告知！
