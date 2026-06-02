---
audio: false
generated: true
lang: zh
layout: post
title: 使用Spotless格式化代码
translated: true
type: note
---

Maven Checkstyle 插件中不存在 `mvn checkstyle:format` 命令。该插件主要用于根据 Checkstyle 配置检查代码并报告违规情况，而非自动格式化代码。不过，您可以通过其他工具（如 Spotless 或 Maven Formatter 插件）基于 Checkstyle 配置实现代码格式化，这些工具可配置为与您的 Checkstyle 规则保持一致。

下面我将说明如何使用 **Spotless Maven 插件**基于 Checkstyle 配置格式化代码，这是实现此功能的常用方案且支持与 Checkstyle 规则集成。

### 解决方案：使用支持 Checkstyle 配置的 Spotless

Spotless Maven 插件可根据 Checkstyle 配置文件（如 `checkstyle.xml`）格式化 Java 代码。配置步骤如下：

#### 1. 在 `pom.xml` 中添加 Spotless

将 Spotless 插件添加到 `pom.xml` 中，并配置为使用您的 Checkstyle 配置文件。

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.diffplug.spotless</groupId>
      <artifactId>spotless-maven-plugin</artifactId>
      <version>2.43.0</version> <!-- 请使用最新版本 -->
      <configuration>
        <java>
          <!-- 指向您的 Checkstyle 配置文件 -->
          <googleJavaFormat>
            <version>1.22.0</version> <!-- 可选：指定特定版本 -->
            <style>GOOGLE</style> <!-- 或 AOSP，默认可省略 -->
          </googleJavaFormat>
          <formatAnnotations>
            <!-- 使用 Checkstyle 配置进行格式化 -->
            <checkstyle>
              <file>${project.basedir}/checkstyle.xml</file> <!-- Checkstyle 配置路径 -->
              <version>10.17.0</version> <!-- 与您的 Checkstyle 版本保持一致 -->
            </checkstyle>
          </formatAnnotations>
        </java>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>apply</goal> <!-- 自动格式化代码 -->
          </goals>
          <phase>process-sources</phase> <!-- 可选：绑定到特定阶段 -->
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

#### 2. 确保 Checkstyle 配置文件存在

请确保项目中存在 `checkstyle.xml` 文件（例如在根目录或子目录中）。该文件定义了代码规范（如缩进、空格等），Spotless 将据此格式化代码。若使用 Google Java Format 等标准规范可直接引用，也可使用为项目定制的自定义 Checkstyle 配置。

基础格式化规则的 `checkstyle.xml` 示例片段：

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

#### 3. 运行 Spotless 进行代码格式化

执行以下命令根据 Checkstyle 配置格式化代码：

```bash
mvn spotless:apply
```

该命令将根据 Checkstyle 配置中的规则及附加格式化设置（如 Google Java Format）格式化项目中的所有 Java 文件。

#### 4. 通过 Checkstyle 验证格式化结果

格式化完成后，可运行 `mvn checkstyle:check` 验证格式化后的代码是否符合 Checkstyle 规则。若按照先前建议设置了 `<failOnViolation>false</failOnViolation>`，该命令会报告剩余违规项但不会中断构建。

### 备选方案：Maven Formatter 插件

若不希望使用 Spotless，也可选用 **Maven Formatter 插件**，该插件同样支持基于规则格式化，但直接集成 Checkstyle 配置的用法较不常见。基础配置如下：

```xml
<build>
  <plugins>
    <plugin>
      <groupId>net.revelc.code.formatter</groupId>
      <artifactId>formatter-maven-plugin</artifactId>
      <version>2.23.0</version> <!-- 请使用最新版本 -->
      <configuration>
        <configFile>${project.basedir}/checkstyle.xml</configFile> <!-- Checkstyle 配置路径 -->
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

通过以下命令执行格式化：

```bash
mvn formatter:format
```

### 注意事项

- **无直接 Checkstyle 格式化命令**：Checkstyle Maven 插件未提供 `format` 目标。需使用 Spotless 或 Formatter 等工具来应用基于 Checkstyle 规则的格式化。
- **Checkstyle 版本兼容性**：确保 Spotless（或 Formatter）中指定的 Checkstyle 版本与插件使用版本一致，避免规则不匹配。
- **自定义 Checkstyle 规则**：您的 `checkstyle.xml` 必须包含格式化相关规则（如 `Indentation`、`WhitespaceAround` 等），Spotless 才能正确应用。
- **多模块项目**：在 Maven 多模块项目中，可将 Spotless/Formatter 配置置于父级 `pom.xml` 以应用于所有模块，也可按模块单独配置。
- **格式化后检查**：格式化后请始终运行 `mvn checkstyle:check` 确认合规性，特别是当 Checkstyle 配置中包含非格式化规则（如方法长度、复杂度）时。

若您没有 `checkstyle.xml` 文件或需要创建指导，请告知，我可提供示例或进一步指引！如果您倾向使用其他工具或有特定格式化需求，也请分享，我将据此调整解决方案。
