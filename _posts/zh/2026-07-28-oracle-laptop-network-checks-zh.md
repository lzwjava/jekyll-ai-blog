---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Oracle笔记本电脑网络检查
translated: true
type: note
---

端口1521在你网络中的所有可见设备上都是关闭的。这意味着我们需要在 **Oracle笔记本电脑** 上检查几项内容。

请你在 **Oracle笔记本电脑** 上执行以下检查，并告诉我结果：

### 1️⃣ 它的IP地址是什么？

在Oracle笔记本电脑的 **命令提示符** 中运行：

```cmd
ipconfig
```

查找活动网络适配器下的 `IPv4 地址`（例如 `192.168.1.xxx`）

### 2️⃣ Oracle监听器是否在运行？

在 **命令提示符** 中运行：

```cmd
lsnrctl status
```

### 3️⃣ 防火墙中是否开放了端口1521？

在 **命令提示符（以管理员身份运行）** 中执行：

```cmd
netsh advfirewall firewall show rule name=all | find "1521"
```

或者，如果缺少该规则，则添加防火墙规则：

```cmd
netsh advfirewall firewall add rule name="Oracle 1521" dir=in action=allow protocol=TCP localport=1521
```

一旦你告诉我IP地址和监听器状态，我将指导你完成后续步骤（在你的开发机上创建数据库用户并更新 `jdbc.properties`）。
