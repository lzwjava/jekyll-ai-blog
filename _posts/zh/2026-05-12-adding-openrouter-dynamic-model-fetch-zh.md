---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加OpenRouter动态模型获取
translated: true
type: note
---

好——我已掌握所需信息。以下是分析（无代码更改）。

## 输入数据来源

`lib/clacky/web/settings.js:99-109` 渲染组合框：一个自由输入的 `<input class="model-name-input">` 加上一个按钮，点击后打开 `<div class="model-name-dropdown">`。下拉列表由 `_updateModelDropdown()`（settings.js:277-315）填充，该函数读取 `provider.models`（一个静态数组）。

`_providers` 数组在启动时从 `GET /api/providers`（settings.js:27,32）加载一次，该接口由 `api_list_providers`（lib/clacky/server/http_server.rb:2815-2832）提供，而该函数仅复制 `Providers::PRESETS[id]["models"]`（来自 `lib/clacky/providers.rb`）。

## 已经完成一半的工作

`providers.rb:78-98` 定义了 OpenRouter 预设，内容如下：
```ruby
"base_url" => "https://openrouter.ai/api/v1",
"models" => [],  # 动态 - 从 API 获取
```
因此代码库原本就打算让 OpenRouter 的模型来自其 API，但获取逻辑从未实际接入。这正是你注意到的差距。

## 如何填补

OpenRouter 暴露了 `GET https://openrouter.ai/api/v1/models`（无需认证），返回 `{ data: [ { id, name, context_length, pricing, ... }, ... ] }`。你需要将每个 `id`（例如 `moonshotai/kimi-k2.6`）作为下拉选项。

两种可行的方案：

**A. 后端获取 + 缓存（推荐）**
在 `api_list_providers`（http_server.rb:2817）内部，遍历预设时，针对 `openrouter` 的 id，使用现有的 HTTP 客户端调用 `https://openrouter.ai/api/v1/models`，将 `data[].id` 映射到 `models`，并缓存结果（例如在实例变量或磁盘上设置 1 小时 TTL），这样每次打开设置时无需重新获取。网络故障时回退到 `[]`，此时 UI 降级为纯文本输入框——与当前行为一致。
- 优点：浏览器端无需额外 CORS 处理，单一缓存位置，无密钥泄露风险，复用现有 HTTP 基础设施。
- 缺点：后端在首次请求时需要执行一次出站调用。

**B. 前端在下拉列表打开时获取**
在 `_updateModelDropdown()`（settings.js:277）中，当匹配的提供者为 OpenRouter 并且 `provider.models` 为空时，直接从浏览器 `fetch("https://openrouter.ai/api/v1/models")`，映射 `data[].id` 并渲染。将结果缓存到 `_providers[i].models` 上，以便后续打开时即时响应。
- 优点：改动最小，无需修改 Ruby 代码。
- 缺点：依赖于 OpenRouter 的 CORS 头部是否宽松（目前是宽松的，但不受你控制）；同时意味着每个用户的浏览器都会直接访问 OpenRouter，即使没有 API 密钥。

我会选择**方案 A**，因为文件注释已经暗示了这一点（“动态 - 从 API 获取”），并且它使前端逻辑保持一致（无论来源如何，`provider.models` 只是一个列表）。

## 实现前值得决定的两项额外事项

1. **数量**：OpenRouter 列出了约 300+ 个模型。当前下拉列表的 CSS（`app.css`，`.model-name-dropdown`）没有滚动或筛选功能——很可能需要在列表顶部添加文本筛选，或者按供应商前缀排序/分组（`anthropic/*`、`moonshotai/*` 等）。否则列表将无法使用。
2. **“动态”的范围**：在 `providers.rb` 中，只有 OpenRouter 具有此属性。其他提供商（如 Kimi、MiniMax、GLM）保留精心设计的静态列表是有原因的——预设充当了已知良好的快捷列表。不要在没有仔细考虑的情况下将获取逻辑泛化到“所有 models 为空的提供商”。

来源：
- [OpenRouter 模型端点](https://openrouter.ai/docs/api-reference/list-available-models)
