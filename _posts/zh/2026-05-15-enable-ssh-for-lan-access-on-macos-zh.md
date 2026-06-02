---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 macOS 上启用 SSH 以进行局域网访问
translated: true
type: note
---

问题：如何在 macOS 上启用 SSH，以便通过局域网（LAN）登录？

答案：

要通过局域网使用 SSH 访问你的 Mac，你需要启用 SSH 服务器（在 macOS 上称为 **远程登录**），然后从另一台设备连接。以下是分步指南：

---

### 1. 在 macOS 上启用 SSH

1. 打开 **系统设置**（或 **系统偏好设置**，取决于 macOS 版本）。
2. 进入 **共享**。
3. 找到并 **勾选“远程登录”**。

   * 这会自动启动 SSH 服务器。
   * 你可以选择允许访问：

     * **所有用户** – 你 Mac 上的任何用户账户。
     * **仅这些用户** – 指定哪些账户可以登录。
4. 注意顶部显示的信息，例如：

   ```
   要远程登录这台电脑，请输入 "ssh username@192.168.x.x"
   ```

   * 其中，`username` 是你的 Mac 账户名，`192.168.x.x` 是你的 Mac 本地 IP 地址。

---

### 2. 查找 Mac 的本地 IP

1. 进入 **系统设置 > 网络**。
2. 选择你当前使用的网络（Wi-Fi 或以太网）。
3. 记下 **IP 地址**（例如 `192.168.1.25`）。

---

### 3. 从局域网内的另一台设备连接

1. 在局域网内的另一台电脑（Windows、Linux 或 Mac）上，打开终端（Windows 上安装 OpenSSH 后使用 PowerShell）。

2. 运行：

   ```bash
   ssh username@192.168.x.x
   ```

   将 `username` 替换为你的 Mac 用户名，将 `192.168.x.x` 替换为第 2 步中的 IP 地址。

3. 首次连接时接受指纹提示。

4. 输入你的 Mac 密码。

---

### 4. 可选：设置静态 IP 或使用主机名

* 为了方便，可以考虑在 Mac 上设置 **静态局域网 IP**，这样 IP 不会改变。
* 或者，如果 Bonjour 已启用，可以使用本地主机名（例如 `ssh username@macbook.local`）。

---

### 5. 故障排除

* 确保 **防火墙** 允许传入的 SSH 连接：
  **系统设置 > 网络 > 防火墙选项**，允许 **远程登录**。
* 确保两台设备在 **同一局域网/子网** 内。
* 先用 `ping <Mac_IP>` 测试连接是否正常。

---

通过以上设置，你可以从本地网络中的任何设备安全地登录到你的 Mac。

参考资料：

* [Apple 支持 – 在 Mac 上共享文件和屏幕](https://support.apple.com/guide/mac-help/share-files-and-screen-on-mac-mchlp2586/mac)
* [macOS SSH 访问指南](https://www.ssh.com/ssh/mac/)

---

如果你愿意，我还可以展示一种 **使用单行终端命令** 的方法来启用 SSH，无需使用系统设置。对于高级用户来说更快。需要我展示吗？
