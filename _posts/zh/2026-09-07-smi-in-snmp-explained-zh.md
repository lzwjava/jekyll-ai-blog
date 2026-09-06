---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SNMP中SMI详解
translated: true
type: note
---

问题：SNMP中的SMI是什么？

答案：

SMI 代表 **管理信息结构（Structure of Management Information）**。它是一组规则和约定，定义了在 SNMP（简单网络管理协议）中如何对管理对象（数据）进行命名、类型定义和编码。

SMI 是 SNMP 的**模式语言**——它本身并不传输数据，而是定义了 MIB（管理信息库）中的数据如何被组织和描述。

**SMI 的关键作用：**

- **命名**——每个管理对象都获得一个称为 OID（对象标识符）的唯一标识符，按层次树状结构组织。
- **类型定义**——定义管理对象允许的数据类型（例如 INTEGER、OCTET STRING、Counter32、Gauge32、TimeTicks、IpAddress）。
- **编码**——使用 ASN.1（抽象语法标记一）以供应商中立的方式描述对象定义。

**两个版本：**

| 版本 | 使用于 | 标准 |
|---|---|---|
| SMIv1 | SNMPv1 | RFC 1155 |
| SMIv2 | SNMPv2c, SNMPv3 | RFC 2578 |

SMIv2 通过添加更好的数据类型、更清晰的语法和增强的通知定义改进了 SMIv1。

**简单类比：** 如果 SNMP 是网络数据的邮政系统，那么 SMI 就是地址格式标准——它定义了如何编写地址（OID）以及每个数据包中允许包含何种内容（数据类型）。

参考文献：
- [RFC 1155 – 管理信息结构 v1](https://www.rfc-editor.org/rfc/rfc1155)
- [RFC 2578 – 管理信息结构 v2 (SMIv2)](https://www.rfc-editor.org/rfc/rfc2578)
- [SNMP 概述 – Cisco](https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/7282-12.html)