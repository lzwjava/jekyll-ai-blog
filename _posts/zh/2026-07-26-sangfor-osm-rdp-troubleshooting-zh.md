---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深信服OSM RDP故障排除
translated: true
type: note
---

问题：**如何通过深信服运维安全管理系统（深信服OSM/堡垒机）连接RDP？EasyConnect已连接，但远程桌面连接失败。**

**回答：**

在深信服运维安全管理系统（运维安全/堡垒机）中，架构通常如下：

```
你的电脑
  |
  | HTTPS
  |
EasyConnect (SSL VPN)
  |
  |
深信服运维安全管理系统
  |
  | RDP 协议
  |
Windows 服务器 / 电脑
```

EasyConnect 只创建 **VPN 隧道**。它**不**直接提供 RDP。VPN 连接后，你仍需访问堡垒机系统并启动 RDP 会话。

---

## 正确工作流程

### 1. 启动 EasyConnect

示例：

```
EasyConnect
    |
    v
https://vpn.company.com
    |
登录
    |
已连接
```

检查 VPN 适配器是否出现：

Windows：

```
Win + R
ncpa.cpl
```

你应看到类似：

```
Sangfor SSL VPN Adapter
```

或一个虚拟网络适配器。

---

### 2. 打开深信服运维安全管理系统 Web 门户

EasyConnect 连接后，打开：

```
https://<堡垒机地址>
```

或有时：

```
https://<vpn-address>:443
```

登录：

```
用户名
密码
OTP / 短信令牌
```

---

### 3. 找到目标资产

通常：

```
资产管理
    |
    └── Windows 服务器
            |
            └── RDP
```

或：

```
我的资源
    |
    └── 远程桌面
```

点击：

```
连接
```

堡垒机系统将创建 RDP 会话。

---

# 如果 RDP 失败

存在多个层次的原因。

## 情况 1：EasyConnect 已连接，但资产列表为空

含义：

```
VPN 正常
堡垒机身份验证正常
资产权限缺失
```

需要管理员授予：

```
用户
 |
资源权限
 |
Windows 服务器
 |
RDP 权限
```

---

## 情况 2：RDP 超时

示例：

```
连接超时
无法连接
```

检查：

从你的机器：

```powershell
Test-NetConnection <目标IP> -Port 3389
```

预期结果：

```
TcpTestSucceeded : True
```

如果为 false：

* Windows 防火墙阻止了 RDP
* 服务器未运行 RDP
* 网络路由缺失

---

## 情况 3：RDP 登录失败

示例：

```
登录尝试失败
```

通常：

错误：

```
用户名
密码
域
```

常见格式：

```
DOMAIN\用户名
```

或：

```
server\administrator
```

---

## 情况 4：浏览器 RDP 插件失败

深信服常使用：

* Web RDP
* ActiveX/插件
* HTML5 RDP

尝试：

### Chrome / Edge

允许弹出窗口：

```
设置
 → 网站权限
 → 弹出窗口
 → 允许
```

如果下载了：

```
.rdp
```

文件，用：

```
mstsc.exe
```

打开。

---

## 检查 EasyConnect 状态

运行：

```cmd
ipconfig
```

你应看到 VPN IP。

示例：

```
Ethernet adapter Sangfor VPN:

IPv4 地址 . . . . . . . . . . . . : 10.x.x.x
```

如果无 VPN IP：

```
EasyConnect 已连接
```

但隧道未建立。

---

## 重要提示：Windows 11 + EasyConnect

你之前的 EasyConnect 版本说明提到：

```
M7.1 之前不支持 Win11
```

意思是：

* M7.1 之前的版本不支持 Windows 11
* M7.6.x 应支持 Windows 11

因此确认：

```
EasyConnect 版本 >= 7.1
```

---

如需精确调试，关键信息是：

1. EasyConnect 状态：

```
已连接 / 失败？
```

2. VPN 登录后，能否打开：

```
https://堡垒机地址
```

3. 点击 RDP 时出现什么错误：

```
超时？
登录失败？
空白页面？
插件错误？
```

4. 你使用的是：

```
Web RDP
```

还是下载了：

```
.rdp 文件 + mstsc
```

失败点可以说明是 **VPN**、**堡垒机权限** 还是 **Windows RDP** 的问题。
