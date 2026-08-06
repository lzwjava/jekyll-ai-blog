---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 默认OpenRouter密钥已配置
translated: true
type: note
---

完成——该密钥现已成为服务器默认配置，用户无需自行提供。已通过公共隧道进行端到端验证。

## 我所做的工作

1. **将该密钥设为服务器默认值**——将 `OPENROUTER_API_KEY=sk-or-v1-346a...613` 追加至 `/root/.config/fluxreel/.env`（权限 600）。服务器的 `load_env()` 钩子在启动时以 `override=True` 加载此文件，所有 OpenRouter 调用（`_openrouter_chat`、`OpenRouterProvider`、`/api/check-key`）已自动回退到 `os.getenv("OPENROUTER_API_KEY")`。

2. **重启了端口 8000 的 FluxReel 服务器**（现 PID 61349，`nohup`/`setsid` 后台运行，日志位于 `/root/fluxreel-8000.log`）。仅限本机的 8081 实例和 frp 隧道保持不变。

3. **更新了前端**（`server.py` → FRONTEND_HTML），使界面显示：*"无需密钥——服务器已配置默认密钥。如需覆盖，请输入您自己的 OpenRouter 密钥。"*“检查”按钮现在在密钥字段为空时也能工作（它会验证默认密钥）。

## 验证结果

| 检查项 | 结果 |
| --- | --- |
| 密钥有效性（直接调用 OpenRouter） | ✅ 有效，上限 3，过期时间 2026-09-05 |
| `POST /api/check-key` **不提供密钥**（通过公共 URL） | ✅ `{"valid":true,"label":"sk-or-v1-346...613","usage":"$0.01"}` |
| 用户提供错误密钥 | ✅ 仍被拒绝（`User not found.`） |
| 前端提示已生效 | ✅ “无需密钥——服务器已配置默认密钥。” |
| 通过公共 URL 访问 `GET /health` | ✅ `{"status":"ok","jobs":0,"local_models":[]}` |

## 最终行为

- **用户不提供密钥提交**→ 服务器静默使用您的默认密钥（免费套餐，并发上限 3）。
- **用户输入自己的密钥**→ 该密钥优先（`req.openrouter_api_key 或环境变量`），因此仍可实现按用户计费。
- 公开 URL 未变：**`https://rc-8666f2536fc493ec.radeon.firstdg.ai/`**

注意：重启后清空了内存中的任务存储，因此之前完成的任务（`eee5172d`）不再列出——任务不会持久化到磁盘。