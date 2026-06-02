---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Linux防火墙设置指南
translated: true
type: note
---

好问题——在 Linux 系统（如 **Red Hat** 或 **Ubuntu**）中设置防火墙主要涉及使用 **`firewalld`** 或 **`ufw`**，具体取决于你的系统。以下是为两种系统系列准备的清晰指南，方便你选择合适的方法。

---

### 🔹 在 **Red Hat / CentOS / Fedora** 系统上（使用 firewalld）

#### 1. 检查 `firewalld` 是否已安装并运行

```bash
sudo systemctl status firewalld
```

如果未运行：

```bash
sudo systemctl enable firewalld
sudo systemctl start firewalld
```

#### 2. 基本用法

检查活动区域（区域将接口和规则分组）：

```bash
sudo firewall-cmd --get-active-zones
```

列出当前区域的所有规则：

```bash
sudo firewall-cmd --list-all
```

#### 3. 允许或阻止端口/服务

允许一个端口（例如 SSH 端口 22）：

```bash
sudo firewall-cmd --permanent --add-port=22/tcp
```

允许一个已知服务（例如 HTTP）：

```bash
sudo firewall-cmd --permanent --add-service=http
```

阻止/移除一个服务：

```bash
sudo firewall-cmd --permanent --remove-service=http
```

重新加载以应用更改：

```bash
sudo firewall-cmd --reload
```

#### 4. 验证规则

```bash
sudo firewall-cmd --list-all
```

---

### 🔹 在 **Ubuntu / Debian** 系统上（使用 ufw）

Ubuntu 自带 **UFW**（简单防火墙），更易于管理。

#### 1. 启用 UFW

```bash
sudo ufw enable
```

#### 2. 允许/拒绝端口或服务

允许 SSH：

```bash
sudo ufw allow ssh
```

允许 HTTP（端口 80）：

```bash
sudo ufw allow 80/tcp
```

允许特定端口范围：

```bash
sudo ufw allow 1000:2000/tcp
```

拒绝一个服务：

```bash
sudo ufw deny 23/tcp
```

#### 3. 检查状态

```bash
sudo ufw status verbose
```

#### 4. 如需重置规则

```bash
sudo ufw reset
```

---

### 🔹 两种系统通用方法

要**阻止所有传入流量，仅允许少数例外**，你可以：

1. 默认拒绝所有传入流量

   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

   （对于 `firewalld`，可使用区域或丢弃区域实现类似行为）

2. 然后有选择地允许端口（例如 22、80、443）。

---

### 🔹 安全提示

在远程启用或更改防火墙规则之前，务必**先允许 SSH**——否则可能会将自己锁在系统外。

---

需要我展示一个**最小化防火墙设置示例**吗（例如，针对典型 Web 服务器，仅允许 SSH + HTTP + HTTPS）？
