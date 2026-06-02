---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nextcloud Talk 机器人故障排除与修复
translated: true
type: note
---

以下是问题的完整分析以及每个问题的修复方法：

---

### 1. Installing Nextcloud Talk (spreed app)

**问题：** `occ app:install spreed` 失败 — Docker 的内部 DNS 无法解析 `github.com`。

**修复：** 在主机上从 GitHub API 下载 spreed v23.0.2 tarball，使用 `docker cp` 将其复制到容器中，解压到 `custom_apps/spreed/`，然后在容器内运行 `composer install`（先安装 composer）以生成 `vendor/autoload.php`。

### 2. Missing frontend assets (404 on CSS/JS)

**问题：** GitHub 源代码中没有预构建的前端资源 — `talk-main.css`、`talk-icons.css` 等均为 404。

**修复：** 在主机上使用 `npm install && npm run build` 构建前端，然后使用 `docker cp` 将编译后的 `css/` 和 `js/` 目录复制到容器中。修复所有权为 `www-data`。

### 3. Plugin installation

**问题：** 无 — `openclaw plugins install @openclaw/nextcloud-talk` 运行正常。该插件已作为标准插件捆绑。

**修复：** 无需修复，但注意：存在“重复插件”警告，因为同时存在标准版和安装版。无论如何都能正常工作。

### 4. Bot created with wrong features

**问题：** `talk:bot:install --feature reaction` 设置 features=8（仅 assistant），因此 bot 从未接收到聊天消息。错误计数为零，未发送任何 webhook。

**修复：** 从数据库中删除 bot，使用 `--feature webhook --feature response --feature reaction`（features=11）重新安装。然后运行 `talk:bot:setup 3 eu42ecdy` 以在房间中启用它。

### 5. UFW firewall blocking port 8788

**问题：** Nextcloud 容器无法访问 `172.19.0.1:8788` — UFW 默认策略为 `deny (incoming)`，且未允许端口 8788。其他 Docker 端口（3000、8080）正常，因为有明确的 UFW 规则。

**修复：** `sudo ufw allow 8788/tcp comment "OpenClaw Nextcloud Talk webhook"`

### 6. groupPolicy blocking rooms

**问题：** 默认 `groupPolicy` 为 `allowlist`，且未列出任何房间 — 所有消息被静默丢弃。

**修复：** `openclaw config set channels.nextcloud-talk.groupPolicy open` + 添加特定房间配置。

### 7. Gateway restart needed

**问题：** 配置更改需要重启 gateway 才能生效。

**修复：** 每次配置更改后运行 `openclaw gateway restart`。

---

### TL;DR 操作顺序

```bash
# 1. 在 Nextcloud 中安装并构建 spreed app
# 2. 安装 OpenClaw 插件
openclaw plugins install @openclaw/nextcloud-talk

# 3. 使用正确的功能创建 bot
docker exec nextcloud-app-1 php occ talk:bot:install "OpenClaw" "<secret>" "<webhook-url>" --feature webhook --feature response --feature reaction
docker exec nextcloud-app-1 php occ talk:bot:setup <bot-id> <room-token>

# 4. 开放防火墙
sudo ufw allow 8788/tcp

# 5. 配置 OpenClaw
openclaw config set channels.nextcloud-talk.enabled true
openclaw config set channels.nextcloud-talk.baseUrl "http://localhost:8080"
openclaw config set channels.nextcloud-talk.botSecret "<secret>"
openclaw config set channels.nextcloud-talk.groupPolicy open

# 6. 重启
openclaw gateway restart
```

最大的陷阱是 #4 — 功能标志。仅使用 `--feature reaction` 不会赋予 bot `webhook` 能力，因此它从未接收到任何消息。
