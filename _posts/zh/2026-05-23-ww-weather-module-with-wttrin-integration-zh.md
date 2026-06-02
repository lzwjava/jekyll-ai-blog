---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 集成wttr.in的ww天气模块
translated: true
type: note
---

一切正常。以下是新增内容：

**新文件：** `/Users/lzwjava/projects/ww/ww/weather/weather.py`

- 使用 `wttr.in`（免费，无需 API 密钥）获取天气数据
- 支持三种模式：
  - `ww weather` — 自动检测位置的完整天气报告
  - `ww weather <城市>` — 指定城市的完整报告
  - `ww weather <城市> --oneline` — 单行摘要（例如 `guangzhou: ☁️  +81°F`）
  - `ww weather <城市> --json` — 结构化 JSON 输出

**修改：** `/Users/lzwjava/projects/ww/ww/main.py`

- 在帮助文本和调度中添加了 `weather`

注意：自动检测位置基于 IP，因此当 VPN 开启时会显示代理位置（洛杉矶）。如需准确的本地天气，请显式传入 `Guangzhou`。
