---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw 安全上下文错误
translated: true
type: note
---

Question: OpenClaw Control UI 显示 "requires device identity (use HTTPS or localhost secure context)" — 如何修复？

Answer:

## 根本原因

现代浏览器在非安全来源上**阻止某些 JavaScript APIs**（如 OpenClaw 使用的 device identity/fingerprinting）。通过纯 `http://` 在非 localhost 地址上提供的页面被浏览器视为**insecure context**。

您有**3 个选项**来修复此问题：

---

## 选项 1 — 使用 SSH Tunnel（最简单，无需配置更改）

这是**最简单的修复方法**。不要直接打开 `http://192.168.1.36:18789`，而是通过 SSH 隧道访问，这样浏览器会将其视为 `localhost`：

**在您的主 PC 上**，运行：

```bash
ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
```

然后在浏览器中打开：

```
http://localhost:18789
```

`localhost` 始终被浏览器视为**secure context** — 无需 HTTPS。✅

---

## 选项 2 — 在 OpenClaw 中启用 HTTPS，使用自签名证书

### 步骤 1 — 生成自签名证书

```bash
mkdir -p ~/.openclaw/certs
cd ~/.openclaw/certs

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
  -days 3650 -nodes \
  -subj "/CN=192.168.1.36" \
  -addext "subjectAltName=IP:192.168.1.36"
```

### 步骤 2 — 配置 OpenClaw 使用 HTTPS

```bash
nano ~/.openclaw/openclaw.json
```

在 `gateway` 内添加 `tls` 块：

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "tls": {
      "cert": "/home/lzw/.openclaw/certs/cert.pem",
      "key": "/home/lzw/.openclaw/certs/key.pem"
    },
    "controlUi": {
      "allowedOrigins": ["*"]
    }
  }
}
```

### 步骤 3 — 重启 gateway

```bash
openclaw gateway stop
openclaw gateway start
```

### 步骤 4 — 在浏览器中打开

```
https://192.168.1.36:18789
```

⚠️ 浏览器会显示**证书警告**（因为是自签名）。点击**高级 → 继续前进**。接受一次后，即可作为 secure context 使用。

---

## 选项 3 — 使用 Caddy 作为反向代理，实现自动 HTTPS（最规范）

如果您想要**无浏览器警告的干净 HTTPS**，可以使用 Caddy，它会自动生成受信任的本地证书。

### 安装 Caddy

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy -y
```

### 配置 Caddyfile

```bash
sudo nano /etc/caddy/Caddyfile
```

```
:18790 {
    tls internal
    reverse_proxy 127.0.0.1:18789
}
```

### 启动 Caddy

```bash
sudo systemctl restart caddy
sudo systemctl enable caddy
```

### 在主 PC 上信任 Caddy 根 CA

```bash
# 在 SERVER 上 - 导出证书
cat $(caddy environ | grep DATA_DIR | cut -d= -f2)/pki/authorities/local/root.crt
```

复制并将该证书安装到主 PC 的浏览器信任存储中。

然后访问：

```
https://192.168.1.36:18790
```

---

## 推荐总结

| 选项 | 难度 | 浏览器警告 | 最适合 |
|---|---|---|---|
| **SSH Tunnel** (`localhost`) | ✅ 最简单 | 无 | 快速访问，单用户 |
| **自签名证书** | 🟡 中等 | 浏览器每次一次 | 始终在线 LAN 访问 |
| **Caddy 反向代理** | 🟡 中等 | CA 安装后无 | 最干净的设置 |

## ✅ 现在最快的修复方法

只需将 `gateway.bind` 改回 `loopback`，并**始终使用 SSH 隧道**：

```bash
openclaw gateway stop
openclaw config set gateway.bind loopback
openclaw gateway start
```

然后从主 PC：

```bash
ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
```

打开：`http://localhost:18789` — 完美运行，无需 HTTPS，最安全。
