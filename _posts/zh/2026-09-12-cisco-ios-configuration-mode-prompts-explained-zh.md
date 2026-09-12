---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cisco IOS 配置模式提示符详解
translated: true
type: note
---

问题：在 Cisco IOS 中，`switch(config)#` 是什么意思，尤其是与 `switch(vlan)#` 相比？

回答：

这些提示告诉你当前所处的**配置模式**。

```text
Switch>
```

**User EXEC 模式** — 基本命令。

```text
Switch#
```

**Privileged EXEC 模式** — 管理命令。

```text
Switch(config)#
```

**全局配置模式** — 你正在配置整个交换机。

通常通过以下方式进入：

```text
Switch# configure terminal
Switch(config)#
```

从那里可以进入更具体的配置模式。

例如：

```text
Switch(config)# vlan 100
Switch(config-vlan)#
```

现在你正在**专门配置 VLAN 100**。

然后：

```text
Switch(config-vlan)# name SALES
```

你可以把它理解为一个层级结构：

```text
Switch#
  └── configure terminal
       └── Switch(config)#
            ├── vlan 100
            │    └── Switch(config-vlan)#
            │
            └── interface GigabitEthernet0/1
                 └── Switch(config-if)#
```

因此，**`(config)` 表示 "全局配置模式"**，而 **`(config-vlan)` 表示 "VLAN 配置子模式"**。

一个小修正：Cisco IOS 通常会显示 **`Switch(config-vlan)#`**，而不是 `Switch(vlan)#`。

我也可以带你完整走一遍 `Switch# → Switch(config)# → Switch(config-if)# → Switch(config-vlan)#` 的流程，结合一个具体的 VLAN 配置示例。