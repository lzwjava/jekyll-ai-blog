---
audio: false
generated: true
lang: zh
layout: post
title: 排查curl下载问题
translated: true
type: note
---

当你尝试使用 `curl -O` 从 eclipse.org 下载 Eclipse ZIP 文件时，可能会遇到下载到 HTML 文件而非所需 ZIP 文件的情况，并伴随 "301 永久移动" 错误。这是因为你使用的 URL 正在重定向到其他位置，而 `curl` 没有自动跟随该重定向到实际文件。以下是解决方法：

### 问题分析

- **301 永久移动**：此 HTTP 状态码表示资源（ZIP 文件）已永久移动到新 URL。服务器通常对下载链接使用重定向，指向镜像站点或更新后的位置。
- **`curl -O` 行为**：`-O` 选项指示 `curl` 将下载内容保存为远程文件名。但若不显式处理重定向，`curl` 可能会保存中间重定向响应（通常是 HTML 页面）的内容，而不是跟随重定向获取 ZIP 文件。

### 解决方案

为确保 `curl` 跟随重定向并下载 Eclipse ZIP 文件，请在使用 `-O` 选项的同时添加 `-L` 选项。`-L` 标志会指示 `curl` 跟随所有重定向直至最终目标。

#### 命令

```bash
curl -L -O <URL>
```

- **`-L`**：跟随重定向（如 301 重定向）到新位置
- **`-O`**：按最终 URL 中的原始文件名保存文件
- **`<URL>`**：替换为具体的 Eclipse 下载 URL，例如 `https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2023-03/R/eclipse-java-2023-03-R-win32-x86_64.zip`

### 操作步骤

1. **获取正确 URL**：
   - 访问 Eclipse 官网（如 `https://www.eclipse.org/downloads/`）
   - 选择所需软件包（如 Eclipse IDE for Java Developers）
   - 右键点击下载链接或按钮复制 URL，或使用浏览器开发者工具（F12，网络标签页）在点击下载时捕获精确 URL

2. **执行命令**：
   - 打开终端
   - 使用复制的 URL 执行带 `-L` 和 `-O` 选项的 `curl` 命令：

     ```bash
     curl -L -O https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2023-03/R/eclipse-java-2023-03-R-win32-x86_64.zip
     ```

   - 这将下载 ZIP 文件（如 `eclipse-java-2023-03-R-win32-x86_64.zip`）到当前目录

### 故障排除

若仍遇到问题，可尝试以下步骤：

- **使用详细输出检查重定向**：
  - 使用 `-v` 选项查看请求和重定向的详细信息：

    ```bash
    curl -v -L -O <URL>
    ```

  - 查看 301 响应中的 `Location` 标头了解重定向目标。若指向 HTML 页面而非 ZIP 文件，则该 URL 可能不是直接下载链接

- **验证 URL**：
  - Eclipse 常使用 `download.php` 脚本重定向到镜像。请确保 URL 是 ZIP 文件的直链或能解析为文件的重定向链接。例如直链可能形如：

    ```bash
    curl -L -O https://mirror.its.dal.ca/eclipse/technology/epp/downloads/release/2023-03/R/eclipse-java-2023-03-R-win32-x86_64.zip
    ```

- **设置用户代理标头**：
  - 某些服务器会根据客户端类型返回不同内容。若服务器因检测到 `curl` 而返回 HTML，可模拟浏览器添加 User-Agent：

    ```bash
    curl -L -O -A "Mozilla/5.0" <URL>
    ```

### 原理说明

Eclipse 网站可能将下载请求重定向到镜像或更新后的 URL。未使用 `-L` 时，`curl -O` 会保存重定向响应（HTML 页面）而不跟随。添加 `-L` 可确保 `curl` 跟踪 301 重定向至实际 ZIP 文件，从而解决问题。

遵循以上步骤，你应当能成功使用 `curl` 从 eclipse.org 下载 Eclipse ZIP 文件。
