---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 截图笔记跳过视觉分析
translated: true
type: note
---

以下是翻译后的中文内容：

---

**3 个文件已修改：**

**`ww/note/screenshot_log.py`**（`ww screenshot note`）

- 添加了 `--skip-analysis` 参数解析
- 启用时：完全跳过 `_vision_describe()` 和 `_summarize_with_extra_prompt()` — 创建笔记时使用简单的回退文本并嵌入截图，不调用视觉模型
- 还在 `_vision_describe()` 中对 `call_openrouter_api_with_messages()` 调用添加了 try/except 包裹，这样非视觉模型（如 `sourceful/riverflow-v2.5-pro`）不会因原始异常崩溃 — 而是打印带有 `--skip-analysis` 提示的警告

**`ww/image/interact_note.py`**（`ww screenshot interact-note`）

- 添加了 `--skip-analysis` 标志（通过 `sys.argv` 检查，因为这是交互式流程，非 argparse）
- 相同的绕过逻辑：跳过视觉模型，创建嵌入截图的笔记

**`ww/main.py`**

- 更新帮助文本，在 `ww screenshot note` 行显示 `[--skip-analysis]`

**用法：**

```bash
# 完全跳过视觉分析 — 无需任何模型
ww screenshot note --skip-analysis

# 带笔记标题提示词
ww screenshot note --skip-analysis --prompt "LLaMA.cpp 基准测试结果"

# 交互模式
ww screenshot interact-note --skip-analysis
```

你遇到的 `sourceful/riverflow-v2.5-pro` 空内容错误是因为它不是视觉模型，但被设置为了 `VISION_MODEL` — 现在使用 `--skip-analysis` 可以完全绕过视觉处理。
