---
audio: false
date: 2025-09-09
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 集成DeepSeek与LibreChat指南
translated: true
type: note
---

在 **LibreChat** 中快速启用 **DeepSeek** 的方法如下。我将介绍两种方案——使用 **官方 DeepSeek API**（推荐），或通过 **OpenRouter** 接入。

---

## 方案 A — 使用 DeepSeek 官方 API（推荐）

1. **获取 DeepSeek API 密钥**
   在您的 DeepSeek 账户中创建密钥，并记录基础 URL：
   `https://api.deepseek.com`（或兼容 OpenAI 的 `https://api.deepseek.com/v1`）。（[DeepSeek API 文档][1]、[deepseek.apidog.io][2]）

2. **在 `librechat.yaml` 中添加 DeepSeek 端点**
   将以下配置置于 `endpoints:` → `custom:` 下：

```yaml
- name: deepseek
  apiKey: ${DEEPSEEK_API_KEY}
  baseURL: https://api.deepseek.com/v1
  models:
    default: deepseek-chat
    fetch: true
    list:
      - deepseek-chat        # V3（通用）
      - deepseek-coder       # 代码专用
      - deepseek-reasoner    # R1 推理
  titleConvo: true
  dropParams: null
```

LibreChat 提供了 **DeepSeek** 配置指南，确认了模型名称（`deepseek-chat`、`deepseek-coder`、`deepseek-reasoner`）并注明 R1 会流式传输其“思考过程”。（[LibreChat][3]）

3. **通过 `.env` 文件配置 API 密钥**
   在 LibreChat 的 `.env` 文件中添加：

```
DEEPSEEK_API_KEY=sk-...
```

LibreChat 支持通过 `librechat.yaml` + `.env` 配置自定义的 OpenAI 兼容提供商。（[LibreChat][4]）

4. **重启服务栈**
   在 LibreChat 目录下执行：

```bash
docker compose down
docker compose up -d --build
```

（此举是为了让 API 容器重新加载 `librechat.yaml` 和 `.env`。）如果自定义端点未显示，请检查 `api` 容器日志以排查配置错误。（[GitHub][5]）

---

## 方案 B — 通过 OpenRouter 使用 DeepSeek

若您已使用 OpenRouter，只需在 OpenRouter 端点配置块中注册 DeepSeek 模型即可。

`librechat.yaml`：

```yaml
- name: openrouter
  apiKey: ${OPENROUTER_KEY}
  baseURL: https://openrouter.ai/api/v1
  models:
    default: deepseek/deepseek-chat
    list:
      - deepseek/deepseek-chat
      - deepseek/deepseek-coder
      - deepseek/deepseek-reasoner
```

LibreChat 文档中有两点重要提示：
• 请勿设置名为 `OPENROUTER_API_KEY` 的环境变量（应使用其他名称如 `OPENROUTER_KEY`），否则会意外覆盖 OpenAI 端点。
• OpenRouter 在 LibreChat 的自定义端点列表中为一等公民。（[LibreChat][6]）

OpenRouter 通过兼容 OpenAI 的接口暴露 DeepSeek 模型。（[OpenRouter][7]）

---

## 提示与注意事项

* **R1 / `deepseek-reasoner`**：该模型可流式传输其思维链（“思考过程”）。部分 OpenAI 参数可能不适用。若输出异常，请先使用 `deepseek-chat` 测试。（[LibreChat][3]）
* **模型获取**：设置 `fetch: true` 可在支持时让 LibreChat 拉取最新模型列表；否则将使用您指定的 `list:` 列表。（[LibreChat][8]）
* **配置位置**：`librechat.yaml` 为自定义端点配置文件；`.env` 用于存储密钥和代理设置。（[LibreChat][8]）

如需帮助，可粘贴您当前的 `librechat.yaml` 内容，我将为您整洁地集成 DeepSeek 配置（绝不使用表格）。

[1]: https://api-docs.deepseek.com/?utm_source=chatgpt.com "DeepSeek API 文档：首次 API 调用"
[2]: https://deepseek.apidog.io/your-first-api-call-835227m0?utm_source=chatgpt.com "DeepSeek API：首次 API 调用"
[3]: https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/deepseek?utm_source=chatgpt.com "Deepseek"
[4]: https://www.librechat.ai/docs/quick_start/custom_endpoints?utm_source=chatgpt.com "自定义端点"
[5]: https://github.com/danny-avila/LibreChat/discussions/2487?utm_source=chatgpt.com "修复主仓库中的 librechat.yaml 文件 #2487"
[6]: https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/openrouter?utm_source=chatgpt.com "Openrouter"
[7]: https://openrouter.ai/deepseek/deepseek-v3-base%3Afree/api?utm_source=chatgpt.com "DeepSeek V3 Base – 通过 API 运行"
[8]: https://www.librechat.ai/docs/configuration/librechat_yaml?utm_source=chatgpt.com "librechat.yaml 配置文件"
