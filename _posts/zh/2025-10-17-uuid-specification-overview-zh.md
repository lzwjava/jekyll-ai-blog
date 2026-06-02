---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: RFC 4122 UUID 规范概述
translated: true
type: note
---

RFC 4122 是由互联网工程任务组（IETF）于2005年7月发布的技术规范。该标准为通用唯一识别码（UUID）定义了统一资源名称URN命名空间，UUID也常被称为全局唯一标识符（GUID）。

UUID是一个128位的数字，用于在计算机系统中唯一标识信息，无需中央管理机构来协调标识符的分配。该标准详细说明了五种UUID版本（例如基于时间戳和MAC地址的版本1、基于随机比特的版本4）、生成方法、编码格式（如常见的带连字符十六进制字符串：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`），以及在协议和应用程序中的使用指南。这确保了不同系统和网络之间的互操作性。

该规范已被软件开发领域广泛采用，适用于数据库主键、会话标识符和分布式系统等场景。

[RFC 4122 - 通用唯一识别码URN命名空间](https://datatracker.ietf.org/doc/html/rfc4122)
[通用唯一识别码 - 维基百科](https://en.wikipedia.org/wiki/Universally_unique_identifier)
