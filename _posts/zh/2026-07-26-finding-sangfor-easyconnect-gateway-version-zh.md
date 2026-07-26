---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 查找Sangfor EasyConnect网关版本
translated: true
type: note
---

问题：**如何查看深信服EasyConnect VPN网关版本？**

答案：

**网关版本是指深信服SSL VPN服务器版本**，而非EasyConnect客户端版本。通常只有公司VPN管理员知晓，但您可以通过以下几种方式找到。

## 方法一：查看EasyConnect登录页面（最简单）

打开公司VPN网址：

```
https://vpn.company.com
```

在登录前，查找以下内容：

* 页脚文字
* "关于"
* "系统信息"
* "版本信息"
* "深信服SSL VPN"
* "aTrust"

示例：

```
Sangfor SSL VPN M7.6.7
```

或

```
深信服SSL VPN 7.6.7
```

---

## 方法二：查看下载的客户端安装包

当您从公司VPN门户下载EasyConnect时，门户通常会嵌入服务器版本信息。

下载后：

Windows：

```
EasyConnectSetup.exe
```

右键点击：

```
属性
 → 详细信息
```

查找：

```
产品版本
```

或：

```
文件版本
```

示例：

```
7.6.7.12345
```

---

## 方法三：浏览器开发者工具

打开VPN登录页面。

按下：

```
F12
→ 网络
→ 刷新页面
```

查看请求/响应。

搜索关键词：

```
version
product
release
M7
```

有时会看到：

```
serverVersion=M7.6.7
```

---

## 方法四：询问VPN管理员

管理控制台通常显示：

```
系统管理
  ↓
系统信息
  ↓
版本信息
```

示例：

```
SSL VPN
版本：
M7.6.7R1
构建号：
xxxx
```

---

## 方法五：尝试最新客户端

针对您的情况（Windows 11 x64）：

安装：

```
EasyConnect M7.6.7+
```

如果网关版本较旧，通常会出现类似错误：

```
客户端版本过高，请下载对应版本客户端
```

或：

```
不支持当前服务端版本
```

如果登录成功，则兼容性良好。

---

鉴于您之前的问题（"EasyConnect在Windows 11上频繁崩溃"），我建议先检查：

1. 在Edge/Chrome中打开公司VPN网址。
2. 查看登录页面页脚/版本信息。
3. 若无显示，安装**M7.6.7+ x86 Windows客户端**。

该客户端通常能与较旧的M7.x网关通信，但Windows 11兼容性问题主要出现在非常旧的网关上（尤其是M7.1之前的版本）。