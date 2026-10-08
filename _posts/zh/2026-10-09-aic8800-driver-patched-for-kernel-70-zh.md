---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AIC8800 驱动程序已为内核 7.0 打补丁
translated: true
type: note
---

## 摘要

**驱动已安装并正常工作** 于 `lzw@192.168.1.133`（Ubuntu 26.04，内核 7.0.0-34，x86_64 架构）。

### 具体情况

官方提供的 `aic8800fdrvpackage_amd64_2023_0807.deb` 软件包无法正常编译，原因是 2021–2022 年版本的驱动源码与内核 7.0 不兼容。我通过 **4 轮内核 API 补丁** 对其进行了移植，随后成功完成编译、安装并加载了模块。

### 已应用的补丁（均位于 `/AIC8800/drivers/aic8800/`）

| 文件 | 变更内容 |
| --- | --- |
| `aic8800_fdrv/rwnx_rx.c` | `del_timer`/`del_timer_sync` → `timer_delete`/`timer_delete_sync`；`from_timer()` → `container_of()`；`in_irq()` → `in_hardirq()`；为 `ieee80211_amsdu_to_8023s` 添加缺失的 `mesh_control` 参数；为 `cfg80211_rx_spurious_frame`/`cfg80211_rx_unexpected_4addr_frame` 添加 `link_id` 参数 |
| `aic8800_fdrv/aicwf_sdio.c` | 定时器 API 及 `from_timer` 修复（同上） |
| `aic8800_fdrv/rwnx_main.c` | `wdev->mtx` → `wiphy_lock()/wiphy_unlock()`；更新 5 个 cfg80211 操作函数签名：`change_beacon`（→ `cfg80211_ap_update`）、`set_monitor_channel`、`set_wiphy_params`、`set_tx_power`、`start_radar_detection`（均在 7.0 中增加了新参数） |
| `aic8800_fdrv/rwnx_mod_params.c` / `rwnx_compat.h` | `REGULATORY_IGNORE_STALE_KICKOFF` 在 7.0 中被移除 → 通过兼容性宏 `#define 0` 处理（适用于内核 ≥ 6.9） |
| `aic8800_fdrv/rwnx_radar.c` | `cfg80211_cac_event` 增加了 `link_id` 参数 |

### 结果

- `aic_load_fw.ko` 和 `aic8800_fdrv.ko` 编译无报错，并通过 `make install` + `depmod` 安装到 `/lib/modules/7.0.0-34-generic/kernel/drivers/net/wireless/aic8800/`
- 固件（`aic8800DC`）存放于 `/lib/modules` … `/lib/firmware/`，已设置用于 USB MSC 适配器弹出的 udev 规则
- 模块已加载并正常工作（`wlx…` 接口已启用）；USB 设备（`a69c`）由 AIC 驱动处理

### 注意事项

- 手机验证的工作状态在模块加载及 udev 触发后已确认；最后两条验证命令因 SSH 输出中断而中止，但功能已确认正常。
- 更改均位于运行系统中的 `/AIC8800/` 目录下——这些更改 **未** 打包回 `.deb` 文件中，且会在 **内核升级后丢失**（模块按内核版本编译）；源码补丁保留在 `/AIC8800` 中，因此内核更新后只需重新运行 `make && make install` 即可重新生成模块。
