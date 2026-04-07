---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双子座网络搜索应用程序接口修复
translated: true
type: note
---

## 会话摘要

### 目标
修复 OpenClaw 中因缺少 `GEMINI_API_KEY` 而失效的 `web_search` 工具。

---

### 发现的问题

- OpenClaw 配置文件位于 `~/.openclaw/openclaw.json`
- Web 搜索配置为 `provider: "gemini"`，但在搜索部分**没有 API 密钥**
- 在 `models.providers.google` 下已存在一个 Google API 密钥

---

### 执行的操作

1. **创建备份** — `~/.openclaw/openclaw.json.bak.20260408_041208`

2. **初步编辑** — 向 `tools.web.search` 添加了 `apiKey`：
   ```json
   "search": { "enabled": true, "provider": "gemini", "apiKey": "***" }
   ```

3. **检测到配置结构错误** — 重启时，openclaw 拒绝了配置：
   > `tools.web.search provider-owned config moved to plugins.entries.<plugin>.config.webSearch`

4. **通过 `openclaw doctor --fix` 自动迁移** — 此操作：
   - 将 API 密钥移至正确位置：`plugins.entries.brave.config.webSearch.apiKey`
   - 启用了 `brave` 插件（该插件负责处理 Gemini web 搜索）
   - 归档了 24 个孤立的会话记录文件
   - 更新了结构字段（`cacheRead`、`cacheWrite` 成本字段，模型上的 `api` 字段）
   - 自动重启了 systemd 服务
   - 在 `~/.openclaw/openclaw.json.bak` 保存了新备份

5. **确认网关正在运行** — 通过 systemd 确认 PID 为 402575

---

### 最终配置状态（相关部分）

```json
"plugins": {
  "entries": {
    "brave": {
      "enabled": true,
      "config": {
        "webSearch": {
          "apiKey": "***"
        }
      }
    }
  }
}
```

---

### Doctor 指出的警告（非阻塞性）
- Telegram、Signal 和 Slack 的 `groupPolicy` 设置为 `"allowlist"`，但 `groupAllowFrom` 为空 — 除非添加群组 ID 或将策略更改为 `"open"`，否则群组消息将被静默丢弃。