---
audio: false
generated: false
image: true
lang: zh
layout: post
title: 一些全球云平台
translated: true
type: post
---

<div align="center"><img src="/assets/images/cloud/platform.jpg" width="400px"/><img/></div>

* [Azure](#azure)
* [AWS Lightsail](#aws-lightsail)
* [Digital Ocean](#digital-ocean)
* [Vultr](#vultr)
* [Google Cloud - 失败](#google-cloud---%E5%A4%B1%E8%B4%A5)
* [Outline](#outline)
* [概括](#%E6%A6%82%E6%8B%AC)

我最近尝试了一些云平台。我用它来设置我的代理服务器。之前，我使用的是第三方代理服务器。服务器被许多用户使用。所以有时速度很慢。我试着自己搭建来解决这个问题。

## Azure

Azure 是一个不错的选择。我在这里创建了 3 个虚拟机。因为平台免费给了我200美金。我的机器位于卡塔尔、美国和香港。从我的广州笔记本电脑到卡塔尔服务器的 ping 时间是 150ms。现在到美国服务器的 ping 数据包 100% 丢失了。前两天可以ping通。而且到香港服务器的ping包也是100%丢了。而且我在我的 iOS 代理客户端中测试了它们，它们无法连接。我需要关闭它们。虽然费用是免费的，但连不上的服务器对我来说没有用。

<div align="center"><img src="/assets/images/cloud/azure.png" /><img/></div>

让我们看看控制台和网络设置，在上图和下图中。

<div align="center"><img src="/assets/images/cloud/network.png" /><img/></div>

我的自定义网络设置很简单。我只是打开任何协议的 1024 到 65535 之间的任何端口。因为它是我的代理服务器。我里面没有任何秘密的数据或程序。所以我按照Outline 应用的建议去做。

## AWS Lightsail

Lightsail 是 AWS 的轻量级产品。 AWS 有很多产品。有时我们只是想在其中创建一些虚拟机。所以他们为我们提供了 AWS Lightsail。

<div align="center"><img src="/assets/images/cloud/lightsail.png" /><img/></div>

## Digital Ocean

Digital Ocean我在海外云平台用的比较多，尤其是2016年到2018年，每个月花5块钱。

我们创建一个这样的虚拟机：

<div align="center"><img src="/assets/images/cloud/do.png" /><img/></div>

这是我的账单历史：

<div align="center"><img src="/assets/images/cloud/bill.png" /><img/></div>

## Vultr

我从 2018 年到 2020 年一直在使用 Vultr。

<div align="center"><img src="/assets/images/cloud/vultr.png" /><img/></div>

## Google Cloud - 失败

我也想试试谷歌云。然而，我失败了。他们不支持中国用户。虽然我们可以提供虚假信息，假设我们是其他国家的公民。但是我们没有相应的信用卡，无法注册成功。

<div align="center"><img src="/assets/images/cloud/google.png" /><img/></div>

## Outline

Outline 不是云平台。它是一个代理工具。因为它帮我架设了我的代理服务器，所以不得不单独写一段来表扬一下。这真的很有帮助。您可以通过在线搜索来了解它。

<div align="center"><img src="/assets/images/cloud/outline.png" /><img/></div>

## 概括

最低配置的最便宜的服务器通常每月花费 5 美元左右。充当少数用户使用的代理服务器就足够了。新加坡、香港或其他亚洲地区的服务器通常比美国或欧洲的服务器连接速度更快。有时当您刚刚搭好服务器时，它工作得很好。然而，几天过去后，它就像僵尸一样。所以关于速度和稳定性，只能在日常使用中才能找到真相。
