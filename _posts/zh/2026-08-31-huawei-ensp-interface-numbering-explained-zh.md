---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华为eNSP接口编号详解
translated: true
type: note
---

问题：在华为eNSP中，`interface Ethernet0/0/1` 里的每个数字分别代表什么？

答案：

格式 `Ethernet0/0/1` 的结构如下：

```
Ethernet [槽位] / [子槽位] / [端口]
            0   /     0     /   1
```

| 位置 | 名称 | 含义 |
| ------ | ------ | ------ |
| 第一个 `0` | **槽位号** | 接口卡所在的物理槽位（机箱槽位）。`0` 通常表示主/默认机箱槽位。 |
| 第二个 `0` | **子槽位号** | 该槽位内的子槽位或卡位。`0` 表示第一个（或唯一的）子卡。 |
| `1` | **端口号** | 该卡上的实际物理端口编号。端口编号通常从 `0` 开始，因此 `1` 表示**第二个端口**。 |

**简单来说：**

- `Ethernet 0/0/0` → 槽位 0，子槽位 0，端口 0（第1个端口）
- `Ethernet 0/0/1` → 槽位 0，子槽位 0，端口 1（第2个端口）
- `Ethernet 1/0/0` → 槽位 1，子槽位 0，端口 0（位于另一块线卡上）

> **注意：** 在 eNSP 模拟设备（如 AR2220）中，由于是虚拟环境，大多数接口的槽位和子槽位都保持为 `0`。通常你只需要修改**端口号**。

---

参考文档：

- [华为 AR 系列接口命名规范](https://support.huawei.com/enterprise/en/doc/EDOC1100055039)
- [eNSP 用户指南 – 华为](https://support.huawei.com/enterprise/en/doc/EDOC1100063899)
