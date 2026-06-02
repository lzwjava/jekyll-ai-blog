---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Node.js OpenSSL 传统提供程序标志
translated: true
type: note
---

### 问题根源
Node.js 16（及更早版本）使用 OpenSSL 1.x，而 Node.js 22 引入了具有更严格安全默认设置的 OpenSSL 3.x。这可能导致某些应用程序出错，特别是那些依赖旧版加密提供商或已弃用算法（例如 MD4 哈希）的应用。`--openssl-legacy-provider` 标志可临时启用与 OpenSSL 1.x 行为的兼容性，以在升级期间解决这些问题。

**注意**：此标志是临时解决方案，可能在未来的 Node.js 版本中被移除。它最适合短期修复——请尽可能更新代码以使用现代 OpenSSL 3.x API。

### 如何使用该标志
您可以在直接运行 Node.js 或通过 npm/yarn 脚本时应用此标志。这是一个运行时选项，并非永久性配置。

#### 直接运行 Node 命令
在脚本或命令前添加该标志。示例：
- 基础脚本执行：`node --openssl-legacy-provider app.js`
- REPL（交互模式）：`node --openssl-legacy-provider`
- 运行模块时：`node --openssl-legacy-provider --input-type=module index.mjs`
- 带附加参数：`node --openssl-legacy-provider --max-old-space-size=4096 script.js`

这将启用旧版提供商支持，避免出现诸如 "digital envelope routines unsupported"（与过时的哈希或密码相关）等常见错误。

#### 用于 npm/Yarn 脚本
修改 `package.json` 中 `"scripts"` 部分，在相关命令中加入该标志。示例：
```json
{
  "scripts": {
    "start": "node --openssl-legacy-provider app.js",
    "dev": "node --openssl-legacy-provider --watch app.js"
  }
}
```
然后照常运行：`npm start` 或 `yarn dev`。

若使用 nodemon 或 vite 等会创建 Node 进程的工具，请在其配置中前置该标志（例如在 nodemon.json 中：`"exec": "node --openssl-legacy-provider"`）。

#### 用于全局命令（如通过 nvm 或系统 Node）
若使用 nvm 管理 Node 版本，请切换至 Node 22 并按所示方式带标志运行命令。对于 Docker 或 CI/CD，请将其添加到运行脚本中（例如 `CMD ["node", "--openssl-legacy-provider", "app.js"]`）。

### 故障排查与替代方案
- **验证标志是否生效**：运行 `node --openssl-legacy-provider --version`——应能无错误输出 Node 22 版本号。
- **已修复的常见问题**：涉及加密模块的 `require()` 调用、webpack 构建或应用启动时的错误。若问题依旧存在，请检查 OpenSSL 专用代码（例如使用 `crypto.createCipheriv` 等替代 `crypto.createCipher`）。
- **长期解决方案**：扫描已弃用的加密用法（使用 ESLint 插件等工具）并更新至 OpenSSL 3.x 兼容方法。Node 22 文档推荐使用 `bcrypt` 或 `crypto.scrypt` 等库进行哈希计算。
- **性能/兼容性说明**：旧版提供商模式可能会轻微影响安全性/功能，但有助于迁移过渡。请进行充分测试，因为某些 OpenSSL 3 功能（例如增强的熵源）将不可用。

更多详细信息，请参阅 Node.js OpenSSL 文档：nodejs.org/api/crypto.html。如果您提供具体的错误信息，我可以给出更具针对性的建议！
