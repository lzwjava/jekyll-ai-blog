---
audio: false
generated: true
lang: zh
layout: post
title: 构建助手Maven插件
translated: true
type: note
---

`builder-helper-maven-plugin`，现称为 **Build Helper Maven Plugin**，是一款多功能工具，旨在协助 Maven 构建生命周期中的各种任务。该插件最初托管在 Codehaus 下，现由 MojoHaus 维护，但其 Maven 坐标仍使用 `org.codehaus.mojo` 组 ID。该插件提供了一系列目标（goals），可帮助执行添加额外源码目录、附加额外构件、解析版本信息等操作。下面我将指导您如何在 Maven 项目中使用此插件。

### 什么是 Maven？
在深入了解该插件之前，我们先来设定背景。Maven 是一个广泛使用的构建自动化工具，主要面向 Java 项目。它通过管理依赖、编译代码、打包应用程序等，简化并标准化了构建过程，所有这些都通过一个名为 `pom.xml` 的中心文件进行配置。

### 步骤 1：在 `pom.xml` 中包含该插件
要使用 Build Helper Maven Plugin，您需要将其添加到 Maven 项目的 `pom.xml` 文件中的 `<build><plugins>` 部分。具体操作如下：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>build-helper-maven-plugin</artifactId>
            <version>3.6.0</version>
            <!-- 特定目标的执行配置将在此处添加 -->
        </plugin>
    </plugins>
</build>
```

- **Group ID**：`org.codehaus.mojo`（反映其起源，尽管现在由 MojoHaus 维护）。
- **Artifact ID**：`build-helper-maven-plugin`。
- **Version**：截至我上次更新，`3.6.0` 是最新版本，但您应查看 [Maven Central](https://mvnrepository.com/artifact/org.codehaus.mojo/build-helper-maven-plugin) 以获取最新版本。

此声明使插件在您的项目中可用，但在配置特定目标之前，它不会执行任何操作。

### 步骤 2：为特定目标配置执行
Build Helper Maven Plugin 提供了多个目标，每个目标都设计用于特定任务。您可以通过在插件声明中添加 `<executions>` 块来配置这些目标，指定它们应在何时运行（通过 Maven 生命周期阶段）以及它们的行为方式。

以下是一些常用目标及其用途：

- **`add-source`**：向项目添加额外的源码目录。
- **`add-test-source`**：添加额外的测试源码目录。
- **`add-resource`**：添加额外的资源目录。
- **`attach-artifact`**：将额外构件（例如文件）附加到项目，以便安装和部署。
- **`parse-version`**：解析项目版本并设置属性（例如主版本、次版本、增量版本）。

每个目标都需要自己的配置，您在 `<execution>` 块中定义这些配置。

### 步骤 3：示例 – 添加额外源码目录
该插件的一个常见用例是添加额外的源码目录，因为 Maven 通常默认只支持一个（`src/main/java`）。以下是配置 `add-source` 目标以包含额外源码目录的方法：

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

- **`<id>`**：此执行的唯一标识符（例如 `add-source`）。
- **`<phase>`**：目标运行的 Maven 生命周期阶段（例如 `generate-sources` 确保在构建早期添加目录）。
- **`<goals>`**：指定要执行的目标（本例中为 `add-source`）。
- **`<configuration>`**：定义额外的源码目录（将 `path/to/your/extra/source/directory` 替换为您的实际路径，例如 `src/main/generated`）。

当您运行如 `mvn compile` 这样的 Maven 命令时，Maven 会将此额外目录作为源码文件夹包含在内。

### 补充说明
- **版本兼容性**：自 3.0.0 版本起，该插件要求 Maven 3 或更高版本。如果您使用的是旧版 Maven，则需要使用 1.12 或更早版本的插件。
- **多目标配置**：您可以在同一插件中定义多个 `<execution>` 块以运行不同的目标。例如，您可以通过为 `add-source` 和 `add-test-source` 添加执行块来同时添加源码和测试源码目录。
- **运行插件**：一旦配置完成，运行 Maven 命令（例如 `mvn clean install`）将在指定阶段触发插件的目标。

### 更多资源
有关其他目标的更多详细信息和示例，请查看[官方使用页面](https://www.mojohaus.org/build-helper-maven-plugin/usage.html)。该页面提供了所有可用目标的全面文档和示例配置。

### 总结
Build Helper Maven Plugin 是您 Maven 工具包中的一个强大补充，尤其适用于需要非标准构建配置的项目。通过将其包含在 `pom.xml` 中并配置适当的目标，您可以定制构建过程以满足特定需求。尽管它起源于 Codehaus，但现在的维护方是 MojoHaus，并且它仍然是增强 Maven 构建的可靠选择。
