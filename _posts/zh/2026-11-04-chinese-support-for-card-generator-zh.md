---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 卡片生成器的中文支持
translated: true
type: note
---

完成 ✓ 中文支持已提交（`fc1d92c`），两张名片已重新生成并在预览中打开。

## 用法 / Usage

```bash
ww card --lang zh    # 中文名片 → card_output/business_card_zh.png
ww card --lang en    # English card → card_output/business_card_en.png
ww card              # 默认为 en
```

## 变更内容

**`ww/card/card.py`**
- `--lang en|zh` 标志（已验证；默认 `en`）
- **中文内容** — 来自你的中文 CV PDF：姓名 **李智维**，角色 **AI 工程师**，地点 **中国广州**
- 中文标签：`关于我` / `联系我`，联系标签 博客/领英/AI 作品集/软件作品集
- 中文精选简介（6 行，约 150 字，来自简历概述）
- **CJK 字体**（macOS）：STHeiti Medium（粗体）+ Hiragino Sans GB（正文），Linux 回退使用 Noto Sans CJK
- **CJK 逐字换行**（`_wrap_cjk`）— 可在任意位置换行，优先在空格/标点后换行，更宽的行高（58px）
- `--llm` 也会通过 OpenRouter 用中文生成简介（≤150 字）；失败时回退到精选简介
- 输出文件带语言后缀：`business_card_{en,zh}.png`（两者可共存）

**`ww/main.py` + `~/.zsh/completions/_ww`** — 帮助文本和 Tab 补全已更新，新增 `--lang en|zh`。

已验证：李智维 bbox (0,3,216,70) = 3 个真实的 72px 字形（无 tofu），CJK 字形在 38px 字号下宽 38px，ZH_INTRO 自动换行为 6 行。中文名片现在同时显示中英文预览 — 请查看，并告诉我是否需要调整中文简介措辞或角色。