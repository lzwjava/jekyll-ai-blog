---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RC隧道成功露出
translated: true
type: note
---

一切运行正常！以下是完整总结：

---

## ✅ RC Tunnel 成功暴露

### 📋 已完成操作

| 步骤 | 状态 |
| ------ | ------ |
| **从 `/proc/1/environ` 提取环境变量** | ✅ 找到 `FRP_BROKER_URL` 和 `FRP_BROKER_TLS_SERVER_NAME` |
| **安装 `rc-tunnel`** | ✅ v0.3.0 → `~/.local/bin/rc-tunnel` |
| **创建测试页面** | ✅ `~/tunnel-demo/index.html` |
| **启动 HTTP 服务器** | ✅ Python3 在 `127.0.0.1:8081` |
| **本地测试** | ✅ `curl` 返回 HTML 页面 |
| **暴露隧道** | ✅ 通过 `rc-tunnel expose --port 8081` |

### 🌐 公网 URL

```
https://rc-a899e6bb9beab78e.radeon.firstdg.ai
```

### 🔍 验证

- **公网 URL 可访问** — 本地和远程 `curl` 均返回：

  ```html
  <!doctype html><title>RC Tunnel</title><h1>RC Tunnel is working</h1>
  ```

- **状态：** `active`，FRPC PID `1140`，代理已登录且健康
- **服务器日志** 显示登录成功及代理启动

### ⚠️ 注意

`status` 和 `logs` 子命令需要导出相同的环境变量（`FRP_BROKER_URL`、`FRP_BROKER_TLS_SERVER_NAME`）。可以从 `/proc/1/environ` 获取，或将其添加到 shell 配置文件中。

### 🛑 停止隧道

```bash
# 导出环境变量后：
export FRP_BROKER_URL=$(grep -z FRP_BROKER_URL /proc/1/environ | tr '\0' '\n' | cut -d= -f2-)
export FRP_BROKER_TLS_SERVER_NAME=$(grep -z FRP_BROKER_TLS_SERVER_NAME /proc/1/environ | tr '\0' '\n' | cut -d= -f2-)
export PATH="$HOME/.local/bin:$PATH"
rc-tunnel stop
```
