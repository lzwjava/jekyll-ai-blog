---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复模式缺少网络命令
translated: true
type: note
---

是的，这是预期的情况——**macOS Recovery**（你通过启动选项或在 M2 上按住电源键进入的模式）运行的是一个非常精简的环境，以保持轻量和安全。许多完整的系统命令（如位于 `/usr/sbin/networksetup` 的 `networksetup`）**并未包含**在 Recovery 分区的 PATH 或二进制文件中。这就是为什么你会看到 "command not found"。

### 快速确认
在你当前的 Terminal 中运行以下命令，查看实际可用的内容：

```bash
ls /usr/sbin
```

（或者 `ls /bin`，`ls /usr/bin`）——你会发现与正常的 macOS 相比，这里的列表非常短。其中没有 `networksetup`。

### 清除 Proxy 设置的替代方案
既然我们在这里无法使用 `networksetup`，以下是当前状态下的最佳选择：

1. **最简单且最有效的：先进入 Safe Mode (通常会绕过 Proxy)**
   - 在 Recovery 中：选择 **Restart**（或长按电源键强制关机）。
   - 立即按住 **电源键** 直到出现启动选项。
   - 选择你的磁盘 → 按住 **Shift** 键 → 点击 **Continue in Safe Mode**。
   - Safe Mode 会加载最少的扩展程序，并且通常会忽略或清除临时的 proxy 故障（包括 Clash 的残留），因为第三方 kexts/登录项不会运行。
   - 如果你进入了桌面/登录界面：
     - 打开 **System Settings > Network > Wi-Fi** (或 Ethernet) → Details... → Proxies 选项卡 → 关闭所有开关 (Web Proxy, Secure Web Proxy, SOCKS, Auto Proxy)。
     - 或者正常打开 Terminal 并运行我之前给出的 `networksetup` 命令（现在可以使用了）。
   - 然后正常重启 → 更新/设置应该就可以在没有 proxy 干扰的情况下进行了。

2. **如果 Safe Mode 也卡住：从 Recovery 重新安装 macOS (非破坏性)**
   - 在 Recovery 中 → 选择 **Reinstall macOS**。
   - 它会在你现有的数据/应用之上下载并重新安装 OS 文件（除非发生严重错误，否则不会抹除用户文件）。
   - 在重新安装过程中，它通常会将网络配置（包括 proxies）重置为默认值，因为它会重建系统组件。
   - 确保连接了良好的 Wi-Fi（连接 Apple 的服务器理想情况下不需要 proxy —— 如果可能，请尝试连接手机热点进行测试）。
   - 这修复了许多 M-series 用户遇到的更新后卡死 + proxy 循环的问题。

3. **高级方案：挂载主卷并直接编辑 Proxy Plist (如果你熟悉 Terminal)**
   在 Recovery Terminal 中：

   ```bash
   diskutil list   # 记录你的主磁盘，例如 disk3s1 或 disk1s5 — 通常是名为 "Macintosh HD" 的最大 APFS 卷
   diskutil apfs list   # 确认卷组
   mkdir /mnt
   mount -uw /Volumes/Macintosh\ HD   # 或者你的卷名；如果有空格请使用引号
   # 如果挂载失败，尝试：mount -uw /
   cd /Volumes/Macintosh\ HD/Library/Preferences/SystemConfiguration   # 此文件夹存放网络偏好设置
   ls   # 查找 com.apple.airport.preferences.plist 或 preferences.plist
   ```

   - 不幸的是，正确编辑 plist 需要 `defaults` 命令或 `plutil`，这些在 Recovery 中可能也缺失。
   - 如果 `defaults` 可用（尝试 `defaults read`），你可以尝试类似操作：
     ```bash
     defaults delete /Volumes/Macintosh\ HD/Library/Preferences/SystemConfiguration/preferences GlobalProxies
     ```
     但这取决于运气——许多工具都不存在，所以经常会失败。

   如果挂载/编辑操作不顺，请跳到选项 1 或 2。

4. **最后手段：抹除并全新安装 (有数据丢失风险——请务必先备份)**
   - 如果其他方法都不起作用，且确实被 proxy 永久卡死：在 Recovery → Disk Utility → 抹除你的主卷 (APFS) → 然后重新安装。
   - 但请先尝试 Safe Mode + 重新安装。

大多数遇到此类“因 proxy 导致的更新卡死”情况的用户，通过强制进入 Safe Mode 几次或重新安装即可解决。请尝试现在启动到 Safe Mode —— 如果你进入了桌面，或者看到什么新的错误/卡顿，请告诉我。如果你使用的是公司网络或重度依赖 VPN 的网络，在尝试启动时也请切换到手机热点 Wi-Fi。加油！