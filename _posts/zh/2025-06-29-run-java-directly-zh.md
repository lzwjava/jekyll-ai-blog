---
audio: false
generated: true
lang: zh
layout: post
title: 像运行Python脚本一样运行Java
translated: true
type: note
---

要直接运行 `MultiMark.java` 文件，类似于运行 Python 脚本的方式，你有几种选择。由于你使用的是类 Unix 系统（根据 `~/projects` 路径和 `ls` 命令可知），我将提供几种让运行 Java 程序尽可能简便的方法。以下是两种主要方案：

---

### **方案一：使用 `java` 命令直接运行 `MultiMark.java`（Java 11+）**
从 Java 11 开始，你可以直接运行单个 Java 源文件而无需先显式编译，这使其更接近运行 Python 脚本的体验。

1. **确保已安装 Java**
   检查是否已安装 Java 11 或更高版本：
   ```bash
   java --version
   ```
   如果未安装 Java 或版本过旧，请安装兼容版本（例如 OpenJDK）：
   ```bash
   sudo apt update
   sudo apt install openjdk-17-jdk
   ```

2. **直接运行 Java 文件**
   导航到包含 `MultiMark.java` 的目录：
   ```bash
   cd ~/projects/lzwjava.github.io/scripts/benchmark
   ```
   使用以下命令直接运行 Java 文件：
   ```bash
   java MultiMark.java
   ```
   此命令将一步完成编译并执行 `MultiMark.java` 文件。输出（例如 CPU 核心数、线程数和时间）将显示在终端中。

---

### **方案二：创建 Shell 脚本以简化操作**
为了让运行 `MultiMark.java` 更接近运行 Python 脚本的体验（例如 `./multimark`），你可以创建一个 Shell 脚本包装器。

1. **创建 Shell 脚本**
   在 `scripts/benchmark` 目录中创建一个名为 `multimark`（无扩展名）的文件：
   ```bash
   nano ~/projects/lzwjava.github.io/scripts/benchmark/multimark
   ```
   添加以下内容：
   ```bash
   #!/bin/bash
   java MultiMark.java
   ```
   保存并退出（在 nano 中按 `Ctrl+O`、`Enter`、`Ctrl+X`）。

2. **使脚本可执行**
   设置执行权限：
   ```bash
   chmod +x multimark
   ```

3. **运行脚本**
   现在你可以像运行 Python 脚本一样运行程序：
   ```bash
   ./multimark
   ```
   这将在底层执行 `java MultiMark.java`。

---

### **方案三：分别编译和运行（传统方法）**
如果你偏好或需要显式编译 Java 文件（例如，为了兼容旧版 Java 或检查编译错误），请按照以下步骤操作：

1. **编译 Java 文件**
   导航到目录：
   ```bash
   cd ~/projects/lzwjava.github.io/scripts/benchmark
   ```
   编译 Java 源文件：
   ```bash
   javac MultiMark.java
   ```
   这将生成一个 `MultiMark.class` 文件。

2. **运行编译后的程序**
   执行编译后的类：
   ```bash
   java MultiMark
   ```
   注意：使用 `MultiMark`（不带 `.java`），因为你在运行编译后的类文件。

---

### **实现类似 Python 的体验**
为了尽可能接近运行 Python 脚本的体验，**方案一**（直接运行 `java MultiMark.java`）是最简单的，因为它跳过了手动编译步骤。**方案二**（Shell 脚本）是理想选择，如果你希望像运行 `./script.py` 一样使用单个命令 `./multimark`。

### **注意事项**
- **Java 版本**：该代码使用标准 Java 库（`java.util.*` 和 `System.nanoTime`），因此应适用于 Java 8 或更高版本。直接运行功能（`java MultiMark.java`）需要 Java 11+。
- **性能**：`MultiMark.java` 程序使用多线程对排序进行基准测试。直接运行或通过脚本运行不会影响其性能，但请确保系统有足够的资源（CPU/内存）来支持测试的线程数（最多 64 个线程）。
- **目录上下文**：由于你显示了 `ls scripts/benchmark/`，我假设 `MultiMark.java` 位于该目录中。如果文件在其他位置，请调整路径。
- **错误处理**：如果遇到错误（例如 `java: command not found`），请确保已安装 Java 并已添加到 `PATH` 中。如果程序运行失败（例如由于内存或线程限制），请检查堆栈跟踪以获取详细信息。

如果你想将此与你的 Python 脚本（`executormark.py`、`multimark.py`、`threadmark.py`）集成到工作流中，请告诉我，我可以建议一些组合方式（例如从 Python 调用 Java 程序）。
