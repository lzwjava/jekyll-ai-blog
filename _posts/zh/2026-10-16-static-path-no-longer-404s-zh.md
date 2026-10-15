---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 静态路径不再返回404
translated: true
type: note
---

前端已部署到 Google Cloud —— `/static/` 不再返回 404。摘要：

## 已完成的修改

1. **将 `live-mobile-web`** 从本机复制到 `live-server` VM 的 `/home/lzw/live-mobile-web`（已排除 `node_modules/`、`.git/`、过时的 `static/` 和 `uploadqn.json` 凭据）——路径与 compose bind mount `../live-mobile-web:/app` 一致
2. **通过 compose profile 运行前端构建**：`docker compose --profile frontend up frontend` → Vite 在 18 秒内成功构建到 `frontend-dist` volume（compose 注入了 `VITE_BASE_URL=/static/`，正确覆盖了 `.env.production`）
3. **外部验证结果：**

| URL | 状态 |
| --- | --- |
| `/static/` | **200** — SPA index.html（趣直播） |
| `/static/index.html` | 200 |
| `/static/assets/index-CgRn8J2L.js` + CSS chunks | 200 |
| `/static/logo.png` | 200 |
| `/topics`（API） | 200 — 仍正常 |

`web` container 无需重启——volume mount 会直接加载构建好的文件。

## 备注

- **`.env.production` 中 `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` 为空** → 聊天功能将显示 "not configured" 提示。填入后再运行 `docker compose --profile frontend up frontend` 重新构建。
- **前端修改后重新构建：** `cd /home/lzw/live-server && docker compose --profile frontend up frontend`
- **VM 上的 `npm ci` 在项目目录中添加了 `node_modules/`（约 112M）**——后续复制时排除？它能加速重新构建，因此我保留了它。
- 磁盘占用现为 **74%**（剩余 2.5G）——node 构建 + 镜像多占用了约 400M。仍然值得挂载更大的磁盘。
- 之前遗留的未完成事项：backend `.env` 中的真实 Supabase keys、HTTPS/域名、数据库密码更换、SRS 推流。
