---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 /etc/hosts 文件中映射主机名
translated: true
type: note
---

问题：如何在 `/etc/hosts` 中添加一条记录，以便轻松访问 `http://192.168.1.36:3001/dashboard`？

回答：

您可以使用 `/etc/hosts` 文件将自定义主机名（例如 `myapp.local`）映射到您的 IP（`192.168.1.36`）。这样，您就可以使用友好名称而不是原始 IP 来访问您的服务。

### 逐步操作

#### 1. 使用 root 权限打开 `/etc/hosts`

```bash
sudo nano /etc/hosts
```

（或使用您喜欢的 `vim`）

#### 2. 在底部添加新条目

```
192.168.1.36   myapp.local
```

#### 3. 保存并退出

* 在 nano 中：`Ctrl + O` → Enter → `Ctrl + X`

#### 4. 访问您的应用

现在您可以打开：

```
http://myapp.local:3001/dashboard
```

---

### 注意事项

* `/etc/hosts` 文件仅映射 **hostname → IP**，不包括端口或路径。
  因此，您仍需在 URL 中包含 `:3001/dashboard`。

* 如果您想要多个名称：

```
192.168.1.36   myapp.local dashboard.local api.local
```

* 如果立即不起作用，请刷新 DNS 缓存：

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

---

### 可选（更干净的 URL）

如果您想访问 **无需端口/路径**，例如：

```
http://myapp.local
```

您需要一个 **reverse proxy**（例如 Nginx）：

示例：

```nginx
server {
    listen 80;
    server_name myapp.local;

    location / {
        proxy_pass http://192.168.1.36:3001/dashboard;
    }
}
```

---

如果您愿意，我可以帮助您设置 Nginx 或本地开发 DNS 设置（例如 `dnsmasq`），以获得更可扩展的解决方案。