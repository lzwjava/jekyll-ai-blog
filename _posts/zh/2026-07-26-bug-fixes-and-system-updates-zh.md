---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 错误修复和系统更新
translated: true
type: note
---

已修复！以下是发现的问题及修复内容：

### 发现并修复的问题

**1. `_generate_scenes` 未传递 `api_key`** — 场景生成（通过LLM调用创建标题/字幕/提示词）在调用 `_openrouter_chat` 时未传入 API 密钥，因此始终回退到环境变量。已在整条调用链中添加了 `api_key` 参数。

**2. 视频生成缺少默认 LLM 模型** — `generate_video_from_content` 在 `model=None` 时没有后备模型。已添加默认值 `openrouter/auto-beta`（与内容生成端点相同）。

**3. `LocalGPUProvider` 中的导入竞态条件** — 多个并行线程同时尝试 `import diffusers`。由于部分导入的竞态条件，前几个线程会报 `AttributeError: module 'diffusers' has no attribute 'FluxPipeline'`。已通过在启动线程池之前，在单线程上预加载模型来修复。

**4. 远程环境缺少 `ffmpeg`** — 视频合成需要 `ffmpeg`。已安装。

### 使用方法

```bash
# 打开前端
open https://rc-26cc80c1b835b7a3.radeon.firstdg.ai

# 在 🔑 字段中粘贴你的 OpenRouter API 密钥，点击 Check
# 选择 🖥️ 本地 GPU（FLUX.1-schnell 已预选）
# 输入一个主题，点击 Generate ✨，审核内容，然后点击 Generate Video 🎬
```