---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 OpenClaw 连接到 Nextcloud Talk
translated: true
type: note
---

以下是如何配置的：

### 步骤 1：安装插件

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

### 步骤 2：在您的 Nextcloud 服务器上创建 bot

```bash
docker exec nextcloud-app-1 php occ talk:bot:install "OpenClaw" "your-shared-secret" "http://<your-server-ip>:8788/nextcloud-talk-webhook" --feature reaction
```

将 `your-shared-secret` 替换为强密码，并将 `<your-server-ip>` 替换为服务器的实际 IP/主机名（Gateway 运行所在的那个）。

### 步骤 3：配置 OpenClaw

```bash
openclaw config set channels.nextcloud-talk.enabled true
openclaw config set channels.nextcloud-talk.baseUrl "http://localhost:8080"
openclaw config set channels.nextcloud-talk.botSecret "your-shared-secret"
```

如果您的 Gateway 在反向代理后面，还需设置：

```bash
openclaw config set channels.nextcloud-talk.webhookPublicUrl "https://your-public-domain/nextcloud-talk-webhook"
```

### 步骤 4：重启并测试

```bash
openclaw gateway restart
```

然后在 Nextcloud Talk 中，打开您要使用的房间，转到 **Room Settings → Bots**，并启用 “OpenClaw” bot。给它发送一条消息，它应该会回复。

需要我帮您运行这些步骤中的任何一个吗？