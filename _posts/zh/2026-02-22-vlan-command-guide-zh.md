---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 创建 VLAN 命令指南
translated: true
type: note
---

问题：在登录交换机后，在 **global configuration mode** 下，用于创建 VLAN 的命令是什么？

答案：

在登录并进入 **global configuration mode** 后，在 Cisco switch（或类似基于 CLI 的网络设备）上创建 VLAN，使用以下命令：

```bash
vlan <vlan-id>
```

### 说明：
- **`vlan`**：这是命令关键字，指示交换机要创建或配置 VLAN。
- **`<vlan-id>`**：这是实际要创建的 VLAN 编号的占位符。有效的 VLAN ID 通常范围为 **1 到 4094**，尽管某些范围被保留（例如，VLAN 1 是默认的，VLAN 1002–1005 为遗留 token ring/FDDI 保留）。

### 逐步示例：
1. 登录交换机。
2. 进入 privileged EXEC mode：
   ```bash
   enable
   ```
3. 进入 global configuration mode：
   ```bash
   configure terminal
   ```
4. 创建 VLAN（例如，VLAN 10）：
   ```bash
   vlan 10
   ```
5. （可选）为 VLAN 命名：
   ```bash
   name Sales
   ```
6. 退出配置模式：
   ```bash
   end
   ```

执行 `vlan 10` 后，交换机将进入 **VLAN configuration mode**（`config-vlan#`），在那里可以可选地为 VLAN 分配名称或其他参数。

这与提供的参考答案匹配：**`vlan vlan-id`**。

参考资料：  

- [Cisco VLAN Configuration Guide](https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/17056-7.html)