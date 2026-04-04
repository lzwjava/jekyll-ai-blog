---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw WhatsApp Mihomo 代理设置
translated: true
type: note
---

问：如何通过Mihomo代理在端口7890上让OpenClaw的WhatsApp通道在中国正常工作？

答：

## 根本原因

WhatsApp在中国大陆被屏蔽，虽然Telegram已通过`channels.telegram.proxy`支持代理配置，但WhatsApp目前在OpenClaw中**尚未**提供原生的代理选项。这是一个已知的待实现功能请求。

您看到的`status=408 请求超时 WebSocket 错误`是由于Baileys WebSocket与WhatsApp Web服务器的连接被阻断所致——尽管通过系统`http_proxy`环境变量的`curl`能够正常工作，但设置`http_proxy`等环境变量并不能保证Node.js应用会使用它们。当应用程序使用其自身的显式代理配置时，会完全绕过系统代理隧道。请务必在应用层进行测试。

---

## 当前可行的解决方案

### 选项一：确认Mihomo确实在监听

首先，确认实际开放的端口：

```bash
for port in 1080 1087 1086 7890 7891 8080 8118 10808 10809; do
  nc -zv 127.0.0.1 $port 2>&1 | grep -v refused
done
```

Mihomo（如ClashX、Clash Verge或Mihomo Party）会暴露一个本地SOCKS5端口（默认：7891）和一个HTTP代理端口（默认：7890），这正是OpenClaw所需要的。

### 选项二：对Node.js使用 `ALL_PROXY` / `GLOBAL_AGENT_HTTP_PROXY`

标准的`http_proxy`环境变量常被Node.js的WebSocket库忽略。尝试在启动前为Node.js强制设置全局代理：

```bash
export ALL_PROXY=http://127.0.0.1:7890
export GLOBAL_AGENT_HTTP_PROXY=http://127.0.0.1:7890
openclaw channels login --channel whatsapp
```

或者使用SOCKS5（Mihomo的7891端口）：

```bash
export ALL_PROXY=socks5://127.0.0.1:7891
openclaw channels login --channel whatsapp
```

### 选项三：使用 `proxychains` 强制所有流量通过代理

安装并配置`proxychains-ng`：

```bash
sudo apt install proxychains4

# 编辑 /etc/proxychains4.conf
# 将最后一行改为：
socks5  127.0.0.1  7891
# 或http代理：
http    127.0.0.1  7890
```

然后运行：

```bash
proxychains4 openclaw channels login --channel whatsapp
```

这将强制OpenClaw的所有TCP连接（包括WebSocket）通过您的Mihomo代理。

### 选项四：将Mihomo设置为“TUN模式”（全局代理）

在Mihomo/Clash Verge中，启用 **TUN模式**（也称为“系统代理”或“全局模式”）。这将在操作系统网络层面路由所有流量，因此Node.js WebSocket也会被代理，无需任何应用层配置。

- 打开Mihomo/Clash Verge UI → 启用 **TUN模式** 或将模式设置为 **全局**
- 然后正常运行 `openclaw channels login --channel whatsapp`

---

## 长期解决方案（待定）

已提交功能请求，以添加类似Telegram代理方式的`channels.whatsapp.proxy`配置选项。提议的解决方案是通过`fetchAgent`选项将来自`undici`的`ProxyAgent`传递给Baileys的`makeWASocket`函数。一旦此功能合并，您将能够简单地运行：

```bash
openclaw config set channels.whatsapp.proxy "http://127.0.0.1:7890"
```

在此之前，**TUN模式**或**proxychains**是最可靠的变通方案。

---

## 另外：修复重复插件警告

您的`nextcloud-talk`插件警告与连接问题无关，但您可以通过移除捆绑的冲突来解决——要么删除自定义扩展，要么在配置中明确设置：

```bash
openclaw config set plugins.allow '["nextcloud-talk", "openclaw-weixin"]'
```

这样可以抑制自动加载警告，并使您的插件列表明确。

参考链接：

- [功能请求：WhatsApp代理支持（GitHub Issue #23500）](https://github.com/openclaw/openclaw/issues/23500)
- [错误报告：WSL2 + 代理出现相同的408错误（GitHub Issue #7885）](https://github.com/openclaw/openclaw/issues/7885)
- [OpenClaw Telegram中国代理调试指南](https://www.xugj520.cn/en/archives/openclaw-telegram-china-proxy-fix.html)