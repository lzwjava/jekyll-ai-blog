---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复BIOS，在B85上启用ReBAR
translated: true
type: note
---

以下是我找到的信息以及针对您的主板我会采取的措施。

## SOYO 官方网站的说法

当前的官方网站是 **`soyocn.net`**（旧的 `soyo.com.cn` 已失效——返回 502）。其下载部分如下：

- 驱动/BIOS 下载：`https://www.soyocn.net/down/zbdrv/INTEL/`（仅 2 页，约 39 块主板，最旧条目是 2014 年的 H81 型号）
- B85 分类：`https://www.soyocn.net/list.php?catid=469` → **仅剩 1 个产品：SY-B85-BTC**

因此 **SY-B85N 全固版 已不在当前官方网站的列表中**——它是一款约 2013/2014 年的廉价主板，SOYO 已将其移除。这对这类主板来说很常见。

## 如何实际获取 BIOS 镜像

### 选项 1（推荐）：从闪存芯片中读取
由于这是一块没有官方下载的老款廉价主板，最可靠的方法是直接从 SPI 闪存芯片中读取 BIOS：

1. 购买一个 **CH341A** 编程器（约 5 美元）+ SOP8 测试夹（这样无需拆焊）
2. 识别主板上的闪存芯片（通常是 25 系列 SPI NOR，例如 Winbond W25Q64/GD25Q64，SOP8 封装）
3. 使用 `flashrom` 读取：
   ```bash
   # Linux
   flashrom -p ch341a_spi -r soyo_b85n_backup.bin
   # 读取 2-3 次并校验校验和是否匹配
   ```
这样您既得到了一个 **可工作的备份（对恢复至关重要）**，也获得了用于修改的精确镜像。即使官方镜像存在，我也会在修改 BIOS 之前先执行此操作。

### 选项 2：Wayback Machine / 存档
尝试抓取旧 SOYO 网站和第三方镜像的存档：
- `https://web.archive.org/web/*/soyo.com.cn/*`
- `https://web.archive.org/web/*/soyocn.net/*`
- 搜索关键词：`梅捷 SY-B85N BIOS`、`SY-B85N 全固版 驱动`

### 选项 3：第三方中文驱动网站/论坛
- `drivers.mydrivers.com`（Soyo 分类：`s-4-878`）
- `drv5.cn`、`160.com`、`pcpop.com`
- 百度贴吧（图拉丁吧 / 主板吧）——人们会备份这些 BIOS 文件

⚠️ 如果您从某个随机下载站点找到了一个“BIOS”，请在刷写前验证该文件是否为真实的闪存镜像（正确的大小，例如 8MB，并且以可识别的 UEFI/Aptio 头部开头）。

## 针对该主板的重要 ReBarUEFI 说明

`SY-B85N` = **Intel B85 芯片组 = 8 系列（Haswell/Broadwell，LGA1150）**。根据 ReBarUEFI 维基，这意味着：

1. **`HswAbove4G.txt` 补丁是必需的**——在 Intel 8/9 系列上，如果没有它，4G 解码 / 可调整大小 BAR 将无法正常工作。在运行 UEFIPatch 之前，将其附加到 `patches.txt` 中。
2. 这是一块 Haswell 主板，因此相关的 `patches.txt` 条目是：
   - PciBus：移除 `<16GB BAR 大小限制`
   - PciBus：`不将 64 位 BAR 降级为 32 位`（Haswell/Broadwell）
   - PciHostBridge / MMIO 空间增加（Haswell/Broadwell 变体）
3. 这块主板几乎肯定使用 **AMI Aptio** BIOS，因此如果稍后 `ReBarState` 失败并显示 `GetLastError: 5`，您可能还需要 NVRAM 白名单解锁补丁。
4. 如果 UEFITool 的“插入后”操作导致 pad-file 损坏错误（这类主板常见），预计会使用 **MMTool 4.50.0.23**（Skylake 之前的主板）。

## 建议的操作顺序

1. 使用 CH341A + flashrom 读取芯片 → 保存 `soyo_b85n_backup.bin`（先做这一步！）
2. 将 `ReBarDxe.ffs` 插入到读取的镜像中（UEFITool 0.28）
3. 使用附加了 `HswAbove4G.txt` 的 `patches.txt` 运行 UEFIPatch
4. 检查 pad-file 损坏；如果存在，则使用 MMTool 4.50 的解决方法
5. 使用 CH341A + flashrom 刷写回去（或使用主板自带的刷写工具）
6. 在 BIOS 中：启用 4G 解码（可能隐藏 → 按维基指南解锁隐藏的 4G 解码），禁用 CSM
7. 启动 Linux/Windows，运行 `ReBarState`，设置为 `32`，重新启动

需要我为您获取 `HswAbove4G.txt` 的内容以及完整的 `patches.txt`（包含我已经有的 Haswell/8 系列条目），以便您有一份可直接用于该主板的 `patches.txt` 吗？如果您告知板上是哪颗闪存芯片，我也可以帮您逐步完成 flashrom 读取/刷写命令。