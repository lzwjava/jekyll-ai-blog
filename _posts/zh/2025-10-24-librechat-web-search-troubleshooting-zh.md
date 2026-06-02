---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: LibreChat 网络搜索故障排除
translated: true
type: note
---

让我们仔细排查这个问题——当**在 LibreChat 中启用网络搜索功能失效**，即使已添加 **Firecrawl**、**SerpApi** 和 **Jina API** 密钥后，问题几乎总是由以下原因之一引起：配置错误、后端启用标志缺失或界面误解。

以下是清晰的排查步骤（无表格，仅说明）：

---

### 1. **检查后端配置中是否启用“网络搜索”**

打开 LibreChat 服务端配置文件（通常是 `.env` 或 `api/config.yaml`，具体取决于你的设置），确认包含如下配置：

```
# 适用于 .env
SEARCH_ENABLED=true
```

或使用 YAML 格式时：

```yaml
features:
  search: true
```

如果 `SEARCH_ENABLED` 或 `search` 未显式设置为 `true`，界面按钮可能显示但实际不会执行搜索。

---

### 2. **确认 API 密钥命名正确**

每个服务商要求特定的环境变量名称。例如：

* 对于 **SerpApi**：

  ```
  SERPAPI_API_KEY=你的密钥
  ```
* 对于 **Firecrawl**：

  ```
  FIRECRAWL_API_KEY=你的密钥
  ```
* 对于 **Jina**：

  ```
  JINA_API_KEY=你的密钥
  ```

同时确保这些变量已在运行 `backend` 进程的同一环境中导出或加载。

检查方法：

```bash
echo $SERPAPI_API_KEY
```

若返回空白，说明后端未检测到该变量。

---

### 3. **编辑密钥后重启 LibreChat**

LibreChat 不会热重载环境变量。请运行：

```bash
docker compose down
docker compose up -d
```

（若未使用 Docker，则运行 `npm run start`）。

---

### 4. **确认 LibreChat 实际使用的搜索服务商**

LibreChat 根据配置顺序选择默认的网络搜索后端。

如需指定 SerpApi，必须设置：

```
SEARCH_PROVIDER=serpapi
```

同理，如需使用 Jina：

```
SEARCH_PROVIDER=jina
```

如果仅设置密钥但未定义使用哪个服务商，LibreChat 可能默认不启用任何服务商。

---

### 5. **查看后端日志**

运行：

```bash
docker logs librechat-backend
```

或

```bash
npm run start:debug
```

查找类似信息：

```
[Search] SerpApi 密钥缺失或无效
```

或

```
搜索服务商未配置
```

这些是最直接的线索。

---

### 6. **直接测试 API**

确保你的密钥实际有效：

**SerpApi 测试：**

```bash
curl "https://serpapi.com/search.json?q=chatgpt&api_key=你的密钥"
```

**Firecrawl 测试：**

```bash
curl "https://api.firecrawl.dev/v1/search?q=chatgpt" -H "Authorization: Bearer 你的密钥"
```

**Jina 测试：**

```bash
curl "https://r.jina.ai/chatgpt" -H "Authorization: Bearer 你的密钥"
```

如果这些请求失败，说明密钥本身无效或受到速率限制。

---

### 7. **前端版本不匹配**

如果最近升级了 LibreChat（特别是从 v0.7 之前版本升级到 v0.8+），前端 `网络搜索` 切换开关可能显示，但你的后端版本尚未支持集成的 Firecrawl/Jina 搜索模块。
运行：

```bash
git pull
```

并重新构建：

```bash
docker compose build --no-cache
docker compose up -d
```

---

### 8. **最终检查——通过网页界面确认**

打开界面，进入 **设置 → 功能**，确认：

* “网络搜索”切换开关处于开启状态
* 你选择的服务商已列出（SerpApi、Firecrawl 或 Jina）

如果显示 *“无可用服务商”*，说明后端未读取到你的密钥。

---

如果需要，你可以粘贴相关的 `.env` 片段（密钥部分打码），我会精准指出哪一行缺失或命名错误。

你愿意分享这段配置吗？
