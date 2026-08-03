---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中文视频生成修复
translated: true
type: note
---

已完成。✅ 以下是分析摘要及构建内容：

## 分析发现（为何视频文字显示为英文）

| # | 问题 | 详情 |
|---|---|---|
| 1 | **提示词偏差** | 场景生成使用了英文示例 + *字数*限制（"2-6 词"）——对中文无效，导致 LLM 即便处理中文文章也默认输出英文标题/字幕 |
| 2 | **无中文字体** | 候选字体 DejaVu/Liberation/Arial 不支持中文 —— 经 `fc-match` 验证：**只有** NotoSansCJK 包含"是/军"。中文将显示为 □□□ 方块 |
| 3 | **基于空格的换行** | `text.split()` 无法处理中文（无空格）→ 形成不可断行的长行 → 字体缩至无法阅读的大小 |

## 构建内容 —— 语言选择器（自动 / English / 中文）

**前端**（`server.py`）：在步骤 1 主题输入框旁新增**语言**下拉菜单；随 `/api/generate-content` 和 `/api/generate-video` 一起发送。

**后端**（`server.py` + `video.py`）：
- 两个请求模型均添加 `language` 字段 → 经 `_run_generation` → `generate_video_from_content` → `_generate_scenes` 传递
- **内容提示词**：以所选语言撰写文章（Auto = 与主题语言一致）
- **场景提示词**：语言感知 —— 中文使用字符数（"title: 2-8 个汉字, subtitle: 10-25 个汉字"）而非单词数；`image_prompt` 保留英文以确保 Flux 最佳画质

**渲染**（`video.py` `_create_slide_frame`）：
- **CJK 字体检测**：若标题/字幕含 CJK 字符，加载 **Noto Sans CJK SC**（标题使用 Black 字重，字幕使用 Regular 字重）并回退至 WenQuanYi —— 这些字体也覆盖拉丁字符，因此混合文本如"GPU是什么？"可完美渲染
- **基于字符的换行**（CJK）+ 对任何语言的超长 token 进行硬断行
- 现有自动缩小循环现通过同一候选字体列表重新加载字体（保留正确的 `.ttc` 字体索引）

**验证结果**：中文幻灯片（"GPU是什么？"、"并行计算之王"、长标题及长字幕）均正常显示，文字完整置于条幅内。

**提交并推送**：`f1eda19` → `origin/main`。服务器运行于 `http://localhost:8000` — 尝试选择**中文**主题+**中文**语言，视频标题和字幕将显示为中文。