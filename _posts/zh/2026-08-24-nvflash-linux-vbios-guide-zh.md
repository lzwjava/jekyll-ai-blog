---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVFlash Linux VBIOS 指南
translated: true
type: note
---

**问题：** 如何在 Linux 上安装并使用 NVFlash 备份和刷写 RTX GPU 的 VBIOS？

**回答：**

---

## ⚠️ 警告

必须以 **root** 身份运行。在 NVFlash 访问 GPU 之前，**必须完全卸载** NVIDIA 内核模块。刷写错误的 VBIOS 可能导致显卡永久变砖——务必先备份。

---

## 第一步 — 下载 NVFlash

前往 **TechPowerUp** 下载最新版本 (v5.867)：
```
https://www.techpowerup.com/download/nvidia-nvflash/
```

解压 zip 文件——其中包含 Linux 二进制文件和 Windows 下的 `.exe` 文件。

```bash
unzip nvflash_5.867.zip -d ~/nvflash
cd ~/nvflash
```

---

## 第二步 — 赋予二进制文件可执行权限

解压后，Linux 二进制文件需要 `chmod +x` 才能运行。

```bash
chmod +x nvflash
```

---

## 第三步 — 停止 X11 / Wayland（桌面图形界面）

最好在文本控制台（TTY）中运行 NVFlash，并停止 X11/Wayland。刷写前切换到多用户（非图形）模式：

```bash
sudo systemctl isolate multi-user.target
```

或者，如果正在使用桌面，只需按 `Ctrl+Alt+F2` 切换到 TTY，以 root 身份登录，然后继续操作。

---

## 第四步 — 卸载 NVIDIA 内核模块

按以下顺序卸载所有 NVIDIA 进程——必须完全卸载 nvidia 模块，nvflash 才能正常运行：

```bash
sudo rmmod nvidia_drm nvidia_modeset nvidia_uvm nvidia
```

验证它们均已卸载：
```bash
lsmod | grep nvidia
# 应无输出
```

> **提示：** 如果模块拒绝卸载，请先停止显示管理器：
> ```bash
> sudo systemctl stop gdm   # 或 sddm / lightdm
> ```

---

## 第五步 — 验证 NVFlash 能检测到 GPU

```bash
sudo ./nvflash --list
```

这将确认 nvflash 正在运行并能检测到你的 GPU。注意显示的索引编号（例如 `0`）——在多 GPU 系统上你会用到它。

---

## 第六步 — 备份当前 VBIOS（必须操作！）


```bash
sudo ./nvflash --save vbios_backup.rom
```


针对特定 GPU 索引：
```bash
sudo ./nvflash -i0 --save vbios_backup_gpu0.rom
```

将备份存储在 **U 盘或另一台机器上**——不要仅存放在本地磁盘。

---

## 第七步 — 关闭写保护


```bash
sudo ./nvflash --protectoff
```


---

## 第八步 — 刷写新 VBIOS

标准刷写：
```bash
sudo ./nvflash vbios_new.rom
```

如果存在子系统 ID 不匹配，使用 `-6` 参数覆盖（请谨慎使用）：
```bash
sudo ./nvflash -6 vbios_new.rom
```


提示时按 `Y` 确认。

---

## 第九步 — 验证新 VBIOS

刷写后，确认新 VBIOS 已生效：
```bash
sudo ./nvflash --version
```


然后重启：
```bash
sudo reboot
```

启动后，重新加载桌面，并通过 `nvidia-smi` 或 GPU-Z（如果使用 Windows 双系统）检查 BIOS 版本字符串是否已更改。

---

## 故障排除 — 模块无法卸载

某些发行版具有 AppArmor 或 SELinux 等安全模块，可能会阻止 nvflash 直接访问设备。如果遇到无法解释的权限错误，请以安全模块的宽松模式启动系统。

也可以尝试终止所有残留进程：
```bash
sudo fuser -k /dev/nvidia*
sudo rmmod nvidia_uvm nvidia_drm nvidia_modeset nvidia
```

---

## Linux 完整工作流程总结

```bash
# 1. 解压并赋予执行权限
chmod +x nvflash

# 2. 停止图形界面
sudo systemctl isolate multi-user.target

# 3. 卸载 NVIDIA 模块
sudo rmmod nvidia_drm nvidia_modeset nvidia_uvm nvidia

# 4. 列出 GPU
sudo ./nvflash --list

# 5. 备份
sudo ./nvflash --save vbios_backup.rom

# 6. 关闭保护
sudo ./nvflash --protectoff

# 7. 刷写
sudo ./nvflash -6 vbios_new.rom

# 8. 验证
sudo ./nvflash --version

# 9. 重启
sudo reboot
```

---

**参考来源：**
- [cyclone-github: nvflash Linux 操作指南（基于 Debian 测试，2025 年更新）](https://github.com/cyclone-github/nvidia_vbios/blob/main/nvflash_how_to_linux.txt)
- [nvflash 参考指南 2026 — Linux 差异](https://www.mvktech.net/nvflash-guide/)
- [HiveOS VBIOS 刷写指南（Linux，多 GPU）](https://hiveon.com/forum/t/guide-nvidia-gpu-vbios-flashing-with-hiveos/4091.rss)
- [TechPowerUp NVFlash 下载](https://www.techpowerup.com/download/nvidia-nvflash/)