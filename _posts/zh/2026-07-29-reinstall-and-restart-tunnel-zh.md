---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重新安装并重启隧道
translated: true
type: note
---

以下是所有服务的完整状态以及如何从外部访问它们：

---

## 🖥️ 内部运行的服务

| 服务 | 本地地址 | 端口 | 描述 |
| ------ | ---------- | ------ | ------ |
| **Jupyter Lab** | `0.0.0.0` | **8888** | Token: `amd-oneclick`, Base URL: `/instances/u-9758-811746f0/` |
| **AHL (AI视频生成器)** | `127.0.0.1` | **8000** | 主演示应用（响应200） |
| **隧道演示页面** | `127.0.0.1` | **8081** | 测试页面（"RC Tunnel is working"） |
| **SSH** | 外部 | **31005** | 您当前的访问方式 |

---

## 🔗 演示URL（已损坏）

**RC Tunnel** (frpc) 已配置为通过以下地址暴露 **端口8000上的AHL**：

```
https://rc-26cc80c1b835b7a3.radeon.firstdg.ai
```

**但它不起作用。** state.json 显示：

```json
{
  "tunnel_id": "tun_cb197ffdbb65782284d9e6af",
  "fqdn": "rc-26cc80c1b835b7a3.radeon.firstdg.ai",
  "local_port": 8000,
  "pid": 25628
}
```

然而，frpc 日志持续显示：

```
oauth2: "invalid_client" "invalid client credentials"
```

OIDC 凭证已**过期** — token (`/var/run/secrets/frp-self-service/token`) 对隧道代理不再有效。

---

## 🛠️ 如何修复 — 重新安装并重启隧道

在服务器上运行以下命令以重新安装并重启隧道：

```bash
# 1. 停止当前隧道
export PATH="$HOME/.local/bin:$PATH"
rc-tunnel stop

# 2. 重新安装隧道客户端
/var/run/secrets/frp-self-service/install

# 3. 如果旧 frpc 仍在运行，停止它
pkill -f frpc 2>/dev/null

# 4. 启动新隧道暴露演示（端口8000上的AHL）
"$HOME/.local/bin/rc-tunnel" expose --port 8000
```

之后，等待约10秒并检查：

```bash
"$HOME/.local/bin/rc-tunnel" status
```

它将会输出一个类似 `https://rc-<random>.radeon.firstdg.ai` 的URL — 这就是你的公共演示URL。

---

## 📌 替代访问方式（无隧道）

由于您通过端口31005拥有**SSH访问权限**，您也可以使用SSH端口转发在本地访问服务：

```bash
# 从您的机器，在本地访问 Jupyter Lab，地址为 http://localhost:8888
ssh -L 8888:localhost:8888 -p 31005 root@36.150.116.206

# 或者在本地访问 AHL 演示，地址为 http://localhost:8000
ssh -L 8000:localhost:8000 -p 31005 root@36.150.116.206
```

然后打开浏览器访问 `http://localhost:8000` 查看**AI视频生成器**演示，或者访问 `http://localhost:8888/instances/u-9758-811746f0/` （token: `amd-oneclick`）使用 Jupyter Lab。

需要我重新安装隧道并为您提供一个可用的公共URL吗？
