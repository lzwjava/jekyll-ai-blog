---
audio: false
generated: true
lang: zh
layout: post
title: npm软件包的安装来源
translated: true
type: note
---

要将 `@ngx-formly/bootstrap` 包的安装源从本地的 `.tgz` 文件切换到 npm 仓库，请按照以下步骤操作：

### 1. 卸载本地安装的包
由于您之前是从本地的 `.tgz` 文件安装的 `@ngx-formly/bootstrap`，它目前位于您项目的 `node_modules` 目录中。要移除它，请在终端中运行以下命令：

```bash
npm uninstall @ngx-formly/bootstrap
```

此命令将从 `node_modules` 中移除该包。如果该包已手动添加到您的 `package.json` 文件中的 `dependencies` 或 `devDependencies` 下，此操作也会将其从中移除。如果它未在 `package.json` 中列出（常见于从 `.tgz` 文件安装但未保存的情况），它仍会从您的项目中移除。

### 2. 从 npm 仓库安装包
现在，通过运行以下命令从 npm 仓库安装该包：

```bash
npm install @ngx-formly/bootstrap
```

此命令将从 npm 仓库（通常是 `https://registry.npmjs.org/`，除非您配置了其他仓库）获取最新版本的 `@ngx-formly/bootstrap`，并将其安装到您的 `node_modules` 目录中。它还会将该包添加到您的 `package.json` 文件中的 `dependencies` 下（在较新的 npm 版本中默认如此），确保它作为项目的一部分被跟踪。

### 可选：验证仓库（如果需要）
如果您之前更改过 npm 仓库，并希望确保它设置为默认的 npm 仓库，您可以通过以下命令检查：

```bash
npm config get registry
```

如果输出是 `https://registry.npmjs.org/`，则表示您正在使用默认仓库，`npm install` 命令将按预期工作。如果它设置为其他仓库，并且您希望恢复到默认设置，请运行：

```bash
npm config set registry https://registry.npmjs.org/
```

不过，由于您提到已经配置了仓库，此步骤可能不是必需的。

### 注意事项
- **版本控制**：如果您需要与 `.tgz` 文件中相同的版本，请在卸载前检查 `node_modules/@ngx-formly/bootstrap/package.json` 中的版本号。然后，安装该特定版本：
  ```bash
  npm install @ngx-formly/bootstrap@<版本号>
  ```
  如果您未指定版本，将安装仓库中的最新版本。
- **依赖类型**：如果您希望将包作为开发依赖而不是常规依赖，请使用：
  ```bash
  npm install @ngx-formly/bootstrap --save-dev
  ```

通过遵循这些步骤，您将成功将 `@ngx-formly/bootstrap` 从通过本地 `.tgz` 文件安装切换到从 npm 仓库安装。
