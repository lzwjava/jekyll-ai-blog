---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 GRUB 优先从 USB 启动
translated: true
type: note
---

Question: 在 Lenovo 笔记本上使用启动 USB 安装 OpenWrt 时，进入 GRUB 模式该如何处理？

Answer: 

你目前看到的是 GRUB 提示符（可能是 `grub>` 或 `grub rescue>`），而不是直接进入 OpenWrt console。当你尝试从 USB 启动 OpenWrt x86 combined image 时，这是一个常见问题，尤其是在 Lenovo 笔记本或 UEFI 系统上。

以下是最高概率的原因及解决方法（按可能性和难易程度排序）：

### 最常见原因：笔记本实际上并未从 USB 启动
- 你的内置硬盘仍然存有旧的 GRUB bootloader（来自 Linux Mint 或之前的 OS），并且 BIOS/UEFI 尝试先从内置驱动器启动 → 结果回退到了它（现已损坏/丢失）的 GRUB。
- **解决方法**（先尝试此操作）：
  1. 在插入 USB 的情况下重启笔记本。
  2. 立即进入 **boot menu**（Lenovo 通常是 **F12**，有时是 **F10**、**Fn+F12** 或 **Novo button** —— 某些型号电源键旁的小孔/按钮）。
  3. 在一次性启动菜单中，明确选择 **USB device**（可能显示为 "USB HDD"、"UEFI: SanDisk"、"Kingston" 等 —— 如果两个都出现，请选择 UEFI 版本）。
  4. 如果仍然失败 → 进入完整的 **BIOS setup**（启动时通常按 **F2** 或 **Fn+F2**）：
     - 设置 **Boot Mode** → UEFI（除非你明确使用了 non-efi image，否则不要选 Legacy/CSM）。
     - 完全禁用 **Secure Boot**（设置为 Disabled）。
     - 在 Boot Priority / Boot Order 中 → 将 USB/Removable Device 移至最顶端。
     - 如果有 **Fast Boot** / **Quick Boot**，将其禁用。
     - 保存 (F10) → 退出 → 重启。
- 更改后，它应该直接启动进入 OpenWrt GRUB 菜单（显示 "OpenWrt" 选项）→ 然后是 kernel messages → 最后是 login prompt（root，无密码）。

### 如果确实是从 USB 启动但仍掉入 GRUB 提示符 / rescue
- 虽然在官方的 combined-efi.img 中很少见，但可能会因写入错误、USB stick 损坏或 image 损坏而发生。
- **快速检查**：
  - 重新制作 USB stick（非常重要）：
    - 在 Windows 中使用 **Rufus** → DD Image 模式（而非 ISO 模式）。
    - 或在 Linux Mint 中：先 `gunzip` .gz 文件 → 然后执行 `sudo dd if=image.img of=/dev/sdX bs=4M status=progress conv=fsync`
    - 尽可能尝试换一个（高质量的）USB stick。
- 在 `grub>` 提示符下，你可以尝试手动启动（仅当你熟悉操作时；通常不需要）：
  ```
  ls               # 列出设备，如 (hd0,gpt1) (hd0) (hd1) 等
  ```
  找到包含 OpenWrt 文件的 USB 分区（通常包含 /boot/grub 或 vmlinuz）。
  示例（根据你的 ls 输出进行调整）：
  ```
  set root=(hd1,gpt2)          # 或 (hd0,msdos1) 等 —— 尝试带有 ext4 的分区
  linux /boot/vmlinuz root=PARTUUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  initrd /boot/initrd (如果存在 —— combined images 通常不需要)
  boot
  ```
  但老实说 —— 95% 的情况下这没有必要。修复启动顺序就足够了。

### 总结 – 现在该做什么
1. 拔掉 USB → 重启 → 进入 boot menu (F12) → 明确选择 USB。
2. 如果没有变化 → 进入 BIOS (F2) → 禁用 Secure Boot + 将 USB 设为第一启动项 + UEFI 模式。
3. 如果确认 USB 启动后仍然显示 GRUB 提示符 → 仔细重新制作 USB stick（如果可能，验证下载的 .img.gz 的 checksum）。
4. 一旦正确启动 → 你应该看到 OpenWrt GRUB 菜单（如果停顿请按 Enter）→ 然后 console 登录：`root`（无密码）。

从 USB 成功启动后 → 按照之前的说明执行 `dd` 安装到 `/dev/sda`（内部磁盘）。

请告知我 GRUB 屏幕具体显示的内容（grub> 或 grub rescue> 或仅是 "GRUB _"）以及是否看到任何错误消息 —— 这有助于进一步缩小问题范围。

References:  

- https://forum.openwrt.org/t/openwrt-x86-on-usb-stick/142430
- https://openwrt.org/docs/guide-user/installation/openwrt_x86
- https://www.reddit.com/r/openwrt/comments/1r3wruz/trouble_booting_openwrt_x86_on_anything_other