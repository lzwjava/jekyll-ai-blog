---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: macOS默认守护进程
translated: true
type: note
---

### macOS 中的默认守护进程

在 macOS 中，守护进程是在后台运行的无界面服务，通常在系统启动时或按需启动。它们由 **launchd**（系统的初始化与服务管理框架，PID 为 1）统一管理。守护进程与代理进程的区别在于：守护进程以 root/系统级权限运行（登录前启动），而代理进程按用户运行（登录后启动）。

默认系统守护进程的定义文件位于 `/System/Library/LaunchDaemons/` 目录的属性列表（.plist）文件中。标准安装通常包含约 300–350 个此类进程（例如 macOS 10.14 Mojave 中有 339 个），涵盖网络、安全到硬件管理等各个方面。用户安装或第三方守护进程则存放在 `/Library/LaunchDaemons/` 目录。

#### 如何查看默认守护进程
在终端中列出所有已加载的守护进程（及代理进程）：
- `sudo launchctl list`（显示系统级守护进程和代理进程）
- `launchctl list`（仅显示用户级代理进程）

查看完整目录列表：`ls /System/Library/LaunchDaemons/`（无需 sudo 权限，但文件为只读）。

这些命令输出的列包括 PID、状态和标签（例如 `com.apple.timed`）。

#### "timed" 守护进程
您特别提到的 "timed" 指的是 **com.apple.timed**（时间同步守护进程）。这是 macOS High Sierra（10.13）引入的核心系统守护进程，用于取代旧的 `ntpd` 进程。

- **功能**：自动通过 NTP（网络时间协议）服务器同步 Mac 系统时钟，每 15 分钟查询一次，确保日志、证书和网络操作的时间精准性
- **运行机制**：由 launchd 从 `/System/Library/LaunchDaemons/com.apple.timed.plist` 启动，以 `_timed` 用户身份运行（属于 `_timed` 和 `_sntpd` 组）。通过 `settimeofday` 系统调用根据服务器响应调整时钟。配置存于 `/etc/ntpd.conf`（NTP 服务器设置），状态缓存于 `/var/db/timed/com.apple.timed.plist`
- **关联功能**：对应系统设置 > 通用 > 日期与时间 > "自动设置日期与时间"。若禁用该选项，timed 将停止同步。对于高精度需求的高级设置，可用 Chrony 等工具替代，但需先禁用 timed

若出现时钟漂移，请检查网络问题或防火墙是否阻断 NTP（UDP 端口 123）。

#### 其他常见默认守护进程（示例）
以下表格列举了一些常驻默认系统守护进程（按功能分类）。这并非完整列表（实际有数百个），但涵盖了核心组件。标签名对应 .plist 文件名。

| 类别            | 守护进程标签                     | 功能描述 |
|-----------------|----------------------------------|----------|
| **核心系统**    | `com.apple.launchd`             | launchd 进程本身，负责启动其他所有进程 |
| **时间同步**    | `com.apple.timed`               | NTP 时间同步（如上所述） |
| **用户管理**    | `com.apple.opendirectoryd`      | 处理用户/组账户及目录服务 |
| **用户管理**    | `com.apple.accounts`            | 管理用户账户与认证 |
| **网络**        | `com.apple.mDNSResponder`       | Bonjour/mDNS 本地网络发现服务（如 AirDrop） |
| **网络**        | `com.apple.nesessionmanager`    | 网络扩展与 VPN 管理 |
| **蓝牙/无线**   | `com.apple.bluetoothd`          | 蓝牙设备处理 |
| **iCloud/同步** | `com.apple.cloudd`              | iCloud 数据同步与服务 |
| **安全**        | `com.apple.securityd`           | 钥匙串与凭证管理（通常也作为代理进程运行） |
| **系统更新**    | `com.apple.softwareupdated`     | 处理软件更新与目录下载 |
| **硬件**        | `com.apple.kextd`               | 内核扩展加载与管理 |
| **日志**        | `com.apple.systemnotificationd` | 系统通知与日志记录 |
| **MDM（若启用）** | `com.apple.mdmclient`          | 企业环境移动设备管理客户端 |

这些进程持续运行或由触发器激活，以维持 macOS 系统稳定。若某个进程异常（如 CPU 占用过高），可临时使用 `sudo launchctl unload /System/Library/LaunchDaemons/com.apple.example.plist` 卸载，但请避免修改系统文件。

要获取您当前 Mac 的完整最新列表（截至 2025 年 10 月，可能为 macOS 15 Sequoia 或更新版本），请运行上述命令——不同系统版本会略有差异。

#### 参考资料
- [The macOS Process Journey — “timed” (Time Sync Daemon)](https://medium.com/@boutnaru/the-macos-process-journey-timed-time-sync-daemon-4898c8185b4b)
- [Daemons and Agents could be slowing down your Mac](https://appleinsider.com/inside/macos/tips/daemons-and-agents-could-be-slowing-down-your-mac)
- [What files are included in the /System/Library/LaunchAgents and /System/Library/LaunchDaemons](https://apple.stackexchange.com/questions/361029/what-files-are-included-in-the-system-library-launchagents-and-system-library)
- [Script management with launchd in Terminal on Mac](https://support.apple.com/guide/terminal/script-management-with-launchd-apdc6c1077b-5d5d-4d35-9c19-60f2397b2369/mac)
- [How to show all running launchctl daemons/agents?](https://apple.stackexchange.com/questions/134817/how-to-show-all-running-launchctl-daemons-agents)
