---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复NVIDIA驱动程序包冲突
translated: true
type: note
---

这看起来是 Ubuntu（根据软件包版本推测可能是 22.04）在更新 NVIDIA 驱动程序时出现的典型包冲突问题。`nvidia-kernel-common-535` 软件包试图覆盖一个已被 `nvidia-firmware-535` 占用的固件文件（`gsp_ga10x.bin`），导致 dpkg 中止操作。这是 Ubuntu 仓库中 NVIDIA 535 系列驱动程序的已知问题。

不必惊慌——您的系统应该仍能启动（不过如果驱动程序部分损坏，图形界面可能会处于软件渲染模式）。以下是安全解决此问题的分步指南。请在终端中运行这些命令（如果图形界面不稳定，可使用 TTY 切换：Ctrl+Alt+F3）。

### 快速修复尝试（优先使用最安全的方法）

1. 尝试自动修复损坏的软件包：

   ```
   sudo apt --fix-broken install
   ```

   这通常能在无需手动干预的情况下解决依赖关系/解包问题。

2. 如果上述方法失败（或部分成功但仍有错误），请清理中断的安装：

   ```
   sudo dpkg --configure -a
   sudo apt update
   sudo apt upgrade
   ```

### 如果问题依旧：强制覆盖冲突文件

错误具体出现在 `nvidia-kernel-common-535` 的 deb 文件上。强制 dpkg 覆盖重复文件：

```
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nvidia-kernel-common-535_535.274.02-0ubuntu1_amd64.deb
```

- 这将仅安装该软件包，忽略文件冲突。
- 然后运行：

  ```
  sudo apt --fix-broken install
  sudo apt autoremove
  sudo apt upgrade
  ```

- 完成后重启：`sudo reboot`。

### 终极方案：清除并重新安装 NVIDIA 软件包

如果上述方法无效（例如存在更深层的版本不匹配），请移除冲突的 NVIDIA 组件并重新安装：

1. 清除有问题的软件包（如需调整版本号，请通过 `dpkg -l | grep nvidia` 检查）：

   ```
   sudo dpkg --force-all -P nvidia-firmware-535-535.274.02 nvidia-kernel-common-535
   ```

2. 清理系统：

   ```
   sudo apt autoremove --purge
   sudo apt autoclean
   ```

3. 重新安装驱动程序：

   ```
   sudo apt update
   sudo apt install nvidia-driver-535
   ```

4. 重启系统。

### 预防措施/提示

- 添加 graphics-drivers PPA 以获取更稳定的 NVIDIA 更新：`sudo add-apt-repository ppa:graphics-drivers/ppa && sudo apt update`。
- 如果您使用的是笔记本电脑，请在安装驱动程序前确保 BIOS 中已禁用 Secure Boot。
- 重启后使用 `nvidia-smi`（应显示您的 GPU）或 `prime-select query`（如果使用 NVIDIA Optimus）进行测试。
- 如果此操作完全破坏了显示功能，请启动到恢复模式并从那里运行修复命令。

如果以上方法均无效或出现新错误，请在此处粘贴完整输出信息以便进一步调整。

### 参考资料

- [Unmet dependencies nvidia-dkms-535 - package conflict breaks Ubuntu 22.04 install](https://forums.developer.nvidia.com/t/unmet-dependencies-nvidia-dkms-535-package-conflict-breaks-ubuntu-22-04-install/265788)
- [Ubuntu and NVIDIA-provided packages conflict, breaking installation](https://forums.developer.nvidia.com/t/ubuntu-and-nvidia-provided-packages-conflict-breaking-installation/259150)
- [Problem with nvidia package dependencies](https://askubuntu.com/questions/1491916/problem-with-nvidia-package-dependencies)
- [nvidia-kernel-common-535 conflicts with nvidia-firmware-535](https://superuser.com/questions/1833427/nvidia-kernel-common-535-conflicts-with-nvidia-firmware-535-535-161-07-535-161-0)
