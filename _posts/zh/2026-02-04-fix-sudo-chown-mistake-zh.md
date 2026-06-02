---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复由于 chown 错误导致的 sudo 损坏
translated: true
type: note
---

你看到的错误：

```
sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set
```

发生的原因正是因为你运行了类似以下的代码：

```bash
sudo chown -R $USER /usr
```

（或者类似的命令 —— 可能是 `$USER:$USER` 或单独的 `$USER`）。这导致 **/usr/bin/sudo**（以及成千上万个其他关键文件）的所有权从 root 变更为普通用户，并移除了特殊的 **setuid bit**。这个位的作用是让 sudo 在普通用户执行时也能以 root 权限运行。

修复 **sudo 本身** 很快，通常能立即见效。但修复 /usr 的其余部分（使系统恢复稳定）要困难得多 —— /usr 包含 libraries、binaries、headers 等，其中许多文件都要求所有权为 root:root（有时是 root:staff 或其他组）。这种递归式的 chown 会破坏大量的系统功能。

### 第一步：修复 sudo 本身（使其恢复可用）

由于你现在无法使用 sudo，需要通过以下方式获取 root 权限：

**选项 A – Recovery mode（在台式机/笔记本上最简单）**

1. 重启电脑。
2. 在启动过程中按住 **Shift** 键（某些机器上是 **Esc**），直到出现 GRUB 菜单。
3. 选择 **Advanced options for Ubuntu** → 选择任何以 **(recovery mode)** 结尾的行 → 按 Enter。
4. 在 recovery 菜单中，选择 **root** → **Drop to root shell prompt** → 按 Enter。
   → 你现在将看到 `#` 提示符（拥有完整的 root 权限，此处无需密码）。
5. 以读写模式重新挂载文件系统：

   ```
   mount -o remount,rw /
   ```

6. 修复 sudo：

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   ```

   之后，运行：

   ```
   ls -l /usr/bin/sudo
   ```

   → 你应该看到类似：

   ```
   -rwsr-xr-x 1 root root ... /usr/bin/sudo
   ```

   （所有者执行权限位置的 `s` 代替了 `x` = setuid bit 已设置）

7. 退出并恢复启动：

   ```
   exit
   ```

   然后选择 **resume** → 正常启动。

8. 重启后测试：

   ```
   sudo -k    # 清除旧的缓存
   sudo ls
   ```

   现在它应该会要求输入密码并正常工作。

**选项 B – 如果没有出现 recovery mode 或你更倾向于使用 live USB**

- 从 Ubuntu live USB 启动（尽可能使用相同版本 —— 24.04 或你当前的版本）。
- 打开 Terminal → 挂载你真实的系统（将 `/dev/nvme0n1p2` 或 `/dev/sda1` 替换为你实际的根分区 —— 使用 `lsblk` 查看）：

  ```
  sudo mkdir /mnt/root
  sudo mount /dev/nvme0n1p2 /mnt/root           # 请根据实际情况调整设备名
  sudo mount --bind /dev   /mnt/root/dev
  sudo mount --bind /proc  /mnt/root/proc
  sudo mount --bind /sys   /mnt/root/sys
  sudo mount --bind /run   /mnt/root/run
  sudo chroot /mnt/root
  ```

- 现在你以 root 身份进入了损坏的系统 → 运行：

  ```
  mount -o remount,rw /
  chown root:root /usr/bin/sudo
  chmod 4755 /usr/bin/sudo
  exit
  ```

- 重启（拔掉 USB）。

### 第二步：sudo 恢复后 —— 评估并修复 /usr 的其余部分

虽然 sudo 恢复了，但许多其他功能可能仍处于损坏状态（例如 apt、图形化应用、libraries 无法正常加载，因为所有权错误）。

运行以下命令查看明显的损坏情况：

```bash
sudo dpkg --configure -a
sudo apt update
sudo apt install --reinstall sudo   # 以防万一
ls -l /usr/bin/ls /usr/bin/bash /usr/lib/x86_64-linux-gnu/libc.so*   # 结果应为 root:root
```

针对大量文件的常用快速修复：

```bash
# 修复通用的系统 binaries 和 libs（耗时较长，但很有帮助）
sudo chown -R root:root /usr/bin /usr/sbin /usr/lib /usr/share

# 某些目录使用其他组（运行这些也是安全的）
sudo chown root:staff   -R /usr/local   # 如果你经常使用 /usr/local
```

但这 **并不能修复所有问题** —— 某些 package 需要非常特定的 owner/group/permissions。

### 此时现实的建议

1. **最好且最快速的长期解决方案**
   → **重新安装 Ubuntu**（如果需要，可以保留 /home）。
   启动 live USB → "Try Ubuntu" → 使用安装程序 → 选择 "Something else" → 复用现有的 / 分区但 **格式化它**（如果你是高级用户，也可以只覆盖 /usr, /etc, /var）。
   → 耗时 20-40 分钟，还你一个干净的系统。

2. **尝试就地修复（高级操作，耗时，且可能无法完全成功）**

   - 重新安装核心 package：

     ```bash
     sudo apt install --reinstall ubuntu-desktop ubuntu-minimal linux-generic
     sudo apt install --reinstall $(dpkg -S /usr/bin/* | cut -d: -f1 | sort -u)
     ```

   - 但要做好处理大量 dependency 错误的准备 —— 这可能会引发连锁反应。

3. **备份重要数据**（如果需要，通过 live USB 操作）并重装。

对 /usr 执行递归 chown 几乎总是以重装系统作为最稳妥的结局 —— 特别是因为许多 setuid/setgid binaries 和 shared libraries 的权限现在都是错误的。

如果你想先尝试更具针对性的修复，请告诉我：
- 你的 Ubuntu 版本（如果现在能运行，执行 `cat /etc/os-release`）
- 当你尝试使用 apt 或打开 GUI 应用时报错是什么
- 在 /home 中是否有重要且未备份的数据

祝你好运 —— 以后千万不要再对系统目录运行递归的 chown/chmod 了！ 😅
