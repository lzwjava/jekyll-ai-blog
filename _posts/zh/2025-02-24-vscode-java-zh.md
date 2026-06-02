---
audio: false
generated: true
lang: zh
layout: post
title: 在 Visual Studio Code 中配置 Java 编译器
translated: true
type: note
---

你好！要在 Windows 系统上为 Visual Studio Code（VSCode）1.96.4 版本配置 Java 编译器（鉴于你已安装 Java Extension Pack），你需要设置 Java 开发工具包（JDK）路径。Java 编译器是 JDK 的一部分，VSCode 需要知道其位置才能编译你的 Java 代码。以下是详细配置步骤：

---

### 步骤 1：确保已安装 JDK

在 VSCode 中进行任何配置之前，请确保你的 Windows 电脑上已安装 JDK（不仅仅是 JRE）。JDK 包含 Java 编译器（`javac`）。如果尚未安装，可以从 Oracle、OpenJDK 或 Adoptium 等提供商处下载（例如 JDK 17 或与你项目兼容的其他版本）。安装完成后，记下安装路径（例如 `C:\Program Files\Java\jdk-17.0.1`）。

---

### 步骤 2：打开 VSCode 设置

通过以下方式告知 VSCode 你的 JDK 位置：

- **通过设置界面：**
  - 按 `Ctrl + ,` 打开设置面板
  - 或通过 `文件 > 首选项 > 设置` 进入
- **通过 settings.json（可选）：**
  - 按 `Ctrl + Shift + P` 打开命令面板
  - 输入 **"Open Settings (JSON)"** 并选择以直接编辑 `settings.json` 文件

---

### 步骤 3：通过 `java.home` 设置 JDK 路径

Java Extension Pack 依赖 `java.home` 设置来定位 JDK 以进行编译和语言功能支持（如 IntelliSense）。配置方法如下：

- **在设置界面中：**
  - 在设置面板搜索 **"java.home"**
  - 在 "Java: Home" 字段中输入 JDK 的完整路径，例如：

    ```
    C:\Program Files\Java\jdk-17.0.1
    ```

  - 注意在 Windows 系统中使用反斜杠（`\`），并确保路径指向 JDK 根目录（该目录应包含带有 `javac.exe` 的 `bin` 文件夹）

- **在 settings.json 中：**
  - 若编辑 `settings.json`，请添加这行内容（请将路径替换为你的实际 JDK 位置）：

    ```json
    "java.home": "C:\\Program Files\\Java\\jdk-17.0.1"
    ```

  - 完整示例：

    ```json
    {
        "java.home": "C:\\Program Files\\Java\\jdk-17.0.1"
    }
    ```

  - 编辑后保存文件

---

### 步骤 4：验证路径

请仔细检查：

- 路径指向的是 JDK（而非 JRE）。JDK 的 `bin` 文件夹应包含 `javac.exe`
- 路径无拼写错误，且与你的 JDK 安装位置完全匹配（例如 `C:\Program Files\Java\jdk-17.0.1`）

如果不确定 JDK 的安装位置，可以查看 `C:\Program Files\Java` 目录或你安装时选择的路径

---

### 步骤 5：可选 - 配置多版本 JDK

如果安装了多个 JDK 版本并需要切换（例如某个项目使用 JDK 8，另一个使用 JDK 17），可以使用 `java.configuration.runtimes` 设置：

- 在 `settings.json` 中添加：

  ```json
  "java.configuration.runtimes": [
      {
          "name": "JavaSE-1.8",
          "path": "C:\\Program Files\\Java\\jdk1.8.0_291"
      },
      {
          "name": "JavaSE-17",
          "path": "C:\\Program Files\\Java\\jdk-17.0.1",
          "default": true
      }
  ]
  ```

- `default: true` 选项可设置运行代码时的默认运行时环境。但就编译而言，Java 扩展主要使用 `java.home` 中指定的 JDK

---

### 步骤 6：重新加载或重启 VSCode

设置 `java.home` 后，你可能需要：

- 重新加载 VSCode 窗口（按 `Ctrl + Shift + P`，输入 **"Reload Window"** 并选择）
- 或完全重启 VSCode 使更改生效

---

### 关于编译的说明

- **单个 Java 文件：** 如果处理独立的 `.java` 文件（未使用构建工具），Java Extension Pack 的 "Language Support for Java(TM) by Red Hat" 会使用 `java.home` 中的 JDK 来编译和运行代码。你可以使用 "Run" 按钮或 **"Java: Run"** 命令
- **使用构建工具的项目：** 如果使用 Maven、Gradle 或其他构建工具，编译器由构建工具的配置管理（例如 `JAVA_HOME` 环境变量、Maven 的 `pom.xml` 或 Gradle 的 `build.gradle`）。不过设置 `java.home` 仍能确保 VSCode 的语言功能正常工作

---

### 故障排除

- **路径问题：** 如果 VSCode 找不到 JDK，请仔细检查 `java.home` 中的路径。避免不必要的空格或引号
- **未安装 JDK：** 如果出现关于缺少 `javac` 的错误，请确保已安装 JDK
- **版本兼容性：** 确保 JDK 版本符合项目要求（例如 JDK 8、11、17）

---

配置完成！现在你应该已经在 VSCode 中配置好了 Java 编译器。如果遇到任何问题或有其他疑问（例如使用特定构建工具），欢迎随时告知，我很乐意进一步协助！😊

---

将 `maven.terminal.userJavaHome` 设置为 true。你可以在终端中检查 Java 版本。
