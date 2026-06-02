---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Hosts 文件中将 IP 映射到主机名
translated: true
type: note
---

问题：如何在 `/etc/hosts` 中添加一条记录，以便轻松访问 `http://192.168.1.36:3001/dashboard`？

答案：

您可以在本地的 `/etc/hosts` 文件中将 IP 地址映射到自定义域名。这让您可以用更容易记住的东西替换 IP。

---

## 1. 编辑 `/etc/hosts`

打开终端并运行：

```bash
sudo nano /etc/hosts
```

（您可以使用 `vim` 或任何您喜欢的编辑器。）

---

## 2. 添加新记录

在文件底部，添加一行像这样的：

```bash
192.168.1.36    mydashboard.local
```

---

## 3. 保存并退出

* 在 `nano` 中：
  按 `Ctrl + O` → Enter → `Ctrl + X`

---

## 4. 在浏览器中访问

现在而不是：

```
http://192.168.1.36:3001/dashboard
```

您可以使用：

```
http://mydashboard.local:3001/dashboard
```

---

## 5. （可选）刷新 DNS 缓存

有时更改会立即生效，但如果没有：

### macOS

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

### Linux（如果使用 systemd-resolved）

```bash
sudo systemd-resolve --flush-caches
```

---

## 关键注意事项

* `/etc/hosts` 仅映射 **hostname → IP**，不包括端口
  → URL 中仍需 `:3001`
* 此方法**仅在您的本地机器上有效**
* `.local` 常用，但您可以使用任何名称（例如 `dashboard.test`）

---

## 额外提示（更干净的 URL）

如果您想不带 `:3001` 访问，比如：

```
http://mydashboard.local/dashboard
```

您需要一个反向代理（例如 Nginx）将端口 80 → 3001。

---

如果您愿意，我可以向您展示一个**1 分钟 Nginx 配置**来完全移除端口。
