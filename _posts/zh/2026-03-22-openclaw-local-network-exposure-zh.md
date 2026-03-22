---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 OpenClaw 暴露至本地网络接口
translated: true
type: note
---

Answer:Answer:

## 根本原因

问题是 OpenClaw 在远程服务器上**绑定到 `127.0.0.1:18789`** — 这意味着它仅监听 localhost，而不是网络接口。这就是为什么一开始需要使用 SSH 隧道的原因。

最干净的修复方法是**让 OpenClaw 监听 `0.0.0.0:18789`**，而不是 `127.0.0.1:18789`。

---

## 解决方案 1：更改 OpenClaw 的绑定地址（最佳解决方案）

在远程服务器 `192.168.1.36` 上，找到 OpenClaw 的启动方式并更改绑定主机。

通常在配置文件或启动命令中：

```bash
# 修改前（仅 localhost）
host = "127.0.0.1"
port = 18789

# 修改后（所有接口，可通过 LAN IP 访问）
host = "0.0.0.0"
port = 18789
```

或者如果通过命令行参数启动：
```bash
# 从以下修改为
openclaw --host 127.0.0.1 --port 18789

# 修改为
openclaw --host 0.0.0.0 --port 18789
```

修改后，您可以从同一 LAN 上的任何机器直接访问 `http://192.168.1.36:18789`。

---

## 解决方案 2：在远程服务器上使用反向代理（nginx）

如果无法更改 OpenClaw 的配置，请在 `192.168.1.36` 上设置 nginx 来代理端口：

```bash
sudo apt install nginx
```

创建配置文件 `/etc/nginx/sites-available/openclaw`：
```nginx
server {
    listen 18790;              # 外部端口（如果更改 openclaw 的端口，也可以使用 18789）
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

启用并重启：
```bash
sudo ln -s /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

然后通过 `http://192.168.1.36:18790` 访问。

---

## 解决方案 3：使用 `socat` 直接暴露端口

在 `192.168.1.36` 上运行一个快速的一行命令：

```bash
socat TCP-LISTEN:18790,fork,reuseaddr TCP:127.0.0.1:18789
```

这会将端口 `18790` 上的所有连接（可通过 LAN IP 访问）转发到本地的 `18789`。通过 `http://192.168.1.36:18790` 访问。

要持久运行，请将其包装在 systemd 服务中或使用 `nohup`：
```bash
nohup socat TCP-LISTEN:18790,fork,reuseaddr TCP:127.0.0.1:18789 &
```

---

## 总结

## 总结

| 解决方案 | 难度 | 备注 |
|---|---|---|
| 更改 OpenClaw 绑定地址 | 低 | 最佳且最干净 |
| nginx 反向代理 | 中等 | 适合生产环境 |
| socat | 低 | 快速临时修复 |

**推荐使用解决方案 1** — 将绑定地址更改为 `0.0.0.0` 是最直接的方法。请确保远程服务器的防火墙允许端口 `18789`：`sudo ufw allow 18789`。

参考资料：

- [SSH Tunneling Explained - Linuxize](https://linuxize.com/post/how-to-setup-ssh-tunneling/)
- [A Visual Guide to SSH Tunnels - iximiuz](https://iximiuz.com/en/posts/ssh-tunnels/)