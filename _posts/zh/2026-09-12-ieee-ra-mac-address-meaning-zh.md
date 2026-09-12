---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IEEE RA MAC地址含义
translated: true
type: note
---

问题：分配MAC地址时，**IEEE RA**是什么意思？

回答：**IEEE RA = IEEE Registration Authority**。

在分配MAC地址时，IEEE RA是负责向企业分配全球唯一的MAC地址前缀（及相关标识符）的组织/服务。

例如：

```text
MAC address:  00:1B:21:12:34:56
              └──────┘
              OUI
```

前 **24位**（`00:1B:21`）通常是由IEEE Registration Authority分配的**OUI（组织唯一标识符）**。然后由公司管理剩余位来创建唯一的MAC地址：

```text
IEEE RA
   │
   └── assigns OUI: 00:1B:21
                    │
                    ├── device 1: 00:1B:21:00:00:01
                    ├── device 2: 00:1B:21:00:00:02
                    └── ...
```

### 实际应用中

如果你正在查看一个**"Assign MAC Address"**表单，"IEEE RA"通常意味着**你需要一个由IEEE分配的标识符**，而不是随意选择MAC前缀。

IEEE有几种相关的标识符类型：

- **MA-L** — 传统上等同于OUI；24位前缀
- **MA-M** — 28位前缀
- **MA-S** — 36位前缀

对于生产以太网/Wi-Fi设备的硬件厂商来说，这就是如何获得合法的全局唯一地址空间。

[IEEE Registration Authority — MAC Address Block Registration](https://standards.ieee.org/products-programs/regauth/tut/mac/?utm_source=chatgpt.com)

如果你告诉我你正在查看哪个**"Assign MAC Address"**屏幕/表单，我可以确切解释IEEE RA在那里期望什么值。