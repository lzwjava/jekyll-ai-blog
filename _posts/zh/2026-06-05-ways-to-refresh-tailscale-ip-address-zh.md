---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 刷新Tailscale IP地址的方法
translated: true
type: note
---

问题：如何刷新或更改 Tailscale IP 地址？

答案：

Tailscale IP 地址通常在网络内保持稳定，但你可以**强制更改**，方法是重新分配或续订 IP。以下是几种实现方式：

1. **重启 Tailscale 服务**

   * 在大多数系统上，这会重新向 Tailscale 注册设备，如果之前的 IP 已被释放，有时会分配一个新 IP。
   * 命令：

     * **Linux/macOS：**

       ```bash
       sudo tailscale down
       sudo tailscale up
       ```
     * **Windows（以管理员身份运行 PowerShell）：**

       ```powershell
       tailscale down
       tailscale up
       ```

2. **删除并重新添加设备**

   * 前往 **Tailscale 管理控制台** → 设备 → 选择你的设备 → **删除**。
   * 然后使用 `tailscale up` 重新连接设备。
   * 这将确保获得一个新的 Tailscale IP。

3. **切换到不同的子网/出口节点**（可选）

   * 如果你的 Tailscale IP 属于某个路由子网，更改出口节点或子网路由器有时可以在该范围内获得一个新 IP。

4. **使用临时 IP（适用于高级配置）**

   * 在某些企业配置中，Tailscale 可以分配临时地址，但对大多数家庭用户而言，删除并重新添加设备是最简单的方法。

**总结：** 对于家庭服务器，最简单的方法是**停止 Tailscale 并重新启动**，或**从管理控制台中删除设备并重新连接**。

参考文档：

* [Tailscale 管理控制台](https://login.tailscale.com/admin)
* [Tailscale CLI 指南](https://tailscale.com/kb/1100/cli/)

如果你愿意，我可以介绍一个**强制 Tailscale 立即分配全新 IP 的技巧**，无需等待租约过期。需要我展示吗？