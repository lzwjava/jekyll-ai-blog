---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Flash之后启用ReBAR
translated: true
type: note
---

刷写成功🎉 现在：

## 1. 关闭 B75 电源，然后进入 BIOS 设置

开机 → 快速按 **Del**（或 F2）→ 进入 BIOS 设置。

## 2. 在 BIOS 设置中，修改两个选项

1. **开启 "Above 4G Decoding"**
   - 通常在 **Advanced → PCI/PnP** 或 **Chipset** 或 **Boot** 下，找到 "Above 4G Decoding" / "Above 4G MMIO" / "Memory Mapped I/O above 4GB" → **Enabled**。

2. **关闭 "CSM"**
   - 在 **Boot** → "CSM" / "Compatibility Support Module" → **Disabled**。

保存并退出（**F10**）。

⚠️ 注意：如果 B75 上的 Ubuntu 是以 **legacy/MBR** 模式安装的，关闭 CSM 会导致无法启动。进入 Ubuntu 后可以检查：
```bash
ls /sys/firmware/efi    # 存在 = UEFI 启动（关闭 CSM 没问题）；"No such file" = legacy/MBR
```
如果确实是 legacy 模式且无法启动，请暂时重新开启 CSM —— 刷写已经完成，这样做是安全的 —— 并告诉我；我们可以选择将 Ubuntu 转换为 UEFI 模式，或者保持 CSM 开启（但 BAR 大小会受到限制）。

## 3. 启动 Ubuntu，然后设置 BAR 大小

`ReBarState` 在 **MSI 机器**上，而不是 B75 —— 先将其复制过去（U盘或 `scp`）：

```bash
# 从这台 MSI 机器复制到 B75（根据实际情况调整用户/主机名）：
scp /home/lzw/Downloads/B75/rebar-work/ReBarState  user@b75-ip:~
```

然后在 B75 上（以 root 身份）：
```bash
sudo ./ReBarState
# 输入：32
```
然后 **重启**。

## 4. 验证

```bash
sudo dmesg | grep -i "root bus resource"   # 最后的 mem window 应结束于 ≥ 0xfffffffff
sudo dmesg | grep -i bar
```
或者，如果你安装了双系统，也可以在 Windows 下用 GPU-Z 查看。

---

请告诉我：
1. 你是否找到了 **Above 4G Decoding**（具体在哪里）？
2. 关闭 CSM 后 Ubuntu 是否还能启动？

如果你需要，我也可以编译一个 **Windows 版的 `ReBarState.exe`**，这样你就能在 Windows 下设置大小，而不用依赖 Linux。