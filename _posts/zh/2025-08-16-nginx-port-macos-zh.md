---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS系统修改Nginx端口指南
translated: true
type: note
---

你希望 macOS 上的 Nginx 监听**不同于默认端口**的端口（HTTP 默认为 80，HTTPS 默认为 443）。以下是一份清晰的逐步指南：

---

### 1. 定位 Nginx 配置文件

* 如果通过 **Homebrew** 安装，默认配置通常位于：

  ```
  /usr/local/etc/nginx/nginx.conf
  ```

  或在 Apple Silicon 芯片的 Mac 上：

  ```
  /opt/homebrew/etc/nginx/nginx.conf
  ```
* 如果手动安装，可能位于 `/usr/local/nginx/conf/nginx.conf`。

---

### 2. 编辑 `listen` 指令

1. 在文本编辑器中打开配置文件：

   ```bash
   nano /opt/homebrew/etc/nginx/nginx.conf
   ```
2. 找到 `server` 块：

   ```nginx
   server {
       listen 80;
       server_name localhost;

       location / {
           root   html;
           index  index.html index.htm;
       }
   }
   ```
3. 将 `listen 80;` 更改为你想要的端口，例如 8080：

   ```nginx
   listen 8080;
   ```

---

### 3. 测试配置

运行：

```bash
nginx -t
```

* 如果显示 `syntax is ok` 和 `test is successful`，说明配置有效。
* 如果有错误，请检查报告的行号。

---

### 4. 重启 Nginx

* 如果通过 Homebrew 安装：

```bash
brew services restart nginx
```

* 或手动重启：

```bash
sudo nginx -s reload
```

---

### 5. 通过新端口访问

* 在浏览器或 curl 中使用：

```
http://localhost:8080
```

---

**额外说明：**

* 端口号 **<1024** 在 macOS 上需要 `sudo` 权限。因此，使用 80 等端口需要 root 权限，但 8080 或 3000 等端口则不需要。
* 如果想同时运行多个 Nginx 服务器，每个服务器**必须使用唯一的端口**。

---

我还可以提供一个**快速技巧，无需编辑 nginx.conf 即可临时在任何端口上运行 Nginx**，使用命令行参数即可。这对于测试非常方便。需要我展示一下吗？
