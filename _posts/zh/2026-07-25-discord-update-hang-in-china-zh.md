---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Discord更新在中国卡住
translated: true
type: note
---

**问：为什么 Discord 一直卡在“正在检查更新”并挂起？**

**答：**

最可能的原因是 **从中国大陆访问 Discord 更新服务器失败或速度极慢**。

Discord 桌面端启动流程：

```
Discord.exe 启动
        |
        v
检查更新清单
        |
        v
下载最新应用包
        |
        v
验证安装包
        |
        v
启动 Electron 应用
```

卡住通常发生在第 1 或第 2 步。

在中国常见的几个原因：

### 1. Discord 更新服务器无法访问 / 不稳定

Discord 使用：

* `discord.com`
* `cdn.discordapp.com`
* `updates.discord.com`
* Cloudflare CDN

如果这些端点被屏蔽、限速或路由不佳，更新程序会无限等待。

测试方法：

```bash
curl -I https://discord.com
curl -I https://updates.discord.com
curl -I https://cdn.discordapp.com
```

如果超时，这就是原因。

---

### 2. Discord 旧缓存损坏

Electron 应用会将更新状态保存在本地。

尝试清理：

Windows：

```
%AppData%\Discord
%LocalAppData%\Discord
```

删除：

```
Cache
Code Cache
GPUCache
```

然后重启 Discord。

或者完全清理：

```powershell
taskkill /F /IM Discord.exe

rmdir /s /q "%AppData%\Discord"
rmdir /s /q "%LocalAppData%\Discord"
```

重新安装。

---

### 3. DNS 问题

中国 ISP 有时会返回错误的路由。

尝试使用：

```
1.1.1.1
8.8.8.8
```

DNS 设置：

Windows：

```
网络设置
 -> IPv4
 -> DNS 服务器
 -> 1.1.1.1
```

然后执行：

```cmd
ipconfig /flushdns
```

---

### 4. 代理/VPN 不匹配

Discord 通常只有在 **更新和应用的流量都通过同一路由** 时才能正常工作。

例如：

* 系统代理开启 → 更新程序使用代理
* Discord 应用不使用代理 → 登录失败

检查：

```
设置
 -> 网络和 Internet
 -> 代理
```

---

### 5. 手动更新方法

从以下地址下载最新 Discord 安装程序：

[Discord 下载](https://discord.com/download?utm_source=chatgpt.com)

覆盖安装现有版本。

---

针对中国用户，最快排查路径：

```bash
# 检查 DNS
nslookup discord.com

# 检查 HTTPS
curl -v https://discord.com

# 检查 CDN
curl -v https://cdn.discordapp.com
```

如果全部失败 → 网络路由问题，而非电脑问题。

很多中国用户通过代理/VPN 运行 Discord，因为 Discord 的服务器在中国大陆网络下无法稳定访问。
