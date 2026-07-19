---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 环境加载顺序和403错误
translated: true
type: note
---

以下是 `ww/env/__init__.py` 中的环境变量加载顺序：

1. **`~/.config/ww/.env`** — 基本默认值（`override=False`）
2. **`$CWD/.env`** — 当前工作目录覆盖（`override=False`）  
   → 你从 `/Users/lzwjava/projects/jekyll-ai-blog` 运行，因此会检查 `jekyll-ai-blog/.env`
3. **`/Users/lzwjava/projects/ww/.env`** — 项目根目录（`override=False`）
4. **`BASE_PATH` 环境变量** — 如果设置，则加载 `$BASE_PATH/.env`（`override=True`）

所有三个 `.env` 文件都以 `override=False` 加载——这意味着如果变量**已经从之前的源设置**，后面的文件不会覆盖它。只有 `BASE_PATH` 使用 `override=True`。

因此，如果你的 `~/.config/ww/.env` 中已经设置了 `VISION_MODEL=google/gemini-2.5-flash-image`，那么在 `/Users/lzwjava/projects/ww/.env` 中修改它不会生效——先加载的优先级更高。

403 错误本身是 OpenRouter 对 `google/gemini-2.5-flash-image` 的**服务条款拒绝**——OpenRouter 上的 Google 模型要求在提供商一侧明确同意其服务条款。这本身不是 `.env` 的问题，但切换到非 Google 的视觉模型可以解决。

要解决此问题，可以：

- **检查你的 `~/.config/ww/.env`** — 如果其中设置了 `VISION_MODEL`，请在那里修改（它先加载，会阻止项目根目录的生效）
- **或者设置一个不同的视觉模型**，例如 `openai/gpt-4o-mini` 或 `anthropic/claude-3-5-sonnet-20241022`，在最先加载的 `.env` 文件中设置

需要我检查 `~/.config/ww/.env` 中的内容吗？
