---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过互联网恢复重新安装 macOS
translated: true
type: note
---

问题：我最近擦除了2017款MacBook Pro上的系统并安装了Fedora，如何自行重新安装macOS？

回答：

由于你用Fedora替换了macOS，恢复分区已不存在。你需要使用**互联网恢复**功能，通过网络从苹果服务器下载安装程序。

## 方法一：互联网恢复（最简单）

1. 完全关机。
2. 开机并立即按住 **Cmd + Option (Alt) + R**，直到看到旋转的地球（而不是苹果标志）。这会启动互联网恢复，并安装你的Mac支持的**最新**macOS版本。
   - 改用 **Cmd + R** 可获取*原始出厂*版本——但这里不适用，因为你的恢复分区已被擦除，所以请使用地球标志的快捷键。
3. 连接Wi-Fi（或以太网——对于数GB的下载更可靠）。
4. 在macOS实用工具中，先打开**磁盘工具**：
   - 选择内置磁盘（顶层，而非Fedora卷宗）。
   - **抹掉** → 格式选择 **APFS**，方案选择 **GUID分区图**。这会清除Fedora/ext4/LUKS的分区布局。
5. 退出磁盘工具 → **重新安装macOS** → 按提示操作。

2017款MacBook Pro（型号`MacBookPro14,x`）官方最高支持**macOS Ventura 13**（Sonoma/Sequoia已放弃支持）。互联网恢复可能提供Ventura，或回退到出厂版本（Sierra 10.12），之后可通过App Store升级。

## 方法二：可启动USB安装盘（更可控，可重复使用）

如果你能使用*另一台正常工作的Mac*，这是更好的途径——但注意你只有这一台Mac，所以方法一是你实际可行的选择，除非你借用一台。

在正常工作的Mac上，准备一个16GB以上的U盘：

```bash
# 从App Store下载安装程序（例如"Install macOS Ventura"），然后：
sudo /Applications/Install\ macOS\ Ventura.app/Contents/Resources/createinstallmedia \
  --volume /Volumes/MyUSB
```

然后在目标Mac开机时按住 **Option (Alt)** 键，选择U盘，在磁盘工具中抹掉磁盘（APFS/GUID），再进行安装。

## 你当前情况的注意事项

- **固件密码**：如果你曾设置过，则需要输入密码才能启动恢复。
- **T2芯片**：2017款**没有T2芯片**，因此没有安全启动限制——启动外部/恢复介质不受限制。这对你有利。
- **互联网恢复需要特定Wi-Fi**：仅支持WPA/WPA2个人网络，不支持强制门户或企业认证。如果你的网络有登录页面，请使用手机热点或以太网适配器。
- **磁盘被Fedora擦除**：Fedora可能转换了分区表或使用了LUKS——磁盘工具中的完整**抹掉**操作可干净地处理此问题。

适合你的实际方案：按住 **Cmd+Option+R**，抹掉为APFS，重新安装。如果互联网恢复提供的是旧版本，之后通过App Store升级到Ventura。
