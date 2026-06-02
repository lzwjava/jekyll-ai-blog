---
audio: false
generated: true
lang: zh
layout: post
title: JShell入门指南：快速上手
translated: true
type: note
---

JShell 是 Java 开发工具包（JDK）从 JDK 9 开始内置的交互式 REPL（读取-求值-输出循环）工具。它允许您直接执行 Java 代码片段，无需编写完整程序。以下是 JShell 的使用简明指南：

### 1. **启动 JShell**

- **确保已安装 JDK**：确认您已安装 JDK 9 或更高版本。可通过在终端或命令提示符中运行 `java -version` 进行验证。
- **启动 JShell**：
  - 打开终端或命令提示符
  - 输入 `jshell` 后按回车键
  - 出现 `jshell>` 提示符即表示 JShell 已就绪

### 2. **基础用法**

- **运行 Java 代码**：
  - 在提示符后直接输入 Java 表达式、语句或声明
  - 示例：

    ```java
    jshell> System.out.println("Hello, JShell!")
    Hello, JShell!
    ```

  - JShell 会立即执行输入并显示结果

- **变量与表达式**：
  - 声明变量或计算表达式：

    ```java
    jshell> int x = 10
    x ==> 10
    jshell> x * 2
    $2 ==> 20
    ```

  - JShell 会自动为表达式结果分配临时名称（如 `$2`）

- **定义方法与类**：
  - 可以定义方法或类：

    ```java
    jshell> void sayHello() { System.out.println("Hello!"); }
    |  created method sayHello()
    jshell> sayHello()
    Hello!
    ```

    ```java
    jshell> class Test { int x = 5; }
    |  created class Test
    jshell> Test t = new Test()
    t ==> Test@7c417213
    jshell> t.x
    $5 ==> 5
    ```

### 3. **核心命令**

JShell 提供以 `/` 开头的内置命令，以下是关键命令：

- **查看所有代码**：`/list` – 显示会话中所有输入过的代码片段

  ```java
  jshell> /list
  ```

- **编辑代码**：`/edit <id>` – 为指定 ID 的代码片段打开图形编辑器
- **保存会话**：`/save myfile.java` – 将所有代码片段保存至文件
- **加载文件**：`/open myfile.java` – 从文件加载并执行代码
- **查看变量**：`/vars` – 列出所有已声明的变量

  ```java
  jshell> /vars
  |    int x = 10
  ```

- **查看方法**：`/methods` – 列出所有已定义的方法
- **退出 JShell**：`/exit` – 结束 JShell 会话
- **获取帮助**：`/help` – 显示所有可用命令

### 4. **导入包**

- JShell 会自动导入常用包（如 `java.util`、`java.io`）。如需使用其他包，需手动导入：

  ```java
  jshell> import java.time.LocalDate
  jshell> LocalDate.now()
  $3 ==> 2025-06-27
  ```

### 5. **编辑与修正代码**

- **修改现有代码**：
  - 使用 `/list` 查找代码片段 ID
  - 输入新版本即可重新定义（JShell 会覆盖旧定义）

    ```java
    jshell> int x = 5
    x ==> 5
    jshell> int x = 10
    x ==> 10
    ```

- **删除片段**：`/drop <id>` – 根据 ID 删除特定代码片段

### 6. **Tab 补全**

- 按 `Tab` 键可自动补全类名、方法名或命令
- 示例：

  ```java
  jshell> System.out.pr<tab>
  ```

  系统将提示 `println`、`print` 等选项

### 7. **运行外部脚本**

- 加载并运行 Java 文件：

  ```java
  jshell> /open MyScript.java
  ```

- 也可在启动时加载脚本：

  ```bash
  jshell MyScript.java
  ```

### 8. **个性化配置**

- **启动脚本**：创建包含导入语句或常用代码的文件（如 `startup.jsh`），通过 `/open startup.jsh` 加载，或设为默认启动脚本：

  ```bash
  jshell --start startup.jsh
  ```

- **反馈模式**：通过 `/set feedback <模式>` 调整输出详细程度（如 `normal`、`concise`、`verbose`）

### 9. **使用技巧**

- **快速原型设计**：使用 JShell 测试代码片段、实验 API 或学习 Java 语法
- **错误处理**：JShell 提供清晰的错误信息，支持实时修正
- **多行输入**：对于复杂代码，可在行尾添加反斜杠（`\`）进行多行编辑：

  ```java
  jshell> int sum(int a, int b) { \
      ...> return a + b; \
      ...> }
  ```

### 10. **故障排除**

- **找不到 JShell**：请确认 JDK 的 `bin` 目录已加入系统 PATH 环境变量
- **启动缓慢**：部分系统中 JShell 可能需要较长时间初始化，建议更新至最新 JDK 版本
- **重置会话**：使用 `/reset` 清除所有代码片段并重新开始

更多详细信息请参阅官方 JDK 文档，或在 JShell 中运行 `/help` 命令。如果您有特定任务或想尝试的代码，欢迎告知，我将进一步指导！
