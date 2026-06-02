---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Windows 上构建 VS Code
translated: true
type: note
---

以下是在Windows上构建VS Code的完整说明：

**所需工具：**

1. **Node.js 22.22.1**（来自.nvmrc的精确版本）
2. **npm**（随Node提供）
3. **Python 3.x** — 由`node-gyp`编译原生模块所需。使用的是node-gyp 11.2.0（`build/npm/gyp/package.json`）。Python必须在PATH环境变量中。
4. **Visual Studio Build Tools**（或完整版VS），包含**“使用C++的桌面开发”**工作负载 — 提供MSVC编译器和Windows SDK，node-gyp在编译原生插件时调用它们。这是Windows上最容易被忽略的依赖项。
5. **Git**

**构建方式：**

- TypeScript通过`gulp`编译（调用方式为`node --experimental-strip-types ./node_modules/gulp/bin/gulp.js`）
- `package.json`中的关键命令：
  - `npm run compile` — 完整编译（客户端 + copilot扩展）
  - `npm run watch` — 增量开发构建
  - `npm run gulp` — 直接访问gulp
- Electron 39.8.8作为devDependency引入，由`build/lib/electron.ts`管理
- `preinstall`脚本（`build/npm/preinstall.ts`）强制使用.nvmrc中的精确Node版本

**Windows上的快速设置：**

```
# 1. 安装Node 22.22.1（通过nvm-windows或直接安装程序）
nvm install 22.22.1
nvm use 22.22.1

# 2. 安装Python 3
winget install Python.Python.3.12

# 3. 安装VS Build Tools（C++工作负载）
winget install Microsoft.VisualStudio.2022.BuildTools
# 安装过程中，选择“使用C++的桌面开发”

# 4. 克隆并构建
git clone https://github.com/microsoft/vscode
cd vscode
npm install        # preinstall检查Node版本，postinstall运行
npm run compile    # 编译TypeScript
npm run watch      # 或：增量开发模式
```

**或者跳过原生工具检查**（如果只需要TypeScript编译，不需要完整的Electron构建）：
```
set VSCODE_SKIP_NODE_VERSION_CHECK=1
npm install
```

官方完整指南位于Wiki：https://github.com/microsoft/vscode/wiki/How-to-Contribute — 但上述4个工具（Node、npm、Python、VS Build Tools）是必需品。主构建不需要单独的Java、Rust或Go。
