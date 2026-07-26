---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Clash 的 Windows 代理设置
translated: true
type: note
---

问题：**如何设置Windows系统代理使用你的Mihomo/Clash配置（`mixed-port: 7892`）？**

回答：

你的Mihomo配置暴露了以下端口：

```yaml
port: 7890          # HTTP代理
socks-port: 7891    # SOCKS5代理
mixed-port: 7892    # HTTP + SOCKS混合端口
allow-lan: true
```

对于**Windows系统代理**，请使用**HTTP代理端口**或**混合端口**。

## 选项1：Windows图形界面

1. 打开：

```
设置
→ 网络和 Internet
→ 代理
```

2. 在**手动设置代理**下：

启用：

```
使用代理服务器：开
```

设置：

```
地址：127.0.0.1
端口：7892
```

示例：

```
http://127.0.0.1:7892
```

保存。

---

## 选项2：PowerShell（快速）

以普通用户身份运行：

```powershell
netsh winhttp set proxy 127.0.0.1:7892
```

检查：

```powershell
netsh winhttp show proxy
```

重置：

```powershell
netsh winhttp reset proxy
```

---

## 选项3：环境代理（适用于命令行工具）

许多开发者工具使用环境变量：

PowerShell：

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7892"
$env:HTTPS_PROXY="http://127.0.0.1:7892"
```

永久设置：

```powershell
[Environment]::SetEnvironmentVariable(
  "HTTP_PROXY",
  "http://127.0.0.1:7892",
  "User"
)

[Environment]::SetEnvironmentVariable(
  "HTTPS_PROXY",
  "http://127.0.0.1:7892",
  "User"
)
```

---

## 验证

打开PowerShell：

```powershell
curl https://www.google.com
```

或：

```powershell
curl https://api.ipify.org
```

你应该能看到代理出口IP。

---

## 重要提示：`allow-lan`

你的配置：

```yaml
allow-lan: true
```

意味着其他设备可以访问Mihomo，但**对于同一台Windows机器**，你只需要：

```
127.0.0.1:7892
```

无需修改防火墙设置。

---

## 如果Mihomo运行在另一台机器（Mac）上

你的命令提示符显示：

```
lzwjava@lzw-mac
```

如果Mihomo运行在你的Mac上，而Windows需要连接它：

1. 查找Mac IP：

```bash
ifconfig en0 | grep inet
```

示例：

```
192.168.1.100
```

2. Windows代理设置：

```
地址：192.168.1.100
端口：7892
```

3. 确保Mac防火墙允许端口7892。

你当前的：

```yaml
allow-lan: true
```

对于这种情况已经是正确的配置。