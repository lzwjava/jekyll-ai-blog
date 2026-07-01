---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Forgejo 软件锻造介绍
translated: true
type: note
---

问题：Forgejo 是什么？请基于官方网站介绍它。

回答：

## 什么是 Forgejo？

Forgejo 是一个 **self-hosted lightweight software forge** — 易于安装且维护成本低，旨在高效完成任务。其座右铭是 **"Beyond coding. We forge."**

---

## 起源与名称

**Forgejo**（发音 /forˈd͡ʒe.jo/）这个名称灵感来源于世界语 *forĝejo*，意为“forge”。

---

## 谁在背后支持？

Forgejo 由 **Codeberg e.V.** 旗下的包容性社区提供支持，这是一个民主的非营利组织。Codeberg e.V. 是一家在德国柏林注册的非营利协会，其目标是“guarantee the openness and continued availability of free software”。

Forgejo 的治理由其贡献者集体定义。

---

## 主要特性

Forgejo 专注于 **security, scaling, federation, and privacy**。以下是其核心亮点的 breakdown：

| 特性 | 描述 |
| --- | --- |
| **Simple Project Management** | 以易用性为设计理念，支持协作与生产力 |
| **GitHub Alternative** | 为 GitHub 用户提供熟悉的环境，便于平稳过渡到您拥有的平台 |
| **Easy Installation** | 托管自己的 forge 无需专家技能 |
| **Lightweight & Performant** | 功能丰富但服务器资源占用低，比其他 forge 需要更少资源 |
| **100% Free Software** | 始终是 Free and Open Source Software (FOSS) |
| **Federation** | 旨在实现去中心化的协作软件开发 |

---

## 与 Gitea 的关系

Forgejo 起源于 Gitea 的一个 fork。从 Gitea 到 Forgejo 的迁移通过 upgrade guide 支持。

---

## 许可证

Forgejo v9.0 及更高版本基于 **GPL v3+** 许可证分发。v8.0 及更早版本基于 MIT 许可证分发。

---

## 路线图与 Federation

Forgejo 的主要目标之一是使用 ForgeFed（ActivityPub 的扩展）实现 **forge federation**。这意味着 Forgejo 实例最终将能够以类似于 Mastodon 实例通信的去中心化方式相互交互。

---

## 如何使用

您可以在 Codeberg 或其他公共实例上创建账户，或者下载 Forgejo 来 self-host 自己的实例。

---

## 平台支持

2024 年放弃了对 Microsoft Windows 的支持，因为 Forgejo 社区目前缺乏维护针对 Windows 的 distribution 的专业知识。Linux 是主要支持的平台。

---

## 可持续性

Forgejo 依赖于志愿者贡献、资助、捐赠和员工委托的混合来维持运营。

参考文献：

- [https://forgejo.org](https://forgejo.org)
- [https://forgejo.org/faq/](https://forgejo.org/faq/)
- [https://forgejo.org/docs/latest/](https://forgejo.org/docs/latest/)
