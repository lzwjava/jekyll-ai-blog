---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacBook 深度休眠唤醒失败
translated: true
type: note
---

以下是完整的诊断结果：

---

**根本原因：系统进入深度休眠（S3）后未能唤醒。**

上一次启动在 03:17:58–03:17:59 的终止序列：

```
systemd-logind[1005]: 电源键短按。
systemd-logind[1005]: 系统即将休眠！
NetworkManager: 休眠请求
systemd-sleep[28058]: 执行休眠操作 'suspend'...
kernel: PM: 休眠入口 (deep)
```

随后**没有任何记录**——没有 `PM: 休眠退出`，没有恢复，没有任何日志条目。系统正常进入休眠，但**唤醒完全失败**。键盘、触摸板或开盖信号均无法唤醒系统，只能通过电源键强制重启。

**原因分析（Apple MacBook 运行 Linux）：**

你的 `/proc/acpi/wakeup` 显示以下问题：

| 设备 | 从 S3（深度休眠）唤醒？ | 从 S4 唤醒？ |
|--------|:---:|:---:|
| LID0（开盖） | **否** | 是（仅休眠） |
| SPIT（触摸板） | 是 | — |
| 键盘 | **未列出** | — |
| 电源键 | **被 systemd-logind 拦截** | — |

在运行 Linux 的 Apple MacBook 硬件上：
- **没有设备正确配置为从深度 S3 休眠唤醒**——键盘未出现在 ACPI 唤醒表中，开盖仅支持 S4（休眠）唤醒，而非 S3。
- 电源键在休眠过程中被按下（注意：03:17:58 和 03:17:59 有两条"电源键短按"日志）——第一次*触发*了休眠，第二次被休眠进程吞没。
- 深度休眠（S3）是默认设置：`s2idle [deep]`——`[deep]` 标记当前活动模式。

**快速修复——切换至 s2idle（现代待机）：**

s2idle 是一种较浅的休眠模式，不会完全关闭 CPU——电池消耗略高，但在 Apple 硬件上**唤醒可靠**，因为键盘/触摸板保持活动状态。

```bash
# 持久化设置
echo 'SleepMode=s2idle' | sudo tee -a /etc/systemd/sleep.conf.d/disable-deep-suspend.conf
```

或立即尝试：

```bash
sudo sh -c 'echo s2idle > /sys/power/mem_sleep'
```

**替代方案——完全禁用自动休眠**（如果不希望合盖休眠）：

```bash
# 合盖时不休眠
gsettings set org.gnome.settings-daemon.plugins.power lid-close-ac-action 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
```

需要我应用以上任一方案吗？