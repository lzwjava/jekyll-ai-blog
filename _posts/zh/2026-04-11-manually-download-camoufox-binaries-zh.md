---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 手动下载 Camoufox 二进制文件
translated: true
type: note
---

**问题：** 在 `@askjo/camofox-browser` 项目中，执行 `npm install && npm start` 时下载速度很慢，我能否从 GitHub 仓库 <https://github.com/apify/camoufox-js> 手动下载 Camoufox 的二进制文件？

**回答：**

是的，你可以手动下载 Camoufox 的二进制文件，但你应该去 **Camoufox 的主仓库**（而不是 camoufox-js 仓库）来获取真正的浏览器二进制文件。

## 在哪里下载 Camoufox 二进制文件

浏览器二进制文件托管在 **daijro/camoufox** 仓库的发布页面，而不是 apify/camoufox-js 仓库。具体步骤如下：

### 第一步：访问 Camoufox 发布页面

前往 Camoufox 的主发布页面，下载适合你系统的二进制文件。

### 第二步：选择对应平台的二进制文件

最新的稳定版本是 **v135.0.1-beta.24**（截至 2025年3月15日）。根据你的操作系统和架构下载对应的文件：

- **Linux x86_64**: `camoufox-135.0.1-beta.24-lin.x86_64.zip`
- **Linux ARM64**: `camoufox-135.0.1-beta.24-lin.arm64.zip`
- **macOS x86_64**: `camoufox-135.0.1-beta.24-mac.x86_64.zip`
- **macOS ARM64**: `camoufox-135.0.1-beta.24-mac.arm64.zip`
- **Windows x86_64**: `camoufox-135.0.1-beta.24-win.x86_64.zip`

### 第三步：解压并放置二进制文件

下载后，解压压缩包，并将其放置在 Camoufox 预期找到的缓存目录中。通常的存放位置是：

- **Linux/macOS**: `~/.cache/camoufox/`
- **Windows**: `%LOCALAPPDATA%\camoufox\`

### 第四步：运行获取命令

手动放置二进制文件后，你可以运行：

```bash
npx camoufox-js fetch
```

此命令应能检测到现有的二进制文件，并跳过缓慢的下载过程。

## 替代方案：先使用 CLI 获取命令

如果你想避免缓慢的 npm postinstall 下载，可以：

1. 安装包时不运行 postinstall 钩子：

   ```bash
   npm install --ignore-scripts
   ```

2. 然后手动获取浏览器：

   ```bash
   npx camoufox-js fetch
   ```

这让你能更好地控制下载过程，并且如果下载失败可以重试。

## 重要说明

- **apify/camoufox-js** 仓库只是一个 JavaScript 封装库/客户端库——它不包含实际的浏览器二进制文件
- 实际的浏览器二进制文件由 **daijro/camoufox** 仓库构建和发布
- 当你运行 `npx camoufox-js fetch` 时，它从 daijro/camoufox 的发布页面下载二进制文件
- 你遇到的下载缓慢问题是因为二进制文件很大（约 700-800 MB）

**参考资料：**

- [https://github.com/daijro/camoufox/releases](https://github.com/daijro/camoufox/releases)
- [https://github.com/apify/camoufox-js](https://github.com/apify/camoufox-js)
- [https://camoufox.com/](https://camoufox.com/)
