---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub CDN连接超时修复方案
translated: true
type: note
---

问题：为何在停止代理后`npx camoufox-js fetch`会因`UND_ERR_CONNECT_TIMEOUT 185.199.109.133:443`而失败，如何修复？

答案：

此错误表明**与 GitHub CDN 的直接连接被阻断或无法访问**：

```
ConnectTimeoutError: 185.199.109.133:443
```

该 IP 属于 **GitHub 发布 CDN**。
情况如下：

* 使用代理 → **极慢但仍可访问**
* 不使用代理 → **被阻断 / 超时**
* 结果 → 您陷入 **低速代理** 与 **被阻断的直连路径** 之间

这在某些网络环境下十分常见。

---

# 错误含义解读

Node.js 正在尝试访问：

```
https://github.com/.../camoufox...
```

它被解析到：

```
185.199.109.133
```

随后发生：

```
timeout: 10000ms
```

这意味着：

* TCP 连接无法建立
* 防火墙 / ISP / 路由问题
* 或您的网络无法访问 GitHub CDN

---

# 最快修复（仅为此命令使用代理）

运行：

```bash
proxychains4 -q npx camoufox-js fetch
```

但请在 proxychains 配置中启用 **dynamic_chain**：

编辑：

```bash
/opt/homebrew/etc/proxychains.conf
```

将：

```
strict_chain
```

改为：

```
dynamic_chain
```

这可以避免失效代理导致的阻塞。

---

# 更好修复（推荐方案）

仅为本次下载设置 HTTPS 代理：

```bash
HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
```

或：

```bash
ALL_PROXY=socks5://127.0.0.1:7890 npx camoufox-js fetch
```

（取决于您的本地代理端口）

此方法 **比 proxychains 快得多**。

---

# 最佳修复（手动下载 — 最快方案）

获取下载链接：

```bash
DEBUG=camoufox* npx camoufox-js fetch
```

输出将显示：

```
Downloading from:
https://github.com/.../camoufox-macos.zip
```

随后使用代理工具下载：

若使用 clash：

```bash
curl -L -x http://127.0.0.1:7890 -o camoufox.zip <URL>
```

或使用 socks：

```bash
curl --socks5 127.0.0.1:7890 -L -o camoufox.zip <URL>
```

解压文件：

```bash
mkdir -p ~/.cache/camoufox
unzip camoufox.zip -d ~/.cache/camoufox
```

最后运行：

```bash
npx camoufox-js fetch
```

程序会自动检测已下载的文件。

---

# 问题成因

您遇到的情况证明：

| 模式         | 结果           |
| ------------ | -------------- |
| proxychains  | 缓慢但有效     |
| 直连         | 超时           |
| 系统代理     | 未配置         |

因此只有 **正确的代理环境变量** 能解决问题。

---

# 简洁解决方案（单条命令）

使用：

```bash
ALL_PROXY=socks5://127.0.0.1:7890 npx camoufox-js fetch
```

通常可在：

```
10–30 秒
```

内完成，而非：

```
14 小时
```

---

若不确定代理端口，请运行：

```bash
lsof -iTCP -sTCP:LISTEN | grep -E "7890|1080|8888"
```

或告知您的代理类型：

* Clash？
* Surge？
* v2ray？
* shadowsocks？

我将提供精确命令。