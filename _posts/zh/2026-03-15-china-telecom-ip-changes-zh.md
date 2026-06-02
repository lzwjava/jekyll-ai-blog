---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国电信 IP 变更详解
translated: true
type: note
---

**问题：** 对于广州、广东的中国电信家庭宽带连接，IP 地址为 `14.19.28.xx` —— 这个 IP 地址会变吗？下周会变吗？它是否永久绑定到我的 ISP 账户？

**回答：**

## 简短回答

**是的，你的 IP 最终很可能改变。不，它并没有永久绑定到你的账户。** 原因如下和工作原理：

---

## 中国电信家庭宽带如何分配 IP

大多数中国电信家庭宽带用户（包括广州）通过 **PPPoE dial-up**（宽带拨号）连接。使用 PPPoE，ISP 会分配给你一个宽带账户和密码；每次连接时，电信提供商会动态分配一个 IP 地址给你。这是 **dynamic IP**，而不是 static IP。

Dynamic IP 地址是临时的，可以多次重新分配——每次重新连接时，电信可能会随机分配不同的 IP 地址。

---

## 你的 IP 何时会改变？

你的 IP `14.19.28.xx` 会在以下场景中改变：

## 你的 IP 下周具体会变吗？

**可能，但不保证。** 如果：
- 你的路由器保持通电并持续连接，没有中断 → 下周 IP 可能保持不变
- 发生任何断开/重新连接事件 → IP 几乎肯定会改变

---

## IP 是否绑定到你的 ISP 账户？

**不。** Static IP 是固定的并持续绑定到订阅者，而 dynamic IP 可以频繁改变。标准的中国电信家庭宽带提供 **dynamic IP** —— 它从地址池中分配，并没有永久分配到你的账户。不同的会话可以从同一地址池（例如 `14.19.28.x` 范围属于中国电信广东）中产生不同的 IP（具体的 `.xx` 后缀是临时的）。

如果你需要一个 **fixed/static IP** 永久绑定到你的账户，你需要向中国电信申请 **static IP service (固定IP)**，这通常需要额外月费，主要提供给企业用户。

---

## 总结

- 你当前的 IP `14.19.28.xx` 是 **dynamic**
- 只要你的连接重置，它 **就会改变**
- **下周**：取决于是否有断开，它可能改变也可能不变
- 它 **没有** 永久绑定到你的账户
- 要保持固定 IP，必须订阅中国电信的付费 **static IP** 服务

**参考资料：**

- [动态IP、静态IP、PPPoE区别 - CSDN](https://blog.csdn.net/u012294613/article/details/129156072)
- [DHCP Lease Time explained - CSDN](https://blog.csdn.net/chengyq116/article/details/85268669)
- [China Static IP Broadband - Connet](https://www.consp.com/china-static-ip-broadband)
- [China Telecom cloud-broadband upgrade explained](https://inntech.solutions/home-internet-in-china/)
