---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 360爪 SSL 密钥泄露丑闻
translated: true
type: note
---

我将搜索有关 360 Claw 以及与这家中国网络安全公司相关的任何 SSL certificate leaks 的信息。问题：Qihoo 360（一家中国网络安全公司）如何在其门户中泄露其 SSL certificate？

答案：

Qihoo 360 在其安装程序中附带了 AI 助手 "Security Claw" 的 *.myclaw.360.cn wildcard SSL private key。私钥覆盖平台上的所有子域名，有效期至 2027 年 4 月。

## SSL 证书泄露过程

*.myclaw.360.cn 的 private key 直接捆绑在下载包中，路径为 `/namiclaw/components/OpenClaw/openclaw.7z/credentials`。这代表了软件构建和打包过程中的严重失误。

## 技术影响

该 certificate 有效期至 2027 年 4 月，即使 360 立即撤销并重新颁发 certificate，从安装程序发布到撤销期间连接到 myclaw.360.cn 的所有用户都处于暴露窗口中。在此期间使用泄露密钥拦截的任何流量均被追溯性 compromised。

## 讽刺的矛盾

产品发布前六天，创始人 Zhou Hongyi 宣布 "360 Security Claw"，并特别承诺它“不会损坏用户系统、删除数据或泄露用户计算机上的密码或其他私人信息”。产品在发布时泄露了 private key。

## 根本原因

SSL key 泄露违反了最基本的セキュリティ实践——不在面向客户端的包中 shipping private keys。这表明构建管道失败，credential 文件未从分发存档中排除。

## 安全影响

拥有泄露的 SSL private key，攻击者现在可以：

- 冒充 360 的服务器
- 拦截用户流量
- 伪造登录页面并将用户重定向到恶意站点
- 潜在窃取通过这些通道传输的敏感用户数据

参考资料：

- [Awesome Agents - China's Top Cybersecurity Firm Ships SSL Key in AI App](https://awesomeagents.ai/news/qihoo-360-ssl-key-leak-openclaw/)
- [Phemex News - 360's OpenClaw AI Assistant Leaks SSL Key](https://phemex.com/news/article/360s-openclaw-ai-assistant-leaks-ssl-private-key-breaching-security-promises-66798)
