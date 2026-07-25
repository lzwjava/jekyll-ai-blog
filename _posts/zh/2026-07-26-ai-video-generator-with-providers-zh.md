---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI视频生成器供应商
translated: true
type: note
---

已完成！以下是所创建的所有内容的摘要：

---

## 构建内容

### Provider 系统（`ahl/gen_video/providers/`）

| 文件 | 描述 |
|---|---|
| `base.py` | `ImageProvider` 抽象基类 |
| `factory.py` | `create_provider()` — 按名称创建 provider：`openrouter`、`local`、`auto` |
| `openrouter_provider.py` | 使用 OpenRouter API（`black-forest-labs/flux.2-pro`）— 保留现有行为，提取为 provider |
| `local_provider.py` | **新增** — 在本地 AMD GPU 上使用 diffusers 运行 FLUX 推理（`FLUX.1-schnell`、`FLUX.1-dev`、`FLUX.2-dev`） |

### 前端 UI（嵌入 `server.py` 中）
- 精美的深色主题单页应用
- **步骤 1**：主题输入框 → 通过 `POST /api/generate-content` 生成 AI markdown 内容
- **步骤 2**：内容预览，支持编辑/重新生成
- **步骤 3**：Provider 选择器，包含 3 个选项：
  - ☁️ **OpenRouter** — `black-forest-labs/flux.2-pro`
  - 🖥️ **本地 GPU** — 在 AMD GPU 上运行 FLUX（提供变体选择器：schnell/dev/2-dev）
  - ⚡ **自动** — 优先尝试本地，失败后回退到 OpenRouter
- 实时任务轮询，带有日志
- 视频预览 + 下载
- 最近任务列表，支持快速下载

### API 端点

| 端点 | 描述 |
|---|---|
| `GET /` | 前端 UI |
| `POST /api/generate-content` | 通过 LLM 从主题生成 markdown 内容 |
| `POST /api/generate-video` | 提交视频任务（接受 `provider`、`local_variant`） |
| `GET /api/jobs/{id}` | 任务状态 |
| `GET /api/jobs/{id}/download` | 下载完成的视频 |

### 启动服务器
```bash
ahl server
# 或在远程：
ahl gen-video server
```