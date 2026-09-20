---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无键盘紧急模式恢复
translated: true
type: note
---

**问题：** 在键盘无响应的紧急模式下，当无法输入时如何恢复？

**回答：**

如果键盘在紧急 shell 中确实完全无法工作，以下选项按难易程度排序：

---

### 1. 尝试不同的键盘 / 端口

- 换用 **不同端口的 USB 键盘**（优先尝试 USB 2.0 端口而非 USB 3.0）
- 如果主板有该端口，尝试 **PS/2 键盘**
- USB 键盘有时在启动初期未能被及时初始化——不同端口或集线器可能有助于解决

---

### 2. 从另一台机器通过 SSH 登录

如果机器有网络连接（即使在紧急模式下，网络有时也会启动）：

```bash
ssh user@<ip-address>
```

然后从那里运行诊断和修复命令。

---

### 3. 从 Live USB/CD 启动

这是在你完全无法与损坏系统交互时最可靠的恢复路径：

1. 启动 **Ubuntu/Debian/Fedora Live USB**
2. 挂载你的根分区：

   ```bash
   sudo mount /dev/sdXN /mnt        # 将 sdXN 替换为你的根分区
   ```

3. 直接编辑 fstab：

   ```bash
   sudo nano /mnt/etc/fstab
   ```

4. 注释掉那两个错误的 UUID 行，保存，重启

---

### 4. 编辑内核启动参数（初始阶段无需键盘）

在 **GRUB 菜单**（Linux 加载之前），有时仅能使用方向键：

- 高亮你的启动项 → 按 **`e`** 编辑
- 找到 `linux` 行，在末尾添加 `single` 或 `init=/bin/bash`
- 按 **Ctrl+X** 启动

这会进入一个最小 shell，在此键盘*或许*能工作，即使在紧急模式下它不能。

---

### 5. 虚拟机专用（如果这是虚拟机）

- 使用 **hypervisor 控制台**（vSphere、Proxmox、VirtualBox 等）——它们拥有自己的键盘输入，完全绕过操作系统
- 将磁盘挂载到另一台虚拟机，从那里编辑 `/etc/fstab`

---

**Live USB 方法（#3）是最安全的**——它让你无需依赖损坏系统的键盘即可修复 `/etc/fstab`。

---

**参考资料：**

- [从紧急模式恢复 – Ubuntu 论坛](https://ubuntuforums.org/showthread.php?t=2282512)
- [如何进入救援/紧急模式 – Red Hat 文档](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_systems_using_the_rhel_system_roles/assembly_recovering-and-restoring-a-system_managing-systems-using-the-rhel-system-roles)
- [fstab – Arch Linux 维基](https://wiki.archlinux.org/title/Fstab)
