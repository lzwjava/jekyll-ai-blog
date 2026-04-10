---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 伪装狐取器代理应用
translated: true
type: note
---

问题：如何通过代理使用 npx camoufox-js fetch 以加速在中国的缓慢下载？

答案：

以下是通过代理进行 Camoufox 下载的方法（当您在中国且直接下载速度极慢时，这是最可靠的方式）。

### 1. 最佳且最简单的方法：设置环境变量（推荐）

在运行 fetch 命令之前，在终端中设置代理环境变量：

**对于大多数代理（HTTP/HTTPS 代理）：**
```bash
export HTTP_PROXY=http://你的代理IP:端口
export HTTPS_PROXY=http://你的代理IP:端口
```

**如果代理需要用户名和密码：**
```bash
export HTTP_PROXY=http://用户名:密码@你的代理IP:端口
export HTTPS_PROXY=http://用户名:密码@你的代理IP:端口
```

**以常见的本地代理如 Clash/V2Ray（端口 7890）为例：**
```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

然后运行 fetch 命令：
```bash
npx camoufox-js fetch
```

您也可以将命令合并为一行：
```bash
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
```

### 2. 如果想强制重新下载
```bash
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch --force
```

### 3. 永久设置（可选）
将 export 命令添加到您的 shell 配置文件中，以便每次生效：
- 对于 zsh（大多数 Mac 用户）：`echo 'export HTTP_PROXY=http://127.0.0.1:7890' >> ~/.zshrc`
- 然后运行 `source ~/.zshrc`

### 4. 替代方案：使用 npm config（有时对 npx 有帮助）
```bash
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890
npx camoufox-js fetch
```

**重要提示：**
- 在设置这些变量之前，请确保您的代理/VPN **正在运行并已连接**。
- 许多中国用户使用 Clash、V2Ray 或 Shadowsocks，端口为 7890 或 1080。
- 大多数情况下，即使对于 SOCKS5 代理也使用 `http://`（某些工具会自动转换）。
- 下载完成后，如果您希望取消设置这些变量，可以运行：
  ```bash
  unset HTTP_PROXY HTTPS_PROXY
  ```

### 5. 检查代理是否正常工作
在开始大文件下载之前，可以用一个小命令进行测试：
```bash
HTTP_PROXY=http://127.0.0.1:7890 curl -I https://www.google.com
```

如果能够快速返回响应头，说明代理对下载有效。

首先尝试环境变量方法——对于大多数在中国使用 Camoufox 时遇到下载缓慢问题的用户来说，此方法都有效。如果仍然无法工作，请告诉我您使用的具体代理（例如端口和类型），我可以提供更具体的命令。

参考资料：  
- https://www.mintlify.com/jo-inc/camofox-browser/installation（提到了为 camoufox-js fetch 设置 HTTP_PROXY）  
- https://github.com/daijro/camoufox/issues/342（用户讨论使用 ENV HTTP_PROXY / HTTPS_PROXY 进行 fetch 操作）  
- Node.js 环境变量代理的一般行为