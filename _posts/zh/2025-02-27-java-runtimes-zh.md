---
audio: false
generated: true
lang: zh
layout: post
title: Visual Studio Code 中的 Java 运行时
translated: true
type: note
---

要在 Visual Studio Code（VS Code）设置中使用 `java.configuration.runtimes`，您需要在 `settings.json` 文件中进行配置。此设置允许您指定多个 Java 开发工具包（JDK）版本供 VS Code 在 Java 项目中使用。当处理需要特定 Java 版本的不同项目时，这尤其有用。以下是设置步骤：

### 配置 `java.configuration.runtimes` 的步骤

1. **打开 VS Code 设置**：
   - Windows/Linux：转到 `文件 > 首选项 > 设置` 或按 `Ctrl + ,`。
   - macOS：转到 `Code > 首选项 > 设置` 或按 `Cmd + ,`。

2. **访问 JSON 设置文件**：
   - 在设置界面中，搜索 `java.configuration.runtimes`。
   - 您会看到类似 "Java: Configuration: Runtimes" 的选项。点击 "在 settings.json 中编辑"（通常位于设置描述下方的链接）以打开 `settings.json` 文件。

3. **编辑 `settings.json`**：
   - 在 `settings.json` 文件中，添加或修改 `java.configuration.runtimes` 数组。该数组包含对象，每个对象代表一个您希望 VS Code 识别的 JDK 版本。
   - 每个对象通常包括：
     - `name`：Java 版本标识符（例如 `JavaSE-1.8`、`JavaSE-11`、`JavaSE-17`）。
     - `path`：系统上 JDK 安装目录的绝对路径。
     - `default`（可选）：设置为 `true` 可将此 JDK 设为非托管文件夹（无构建工具如 Maven 或 Gradle 的项目）的默认 JDK。

   以下是一个配置示例：

   ```json
   {
       "java.configuration.runtimes": [
           {
               "name": "JavaSE-1.8",
               "path": "C:/Program Files/Java/jdk1.8.0_351",
               "default": true
           },
           {
               "name": "JavaSE-11",
               "path": "C:/Program Files/Java/jdk-11.0.15"
           },
           {
               "name": "JavaSE-17",
               "path": "C:/Program Files/Java/jdk-17.0.6"
           }
       ]
   }
   ```

4. **验证 JDK 路径**：
   - 确保 `path` 指向 JDK 安装的根目录（例如，包含 `java.exe` 或 `java` 的 `bin` 文件夹所在位置）。
   - 在 Windows 上，路径中使用正斜杠（`/`）或转义反斜杠（`\\`）。
   - 在 macOS/Linux 上，使用适当的文件系统路径（例如 `/usr/lib/jvm/java-17-openjdk`）。

5. **保存并重新加载**：
   - 保存 `settings.json` 文件。
   - 重启 VS Code 或重新加载窗口（`Ctrl + R` 或 `Cmd + R`）以应用更改。

6. **检查配置**：
   - 打开命令面板（`Ctrl + Shift + P` 或 `Cmd + Shift + P`）并运行命令 `Java: Configure Java Runtime`。
   - 这将打开一个视图，显示可用于项目的 JDK。在 "Project JDKs" 选项卡下验证您配置的运行时是否出现。

### 工作原理

- **非托管文件夹**：对于没有构建工具的项目（例如纯 Java 文件），VS Code 使用 `java.configuration.runtimes` 中指定的 `default` JDK。
- **托管项目（Maven/Gradle）**：对于有构建工具的项目，JDK 版本由构建配置（例如 `pom.xml` 或 `build.gradle`）决定，但 VS Code 仍会识别此处列出的运行时以确保兼容性。
- **语言服务器**：Java 语言服务器（Java 扩展的一部分）需要 JDK 17+ 才能运行。如果需要，您可以使用 `java.jdt.ls.java.home` 单独指定（例如 `"java.jdt.ls.java.home": "C:/Program Files/Java/jdk-17.0.6"`）。

### 多 JDK 配置示例

如果您在 Mac 上通过 Homebrew 安装了 JDK 8 和 17，您的配置可能如下所示：

```json
{
    "java.configuration.runtimes": [
        {
            "name": "JavaSE-1.8",
            "path": "/Library/Java/JavaVirtualMachines/jdk1.8.0_351.jdk/Contents/Home",
            "default": true
        },
        {
            "name": "JavaSE-17",
            "path": "/Library/Java/JavaVirtualMachines/jdk-17.0.6.jdk/Contents/Home"
        }
    ]
}
```

### 提示

- 使用正确的 `name` 格式（`JavaSE-<version>`），与 Java 版本匹配（例如，Java 11 使用 `JavaSE-11`）。
- 如果您只有一个 JDK，仍可以列出它以确保 VS Code 明确使用它。
- 要查找 JDK 路径，请在终端中运行 `java -version`，并检查安装目录（例如，在 Windows 上使用 `where java`，在类 Unix 系统上使用 `which java`，然后追溯到 JDK 根目录）。

此设置使您能够灵活地在 VS Code 中无缝使用多个 Java 版本！如果您需要帮助查找 JDK 路径或进行故障排除，请告诉我。
