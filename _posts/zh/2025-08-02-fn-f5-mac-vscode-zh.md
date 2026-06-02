---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Mac 版 VSCode 中的 Fn + F5 快捷键
translated: true
type: note
---

如果在 Mac 上的 Visual Studio Code (VSCode) 中按下 **Fn + F5** 无法启动 **Extension Development Host**，这通常是由于 Mac 上 `Fn` 键和功能键的配置方式、VSCode 键绑定冲突，或扩展开发环境配置错误导致的。下面我将解释可能的原因及解决方法。

### 为什么在 Mac 上 **Fn + F5** 无效

1. **Mac 功能键行为**：
   - Mac 键盘的功能键 (F1–F12) 默认通常被分配为系统功能（例如，F5 可能控制键盘亮度或媒体播放）。
   - `Fn` 键用于访问“标准”功能键行为（例如，`Fn + F5` 发送实际的 F5 键信号而非系统功能）。
   - 如果 `Fn + F5` 在 VSCode 中未触发预期操作，可能是 Mac 的键盘设置或 VSCode 的键绑定未能正确识别输入。

2. **VSCode 键绑定冲突或配置错误**：
   - VSCode 可能未将 `F5`（或 `Fn + F5`）映射到用于启动 Extension Development Host 的“运行扩展”命令。
   - 其他扩展或自定义键绑定可能覆盖了 `F5`。

3. **扩展开发环境配置问题**：
   - 如果 VSCode 扩展项目未正确配置（例如，缺少或错误的 `launch.json`），按下 `F5`（无论是否使用 `Fn`）将无法启动 Extension Development Host。

4. **macOS 系统设置**：
   - macOS 可能拦截了 `F5` 键用于系统功能，或者 `Fn` 键行为被自定义设置影响，导致 VSCode 无法检测到。

### 解决 Mac 上 VSCode 中 **Fn + F5** 无效的步骤

#### 1. **检查 macOS 键盘设置**

- **启用标准功能键行为**：
  - 前往 **系统设置 > 键盘**。
  - 勾选 **“将 F1、F2 等键用作标准功能键”**。
  - 如果启用，可直接按 `F5`（无需 `Fn`）向 VSCode 发送 F5 键信号。尝试单独按 `F5` 查看是否能启动 Extension Development Host。
  - 如果未勾选，则需要按 `Fn + F5` 发送 F5，因为单独按 F5 可能控制系统功能（例如键盘亮度）。
- **测试 F5 行为**：
  - 打开文本编辑器（如 TextEdit），分别按 `F5` 和 `Fn + F5`。如果单独按 `F5` 触发系统操作（如亮度调节），而 `Fn + F5` 无反应，则 `Fn` 键按预期发送了标准 F5 信号。
- **重置 NVRAM/PRAM**（如需）：
  - 重启 Mac，在启动时按住 `Cmd + Option + P + R` 直到听到启动声两次（或在新款 Mac 上看到 Apple 标志出现两次）。这将重置键盘相关设置，可能解决检测问题。

#### 2. **验证 VSCode 键绑定**

- 打开 VSCode，前往 **Code > 首选项 > 键盘快捷方式** (`Cmd+K, Cmd+S`)。
- 在搜索栏中输入 `F5` 或 `Run Extension`。
- 查找命令 **“Debug: Start Debugging”** 或 **“Run Extension”**（关联启动 Extension Development Host）。
- 确保其映射到 `F5`。如果没有，双击该命令，按 `F5`（或如需则按 `Fn + F5`），保存新键绑定。
- 检查冲突：搜索其他绑定到 `F5` 或 `Fn + F5` 的命令，移除或重新分配它们。
- 如需重置键绑定：点击键盘快捷方式编辑器中的三个点 (`...`)，选择 **重置键绑定**。

#### 3. **检查扩展项目配置**

- 确保扩展项目设置正确：
  - 在 VSCode 中打开扩展项目文件夹（必须包含 `package.json` 和 `extension.js` 或等效文件）。
  - 验证 `package.json` 包含必要字段：

       ```json
       {
         "name": "your-extension-name",
         "displayName": "Your Extension Name",
         "version": "0.0.1",
         "engines": {
           "vscode": "^1.60.0"
         },
         "categories": ["Other"],
         "activationEvents": ["*"],
         "main": "./extension.js"
       }
       ```

- 检查 `.vscode/launch.json` 文件：
  - 如果不存在，VSCode 应在按 `F5` 时创建。如果未创建，请在 `.vscode` 文件夹中手动创建，内容如下：

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

  - 确保 `preLaunchTask`（如 `npm: watch`）与 `.vscode/tasks.json` 中的任务匹配（如果使用 TypeScript 或构建步骤）。
- 在 VSCode 终端 (`Cmd+``) 中运行`npm install`，确保依赖（如`@types/vscode`）已安装。

#### 4. **测试启动 Extension Development Host**

- 打开扩展项目，尝试按 `F5`（或如果“将 F1、F2 等用作标准功能键”设置关闭，则按 `Fn + F5`）。
- 或者，打开 **运行和调试** 面板 (`Cmd+Shift+D`)，从下拉菜单中选择 **“Run Extension”**，点击绿色播放按钮。
- 如果 Extension Development Host 未启动：
  - 检查 **输出** 面板 (`Cmd+Shift+U`)，从下拉菜单中选择 **“Extension”** 查看错误信息。
  - 检查 **调试控制台** 中与扩展或调试过程相关的错误。
  - 确保 Node.js 已安装（在终端中输入 `node -v`），且项目无语法错误。

#### 5. **使用其他键盘测试**

- 将外接 USB 键盘连接到 Mac，在 VSCode 中按 `F5`（或 `Fn + F5`）。
- 如果有效，问题可能出在 Mac 内置键盘硬件或固件。通过 Mac 制造商（如 Apple Software Update）检查键盘固件更新。

#### 6. **更新 VSCode 和 macOS**

- 确保 VSCode 为最新版本：前往 **Code > 检查更新** 或从 VSCode 官网下载最新版本。
- 更新 macOS：前往 **系统设置 > 通用 > 软件更新** 安装可用更新，可能包含键盘驱动修复。

#### 7. **禁用冲突的扩展或软件**

- **VSCode 扩展**：
  - 禁用所有扩展：在终端中运行 `code --disable-extensions`，然后打开 VSCode 再次尝试 `F5`。
  - 如果有效，逐个重新启用扩展以找出问题扩展。
- **第三方软件**：
  - 检查键盘重映射工具，如 Karabiner-Elements 或 BetterTouchTool。打开其设置，确保 `F5` 或 `Fn + F5` 未被重映射。
  - 临时禁用这些工具进行测试。

#### 8. **调试日志**

- 启用 VSCode 开发者工具检查键事件：
  - 打开 VSCode，按 `Cmd+Option+I` 打开开发者工具。
  - 前往 **控制台** 标签，按 `Fn + F5`。查看键事件日志，确认 VSCode 是否收到正确输入。
- 如果无键事件日志，问题可能出在系统层面（macOS 或键盘硬件）。

### 如果问题依旧

- 提供更多细节：
  - macOS 版本（如 Ventura、Sonoma）。
  - VSCode 版本（通过 **Code > 关于 Visual Studio Code** 查看）。
  - 键盘类型（如 MacBook 内置、外接键盘型号）。
  - `F5` 或 `Fn + F5` 在其他应用中是否有效（例如，`F5` 是否能刷新浏览器？）。
  - VSCode **输出** 或 **调试控制台** 中的任何错误信息。
- 尝试创建最小化扩展项目以隔离问题：
  - 运行 `yo code`（需要 Yeoman 和 VSCode 生成器：`npm install -g yo generator-code`）搭建新扩展。
  - 在 VSCode 中打开新项目，按 `F5` 查看是否能启动 Extension Development Host。

[VS Code 扩展开发](https://code.visualstudio.com/api/get-started/your-first-extension)
[Mac 键盘设置](https://support.apple.com/guide/mac-help/change-the-behavior-of-the-function-keys-mchlp2882/mac)
[VS Code 键绑定](https://code.visualstudio.com/docs/getstarted/keybindings)
