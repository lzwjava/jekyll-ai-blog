---
audio: false
generated: true
lang: zh
layout: post
title: 修复VisualVM中的“不支持的OpenJDK”错误
translated: true
type: note
---

在运行 VisualVM 时出现错误“Version of OpenJDK is not supported. Please use the default-jdk”，表明当前使用的 Java 开发工具包（JDK）版本与 VisualVM 不兼容。当 VisualVM 无法找到受支持的 JDK 或安装的 JDK 未正确配置时，通常会出现此问题。以下是根据您的设置（YourKit Java Profiler 2025.3 和 VisualVM，似乎是在 Linux 系统上）解决此问题的步骤。

### 解决步骤

1. **检查当前 Java 版本**
   运行以下命令以验证已安装的 Java 版本：
   ```bash
   java -version
   ```
   这将显示 OpenJDK 版本，例如：
   ```
   openjdk version "17.0.9" 2023-10-17
   OpenJDK Runtime Environment (build 17.0.9+9-Ubuntu-122.04)
   OpenJDK 64-Bit Server VM (build 17.0.9+9-Ubuntu-122.04, mixed mode, sharing)
   ```
   VisualVM 通常需要 JDK（不仅仅是 JRE），并支持 Oracle JDK 8+ 或兼容的 OpenJDK 版本。请确保您安装了受支持的 JDK。[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)[](https://visualvm.github.io/troubleshooting.html)

2. **安装默认 JDK**
   错误提示建议使用 `default-jdk`。在 Ubuntu/Debian 上，您可以使用以下命令安装：
   ```bash
   sudo apt update
   sudo apt install default-jdk
   ```
   这通常会安装一个稳定、受支持的 OpenJDK 版本（例如 OpenJDK 11 或 17）。安装后，再次使用 `java -version` 验证版本。[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)[](https://askubuntu.com/questions/1504020/visualvm-version-of-openjdk-is-not-supported)

3. **设置 JAVA_HOME 环境变量**
   VisualVM 依赖 `JAVA_HOME` 环境变量来定位 JDK。检查是否已设置：
   ```bash
   echo $JAVA_HOME
   ```
   如果未设置或指向不受支持的 JDK，请将其设置为正确的 JDK 路径。例如，如果 `default-jdk` 安装了 OpenJDK 17，路径可能为 `/usr/lib/jvm/java-17-openjdk-amd64`。使用以下命令设置：
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
   ```
   要使其永久生效，请将该行添加到您的 `~/.bashrc` 或 `~/.zshrc`：
   ```bash
   echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
   source ~/.bashrc
   ```
   将路径替换为您系统上的实际 JDK 路径（使用 `update-alternatives --list java` 查找）。[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)[](https://github.com/oracle/visualvm/issues/558)

4. **为 VisualVM 指定 JDK 路径**
   如果设置 `JAVA_HOME` 无法解决问题，您可以在启动 VisualVM 时显式指定 JDK 路径：
   ```bash
   ~/bin/YourKit-JavaProfiler-2025.3/bin/visualvm --jdkhome /usr/lib/jvm/java-17-openjdk-amd64
   ```
   将 `/usr/lib/jvm/java-17-openjdk-amd64` 替换为您的 JDK 路径。这确保 VisualVM 使用指定的 JDK。[](https://visualvm.github.io/download.html)[](https://notepad.onghu.com/2021/solve-visualvm-does-not-start-on-windows-openjdk/)

5. **安装兼容的 JDK**
   如果 `default-jdk` 仍然不兼容，请考虑安装已知与 VisualVM 兼容的特定 JDK 版本，例如 OpenJDK 11 或 Oracle JDK 8+：
   ```bash
   sudo apt install openjdk-11-jdk
   ```
   然后，按照上述方法更新 `JAVA_HOME` 或使用 `--jdkhome` 选项。[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)

6. **检查 VisualVM 安装**
   确保 VisualVM 已正确安装。错误提示您正在从 YourKit Java Profiler 目录（`~/bin/YourKit-JavaProfiler-2025.3/bin`）运行 VisualVM。这并不常见，因为 VisualVM 通常是独立工具或与 JDK 捆绑提供。验证 VisualVM 是否未损坏：
   - 从 `visualvm.github.io/download.html` 下载最新的 VisualVM 版本（例如，VisualVM 2.2，发布于 2025 年 4 月 22 日，支持 JDK 24）。[](https://visualvm.github.io/relnotes.html)[](https://visualvm.github.io/)
   - 将其解压到新目录并运行：
     ```bash
     unzip visualvm_22.zip
     cd visualvm_22/bin
     ./visualvm --jdkhome /usr/lib/jvm/java-17-openjdk-amd64
     ```
   避免在现有的 VisualVM 安装上解压覆盖，因为这可能导致问题。[](https://visualvm.github.io/troubleshooting.html)

7. **检查多个 Java 安装**
   多个 Java 版本可能导致冲突。列出所有已安装的 Java 版本：
   ```bash
   update-alternatives --list java
   ```
   如果列出了多个版本，请将所需的版本设置为默认：
   ```bash
   sudo update-alternatives --config java
   ```
   选择与兼容 JDK（例如 OpenJDK 11 或 17）对应的编号。[](https://askubuntu.com/questions/1504020/visualvm-version-of-openjdk-is-not-supported)

8. **验证 VisualVM 依赖项**
   VisualVM 需要 `libnb-platform18-java` 和 `libvisualvm-jni`。确保这些已安装：
   ```bash
   sudo apt install libnb-platform18-java libvisualvm-jni
   ```
   如果您通过 `apt` 安装 VisualVM，这一点尤其相关。[](https://askubuntu.com/questions/1504020/visualvm-version-of-openjdk-is-not-supported)

9. **绕过 OpenJDK 限制（可选）**
   如果您使用的是不受支持的 OpenJDK 构建（例如 IcedTea 或 AdoptOpenJDK），分析功能可能受限。您可以通过添加命令行参数来绕过某些限制：
   ```bash
   ./visualvm --jdkhome /usr/lib/jvm/java-17-openjdk-amd64 -J-Dorg.graalvm.visualvm.profiler.SupportAllVMs=true
   ```
   这将为不受支持的 JVM 启用分析功能，但不能保证完美运行。[](https://github.com/oracle/visualvm/issues/143)

10. **检查 YourKit 和 VisualVM 兼容性**
    由于您从 YourKit Java Profiler 目录运行 VisualVM，请确保 YourKit 的环境没有干扰。YourKit Java Profiler 2025.3 可能捆绑了特定的 VisualVM 版本或配置。请查阅 YourKit 的文档或联系 `support@yourkit.com` 以确认与您的 JDK 的兼容性。或者，尝试独立运行 VisualVM（单独下载）以隔离问题。[](https://www.yourkit.com/changes/)

### 附加说明
- **YourKit 上下文**：该错误与 YourKit Java Profiler 没有直接关系，但从 YourKit 目录运行 VisualVM 表明存在集成。YourKit 支持 Java 7–15 及更高版本的 EAP 构建，因此如果这两个工具一起使用，请确保您的 JDK 与两者兼容。[](https://www.yourkit.com/forum/viewtopic.php?t=41723)[](https://www.yourkit.com/forum/viewtopic.php?t=40299)
- **日志文件**：检查 VisualVM 日志以获取更多详细信息。日志通常位于 `~/.visualvm/<version>/var/log`。对于 YourKit，请检查 `~/.yjp/log/` 以获取分析器代理日志。如果问题仍然存在，请将日志发送至 `support@yourkit.com`。[](https://stackoverflow.com/questions/70211315/java-17-and-yourkit-2021-11)[](https://www.yourkit.com/forum/viewtopic.php?t=40299)
- **替代方案**：如果 VisualVM 持续失败，请考虑使用 YourKit 的内置分析工具或其他分析器，如 JProfiler 或 Async Profiler，它们可能与您的设置具有更好的兼容性。[](https://digma.ai/9-best-java-profilers-to-use-in-2024/)[](https://bell-sw.com/blog/a-guide-to-java-profiling-tools-techniques-best-practices/)

### 如果问题仍然存在
如果以上方法均无法解决问题，请提供：
- `java -version` 和 `echo $JAVA_HOME` 的输出。
- `update-alternatives --list java` 的输出。
- 确切的 VisualVM 版本（通过 `visualvm --help` 或下载页面检查）。
- 您使用的是 YourKit 捆绑的 VisualVM 还是独立安装。

这将有助于进一步定位问题。您也可以将问题报告给 VisualVM GitHub 页面（`https://github.com/oracle/visualvm`）或 YourKit 支持以获取具体指导。[](https://github.com/oracle/visualvm/issues/558)
