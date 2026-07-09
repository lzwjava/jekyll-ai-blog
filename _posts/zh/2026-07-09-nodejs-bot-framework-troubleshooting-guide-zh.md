---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Node.js Bot Framework 故障排除指南
translated: true
type: note
---

## 摘要

### openclaw

**描述**：一个基于 Node.js 的多通道机器人代理框架（类似于 Hermes Agent），全局安装。

| 字段 | 详情 |
| --- | --- |
| 包名 | `openclaw@2026.5.12` — 全局 npm 安装 |
| 二进制文件 | `/home/lzw/.npm-global/bin/openclaw` |
| 安装路径 | `/home/lzw/.npm-global/lib/node_modules/openclaw/` |
| 配置目录 | `~/.openclaw/`（用户主目录，约 `512KB` 总大小） |
| 配置文件 | `~/.openclaw/openclaw.json` |
| 工作区 | `~/.openclaw/workspace/`（28 个目录） |
| 通道 | Telegram（默认）、Nextcloud Talk、WhatsApp、WeChat（`openclaw-weixin`） |
| 扩展 | `@openclaw/nextcloud-talk`、`@tencent-weixin/openclaw-weixin` |
| 运行时 | Node.js v25.8.1 |

**状态**：Telegram 通道处于崩溃循环中。日志位于 `/tmp/openclaw/openclaw-2026-07-09.log`（约 3.5MB），显示：

- `fetch timeout` — 对 `api.telegram.org` 的 `getMe` 请求反复超时（10 秒超时）
- `UND_ERR_CONNECT_TIMEOUT` — DNS 解析成功但 IP 不可达
- 自动重启尝试（1/10、2/10……）持续失败
- 传输退避：10 秒 → 20 秒 → 40 秒不健康标记窗口
- 最近 24 小时日志中无成功连接

**根本原因**：可能是该机器上的代理/防火墙阻止了 Telegram API。Bot token 存在，但无法到达 Telegram 服务器进行轮询/getUpdates。

**你的配置中也引用了**：

- `~/ww/ww/config/openclaw.json` — 你的 `ww` 工具中嵌入了指向同一工作区的 openclaw 配置
- `~/projects/config/openclaw/openclaw.json` — 另一个配置变体

---

### myopia-reversal-app

**位置**：`/home/lzw/.openclaw/workspace/myopia-reversal-app/`

**类型**：单页 Web 应用（HTML/CSS/JS），无框架/构建步骤——仅 `index.html` + Vite 开发依赖（生产环境未使用）

**用途**：一个计算器，根据完整的远用处方推荐“近用”处方——通常减少 **-1.50D**（亚洲格式为 150 度）。基于主动近视逆转/眼球缩短理论。

**功能**（全部客户端 JS）：

- 输入左/右眼远用处方（球镜 + 柱镜）
- 输出推荐的近用处方
- 单位切换：亚洲（度） vs 西方（屈光度）
- 语言：英文 / 中文（双语切换）
- 深色/浅色主题切换
- 恢复提示区域

**文件**：

```
myopia-reversal-app/
  index.html         (14KB, 345 行 — 所有 UI 和逻辑内联)
  README.md          (英文)
  README_CN.md       (中文)
  package.json       (仅 Vite 开发依赖)
  package-lock.json
  node_modules/
  .git/              (1 次提交，3 月 14 日)
```

**Git**：单分支 `master`，一次提交于 3 月 14 日。无远程仓库（仅本地）。

---

### nginx 配置

**配置文件**：`/etc/nginx/conf.d/default.conf` — 单个服务器块，监听 80 端口

**路由**：

| 路径 | 目标 | 类型 |
| --- | --- | --- |
| `/` | `/var/www/html/` | 静态文件 |
| `/todo/` | `/var/www/html/todo/` | 静态文件 |
| `/myopia/` | `/home/lzw/.openclaw/workspace/myopia-reversal-app/` | **刚刚添加** |
| `/movies/` | `/home/lzw/qDownloads/` | 目录列表 |

**其他**：`/etc/nginx/conf.d/pincc-proxy.conf` — 反向代理，端口 8742 → `v2-as.pincc.ai`（Claude Code API 代理，硬编码 auth token `sk-8a2...ea7f` 和伪造的客户端头）

**状态**：`nginx -t` 通过，重新加载成功，`curl http://localhost/myopia/` → 200

**在浏览器中打开**：`http://<工作站 IP>/myopia/` 或如果在工作站上则 `http://localhost/myopia/`。
