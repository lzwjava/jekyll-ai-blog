---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 挂起修复：s2idle 切换已应用
translated: true
type: note
---

两项变更已应用并验证：

| 检查项 | 修改前 | 修改后 |
| --- | --- | --- |
| `/sys/power/mem_sleep` | `s2idle [deep]` | **`[s2idle] deep`** |
| 配置文件 | 不存在 | `/etc/systemd/sleep.conf.d/disable-deep-suspend.conf` → `SleepMode=s2idle` |

- **即时修复**：当前运行的内核已切换——`s2idle` 现为活动状态，`[deep]` 作为备用方案。
- **持久生效**：通过 systemd 配置片段可在重启后保留设置。

s2idle 在空闲时耗电量略高，但由于键盘/触控板控制器保持供电，在 Apple 硬件上能可靠唤醒。下次合上盖子或按下电源键时，系统应正常挂起和恢复，而不会崩溃导致死机。
