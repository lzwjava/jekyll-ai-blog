---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot与Java版本兼容性
translated: true
type: note
---

### 理解错误原因

当您使用 Spring Boot 3.4.3 运行 `mvn spring-boot:run` 并遇到错误"class file has wrong version 61.0, should be 52.0"时，这表明存在 Java 版本兼容性问题。在 Java 中，类文件具有与其编译所用的 Java 版本对应的版本号：

- **版本 52.0** 对应 Java 8
- **版本 61.0** 对应 Java 17

该错误表明您的 Spring Boot 应用程序的类文件是用 Java 17（版本 61.0）编译的，但尝试运行它们的 Java 虚拟机（JVM）期望的是与 Java 8（版本 52.0）兼容的类文件。由于 Java 8 的 JVM 无法执行用 Java 17 编译的类文件（因为 Java 在此背景下向后兼容但不向前兼容），所以会出现此错误。

### 问题产生的原因

Spring Boot 3.4.3 要求**Java 17 或更高版本**作为其最低支持版本。这意味着您的项目应该使用至少 Java 17 进行编译和运行。出现不匹配的情况很可能是因为：

1. **编译**：您的项目配置为使用 Java 17 进行编译，生成了版本为 61.0 的类文件。这通常在您的 `pom.xml` 中通过 `maven-compiler-plugin` 或 `<java.version>` 属性设置。
2. **运行时**：当您执行 `mvn spring-boot:run` 时，Spring Boot Maven 插件会启动一个新的 Java 进程来运行应用程序。然而，它使用的 `java` 可执行文件来自 Java 8 安装（版本 52.0），该版本无法处理 Java 17 编译的类文件。

### 解决步骤

要解决此问题，您需要确保编译和运行时环境都使用 Java 17。以下是修复方法：

#### 1. 验证项目的 Java 版本

首先，确认您的项目设置为使用 Java 17。在您的 `pom.xml` 中，检查以下内容：

```xml
<properties>
    <java.version>17</java.version>
</properties>
```

此属性告知 `maven-compiler-plugin` 使用 Java 17 编译您的代码。Spring Boot 3.4.3 默认设置此属性，但最好进行验证。如果缺失或设置为其他版本（例如 8），请将其更新为 17。

#### 2. 安装 Java 17

确保您的系统上安装了 Java 17。您可以从以下位置下载：

- [Adoptium (Eclipse Temurin)](https://adoptium.net/)
- [Oracle JDK](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)（如果您接受许可条款）

要检查是否安装了 Java 17，请打开终端并运行：

```bash
java -version
```

如果未显示 Java 17（例如 `openjdk 17.x.x` 或类似内容），请安装它并继续。

#### 3. 更新您的环境以使用 Java 17

Spring Boot Maven 插件使用来自您环境的 `java` 可执行文件，通常由 `JAVA_HOME` 环境变量或系统 PATH 中的 `java` 命令决定。如果您当前的 `java` 命令指向 Java 8，则需要更新它。

##### 选项 A：设置 JAVA_HOME 和 PATH

将您的 `JAVA_HOME` 环境变量指向 Java 17 安装目录，并确保 PATH 中的 `java` 命令使用它。

- **在 Linux/Mac 上**：
  1. 找到您的 Java 17 安装目录（例如 `/usr/lib/jvm/java-17-openjdk` 或您安装它的任何位置）。
  2. 在终端中设置 `JAVA_HOME` 并更新 `PATH`：

     ```bash
     export JAVA_HOME=/path/to/java-17
     export PATH=$JAVA_HOME/bin:$PATH
     ```

  3. 验证：

     ```bash
     java -version
     ```

     现在应显示 Java 17。

  要使此设置永久生效，请将 `export` 行添加到您的 shell 配置文件中（例如 `~/.bashrc`、`~/.zshrc`）。

- **在 Windows 上**：
  1. 找到 Java 17 安装目录（例如 `C:\Program Files\Java\jdk-17`）。
  2. 设置 `JAVA_HOME`：
     - 打开系统属性窗口（在开始菜单中搜索"环境变量"）。
     - 在"系统变量"下，添加或更新 `JAVA_HOME` 为 `C:\Program Files\Java\jdk-17`。
  3. 更新 `Path`：
     - 在"系统变量"中，编辑 `Path` 并添加 `%JAVA_HOME%\bin`（确保其位于顶部或移除较旧的 Java 路径，如 Java 8）。
  4. 打开新的命令提示符并验证：

     ```cmd
     java -version
     ```

     应显示 Java 17。

##### 选项 B：为 Maven 使用特定的 Java 版本

如果您安装了多个 Java 版本并且不想更改系统范围的 `JAVA_HOME`，您可以使用特定的 Java 版本运行 Maven：

- 在运行 `mvn spring-boot:run` 之前，仅为该命令设置 `JAVA_HOME`：

  ```bash
  JAVA_HOME=/path/to/java-17 mvn spring-boot:run
  ```

  这确保 Spring Boot Maven 插件使用 Java 17，而无需更改系统设置。

#### 4. 再次运行应用程序

正确设置 Java 17 后，运行：

```bash
mvn spring-boot:run
```

该插件现在将使用 Java 17 执行您的应用程序，与编译的类文件版本（61.0）匹配，错误应该消失。

### 额外检查

- **Maven 的 Java 版本**：运行 `mvn -version` 查看 Maven 使用的 Java 版本。它应与您的 `JAVA_HOME` 匹配。如果不匹配，请确保您的 PATH 和 `JAVA_HOME` 配置正确。
- **依赖项**：如果错误仍然存在，可能是某个依赖项是用 Java 17 编译的，而您的运行时配置仍然不正确。由于 Spring Boot 3.4.3 强制要求 Java 17，确保您的运行时是 Java 17 应该能解决此问题。

### 为什么不使用 Java 8？

Spring Boot 3.4.3 不支持 Java 8。如果您需要使用 Java 8，则必须降级到较旧的 Spring Boot 版本（例如 2.x），但除非有特定限制，否则不推荐这样做。由于您的类文件版本是 61.0，坚持使用 Java 17 符合 Spring Boot 3.4.3 的要求。

### 最终解决方案总结

要修复在 Spring Boot 3.4.3 中运行 `mvn spring-boot:run` 时出现的"class file has wrong version 61.0, should be 52.0"错误：

1. 确保 `pom.xml` 中包含 `<java.version>17</java.version>`。
2. 如果尚未安装，请安装 Java 17。
3. 将 `JAVA_HOME` 设置为您的 Java 17 安装目录。
4. 更新您的 PATH，使 `java -version` 显示 Java 17。
5. 再次运行 `mvn spring-boot:run`。

这确保您的运行时与编译的 Java 17 类文件匹配，从而解决了兼容性问题。
