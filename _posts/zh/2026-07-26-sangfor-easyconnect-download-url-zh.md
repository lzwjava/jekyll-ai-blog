---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深信服EasyConnect下载链接
translated: true
type: note
---

问题：**这个深信服URL是什么（`support.sangfor.com.cn/productSoftware/list?product_id=20&category_id=56`）？**

答案：

这是**深信服（Sangfor）技术支持的特定产品软件下载页面**。（[深信服支持][1]）

关键部分：

```
product_id=20
category_id=56
```

含义：

* `product_id=20` → 深信服产品ID
* `category_id=56` → 该产品下的软件下载分类

根据公开资料，此URL通常用于下载**深信服EasyConnect / SSL VPN客户端软件**。（[超腾开源][2]）

深信服产品包括：

* **EasyConnect** → 传统SSL VPN客户端，供员工远程访问公司内网。
* **aTrust** → 较新的零信任访问客户端。（[超腾开源][2]）

典型场景：

```
员工笔记本电脑
      |
      | EasyConnect客户端
      |
互联网
      |
      |
深信服SSL VPN网关
      |
      |
公司内部系统
（数据库 / Git / RDP / 内网应用）
```

因此，如果您的公司说：

> "安装EasyConnect"

通常意味着：

1. 从此页面下载Windows/macOS/Linux客户端。
2. 安装客户端。
3. 输入公司的VPN地址。
4. 使用公司账号/多因素认证登录。
5. 访问内部资源。

深信服支持门户还提供其安全和云产品的软件下载、工具、手册及故障排查资源。（[深信服支持][1]）

鉴于您之前关于**深信服RDP Web / 运维安全管理系统**的问题，这很可能属于同一企业远程访问生态系统的一部分：EasyConnect帮助您接入企业网络，然后您可以访问RDP、堡垒机或内部应用。（[深信服支持][1]）

参考：

* [深信服技术支持门户](https://support.sangfor.com.cn/?utm_source=chatgpt.com)
* [深信服EasyConnect与aTrust下载指南](https://www.hylab.cn/blog/detail/7461373793215320064?utm_source=chatgpt.com)
* [深信服产品支持分类](https://support.sangfor.com.cn/?pageType=2&utm_source=chatgpt.com)

[1]: https://support.sangfor.com.cn/?utm_source=chatgpt.com "深信服技术支持-简单、高效、自助化服务"
[2]: https://www.hylab.cn/blog/detail/7461373793215320064?utm_source=chatgpt.com "深信服VPN客户端下载：EasyConnect与aTrust零信任访问指南 - 超腾开源"
