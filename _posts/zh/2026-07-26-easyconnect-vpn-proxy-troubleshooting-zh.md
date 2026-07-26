---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EasyConnect VPN代理故障排除
translated: true
type: note
---

问题：**如何使用Sangfor EasyConnect 20.80MB Windows客户端？显示代理设置/浏览器代理/用户名和VPN连接失败。**

答案：

`EasyConnect` 并非普通的 HTTP 代理客户端，它是深信服（Sangfor Technologies）的 **VPN SSL 客户端**。其流程通常如下：

```
Windows 电脑
   |
   | HTTPS (443)
   |
深信服 SSL VPN 网关
   |
企业网络资源
```

**通常不需要设置浏览器代理**。Windows 代理和 EasyConnect VPN 是独立的两个部分。微软也指出 VPN 连接和代理设置是分别配置的。（[微软支持][1]）

---

## 1. 安装 EasyConnect

运行：

```
EasyConnect_x64_7_6_7_3.exe
```

根据你的文本，要求如下：

* 支持 Windows x86/x64
* 支持 ARM Windows 8/10
* 不支持 ARM Windows 11
* 不支持 Windows Server

你的联想小新 / 普通 Intel 笔记本：

```
CPU: x86_64
Windows 11
```

应使用：

```
x64 版本
```

---

## 2. 正常连接步骤

打开 EasyConnect：

```
服务器地址：
https://vpn.example.com
```

例如：

```
https://vpn.company.com
```

然后：

```
连接
    |
    v
用户名
密码
OTP（如果需要）
    |
    v
VPN 已连接
```

你需要的是 **VPN 网关地址**，而非代理地址。

---

## 3. **不要**在此处设置 Mihomo/Clash 代理

你之前有：

```yaml
port: 7890
socks-port: 7891
mixed-port: 7892
```

**不要**将：

```
127.0.0.1:7890
```

填入 EasyConnect，除非你的公司明确要求使用出站代理。

错误示例：

```
EasyConnect
代理：
127.0.0.1
7890
用户名
密码
```

这通常会导致：

```
连接失败
代理认证失败
```

因为 EasyConnect 尝试通过 Clash 代理访问 VPN 网关。

---

## 4. 如果公司要求使用代理

部分企业网络要求：

```
互联网
   |
HTTP 代理
   |
EasyConnect
   |
VPN 网关
```

此时在 EasyConnect 中配置：

通常路径：

```
设置
  |
  高级
  |
  代理
```

填写：

```
代理类型：
HTTP

服务器：
proxy.company.com

端口：
8080

用户名：
<公司代理用户名>

密码：
<公司代理密码>
```

这里的用户名/密码是**代理凭据**，而非 VPN 凭据。当这些凭据与代理服务器不匹配时，会出现代理认证失败。（[Magic Connect][2]）

---

## 5. 排查连接失败

打开 Windows 命令提示符：

### 检查 DNS

```cmd
nslookup vpn.company.com
```

应返回 IP 地址。

---

### 检查 HTTPS 端口

```powershell
Test-NetConnection vpn.company.com -Port 443
```

预期结果：

```
TcpTestSucceeded : True
```

如果为 False：

* 防火墙阻止
* VPN 地址错误
* 网络无法到达网关

---

### 检查 Windows 代理

前往：

```
设置
 → 网络和 Internet
 → 代理
```

临时关闭：

```
使用代理服务器 = 关闭
```

微软建议在应用程序无法通过代理连接时，检查代理地址和端口。（[微软支持][1]）

---

## 6. 常见的 EasyConnect 问题

### 错误：立即连接失败

可能原因：

```
错误的 VPN URL
错误的端口
DNS 故障
```

---

### 登录成功但 VPN 失败

可能原因：

```
未安装 EasyConnect 驱动
Windows 11 兼容性问题
端点安全软件拦截
```

运行：

```
services.msc
```

查找深信服相关服务。

---

### 浏览器能上网但 EasyConnect 失败

这很正常。

浏览器：

```
HTTP/HTTPS
```

EasyConnect：

```
SSL VPN 隧道
虚拟网卡
网络驱动
```

处于不同层级。

---

## 建议的首次测试步骤

1. 关闭 Windows 代理：

```
设置
→ 网络
→ 代理
→ 关闭
```

2. 临时关闭 Clash/Mihomo。

3. 打开 EasyConnect。

4. 仅输入：

```
VPN 服务器 URL
VPN 用户名
VPN 密码
```

5. 点击连接。

如果仍然失败，请提供：

```
EasyConnect 错误截图
VPN 服务器 URL 格式（敏感信息可隐藏公司域名）
Windows 版本
EasyConnect 版本
```

我们可以进一步排查具体的失败路径。

[1]: https://support.microsoft.com/en-US/Windows/Experience/Connectivity-Networking/use-a-proxy-server-in-windows?utm_source=chatgpt.com "在 Windows 中使用代理服务器 | 微软支持"
[2]: https://www.magicconnect.net/faq/trouble/faq_254/?utm_source=chatgpt.com "「HTTP Proxy[xxx.xxx.xxx.xxx : xxxx]的认证失败。……（咨询代码:1461或1463）」显示。｜常见问题｜值得信赖的远程接入 MagicConnect｜NTT TechnoCross"