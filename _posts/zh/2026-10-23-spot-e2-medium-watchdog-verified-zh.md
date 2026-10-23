---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 抢占式 e2-medium 看门狗已验证
translated: true
type: note
---

一切正常。最终验证通过——以下是完整概述：

## ✅ 已切换到 SPOT e2-medium + watchdog

### 当前运行状态

| 项目 | 状态 |
| --- | --- |
| **VM** | `live-server`，**e2-medium**（2 vCPU / 4 GB），**provisioningModel: SPOT**（可抢占，终止操作：STOP） |
| **IP** | `34.150.108.243` — 不变，静态，DNS 完好 |
| **容器** | app、web、database、redis、srs — 全部 `Up`，开机后自动启动（重启策略） |
| **公共站点** | funlive.io / web.funlive.io / api.funlive.io → **200** |
| **SRS** | API 200（RTMP/HLS 已恢复） |
| **内存** | 4 GB 机器，仅使用约 730 MB — 余量充足 |
| **Swap** | 2 GB 持久化（仍然存在） |

### watchdog（实现抢占自愈）

- **Cloud Function** `spot-watchdog`（gen2，首尔/asia-east1，256 MB）：每次检查获取 VM 状态；如果未 RUNNING → 调用 `instances.start`
- **Cloud Scheduler** 任务每 **5 分钟** → OIDC 认证调用
- **专用 SA** `spot-watchdog-sa`，仅 2 个权限（`compute.instances.get`、`compute.instances.start` + 函数调用者）
- **已验证可用**：调度器任务在 18:15 成功运行（此前的 PERMISSION_DENIED 已通过 `roles/run.invoker` 修复），函数返回 `{"status": "RUNNING", "action": "noop"}`
- **费用：约 $0** — 在 Cloud Functions 和 Scheduler 免费额度内

因此，如果 GCP 回收 VM：它会停止 → watchdog 在 ≤5 分钟内重启它 → 静态 IP 重新挂载 → Docker 自动恢复所有服务。最坏情况下停机约 5–10 分钟，仅在实际抢占事件期间发生。

### 当前月度费用

| 项目 | $/月 |
| --- | --- |
| 计算 — **e2-medium SPOT**（2×$0.00874 + 4×$0.00097）/h | **$15.59** |
| 磁盘 50 GB pd-standard | $2.49 |
| 快照（14 天保留） | ~$0.25 |
| GCS 存储 | ~$1.00 |
| 网络出站流量（约 5 GB） | ~$0.60 |
| **总计** | **≈ $20/月** |

**结果：从约 $44–46 → 约 $20/月（便宜约 55%），与你开始使用的 4 GB/2 vCPU 机器相同。** 原来的 e2-medium 按需付费约为 $57；香港的 spot 定价约为 70% 折扣，因此计算组件从约 $40 → $15.6。

### 需要注意的事项

- **抢占是可能的** — 这是与按需付费相比唯一的可用性注意事项。Watchdog 可以缓解；香港的实际事件通常很少见，但并非不可能。
- 留意 watchdog：`gcloud scheduler jobs describe spot-watchdog --location=asia-east1` 会显示日志中的任何失败运行。
- 只有当视频流量增长时，出站流量/GCS 费用才会增加——如果账单上涨，这就是需要关注的。
