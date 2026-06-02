---
audio: false
date: 2025-09-09
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 环境变量更新后重启Docker容器
translated: true
type: note
---

当你修改 `.env` 文件后，Docker 不会自动重新加载这些环境变量。你需要重启容器以使新值生效。对于 LibreChat 设置，可以按以下步骤操作：

1. 确保位于包含 `docker-compose.yml` 文件的目录中
2. 执行以下命令：

```bash
docker compose down
docker compose up -d
```

这将停止并移除正在运行的容器，然后使用新的 `.env`值重新创建它们。

---

### 备选方案：仅重启

如果不想完全拆除所有容器，可以通过重建强制容器获取新环境变量：

```bash
docker compose up -d --force-recreate
```

如果还修改了 Dockerfile 或依赖项，可添加 `--build` 参数：

```bash
docker compose up -d --build
```

---

✅ 简而言之：

* 编辑 `.env` 后，务必**重新创建**容器（使用 `down` + `up` 或 `up --force-recreate`）
* 单纯的 `docker compose restart` 不会重新加载新环境变量，它只会用旧值重启容器

需要我演示如何**验证** LibreChat 容器是否正在使用新的环境变量吗（例如通过 `docker inspect` 或 `docker exec env`）？
