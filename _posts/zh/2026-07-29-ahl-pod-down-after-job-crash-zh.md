---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AHL服务因任务崩溃而宕机
translated: true
type: note
---

Pod 已崩溃且未恢复。目前情况如下：

---

## 🚨 服务器宕机

SSH 端口 **31005** — 连接被拒绝
隧道 URL — **404 Not Found**

## 🔍 可能的原因

**AHL 视频生成任务** 已提交并进入 `processing` 状态，但随后出错（变为 "Not found"）。这很可能导致 AHL 服务器崩溃或触发 OOM 终止，因为 AHL 进程当时使用了 **约 35GB 内存**。随后 Pod 被重启或终止。

## 🛠️ 可能的原因

1. **OOM（内存不足）** — 视频生成模型（FLUX）非常消耗内存，Pod 可能因超出限制而被终止
2. **Pod 重启** — 如果 Jupyter 进程（PID 1）退出，Pod 会重启
3. **任务后端崩溃** — 视频生成处理遇到错误并崩溃

## 下一步操作

待 Pod 恢复后，请尝试以下步骤：

1. **从平台控制台检查 Pod 是否仍在运行**
2. 如果 Pod 被重建，重新运行隧道设置：

   ```bash
   ssh -p 31005 root@36.150.116.206
   export FRP_BROKER_URL=$(grep -z FRP_BROKER_URL /proc/1/environ | tr "\0" "\n" | cut -d= -f2-)
   export FRP_BROKER_TLS_SERVER_NAME=$(grep -z FRP_BROKER_TLS_SERVER_NAME /proc/1/environ | tr "\0" "\n" | cut -d= -f2-)
   export PATH="$HOME/.local/bin:$PATH"
   /var/run/secrets/frp-self-service/install
   rc-tunnel expose --port 8000
   ```

3. 检查 AHL 服务器日志：

   ```bash
   curl http://127.0.0.1:8000/health  # 如果服务器正在运行
   ```

是否需要我继续定期尝试重新连接？
