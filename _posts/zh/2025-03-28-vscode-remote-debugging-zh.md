---
audio: false
generated: true
lang: zh
layout: post
title: VSCode远程调试
translated: true
type: note
---

要在 Visual Studio Code (VSCode) 中对运行在调试模式下的 WebSphere Liberty Server 进行远程调试，您可以使用 VSCode 内置的 Java 调试功能。以下是详细的设置步骤，无需安装任何 WebSphere Liberty 特定插件，前提是您已安装标准的 **Java Extension Pack**（包含 **Debugger for Java**）。

---

### 步骤 1：以调试模式启动 WebSphere Liberty Server
1. 打开终端或命令提示符。
2. 导航到您的 WebSphere Liberty 安装目录。
3. 运行以下命令以调试模式启动服务器：
   ```
   server debug default
   ```
   - 如果您的服务器名称不同，请将 `default` 替换为您的服务器名称。
4. 服务器将以调试模式启动，通常监听端口 **7777**。
5. 检查服务器的控制台输出或日志，寻找类似以下的消息：
   ```
   Listening for transport dt_socket at address: 7777
   ```
   - 这确认了调试端口。如果端口不同（例如由于冲突），请记下显示的数字。

---

### 步骤 2：在 VSCode 中配置远程调试
1. **在 VSCode 中打开您的项目**：
   - 确保您的 Java 项目（包含部署到服务器的源代码）已在 VSCode 中打开。这允许调试器将断点映射到运行中的代码。

2. **访问“运行和调试”视图**：
   - 点击左侧边栏中的 **运行和调试** 图标（一个带有虫子的播放按钮）或按 `Ctrl+Shift+D`（Windows/Linux）或 `Cmd+Shift+D`（Mac）。

3. **创建或编辑 `launch.json` 文件**：
   - 在 **运行和调试** 视图中，点击配置下拉菜单旁边的 **齿轮图标**。
   - 如果提示选择环境，请选择 **Java**。这将在您工作区的 `.vscode` 文件夹中创建一个 `launch.json` 文件。
   - 如果文件已存在，它将打开以供编辑。

4. **添加调试配置**：
   - 在 `launch.json` 文件中，确保包含一个用于附加到远程 JVM 的配置。以下是一个示例：
     ```json
     {
         "version": "0.2.0",
         "configurations": [
             {
                 "type": "java",
                 "name": "Attach to WebSphere Liberty",
                 "request": "attach",
                 "hostName": "localhost",
                 "port": 7777
             }
         ]
     }
     ```
   - **字段说明**：
     - `"type": "java"`：指定 Java 调试器。
     - `"name": "Attach to WebSphere Liberty"`：此配置的描述性名称。
     - `"request": "attach"`：表示 VSCode 将附加到现有的 JVM 进程。
     - `"hostName": "localhost"`：运行服务器的机器的主机名。如果服务器在不同的机器上，请使用服务器的 IP 地址或主机名。
     - `"port": 7777`：来自步骤 1 的调试端口。如果服务器使用不同的端口，请更新此值。

5. **保存文件**：
   - 添加或编辑配置后，保存 `launch.json` 文件。

---

### 步骤 3：启动调试会话
1. **确保服务器正在运行**：
   - 验证 WebSphere Liberty Server 是否仍以调试模式运行（来自步骤 1）。

2. **选择配置**：
   - 在 **运行和调试** 视图中，从顶部的下拉菜单中选择 **"Attach to WebSphere Liberty"**。

3. **启动调试器**：
   - 点击绿色的 **播放按钮** 或按 `F5`。VSCode 将连接到服务器的 JVM 进程。

4. **设置断点**：
   - 在 VSCode 中打开您的 Java 源文件。
   - 点击行号左侧的边距以在您希望执行暂停的位置设置断点。

5. **与应用程序交互**：
   - 使用您的应用程序（例如发送 HTTP 请求）来触发带有断点的代码路径。当断点被命中时，VSCode 将暂停执行，允许您检查变量、逐步执行代码并进行调试。

---

### 附加说明
- **本地与远程服务器**：
  - 如果服务器在不同的机器上运行，请在 `launch.json` 文件中将 `"localhost"` 替换为服务器的主机名或 IP 地址。确保调试端口可通过网络访问（例如未被防火墙阻止）。

- **调试端口确认**：
  - 如果不确定端口，请在运行 `server debug default` 后始终检查服务器的输出。它将明确说明它正在监听的端口。

- **源代码匹配**：
  - VSCode 中的源代码必须与服务器上运行的代码匹配，断点才能正常工作。确保您的项目是最新的，并使用调试信息编译（大多数 Java 构建中的默认设置）。

- **服务器行为**：
  - 使用 `server debug default` 时，服务器会立即启动（不等待调试器）。您可以在其运行期间的任何时间附加 VSCode。

- **先决条件**：
  - **Java Extension Pack**（或至少 **Debugger for Java** 扩展）必须安装在 VSCode 中。这是 Java 开发的标准工具，提供了必要的调试功能。

---

通过遵循这些步骤，您可以有效地使用 VSCode 的内置功能远程调试您的 WebSphere Liberty Server，而无需额外的 WebSphere 特定插件。
