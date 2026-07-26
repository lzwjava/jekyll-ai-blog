---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacBook Pro 2017 上的 Windows 11
translated: true
type: note
---

问：直接在 MacBook Pro 2017 上通过 Boot Camp 安装 Windows 11，但没有 TPM 2.0 该怎么办？

答：可行，但需要绕过限制，因为你的 2017 款 MacBook Pro 没有 TPM 2.0 芯片，处理器（第七代英特尔）也不在微软支持列表中。以下是具体操作步骤：

**1. 检查可用空间** — 至少需要 64GB 以上的分区，建议预留 100GB 以上。

**2. 使用 Boot Camp 助理进行分区（但不要让它创建安装盘）：**
- 打开 Boot Camp 助理（Spotlight → "Boot Camp 助理"）
- 如果它允许你仅进行分区操作（取消勾选"下载 Windows 支持软件"/"创建安装盘"，如果它提示 Windows 11 ISO 不兼容的话），直接划分出 Windows 分区。
- 如果 Boot Camp 助理直接拒绝你的 Windows 11 ISO，则跳过它，改为手动分区：`磁盘工具` → 对硬盘进行分区，将新卷格式设置为 **MS-DOS (FAT)**，后续在安装程序中将自动格式化为 NTFS。

**3. 使用 balenaEtcher 创建可引导 U 盘**（参照你之前的问题），因为 Boot Camp 助理自带的 U 盘创建工具可能会拒绝不兼容的 ISO 文件。

**4. 从 U 盘启动：** 开机时按住 `Option (⌥)` 键 → 选择 EFI 启动 U 盘。

**5. 在 Windows 安装界面，当出现"这台电脑目前不满足 Windows 11 系统要求"时：**
```
Shift + Fn + F10
```
（MacBook 键盘需按 `Fn` 键，因为单独按 F10 是媒体键）。这会打开命令提示符。然后输入：
```cmd
regedit
```
导航至 `HKEY_LOCAL_MACHINE\SYSTEM\Setup`，新建一个名为 `LabConfig` 的项，并在其中添加以下 DWORD (32 位) 值，全部设置为 `1`：
```
BypassTPMCheck
BypassSecureBootCheck
BypassRAMCheck
BypassCPUCheck
BypassStorageCheck
```
关闭注册表编辑器，关闭命令提示符，在安装界面点击**返回**再点击**下一步**——它将跳过兼容性检测继续安装。

**6. 安装到你创建的 Boot Camp 分区**，让安装程序正常完成。

**7. Windows 启动后，安装苹果 Boot Camp 驱动**（包括 WiFi、触控板、音频、显卡）——需要单独下载 Boot Camp 支持软件，因为 Boot Camp 助理的自动下载功能可能也会因系统版本受限；可从一台正常工作的 Mac 获取驱动包，或如果助理无法下载，搜索"Boot Camp 6 support software download"。

需要如实提醒：微软已逐渐收紧绕过限制的措施，在不支持的配置上运行 Windows 更新偶尔会失败或被阻止——这是已知的取舍，并非永久有效的方案。

参考链接：
- [在无 TPM 的 MacBook 上运行 Windows 11 - Intel Mac 指南](https://www.positioniseverything.net/run-windows-11-on-macbook-without-tpm-step-by-step-guide-for-intel-macs/)
- [在无 TPM 的 MacBook 上安装 Windows 11 24H2 - Mac Observer](https://www.macobserver.com/tips/how-to/install-windows-11-24h2-on-macs-without-tpm/)