---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GraalVM安装与使用指南
translated: true
type: note
---

## 什么是 GraalVM？

GraalVM 是一款开源的高性能运行时环境（JDK 发行版），支持 Java、JavaScript、Python 等多种编程语言。它具备先进的 JIT 编译器以提升执行速度，并能通过 Native Image 技术将 Java 应用程序编译为原生可执行文件，从而显著降低启动时间和内存占用。

## 安装指南

1. **下载 GraalVM**：
   - 访问 GraalVM 官方下载页面。
   - 选择社区版（免费）或 Oracle GraalVM（含附加功能）。
   - 根据您的操作系统（如 Linux、macOS、Windows）和架构（x64 或 ARM）选择对应版本。
   - 截至 2025 年，最新稳定版为基于 JDK 22 或 23 的 GraalVM，请查阅官网获取最新信息。

2. **解压安装**：
   - 将下载的压缩包解压至目标目录，例如 Linux/macOS 系统可解压至 `/opt/graalvm`，Windows 系统可解压至 `C:\Program Files\GraalVM`。
   - 无需安装程序，该发行版为便携式版本。

3. **配置环境变量**：
   - 将 `JAVA_HOME` 指向 GraalVM 目录（例如在 Linux/macOS 中执行 `export JAVA_HOME=/opt/graalvm`）。
   - 将 `bin` 目录添加至 `PATH` 环境变量（例如 `export PATH=$JAVA_HOME/bin:$PATH`）。
   - 通过 `java -version` 验证安装，命令行应显示 GraalVM 相关信息。

4. **安装附加组件（可选）**：
   - 使用 `gu`（GraalVM 更新器）安装语言运行时或 Native Image：执行 `gu install native-image`（Linux 系统需预装 `build-essential` 等构建工具）。

## 构建 Hello World 程序

本例将以 Java 为例演示基础开发流程，包括创建简单程序、编译和运行。

### 步骤 1：编写代码
创建名为 `HelloWorld.java` 的文件：

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World from GraalVM!");
    }
}
```

### 步骤 2：编译程序
在文件所在目录打开终端并执行：
```
javac HelloWorld.java
```
编译后将生成 `HelloWorld.class` 文件。

### 步骤 3：运行程序
```
java HelloWorld
```
输出结果：
```
Hello, World from GraalVM!
```

### 进阶操作：编译为原生可执行文件
通过 GraalVM 的 Native Image 功能可构建独立二进制文件。

1. 确保已安装 Native Image：执行 `gu install native-image`。
2. 生成配置文件（首次运行可能需要此步骤）：
   ```
   native-image --no-fallback -H:+ReportExceptionStackTraces HelloWorld
   ```
   - 此操作将生成原生二进制文件 `HelloWorld`（Windows 系统为 `helloworld.exe`）。
   - 首次构建时会进行应用分析，可能需要数分钟。

3. 运行原生二进制文件：
   ```
   ./HelloWorld
   ```
   输出结果相同，但程序可实现瞬时启动且内存占用极低。

## GraalVM 使用技巧
- **JDK 版本切换**：推荐使用 SDKMAN!（执行 `sdk install java 22.0.2-graal`）进行便捷管理。
- **多语言支持**：通过 GraalVM 的 `node` 命令运行 Node.js 代码，或使用 `python` 命令运行 Python 程序。
- **性能优化**：使用 `-XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler` 参数启用 GraalVM JIT 编译器。
- **故障排查**：检查 `~/.gu/` 目录下的日志文件；使用 Native Image 时请确保系统已安装 C 编译器。

更多详细信息请参阅官方文档。

[GraalVM 下载页面](https://www.graalvm.org/downloads/)
[GraalVM 用户指南](https://www.graalvm.org/latest/reference-manual/)
[Native Image 教程](https://www.graalvm.org/latest/reference-manual/native-image/)
