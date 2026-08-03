---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FluxReel已部署并上线
translated: true
type: note
---

所有验证通过。**FluxReel 已部署并在互联网上提供服务。** 🎉

## ✅ 最终状态

### 实时服务

| | |
|---|---|
| **公开 URL** | **https://rc-63980f23582dde21.radeon.firstdg.ai** |
| 隧道 | `rc-tunnel 0.3.0`，状态 **active**，FRPC PID 11650 |
| 本地服务器 | `fluxreel server` (uvicorn, PID 11614) 运行在 `127.0.0.1:8081` |
| 健康检查 | `/health` → `{"status":"ok","jobs":0,"local_models":[]}` — **HTTP 200** 本地及通过公开 URL 均可访问 |

### Web UI + API 可访问
- `/` → **FluxReel — AI 视频生成器** Web 界面
- `/openapi.json` → FluxReel API（健康检查、内容生成、视频生成、任务管理、任务状态/下载、密钥验证）

### 已完成的工作
1. **部署** — 将更新后的源代码完整 rsync 至 `/root/amd-hackathon-lzwjava`（可编辑安装 → 实时生效）
2. **安装 rc-tunnel** — 安装脚本需要先从 `/proc/1/environ` 导出 `FRP_BROKER_URL` 和 `FRP_BROKER_TLS_SERVER_NAME`（shell 环境中不存在）
3. **启动服务器**，绑定到 `127.0.0.1:8081`（根据平台要求—只有 127.0.0.1 的服务可通过隧道访问）
4. **暴露服务** — 通过 `rc-tunnel expose --port 8081` → 平台分配的 `rc-*.radeon.firstdg.ai` URL
5. **从互联网验证**：健康检查返回 200，UI 可访问，API 文档正常

### 管理命令
```bash
# 从远程主机执行（需先导出 FRP_BROKER_URL）
~/.local/bin/rc-tunnel status    # 或 logs --lines 100 / stop
tail -f /root/server.log          # 服务器日志
```

### ⭐ 提醒（来自平台说明）
此实例**运行时会消耗积分**。完成后请销毁它：**Profile → Active Instance → 红色 Destroy Instance 按钮**。销毁后 URL 立即失效，重新创建 Notebook 后需重新安装 rc-tunnel 并再次暴露服务（域名前缀 24 小时冻结期适用）。

另请注意：隧道仅支持每个 Pod 一个端口，且应用本身**无身份验证**——任何人都可以访问公开 URL，因此请勿通过它暴露任何敏感内容。