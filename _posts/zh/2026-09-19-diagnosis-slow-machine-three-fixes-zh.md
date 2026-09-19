---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断：机器运行缓慢，三种修复方法
translated: true
type: note
---

我现在有完整的了解了。以下是诊断。

## 192.168.1.53 (`lzw-MS-7996`) 的硬件

| 组件 | 规格 | 评价 |
|---|---|---|
| CPU | Intel Core i5-4460，4核 / 4线程 @ 3.2 GHz（Haswell，2014年）| 够用，不是瓶颈 |
| 内存 | **总计 3.2 GiB**（`MemTotal: 3399592 kB`）| **非常低** |
| 交换空间 | 3.7 GiB 文件，**开机5分钟后已使用 578 MB** | 频繁交换 |
| 磁盘 | **WDC WD10EZEX — 1 TB 7200 RPM 机械硬盘**（`rotational=1`）| **主要瓶颈** |
| GPU | Intel 集成显卡 + NVIDIA Tesla P100 16GB | 驱动故障 |
| 操作系统 | Ubuntu，内核 7.0.0-31，GNOME/snap 套件 | 对此机配置过于沉重 |

## 速度慢的原因——三个相互叠加的问题

**1. NVIDIA P100 陷入无限驱动故障循环（CPU 的最大元凶）**
```
journalctl -b | grep -c "probe with driver nvidia failed"        → 412
journalctl -b | grep -c "Failed to start nvidia-persistenced"    → 128
NVRM: BAR1 is 0M @ 0x0 (PCI:0000:01:00.0)
```
在**约 6 分钟的正常运行时间内出现了 128 次服务启动失败和 412 次驱动探测失败**——大约每 2 到 3 秒一次。P100 是需要启用 BIOS 中 *Above 4G Decoding* 功能的数据中心显卡；MSI 主板未正确映射其 BAR1，导致 `nvidia` 探测失败，udev 不断重试，`nvidia-persistenced` 无限重启。这就是为什么你会看到 `modprobe` 占用 90% CPU、`%sy` 占 18–28%，以及 `nvidia-persis` 卡在 **D 状态**。

**2. 机械硬盘在随机 I/O 上饱和**
- `iowait` 22–38%，`%util` **61–99%**，`r_await` 高达 **99 毫秒**
- 请求小而随机（`rareq-sz` 6–65 KB）——这正是 7200 RPM 磁盘最不擅长的负载
- 实时按进程显示的 I/O 显示一个 `snap` 进程正在从 `/dev/sda` 随机读取 **约 4 MB/s**
- 4 核上的平均负载为 3.4–4.05，**71% wa** = 机器是 *I/O 瓶颈*，而非 CPU 瓶颈

**3. 仅 3.2 GiB 内存 + 21 个 snap loop 挂载，且没有 zram**
- `Committed_AS: 4.7 GB` 对 3.4 GB 物理内存 → 开机时已在交换 `so: 6696`
- 主要交换空间占用者：`gnome-shell` 69 MB、`ptyxis` 28 MB、`Xwayland` 24 MB
- **21 个 loop 设备** = 每个 snap（firefox、gnome-46-2404、mesa、snapd 等）都是存储在硬盘上的 squashfs 镜像。snap refresh/seed 就是导致磁盘读写频繁的原因。
- 在 3.2 GB / 机械硬盘上运行 GNOME 桌面 + snap Firefox 确实配置不足。

## 修复方案，按影响程度排序

```bash
# 1. 停止 NVIDIA 重试风暴（立竿见影，效果最佳）
sudo systemctl disable --now nvidia-persistenced.service
echo -e "blacklist nvidia\nblacklist nvidia_drm\nblacklist nvidia_modeset" | sudo tee /etc/modprobe.d/blacklist-nvidia.conf
sudo update-initramfs -u && sudo reboot
# 或者彻底修复：在 BIOS 中为 P100 启用 "Above 4G Decoding" 和 "Resizable BAR"

# 2. 添加 zram 压缩支持（对 3.2 GB 内存帮助很大）
sudo apt install zram-tools && echo -e "ALGO=zstd\nPERCENT=50" | sudo tee /etc/default/zramswap && sudo systemctl restart zramswap

# 3. 尽可能将 snap 替换为 deb 软件包 + 减少磁盘压力
sudo snap remove --purge snap-store firefox   # 然后 apt install firefox-esr / 在 SSD 上使用 flatpak
# 为 / 添加 SSD（机械硬盘仅用于大容量数据）—— 单次硬件升级中效果最显著

# 4. 确认磁盘健康（SMART 需要 sudo 权限）
sudo smartctl -H -A /dev/sda | grep -iE "health|Reallocated|Pending|CRC"
```

**总结：** CPU/内存规格虽然一般但可用；卡顿的原因在于（1）NVIDIA P100 驱动故障循环占用 CPU 并阻塞进程，（2）7200 RPM 机械硬盘因 snap squashfs 随机读取达到 99% 利用率，以及（3）3.2 GB 内存导致交换。修复 #1 免费且立即可行；而 SSD 则是真正治本的方案。

需要我在那台主机上实施 NVIDIA 黑名单和 zram 修复吗？