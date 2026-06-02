---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在VSCode中启动扩展主机
translated: true
type: note
---

要在 Visual Studio Code（VSCode）中按 **F5** 启动 **扩展开发宿主** 以开发 VSCode 扩展，请按照以下步骤操作：

1. **在 VSCode 中打开扩展项目**：
   - 确保您已设置好 VSCode 扩展项目。这通常包括包含必要扩展配置（例如 `contributes`、`activationEvents`）的 `package.json` 文件。
   - 通过选择 `文件 > 打开文件夹` 或使用 `Ctrl+K、Ctrl+O`（Windows/Linux）或 `Cmd+K、Cmd+O`（Mac）在 VSCode 中打开包含扩展项目的文件夹。

2. **验证扩展设置**：
   - 确保项目根目录中有有效的 `package.json` 文件，至少包含以下字段：

     ```json
     {
       "name": "your-extension-name",
       "displayName": "Your Extension Name",
       "description": "Description of your extension",
       "version": "0.0.1",
       "engines": {
         "vscode": "^1.60.0"
       },
       "categories": ["Other"],
       "activationEvents": ["*"],
       "main": "./extension.js",
       "contributes": {}
     }
     ```

   - 确保有 `extension.js`（或等效文件）作为扩展代码的入口点。
   - 如果扩展使用 Node.js 模块，请在集成终端（`Ctrl+``）中运行`npm install` 安装依赖项。

3. **按 F5 启动扩展开发宿主**：
   - 在 VSCode 中打开扩展项目时，按键盘上的 **F5**。
   - 这将启动 **扩展开发宿主**，这是一个单独的 VSCode 窗口，用于加载和测试您的扩展。
   - VSCode 将自动：
     - 构建您的扩展（如果使用 TypeScript，会将 `.ts` 文件编译为 `.js`）。
     - 启动一个新的 VSCode 实例，并激活您的扩展。
     - 打开附加到扩展宿主进程的调试器。

4. **调试配置**：
   - VSCode 使用 `.vscode` 文件夹中的 `launch.json` 文件来配置调试。如果该文件不存在，当您首次按 F5 时，VSCode 会自动创建一个。
   - 典型的扩展 `launch.json` 如下所示：

     ```json
     {
       "version": "0.2.0",
       "configurations": [
         {
           "name": "Run Extension",
           "type": "extensionHost",
           "request": "launch",
           "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
           "outFiles": ["${workspaceFolder}/out/**/*.js"],
           "preLaunchTask": "npm: watch"
         }
       ]
     }
     ```

   - 确保 `preLaunchTask`（如果存在）与 `tasks.json` 中的任务匹配（例如用于编译 TypeScript）。

5. **测试扩展**：
   - 在扩展开发宿主窗口中，您的扩展应处于活动状态。根据 `package.json` 和代码中的定义测试其功能（例如命令、UI 贡献）。
   - 使用主 VSCode 窗口中的 **调试控制台** 查看扩展的日志或错误。

6. **故障排除**：
   - 如果 F5 不起作用：
     - 确保已安装 Node.js 和 npm，因为扩展开发需要它们。
     - 检查是否已安装 VSCode 扩展 API 依赖项（`npm install @types/vscode`）。
     - 验证 `launch.json` 配置指向正确的路径。
     - 如果看到错误，请检查扩展开发宿主窗口中的 **输出** 面板（在下拉菜单中选择“扩展”）。
   - 如果扩展宿主未启动，请确保项目在 `package.json` 或主扩展文件中没有语法错误。

**附加说明**：

- 您还可以通过打开 **运行和调试** 面板（Windows/Linux 为 `Ctrl+Shift+D`，Mac 为 `Cmd+Shift+D`），从下拉菜单中选择“运行扩展”，然后单击绿色播放按钮来启动扩展开发宿主。
- 要在进行更改后重新加载扩展宿主，请在扩展开发宿主窗口中使用 `Ctrl+R`（Windows/Linux）或 `Cmd+R`（Mac），或使用 F5 重新启动。

有关更多详细信息，请参阅官方 VSCode 扩展开发指南：
[VS Code 扩展开发](https://code.visualstudio.com/api/get-started/your-first-extension)
