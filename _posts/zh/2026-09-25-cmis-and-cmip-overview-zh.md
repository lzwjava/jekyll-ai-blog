---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMIS与CMIP概述
translated: true
type: note
---

**问题：** CMIS和CMIP在网络中是什么，它们之间有什么关系？

**答案：**

CMIS和CMIP是一对密切相关的OSI网络管理标准——CMIS定义了“什么”（服务接口），而CMIP定义了“如何”（实现它的协议）。

---

### CMIS — Common Management Information Service

CMIS是ITU-T建议X.710 / ISO/IEC 9595中指定的服务接口，用于OSI网络元素的网络管理。它定义了由CMIP（X.711）实现的服务接口，并且是开放系统互连（OSI）国际网络标准体系的一部分。

CMIS定义了一个消息集，用于对等进程之间交换信息和命令，以进行网络管理。在概念上，它类似于SNMP，但更强大——因此也更复杂。

CMIS提供的服务（通过所谓的**CMISE**元素）包括：

- **M-CREATE** – 创建一个管理对象的实例
- **M-DELETE** – 删除一个管理对象的实例
- **M-GET** – 请求管理对象的属性（对于一个或一组对象）
- **M-CANCEL-GET** – 取消未完成的GET请求
- **M-SET** – 设置管理对象的属性
- **M-ACTION** – 请求对管理对象执行一个动作
- **M-EVENT-REPORT** – 发送管理对象上发生的事件

---

### CMIP — Common Management Information Protocol

CMIP是OSI指定的网络管理协议，定义在ITU-T建议X.711 / ISO/IEC 9596-1中。它提供了对CMIS定义的服务的一种实现，允许网络管理应用程序和管理代理之间的通信。CMIP以管理对象的形式对管理信息进行建模，并允许修改和对它们执行动作。管理对象使用GDMO（管理对象定义指南）进行描述，并且可以通过X.500中的区分名（DN）进行标识。

CMIP还提供了良好的安全性——支持授权、访问控制和安全日志——以及灵活的报告异常网络条件的能力。

**实现栈：** CMIP与ACSE和ROSE协议联合实现，两者都是第7层OSI（应用层）协议。ACSE管理管理应用程序之间的关联（即CMIP代理之间的连接），而ROSE用于所有数据交换交互。

---

### CMIS与CMIP的关系

可以这样理解：

| | CMIS | CMIP |
| --- | --- | --- |
| **角色** | 服务定义（API） | 协议实现（有线格式） |
| **标准** | ITU-T X.710 / ISO 9595 | ITU-T X.711 / ISO 9596-1 |
| **定义** | *什么*操作可用 | *如何*传输这些操作 |
| **层** | 应用层（接口） | 应用层（协议） |

> 注意：术语CMIP有时被错误地用于指代CMIS。

---

### CMIS/CMIP与SNMP对比

CMIP的功能在管理操作和管理信息方面都高于SNMP且更复杂。GDMO（由CMIP使用）也比SMI（由SNMP使用）更复杂。

CMIS/CMIP最常用于电信应用程序；在其他领域，SNMP变得更流行。

---

**参考：**

- [CMIS – Wikipedia](https://en.wikipedia.org/wiki/Common_Management_Information_Service)
- [CMIP – Wikipedia](https://en.wikipedia.org/wiki/Common_Management_Information_Protocol)
- [RFC 1189 – CMOT和CMIP (IETF)](https://www.rfc-editor.org/rfc/rfc1189.html)
- [CMIS – FOLDOC](https://foldoc.org/CMIS)
