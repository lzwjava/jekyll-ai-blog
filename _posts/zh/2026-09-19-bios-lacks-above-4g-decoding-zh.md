---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BIOS缺少4G以上解码
translated: true
type: note
---

我已无法通过远程方式确定更多信息。以下是完整情况。

## 你的重启发生了什么

重启被**拒绝，机器从未关机**（`uptime` 显示 `up 1:23`）。GNOME 注册了一个 *阻塞* 模式的抑制器：

```
gnome-session-s  shutdown  user session inhibited   ← block
gsd-power        handle-lid-switch                  ← block
gsd-media-keys   handle-power-key...                ← block
```

`systemctl reboot` 会遵循该抑制。我的重连循环随后一直旋转直到超时 —— 这就是你看到的“命令已中止”。没有任何损坏。

## 步骤 1–4 已完成并验证

| 步骤 | 状态 |
| --- | --- |
| 1. `apt update` | ✅ |
| 2. `build-essential dkms linux-headers-$(uname -r)` | ✅ dkms 已安装，headers 已存在 |
| 3. `nvidia-driver-580` (580.178.04) | ✅ 全部 5 个模块已构建并安装：`nvidia/580.178.04, 7.0.0-31-generic, x86_64: installed` |
| 4. 禁用 nouveau | ✅ `/etc/modprobe.d/blacklist-nouveau.conf` + initramfs 已重建 |

驱动本身没问题 —— 它加载并初始化了 nvlink。但：

```
NVRM: BAR1 is 0M @ 0x0 (PCI:0000:01:00.0)
nvidia 0000:01:00.0: probe with driver nvidia failed with error -1
```

## 真正的问题：你的 BIOS 没有 64 位 MMIO 窗口

M40 请求 `BAR 1 [mem size 0x400000000 64bit pref]` = **16 GiB**，这对于 Tesla 显卡来说是正常的。你的根端口报告：

```
Prefetchable memory behind bridge: [disabled] [64-bit]
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: can't assign; no space
```

因此**没有任何驱动能工作** —— nouveau 之前也以同样的方式失败了（`bar: one-time init failed, -12`）。这可以通过在 BIOS 中启用 **Above 4G Decoding** 来解决。

## 关于你 BIOS 的发现（附更正）

- 主板：MSI B150M PRO-VH (MS-7996)，BIOS **1.80，2016-07-27**
- 存在更新的 BIOS：最高 **3.A0，2018-07-12**（`download.msi.com/bos_exe/mb/7996v3A.zip`）
- **更正：** 我最初在 BIOS 映像中搜索“Above 4G”未找到任何内容 —— 但这是一个*假*阴性。已知字符串“Secure Boot”和“SATA Configuration”也缺失，这意味着 AMI 设置字符串是压缩的。我解压了 314 个 LZMA 流仍无法触及它们（使用 Tiano 压缩），因此**我无法确定该选项是否存在。**

一个软信号：1.80 和 3.A0 的发行说明只提到了 PCIe/USB 兼容性和微码 —— 两者均未提及 Above 4G。因此，更新 BIOS 很可能无济于事。

## 你需要做什么

1. 重启并在 MSI 徽标处按 **Del** 键。
2. 寻找 **Above 4G Decoding** / **Above 4G Memory** / **Crypto Currency mining** —— 通常位于 `Settings → Advanced → PCI Subsystem Settings` 下。
3. **如果找到：** 启用，保存并退出。然后我将验证：

   ```
   nvidia-smi
   ```

4. **如果缺失：** M40 物理上无法在此主板上工作，你需要一块支持 Above-4G 解码的主板。

既然你无论如何都要进入 BIOS，那自然是重启的时机。如果你希望我现在就从这里强制重启，我可以运行 `sudo systemctl reboot -i`（忽略 GNOME 抑制器）—— 但这会终止你已登录的 GNOME 会话，并且不会改变结果。

两个附注：`nvidia-persistenced` 每次启动时都会无害地失败，直到 GPU 初始化；你之前的 Fermi 显卡之所以能工作，纯粹是因为它有一个大约 128 MB 的 BAR1，刚好适配在 4 GB *以下* —— 这也是 Pascal/GeForce 显卡无需任何 BIOS 修改就能工作的原因。另外，M40 是被动散热，所以需要真正的气流，并且 ECC 默认开启（因此 12288 MiB 中可用 11520 MiB）。
