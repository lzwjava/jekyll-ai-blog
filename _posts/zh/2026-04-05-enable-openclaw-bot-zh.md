---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Nextcloud Talk 中启用 OpenClaw 机器人
translated: true
type: note
---

**问题：** 如何在 Nextcloud Talk 对话中启用 OpenClaw 机器人（ID: 4）？我在 Talk 界面中找不到它 —— 只看到管理面板。

**答案：**

在 Nextcloud Talk 界面中**没有可见的“机器人列表”**来启用机器人。出于安全考虑，机器人只能通过命令行使用 `occ` 命令添加和管理。界面只会在机器人**先通过 CLI 针对特定对话启用后**才显示它们。

你需要通过**Nextcloud 服务器上的命令行**（或 Docker 容器）来操作。

---

## 步骤 1：获取对话令牌

打开你想让机器人加入的 Talk 对话。查看 URL：
```
http://192.168.1.36:8080/apps/spreed/#/XXXXXXXX
```
末尾的 `XXXXXXXX` 就是你的**房间令牌**。

---

## 步骤 2：在该对话中启用机器人

在你的 Nextcloud 服务器上（或在 Docker 内）运行：

```bash
# 如果在 Docker 中运行：
docker exec -it -u 33 <nextcloud_container_name> /var/www/html/occ talk:bot:setup 4 <ROOM_TOKEN>
```

将 `<ROOM_TOKEN>` 替换为步骤 1 中的令牌。

`talk:bot:setup <bot-id> <token>` 命令用于在特定对话中启用机器人。

---

## 需要了解的有用 OCC 命令

以下是关键的机器人管理命令：
- `talk:bot:list` — 列出所有已安装的机器人
- `talk:bot:remove <bot-id>` — 从特定对话中移除机器人
- `talk:bot:setup <bot-id> <token>` — 在对话中启用机器人
- `talk:bot:state <bot-id> <state>` — 更改机器人状态（0=禁用，1=启用，2=无设置）
- `talk:bot:uninstall <id>` — 从服务器上完全移除机器人

---

## 步骤 3：验证机器人已启用

```bash
docker exec -it -u 33 <container_name> /var/www/html/occ talk:bot:list
```

你应该能看到 OpenClaw 机器人被列出，状态为 `1`（启用）。

---

## 之后

通过 CLI 启用后，回到 Talk 对话并发送消息 —— 机器人现在应该处于活动状态并会响应。如果你的 DM 策略是 `pairing`，你需要按照设置说明中的描述批准配对码。

**参考资料：**

- [Nextcloud Talk 机器人与 Webhooks 文档](https://nextcloud-talk.readthedocs.io/en/latest/bots/)
- [OCC 命令参考](https://nextcloud-talk.readthedocs.io/en/latest/occ/)
- [OpenClaw Nextcloud Talk 设置指南](https://open-claw.me/channels/nextcloud)