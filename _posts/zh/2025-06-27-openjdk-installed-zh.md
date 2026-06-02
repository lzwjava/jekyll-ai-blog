---
audio: false
generated: true
lang: zh
layout: post
title: 在 Ubuntu 22.04 中定位 OpenJDK 21.0.7 安装路径
translated: true
type: note
---

您运行的 `java --version` 命令显示系统已安装 OpenJDK 21.0.7，这是专为 Ubuntu 22.04 打包的版本。该输出确认 Java 开发工具包（JDK）已安装且可通过命令行访问。

Java 安装路径通常可通过检查 `java` 二进制文件位置来确定。由于您使用的是基于 Ubuntu 的系统，OpenJDK 很可能安装在标准系统目录中，例如 `/usr/lib/jvm/`。

要定位 Java 安装的确切路径：

1. **查找 `java` 二进制文件路径**：
   在终端中运行以下命令：
   ```bash
   which java
   ```
   这可能会输出类似 `/usr/bin/java` 的结果。这是一个指向实际 Java 二进制文件的符号链接。

2. **追踪符号链接至实际位置**：
   由于 `/usr/bin/java` 通常是符号链接，您可以通过以下命令查找实际安装目录：
   ```bash
   readlink -f $(which java)
   ```
   这可能会输出类似 `/usr/lib/jvm/java-21-openjdk-amd64/bin/java` 的结果，表明 JDK 安装在 `/usr/lib/jvm/java-21-openjdk-amd64/` 目录中。

3. **验证安装目录**：
   您可以列出 JVM 目录的内容进行确认：
   ```bash
   ls /usr/lib/jvm/
   ```
   您应该会看到类似 `java-21-openjdk-amd64` 的目录，其中包含 OpenJDK 安装文件。

### 总结
您的 Java 安装很可能位于 `/usr/lib/jvm/java-21-openjdk-amd64/`（或 `/usr/lib/jvm/` 下的类似目录）。您运行的 `java` 命令是指向该目录内 `java` 二进制文件的符号链接。如需确认确切路径，请使用 `readlink -f $(which java)` 命令。
