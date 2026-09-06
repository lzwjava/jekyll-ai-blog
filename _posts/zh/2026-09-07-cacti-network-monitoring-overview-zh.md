---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cacti网络监控概述
translated: true
type: note
---

**问题：** 什么是网络监控软件 Cacti？

**答案：**

**什么是 Cacti？**

Cacti 是一个开源的、基于 Web 的网络监控、性能、故障和配置管理框架，它是为开源、行业标准的数据记录工具 RRDtool 设计的前端应用程序。

**起源**

Cacti 起源于 2001 年，当时在一家小型 ISP 工作的高中生 Ian Berry 认识到需要一个易于访问且高效的网络数据可视化和监控工具。凭借他在 PHP 和 MySQL 方面的编程技能，Berry 开发了 Cacti，旨在使数据监控比当时的现有工具 RRDtool 更加用户友好。

**核心技术栈**

Cacti 使用 RRDtool、PHP，并将数据存储在 MySQL 中。它支持使用 SNMP 并通过 RRDtool 生成图形。Cacti 是 RRDtool 的完整前端——它将创建图形并用数据填充图形所需的所有信息存储在 MySQL 数据库中，其前端完全由 PHP 驱动。

**监控内容**

Cacti 旨在可视化时间序列数据，例如 CPU 负载、带宽使用率、磁盘 I/O 和内存利用率。它依赖于网络设备（路由器、交换机、服务器等）提供的 SNMP 数据，然后以图形方式处理和呈现这些数据，使用户能够轻松识别趋势。

**主要特性**

Cacti 完全支持 SNMPv1、SNMPv2 和 SNMPv3，使其几乎兼容所有网络设备。图形模板允许快速创建一致且可重复使用的性能图表，管理员可以通过最少的 manual 工作为数以百计的设备复制图形。

Cacti 最终用户前端支持用户和用户组安全模型，并支持基于角色的访问控制 (RBAC)。用户来源可以在本地定义，也可以通过 Apache 和 Nginx 基础身份验证协议（包括单点登录 (SSO) 提供商）从 LDAP、Active Directory 和其他协议中获取。Cacti 框架还可以通过插件进行扩展以增加额外功能。

**谁在使用它？**

Cacti 主要被全球的电信运营商和网络运营中心使用，同时也是商业 Spectrum LSF RTM 解决方案的核心，该解决方案用于监控基于 IBM LSF 的高性能计算 (HPC) 集群。

**为什么选择 Cacti？**

Cacti 提供企业级监控功能而无需许可费用，这对于任何规模的组织来说都具有成本效益。与 Zabbix 或 Nagios 等重量级监控解决方案相比，Cacti 消耗更少的系统资源，即使在长期使用中也能保持稳定。

---

**参考文献：**

- [Cacti (软件) — 维基百科](https://en.wikipedia.org/wiki/Cacti_(software))
- [供应商洞察：Cacti — Network Admin Tools](https://www.netadmintools.com/cacti/)
- [Cacti 监控工具：完整指南 — bckinfo.com](https://bckinfo.com/cacti-monitoring-tool-a-complete-guide-for-modern-it-infrastructure/)
- [Cacti 软件：网络监控与性能工具 — Click Magixo](https://clickmagixo.com/cacti-software)
- [Cacti 官方网站](https://www.cacti.net/)
