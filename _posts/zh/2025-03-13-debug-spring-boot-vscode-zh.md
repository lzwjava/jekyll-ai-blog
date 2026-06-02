---
audio: false
generated: true
lang: zh
layout: post
title: 在Visual Studio Code中调试Spring Boot应用
translated: true
type: note
---

要在 Visual Studio Code (VSCode) 中调试 Maven Spring Boot 项目，您可以按照以下简单步骤设置并在调试模式下运行应用程序。本指南假设您已有一个基础的 Maven Spring Boot 项目，包含 `pom.xml` 文件以及带有 `@SpringBootApplication` 注解的主类。具体操作如下：

### 步骤 1：安装必要扩展
开始之前，请确保 VSCode 已安装 Java 和 Spring Boot 开发所需的扩展：
- **Java Extension Pack**：包含 Red Hat 提供的 Java 语言支持等基础工具，具备调试功能及其他 Java 开发实用程序。
- **Spring Boot Extension Pack**：通过 Spring Boot 仪表盘、Spring Boot 工具等功能增强 Spring Boot 开发体验。

安装方法：
1. 打开 VSCode。
2. 进入扩展视图（Windows/Linux 按 `Ctrl+Shift+X`，macOS 按 `Cmd+Shift+X`）。
3. 搜索 "Java Extension Pack" 和 "Spring Boot Extension Pack"，分别点击**安装**。

### 步骤 2：打开 Maven Spring Boot 项目
- 启动 VSCode，通过**文件 > 打开文件夹**选择包含 `pom.xml` 的项目目录。
- VSCode 会自动检测 `pom.xml`，Java Extension Pack 将索引项目并解析依赖（右下角状态栏会显示进度，请等待完成）。

### 步骤 3：创建或编辑 `launch.json` 文件
配置调试需设置 `launch.json` 文件：
1. 点击侧边栏的调试图标或按 `Ctrl+Shift+D` 打开**运行和调试**视图。
2. 若不存在调试配置，点击"创建 launch.json 文件"；若已存在，点击齿轮图标编辑。
3. 选择 **Java** 作为环境，VSCode 会在项目的 `.vscode` 文件夹中生成默认 `launch.json`。
4. 添加或修改 Spring Boot 应用的调试配置，示例如下：

    ```json
    {
        "type": "java",
        "name": "Debug Spring Boot",
        "request": "launch",
        "mainClass": "com.example.demo.DemoApplication",
        "projectName": "demo"
    }
    ```

    - 将 `"com.example.demo.DemoApplication"` 替换为主类的完全限定名（如 `com.yourcompany.yourapp.YourApplication`）。
    - 将 `"demo"` 替换为项目名称（通常对应 `pom.xml` 中的 `<artifactId>`）。

5. 保存 `launch.json` 文件。

#### 可选：添加参数
若应用需特定参数（如 Spring 配置），可添加：
```json
{
    "type": "java",
    "name": "Debug Spring Boot",
    "request": "launch",
    "mainClass": "com.example.demo.DemoApplication",
    "projectName": "demo",
    "args": "--spring.profiles.active=dev"
}
```

### 步骤 4：开始调试
- 在**运行和调试**视图中，从顶部下拉菜单选择 **"Debug Spring Boot"**。
- 点击绿色播放按钮（或按 `F5`）以调试模式启动应用。
- VSCode 将使用 Maven 编译项目，启动 Spring Boot 应用并自动附加调试器。

### 步骤 5：设置断点并调试
- 打开项目中的 Java 文件（如控制器或服务类）。
- 在行号左侧空白处点击设置断点（红色圆点将出现）。
- 通过浏览器或 API 客户端访问应用。当执行到断点时，VSCode 会暂停，此时您可以：
  - 在**变量**面板中检查变量值。
  - 使用**单步跳过**（`F10`）、**单步进入**（`F11`）或**继续**（`F5`）控制执行流程。
  - 在调试侧边栏中查看调用栈等信息。

### 替代方法
除 `launch.json` 外，还可通过以下方式调试：
- **Maven 视图**：
  1. 打开侧边栏 Maven 视图（查找 "M" 图标或通过扩展启用）。
  2. 展开项目，在插件下找到 `spring-boot`，右键点击 `spring-boot:run` 选择**调试**。
  3. 应用启动后调试器将自动附加。
- **Spring Boot 仪表盘**：
  1. 打开 Spring Boot 仪表盘（通常在资源管理器视图或通过命令面板输入 `Spring Boot Dashboard`）。
  2. 找到应用项，右键选择**调试**（若可用）。

### 前提条件与注意事项
- 确保系统已安装 **Maven** 且可通过命令行访问，或使用 VSCode 内置 Maven（需在设置中配置）。
- 验证项目可成功构建（执行 `mvn clean install`），避免调试时出现运行时错误。
- 使用 `pom.xml` 中指定的兼容 Java 版本（如通过 `<java.version>` 配置）。

通过以上步骤，您可以在 VSCode 中高效调试 Maven Spring Boot 项目，利用其强大的调试工具定位并解决代码问题。
