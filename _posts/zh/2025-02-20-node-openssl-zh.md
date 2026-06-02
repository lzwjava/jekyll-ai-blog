---
audio: false
generated: false
lang: zh
layout: post
title: Node.js OpenSSL 兼容性
translated: true
type: note
---

在使用 **Node.js 22.9.0** 和 **npm 10.8.3** 运行 `ng build` 时，遇到以下错误：

```
error 0308010C digital envelope routines::unsupported
```

该错误通常是由于新版 Node.js（如 22.9.0 使用 OpenSSL 3.0 或更高版本）与某些加密算法之间的兼容性问题导致的，这些算法被 Angular 底层使用的 Webpack 等工具所依赖。以下是解决此问题的分步指南。

---

### 解决方案

#### 步骤 1：启用 OpenSSL 传统提供程序

最直接快速的解决方法是设置 `NODE_OPTIONS` 环境变量来启用 OpenSSL 传统提供程序，从而允许 Node.js 使用 OpenSSL 3.0+ 默认不再支持的旧版加密算法。

- **对于 macOS/Linux**：
  打开终端并运行：

  ```bash
  export NODE_OPTIONS=--openssl-legacy-provider
  ng build
  ```

- **对于 Windows（命令提示符）**：
  打开命令提示符并运行：

  ```cmd
  set NODE_OPTIONS=--openssl-legacy-provider
  ng build
  ```

- **对于 Windows（PowerShell）**：
  打开 PowerShell 并运行：

  ```powershell
  $env:NODE_OPTIONS="--openssl-legacy-provider"
  ng build
  ```

设置环境变量后，再次运行 `ng build`。在大多数情况下，这应该能通过允许 Node.js 处理不支持的例程来解决错误。

---

#### 步骤 2：验证并更新 Angular CLI（如果需要）

如果在步骤 1 之后错误仍然存在，您使用的 Angular CLI 版本可能与 Node.js 22.9.0 不完全兼容。将其更新到最新版本可能会有所帮助。

- 检查您当前的 Angular CLI 版本：

  ```bash
  ng --version
  ```

- 全局更新 Angular CLI：

  ```bash
  npm install -g @angular/cli
  ```

- 然后，再次尝试运行 `ng build`。

---

#### 步骤 3：检查并更新项目依赖项（可选）

如果问题仍未解决，可能是项目中过时的依赖项导致了问题。为此：

- 打开您的 `package.json` 文件，并检查依赖项的版本（例如 `@angular/core`、`@angular/cli` 等）。
- 将它们仔细更新到最新的兼容版本：

  ```bash
  npm install
  ```

  或者，如果您想更新所有依赖项：

  ```bash
  npm update
  ```

- 再次运行 `ng build` 进行测试。

*注意*：更新时请谨慎，因为它们可能会引入破坏性变更。之后请彻底测试您的应用程序。

---

#### 步骤 4：降级 Node.js（最后的手段）

如果以上解决方案均无效，则 Node.js 22.9.0 可能尚未得到您项目当前配置的完全支持。降级到 Node.js 的长期支持版本，例如 **20.x** 或 **18.x**，可能会解决问题。

- 卸载您当前的 Node.js 版本。
- 从 [Node.js 官网](https://nodejs.org/) 下载并安装一个 LTS 版本。
- 验证安装的版本：

  ```bash
  node -v
  ```

- 重新安装项目依赖项：

  ```bash
  npm install
  ```

- 再次运行 `ng build`。

---

### 推荐方法

从**步骤 1**（设置 `NODE_OPTIONS`）开始，因为它是最快的修复方法，并且允许您继续使用 Node.js 22.9.0。如果无效，请继续执行**步骤 2** 和**步骤 3**。仅在必要时使用**步骤 4**，因为降级 Node.js 可能会限制对新功能的访问。

这应该能解决 "error 0308010C digital envelope routines::unsupported" 错误，并让您的 `ng build` 命令重新正常工作！
