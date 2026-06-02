---
audio: false
generated: true
lang: zh
layout: post
title: 创建VSCode扩展
translated: true
type: note
---

创建 Visual Studio Code（VSCode）扩展是提升开发工作流程或为社区贡献价值的有益方式。以下是一份详尽的指南，帮助您开始编写 VSCode 插件：

### 1. 环境准备
- **Node.js 和 npm**：确保已安装 Node.js 和 npm，可从 [nodejs.org](https://nodejs.org/) 下载
- **Yeoman 和 VSCode 扩展生成器**：通过 npm 全局安装 Yeoman 和 VSCode 扩展生成器

```bash
npm install -g yo generator-code
```

### 2. 搭建开发环境
- **安装 Visual Studio Code**：确保已安装 VSCode，可从 [code.visualstudio.com](https://code.visualstudio.com/) 下载

### 3. 创建新扩展
使用 Yeoman 生成器快速搭建扩展框架。在终端中运行：

```bash
yo code
```

根据提示设置扩展参数：
- 扩展类型（如新建扩展、新建颜色主题等）
- 扩展名称
- 标识符（如 `my-extension`）
- 功能描述
- 是否初始化 Git 仓库
- 开发语言（TypeScript 或 JavaScript）
- 是否安装依赖包

### 4. 项目结构解析
新创建的扩展包含以下结构：
- `.vscode/`：存放调试启动配置
- `src/`：存放扩展源代码
- `package.json`：扩展功能清单文件
- `tsconfig.json`：TypeScript 配置文件（如使用 TypeScript）

### 5. 编写扩展功能
- **激活时机**：在 `package.json` 的 `activationEvents` 字段中定义扩展激活条件
- **功能贡献点**：在 `package.json` 的 `contributes` 部分声明扩展提供的功能（如命令、视图、语言支持）

### 6. 实现命令功能
创建用户可调用的命令。在 `package.json` 中定义命令，并在主扩展文件（如 `src/extension.ts` 或 `src/extension.js`）中实现

`package.json` 中的命令示例：

```json
"contributes": {
    "commands": [
        {
            "command": "extension.sayHello",
            "title": "Say Hello"
        }
    ]
}
```

在 `src/extension.ts` 中的实现示例：

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.sayHello', () => {
        vscode.window.showInformationMessage('Hello, World!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
```

### 7. 调试扩展
- 按 `F5` 启动加载扩展的调试窗口
- 设置断点并使用调试控制台测试扩展功能

### 8. 打包与发布
- **扩展打包**：使用 `vsce` 工具打包扩展

```bash
npm install -g vsce
vsce package
```

- **发布到商店**：参照 [VSCode 应用商店指南](https://code.visualstudio.com/api/working-with-extensions/publishing-extension) 发布扩展

### 9. 文档与最佳实践
- **文档说明**：在 `README.md` 文件中提供清晰的扩展说明
- **功能测试**：编写测试用例确保扩展稳定性
- **版本管理**：遵循语义化版本规范进行迭代

### 10. 扩展资源
- **VSCode API 文档**：[vscode-api](https://code.visualstudio.com/api)
- **扩展示例代码**：[vscode-extension-samples](https://github.com/microsoft/vscode-extension-samples)

遵循以上步骤，您将能创建出功能完善、实用高效的 VSCode 扩展。祝您编码愉快！
