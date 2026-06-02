---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 快速修复损坏的 Sudo 权限
translated: true
type: note
---

错误信息：

```
sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set
```

这意味着 **sudo** binary 的所有权或权限不正确。通常情况下，它必须：

- 由 **root** (UID 0) 所有
- 设置了 **setuid bit**（以便普通用户调用时也能以 root 身份运行）

这通常是由于误操作命令（如 `chown`、`chmod -R`）或错误修改 `/usr/bin` 导致的。

你无法使用 `sudo` 来修复此问题（因为它已经损坏），因此需要通过其他方式获取 root access。以下是适用于 Ubuntu（支持 20.04–26.04+ 版本）的主要修复方法。

### Method 1: 进入 Recovery Mode (推荐 & 最安全)

1. **重启**电脑。
2. 在启动时按住 **Shift** 键（某些系统上是 **Esc**）以显示 **GRUB menu**。
3. 选择 **Advanced options for Ubuntu**。
4. 选择以 **(recovery mode)** 结尾的一行 → 按 Enter。
5. 在 recovery menu 中，选择 **root** → **Drop to root shell prompt** → 按 Enter。
   - 你将获得一个 `#` 提示符（此处无需密码）。
6. 将 filesystem 重新 mount 为 read-write 模式（非常重要！）：

   ```
   mount -o remount,rw /
   ```

7. 修复 sudo binary：

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   ```

   - `4755` = owner read/write/execute + setuid bit + group/other read/execute。
   - 完成后，执行 `ls -l /usr/bin/sudo` 应该显示如下：
     ```
     -rwsr-xr-x 1 root root ... /usr/bin/sudo
     ```
     （`x` 位置显示的 `s` = setuid bit）

8. 可选操作：如果 `su` 也损坏了，顺便修复它：

   ```
   chown root:root /usr/bin/su
   chmod 4755 /usr/bin/su
   ```

9. 退出 shell：

   ```
   exit
   ```

10. 回到 recovery menu：选择 **resume** → 正常启动。
11. 重启后，使用以下命令测试：

    ```
    sudo ls
    ```

它现在应该会要求输入密码并正常工作。

### Method 2: 如果你设置了 Root 密码 (或可以通过 TTY 以 Root 登录)

- 切换到 text console：按下 **Ctrl + Alt + F3** (或 F2–F6)。
- 以 **root** 身份登录（如果你有 root 密码），或者如果允许 root 登录则以对应用户登录。
- 然后运行与上述相同的修复命令：

  ```
  mount -o remount,rw /
  chown root:root /usr/bin/sudo
  chmod 4755 /usr/bin/sudo
  exit
  ```

- 返回 GUI：按下 **Ctrl + Alt + F1** 或 **F2**。

### Method 3: 如果 Recovery Mode 失败或偏好使用 Live USB

1. 从 **Ubuntu Live USB** 启动（尽可能使用相同版本）。
2. 打开 Terminal → mount 你已安装的系统（将 `/dev/sda1` 替换为你的 root partition – 通过 `lsblk` 查看）：

   ```
   sudo mkdir /mnt/root
   sudo mount /dev/sda1 /mnt/root
   sudo mount --bind /dev /mnt/root/dev
   sudo mount --bind /proc /mnt/root/proc
   sudo mount --bind /sys /mnt/root/sys
   sudo mount --bind /run /mnt/root/run
   sudo chroot /mnt/root
   ```

3. 现在你已经以 root 身份“进入”了损坏的系统 → 运行：

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   exit
   ```

4. 拔掉 USB 并重启。

### 修复后的额外检查

- 运行 `ls -l /usr/bin/sudo` → 应显示 `-rwsr-xr-x root root`
- 如果错误信息中提到的是 `/usr/local/bin/sudo`：请将其删除（因为它覆盖了真实的 sudo）：

  ```
  sudo rm /usr/local/bin/sudo
  hash -r   # 刷新 shell 缓存
  ```

- 如果仍然异常，重新安装 sudo package：

  ```
  sudo apt update
  sudo apt install --reinstall sudo
  ```

这几乎总能解决问题。如果你遇到其他错误或仍然失败，请告知具体的错误信息（以及你的 Ubuntu 版本）。
