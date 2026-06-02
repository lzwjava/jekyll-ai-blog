---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 修复LibreChat OpenRouter网络搜索错误
translated: true
type: note
---

使用 LibreChat 与 OpenRouter 进行网络搜索时出现的 **"404 未找到支持工具使用的端点"** 错误是一个已知问题。以下是问题原因及解决方法：

---

## **问题原因**

- **并非所有 OpenRouter 模型都支持"工具使用"功能**（如网络搜索、函数调用等）——仅部分模型支持。如果选择了不支持工具的模型，就会出现此 404 错误。
- OpenRouter 要求用户**必须明确选择支持工具/函数调用的模型**才能使用网络搜索等功能。
- LibreChat 的配置若未正确设置，也可能覆盖端点导致路由问题。

---

## **解决方案**

### 1. **选择支持工具使用的模型**

- 访问 [OpenRouter 模型列表](https://openrouter.ai/models)，在侧边栏**勾选"tools"筛选条件**。只有支持工具使用的模型才能兼容 LibreChat 的网络搜索功能。
- 推荐模型：寻找标注支持"function calling"或"tools"的模型（例如某些版本的 GPT-4、Claude 或其他高级模型）。

### 2. **更新 LibreChat 配置**

- **请勿在配置中使用 `OPENROUTER_API_KEY`**，这可能会覆盖 OpenAI 端点引发冲突。
- 在 `librechat.yaml` 配置文件中，确保 OpenRouter 端点配置正确，且未被"忽略服务商"阻止或受"允许服务商"限制。

### 3. **解除服务商限制**

- 在 OpenRouter 设置中**取消所有"忽略服务商"的勾选**，并**清空"允许服务商"** 以确保 LibreChat 能访问所有可用端点。

### 4. **重启 LibreChat**

- 完成上述修改后，重启 LibreChat 使新设置生效。

---

## **问题依旧存在？**

- 查阅 [LibreChat 自定义端点文档](https://www.librechat.ai/docs/quick_start/custom_endpoints) 获取高级设置指导。
- 若问题仍未解决，可尝试切换至官方 OpenAI API（若已获得访问权限）或其他支持工具使用的服务商。
