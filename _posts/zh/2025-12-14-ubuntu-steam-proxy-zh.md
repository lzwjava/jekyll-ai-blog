---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ubuntu 上设置 Steam 代理
translated: true
type: note
---

问题：如何在 Ubuntu 上为 Steam 设置代理？

答案：

Ubuntu 上的 Steam 在其 UI 中没有内置的代理设置。它通过环境变量部分支持 HTTP/HTTPS 代理，用于客户端更新、登录和下载，但 Steam 的大部分流量（包括内容服务器和多人游戏）使用 UDP，而标准的 HTTP 代理不支持 UDP。这意味着在典型代理后面，完整功能（尤其是联机游戏）可能无法正常工作。

### 基本方法：使用环境变量（用于 HTTP/HTTPS 代理）
如果代理允许必要的连接，此方法适用于初始更新、登录和某些下载。

1. 打开终端。
2. 设置代理变量（替换为您的代理详细信息；如果需要身份验证，请包含 username:password）：
   ```
   export http_proxy="http://username:password@proxy-server:port/"
   export https_proxy="http://username:password@proxy-server:port/"
   export HTTP_PROXY=$http_proxy
   export HTTPS_PROXY=$https_proxy
   ```
   (通常大小写都需要。)
3. 从同一个终端启动 Steam：
   ```
   steam
   ```
   如果从菜单/GUI 启动，变量可能无法继承——设置后请务必从终端启动。

为了方便起见，将 exports 添加到 `~/.bashrc` 或 `~/.profile` 以实现持久性，但请通过终端启动 Steam 或创建自定义启动器。

### 高级方法：使用 Proxychains（用于 SOCKS 或更复杂的代理）
如果您的代理是 SOCKS5（在某些情况下更适合 UDP）或者上述方法不足：

1. 安装 proxychains：
   ```
   sudo apt update
   sudo apt install proxychains
   ```
2. 编辑配置文件：
   ```
   sudo nano /etc/proxychains.conf
   ```
   注释掉默认值并添加您的代理（例如，对于 SOCKS5）：
   ```
   socks5  proxy-server  port  username  password
   ```
   （或者如果支持，添加 http。）
3. 通过 proxychains 启动 Steam：
   ```
   proxychains steam
   ```
   这会强制更多的流量通过代理，但对于游戏来说可能会更慢或不稳定。

### 其他提示
- 添加 `-tcp` 启动选项以强制 TCP 连接（可能有助于兼容性）：
  ```
  steam -tcp
  ```
- Ubuntu 中的系统范围代理设置（Settings > Network > Proxy）不会可靠地影响 Steam。
- 如果在机构代理后面，请先在不受限制的网络上登录/更新 Steam，然后切换（下载可能仍需要代理）。
- 注意：使用代理（尤其是用于区域更改）可能违反 Steam 的服务条款。

参考：  

- [https://askubuntu.com/questions/227064/steam-linux-behind-a-proxy-server](https://askubuntu.com/questions/227064/steam-linux-behind-a-proxy-server)
- [https://blog.navinda.xyz/using-steam-with-proxy/](https://blog.navinda.xyz/using-steam-with-proxy/)
- [https://medium.com/@limeproxiesserver/how-to-use-steam-on-a-proxy-network-step-by-step-guide-6cfdd74c5b6](https://medium.com/@limeproxiesserver/how-to-use-steam-on-a-proxy-network-step-by-step-guide-6cfdd74c5b6)
- [https://superuser.com/questions/387856/getting-steam-exe-to-run-through-a-http-proxy](https://superuser.com/questions/387856/getting-steam-exe-to-run-through-a-http-proxy)