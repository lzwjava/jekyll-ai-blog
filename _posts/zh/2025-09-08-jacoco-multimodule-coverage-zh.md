---
audio: false
date: 2025-09-08
generated: true
image: false
lang: zh
layout: post
title: JaCoCo多模块覆盖率报告策略
translated: true
type: note
---

当然。您的分析非常准确，特别是关于 JaCoCo 与外部集成测试的复杂性。构建两次绝对不是理想方案。

您正在寻找的策略涉及集中化测试执行然后聚合结果。您已经很接近了，`aggregate` 目标确实是正确的工具，但需要针对此场景以特定方式应用。

以下是推荐策略：**在您的 Web 应用模块中生成一个覆盖率文件 (`.exec`)，然后使用一个单独的、专门的报告模块来为所有相关模块创建单一的聚合报告。**

这种方法清晰、可扩展，并且避免了冗余构建。

-----

## 核心概念

当您的 `PlaygroundWeb` 应用程序在带有 JaCoCo 代理的 Jetty 上运行时，该代理会检测**应用程序类加载器加载的所有类**。这包括 `PlaygroundWeb` 自身的类*以及*其所有依赖项，例如 `PlaygroundUtils.jar`。

因此，在 `PlaygroundWeb` 构建期间生成的单个 `jacoco-it.exec` 文件已经包含了**两个模块**的覆盖率数据。挑战仅仅在于将 JaCoCo 报告工具指向它构建最终 HTML 报告所需的所有模块的源代码。

-----

## 一个可扩展的四步策略

以下是重构您的项目以实现清晰、聚合的覆盖率报告的分步指南。

### 步骤 1：创建一个专门的报告模块

首先，创建一个专门用于聚合的新模块。这是 Maven 的最佳实践，可以保持关注点分离。

1. 在您的根 `pom.xml` (`PlaygroundLib`) 中，添加新模块：

    ```xml
    <modules>
        <module>PlaygroundUtils</module>
        <module>PlaygroundWeb</module>
        <module>PlaygroundReports</module> </modules>
    ```

2. 在根目录下创建一个新目录 `PlaygroundReports` 及其自己的 `pom.xml`。

您的新项目结构将如下所示：

```
.
├── PlaygroundReports
│   └── pom.xml
├── PlaygroundUtils
│   └── pom.xml
├── PlaygroundWeb
│   └── pom.xml
└── pom.xml
```

### 步骤 2：配置报告模块的 `pom.xml`

这个新的 `pom.xml` 是实现魔力的地方。它将依赖于您想要包含在报告中的所有模块，并运行 `report-aggregate` 目标。

**`PlaygroundReports/pom.xml`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.lzw</groupId>
        <artifactId>PlaygroundLib</artifactId>
        <version>1.0</version>
    </parent>
    <artifactId>PlaygroundReports</artifactId>
    <packaging>pom</packaging>
    <name>PlaygroundReports</name>

    <dependencies>
        <dependency>
            <groupId>com.lzw</groupId>
            <artifactId>PlaygroundWeb</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId>com.lzw</groupId>
            <artifactId>PlaygroundUtils</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <id>aggregate-report</id>
                        <phase>verify</phase>
                        <goals>
                            <goal>report-aggregate</goal>
                        </goals>
                        <configuration>
                            <dataFiles>
                                <dataFile>${project.basedir}/../PlaygroundWeb/target/jacoco-it.exec</dataFile>
                            </dataFiles>
                            <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate</outputDirectory>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### 步骤 3：简化 `PlaygroundWeb` 模块

您的 `PlaygroundWeb` 模块现在只负责**生成覆盖率数据**，而不负责为其生成报告。您可以从其 `pom.xml` 中移除 `jacoco:report` 的执行。

**`PlaygroundWeb/pom.xml` (仅显示更改):**

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
            <configuration>
                <propertyName>jacoco.it.agent</propertyName>
                <destFile>${project.build.directory}/jacoco-it.exec</destFile>
            </configuration>
        </execution>
        </executions>
</plugin>

<plugin>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>start-jetty</id>
            <phase>pre-integration-test</phase>
            <goals>
                <goal>start</goal>
            </goals>
            <configuration>
                <daemon>true</daemon>
                <jvmArgs>
                    ${jacoco.it.agent}
                </jvmArgs>
                </configuration>
        </execution>
        </executions>
</plugin>
```

*注意*：我稍微修改了 `prepare-agent` 的配置，使用一个属性 (`jacoco.it.agent`)，然后在 `jetty-maven-plugin` 中引用该属性。这是一种传递代理字符串的健壮方式。您之前 `pom.xml` 中的配置也是可以的，但这使得意图更清晰。

### 步骤 4：清理 `PlaygroundUtils`

`PlaygroundUtils` 模块不需要为集成测试配置任何 JaCoCo 插件。它的代码通过 `PlaygroundWeb` 被覆盖，报告由 `PlaygroundReports` 处理。您可以从其 `pom.xml` 中移除任何与 JaCoCo 相关的属性或插件。

-----

## 这如何解决问题

1. **单一构建：** 您只需从根目录运行一次 `mvn clean verify`。
2. **正确的生命周期：**
      * Maven 构建 `PlaygroundUtils`。
      * Maven 构建 `PlaygroundWeb`，启动带有 JaCoCo 代理的 Jetty，运行您的 Python 测试（这些测试会触及两个模块中的代码），停止 Jetty，并生成 `PlaygroundWeb/target/jacoco-it.exec`。
      * Maven 构建 `PlaygroundReports`。在 `verify` 阶段，`report-aggregate` 目标运行。它从 `PlaygroundWeb` 找到 `.exec` 文件，并且由于依赖关系，它知道在哪里可以找到 `PlaygroundWeb` 和 `PlaygroundUtils` 的源代码。
      * 它生成一个**单一的、统一的 HTML 报告**，其中包含两个模块的覆盖率。
3. **可扩展性：** 如果您再添加十个库模块，只需将它们作为依赖项添加到 `PlaygroundReports/pom.xml` 中。核心逻辑不会改变。这正是您正在寻找的清晰、可扩展的解决方案。
