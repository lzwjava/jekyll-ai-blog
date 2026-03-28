---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Immich v2.6.1 部署概览
translated: true
type: note
---

Immich v2.6.1 已启动并运行。以下是运行状态：

**✅ 正在运行 — `http://192.168.1.36:2283`**

| Container | Status |
|---|---|
| immich_server | Starting up |
| immich_postgres | Healthy ✅ |
| immich_redis | Starting |
| immich_machine_learning | Starting (face recognition, search) |

**配置信息：**
- **Version:** v2.6.1 (pinned)
- **Timezone:** Asia/Hong_Kong
- **Photo storage:** `~/immich-app/library`
- **DB password:** 随机 20 位字母数字
- **Port:** 2283

**后续步骤：**
1. 在浏览器中打开 `http://192.168.1.36:2283`
2. 创建 admin 账户
3. 安装 Immich 移动端 App (iOS/Android) — 它会通过 WiFi 自动备份你的照片
4. 上传照片后，ML container 将开始对人脸和物体进行 indexing

需要我为你配置用于外部访问的 HTTPS reverse proxy，还是目前仅限本地访问即可？