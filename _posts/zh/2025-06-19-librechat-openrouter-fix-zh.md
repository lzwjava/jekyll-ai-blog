---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 修复LibreChat OpenRouter模型错误
translated: true
type: note
---

此错误发生在使用 **LibreChat** 搭配 **OpenRouter** 作为后端时，所选模型（`gpt-5-chat` 或类似模型）不可用或未正确路由。以下是问题解析及解决方案：

---

## **错误原因**
- **OpenRouter** 作为各类 AI 模型的代理服务，但并非所有模型都默认可用或已启用。
- 错误提示 `404 未找到支持工具使用的端点` 意味着您选择的模型（`gpt-5-chat`）存在以下情况之一：
  - 未被 OpenRouter 支持
  - 未在 LibreChat 配置中设置
  - 需要其他服务提供商或 API 密钥

---

## **解决方案**

### 1. **检查 OpenRouter 可用模型**
- 访问 [OpenRouter 模型列表](https://openrouter.ai/models) 查看可用模型
- 截至目前，`gpt-5-chat` 并非 OpenAI 官方模型（最新版为 GPT-4o）。若需使用 GPT-4，请选择 `openai/gpt-4` 或类似模型

### 2. **更新 LibreChat 配置**
- 在 LibreChat 中进入 **设置** > **模型选择**
- 选择 **受 OpenRouter 支持** 的模型（如 `openai/gpt-4`、`mistralai/mistral-7b` 等）
- 若需直接使用 OpenAI 服务，请将 **API 服务商** 切换为 **OpenAI** 而非 OpenRouter

### 3. **验证 API 密钥**
- 确保您拥有有效的 **OpenRouter API 密钥**（使用 OpenRouter 时）或 **OpenAI API 密钥**（使用 OpenAI 时）
- 在 LibreChat 的 **设置** > **API 密钥** 中添加密钥

### 4. **重启 LibreChat**
- 修改设置后重启 LibreChat 使配置生效

### 5. **查阅 LibreChat 文档**
- 参考 [LibreChat 的 OpenRouter 配置指南](https://github.com/danny-avila/LibreChat#openrouter) 获取详细说明

---

## **替代方案**
- 若需使用 OpenAI 模型，请将服务商设置为 **OpenAI** 并选择 `gpt-4`、`gpt-4o` 或 `gpt-3.5-turbo`
- 若需使用 OpenRouter，请从其 [支持模型列表](https://openrouter.ai/models) 中选择合适模型

---
