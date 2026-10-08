---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AIC8800驱动与内核7.0不兼容
translated: true
type: note
---

## 总结

**我的操作：**

1.  检查了软件包（`aic8800fdrvpackage_amd64_2023_0807.deb`）—— 这是一个 AIC8800 USB 无线/蓝牙驱动程序（包含 `aic_load_fw` 和 `aic8800_fdrv` 内核模块），会在安装时**从源代码编译**以适配当前运行的内核。
2.  将 amd64 版本的 `.deb` 包复制到 `lzw@192.168.1.133:/tmp/` 并执行 `sudo dpkg -i`。目标机器上已连接该设备（USB ID `a69c:5721`）。

**结果——软件包“安装成功”，但驱动程序并未正常工作：**

*   `dpkg -i` 报告安装成功，相关文件已部署（`/AIC8800/` 目录、`/lib/firmware/aic8800DC` 下的固件、udev 规则以及测试工具）。
*   **但内核模块编译失败了。** 安装后脚本（postinst）没有错误检查机制，虽然打印了“成功”信息，但实际 `make` 过程出错。系统中没有生成 `.ko` 模块文件，后续的 `insmod` 步骤也已失败。

**根本原因：** 驱动程序源代码来自 2021–2022 年，与目标系统 **内核 7.0.0-34（Ubuntu 26.04）** 不兼容。构建错误如下：

| 文件 | 错误信息 | 内核 7.0 的变更 |
| --- | --- | --- |
| `rwnx_rx.c` | `ieee80211_amsdu_to_8023s` — 参数数量不足 | 函数签名新增了一个参数 |
| `rwnx_rx.c` | `del_timer` / `del_timer_sync` / `from_timer` — 隐式声明 | 定时器 API 已重命名（改为 `timer_delete`/`timer_delete_sync`） |
| `rwnx_rx.c` | `cfg80211_rx_spurious_frame` / `cfg80211_rx_unexpected_4addr_frame` — 参数数量不足 | 函数新增了一个参数 |
| `rwnx_rx.c` | `in_irq()` — 隐式声明 | 已从内核头文件中移除 |

**当前状态：** `wlxfc221c401af8` 接口仍使用之前的驱动程序（接口已启用，MAC 地址为 `fc:22:1c:40:1a:f8`）。AIC8800 模块未加载，USB 设备仍处于“Aic MSC”（大容量存储/转接器）模式——只有当驱动程序加载成功后，udev 规则才会将其弹出。

**完成所需的后续步骤：** 修补位于 `/AIC8800/drivers/aic8800/` 下的驱动程序源代码，以适配内核 7.0 的 API 变更（目前所有错误均出现在 `rwnx_rx.c` 文件中；修复这些错误后可能还会出现更多问题）。然后执行 `make && make install` 并重新加载模块。我用于获取确切新内核签名的上一个命令已中断——如果您希望驱动程序真正运行起来，我可以继续该操作并应用修复。