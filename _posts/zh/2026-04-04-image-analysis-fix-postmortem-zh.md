---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 影像分析故障事后分析
translated: true
type: note
---

**图像分析功能修复 – 完整报告**

---

## 根本原因

`image` 工具默认使用 `openai/gpt-5-mini`，但配置的 OpenAI API 密钥已过期（`999VUv4m...`），导致出现 401 错误。

---

## 修复步骤

**步骤 1：定位配置**

```bash
openclaw config get agents.defaults.imageModel
# 无输出（未设置）
cat ~/.openclaw/openclaw.json | grep image
```

发现 `imageGenerationModel` 已设置，但 `imageModel`（用于分析）缺失。

**步骤 2：尝试设置 Gemini 模型**

```bash
openclaw config set agents.defaults.imageModel.primary google/gemini-3-pro-image-preview
```

→ 失败 —— `gemini-3-pro-image-preview` 在 google provider 中不存在（模型列表为空）。

**步骤 3：使用 OpenRouter 上可用的模型**

```bash
openclaw config get agents.defaults.models
```

在 OpenRouter 上找到可用的 Gemini 模型：`openrouter/google/gemini-3-flash-preview`

**步骤 4：正确设置**

```bash
openclaw config set agents.defaults.imageModel.primary openrouter/google/gemini-3-flash-preview
```

→ ✅ 成功

**步骤 5：重启网关**

```bash
openclaw gateway restart
```

→ 发送了 SIGTERM，但网关没有自动重启。手动运行 `start` 修复。

---

## 最终配置

```json
"agents": {
  "defaults": {
    "imageModel": {
      "primary": "openrouter/google/gemini-3-flash-preview"
    },
    "imageGenerationModel": {
      "primary": "google/gemini-3-pro-image-preview"
    }
  }
}
```

- **分析（image 工具）**：`openrouter/google/gemini-3-flash-preview` ✅
- **生成（image_generate）**：`google/gemini-3-pro-image-preview` ✅（使用 Google 原生密钥）

---

## 经验总结

1. OpenRouter 模型格式为 `openrouter/provider/model-id`
2. Google provider 的模型列表为空 —— 所有模型都需要通过 OpenRouter 访问
3. 网关在 SIGTERM 后未自动重启 —— 可能是 systemd 启动超时。下次可尝试添加 `sleep` 或检查依赖项
