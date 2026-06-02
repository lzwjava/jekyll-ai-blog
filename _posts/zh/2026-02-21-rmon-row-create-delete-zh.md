---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RMON 启用行创建与删除
translated: true
type: note
---

问题：在不修改或违反 SNMPv1 管理框架的情况下，RMON 规范提供了哪些操作？

答案：

正确答案是 **C：行创建和行删除操作**。

### 解释：
- **SNMPv1 的局限性**：原始 SNMPv1 框架（定义于 RFC 1157）在表操作方面存在显著限制。虽然它支持 `GET`、`GETNEXT`、`SET` 和 `TRAP` 操作，但缺乏标准化的原子机制来创建表中的新行或删除现有行。`SET` 操作可以修改单个单元格，但无法以健壮的方式原生支持确保整行的完整性（例如同时创建所有必要的列）。
- **RMON 的解决方案**：远程监控（RMON）规范（最初为 RFC 1271，后为 RFC 2819）旨在在不修改核心协议的情况下与现有 SNMPv1 框架协同工作。为克服表操作的限制，RMON 引入了一组**文本约定**和**程序规则**。
- **行状态（Row Status）**：该解决方案的关键部分是“行状态”概念（通常使用整数列控制行的状态，如 `createRequest`、`active`、`destroy` 等）。这允许管理站通过标准 SNMP `SET` 操作对特定控制列进行操作，按照定义的程序规则逻辑**添加（创建）**和**删除** RMON 表（如 `etherStatsTable`）中的行。
- **其他选项为何错误**：
    - **A**：检索未知对象通常通过标准 SNMPv1 中的 `GETNEXT` 完成，并非 RMON 为此目的特别添加的功能。
    - **B**：检索表对象通过标准 SNMPv1 中的 `GETNEXT` 实现。
    - **D**：设置或更新变量值是 SNMPv1 中基本的 `SET` 操作，并非 RMON 为弥补框架缺陷而特别提供的新能力。

因此，RMON 特别填补了**行创建和删除**的功能空白（选项 C）。

参考资料：

- [RFC 2819: Remote Network Monitoring Management Information Base](https://datatracker.ietf.org/doc/html/rfc2819)
- [RFC 1157: Simple Network Management Protocol (SNMP)](https://datatracker.ietf.org/doc/html/rfc1157)
