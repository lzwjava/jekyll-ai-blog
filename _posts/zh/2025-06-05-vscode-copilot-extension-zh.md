---
audio: false
generated: true
lang: zh
layout: post
title: 如何从VSCode扩展调用GitHub Copilot
translated: true
type: note
---

GitHub Copilot 是一款强大的 AI 编程助手，通过相应插件集成在 Visual Studio Code (VSCode) 和 IntelliJ IDEA 中。虽然 Copilot 没有提供直接调用的公共 REST API，但开发者可以通过 VSCode Chat API、Language Model API 或基于命令的交互方式，在 VSCode 扩展中以编程方式使用其功能。本篇博客将逐步演示如何创建一个 VSCode 扩展，通过自定义提示触发 Copilot 的聊天功能，有效模拟 Copilot 的“API 调用”，并讲解如何利用 Copilot 自身来简化开发流程。

## 理解 Copilot 在 VSCode 中的集成方式

GitHub Copilot 并未提供传统 API（如 REST 端点）供直接编程调用，而是通过以下方式提供功能：

- **VSCode Chat API**：允许扩展创建自定义聊天参与者，与 Copilot 的聊天系统进行自然语言交互
- **VSCode Language Model API**：允许扩展访问 Copilot 的大型语言模型 (LLM)，用于代码生成或分析等任务
- **VSCode 命令**：支持触发 Copilot 的内置功能，例如使用预定义提示打开聊天窗口

本指南重点介绍使用 `workbench.action.chat.open` 命令触发 Copilot 聊天界面，这是将 Copilot 功能集成到扩展中最简单的方法。

## 逐步指南：构建触发 Copilot 聊天的 VSCode 扩展

以下将逐步演示如何创建 VSCode 扩展，通过自定义提示打开 Copilot 聊天窗口，实现“调用” Copilot 处理用户定义查询的功能。

### 1. 设置 VSCode 扩展

1. **创建项目脚手架**：
   - 安装 Yeoman VSCode 扩展生成器：`npm install -g yo generator-code`
   - 运行 `yo code` 并选择 "New Extension (TypeScript)" 创建基于 TypeScript 的扩展
   - 为扩展命名，例如 `copilot-api-caller`

2. **配置 `package.json`**：
   - 定义触发 Copilot 聊天的命令
   - `package.json` 示例：

```json
{
  "name": "copilot-api-caller",
  "displayName": "Copilot API Caller",
  "description": "使用自定义提示触发 GitHub Copilot 聊天",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "activationEvents": [
    "onCommand:copilot-api-caller.triggerCopilotChat"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "copilot-api-caller.triggerCopilotChat",
        "title": "触发 Copilot 聊天"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "^20.2.5",
    "typescript": "^5.1.3"
  }
}
```

- **使用 Copilot**：在编辑 `package.json` 时，Copilot 可能会在您输入时建议 `contributes.commands`
