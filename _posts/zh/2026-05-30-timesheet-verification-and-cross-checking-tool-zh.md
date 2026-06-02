---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工时表验证与交叉核对工具
translated: true
type: note
---

完成。以下是构建的内容：

```
tt/
├── __init__.py
├── cli.py          # CLI: tt verify [-i DIR] [-m MODEL] [-t THRESHOLD]
├── models.py       # Pydantic: ClientWeek, VendorPunchDay, VerificationResult 等
├── extractor.py    # 通过 OpenRouter 使用视觉 LLM 进行提取（客户考勤表、打卡卡、供应商考勤表）
├── verify.py       # 交叉核对逻辑 + 每周/每月阈值验证
└── openrouter.py   # OpenRouter API 客户端（你的代码，添加了 call_openrouter_vision）
```

用法：

```bash
uv run tt verify                           # 使用默认设置运行
uv run tt verify -i input -m google/gemini-2.5-flash -t 0.60
```

`tt verify` 的功能：
1. 读取 `input/client/`、`input/vendor/punch/`、`input/vendor/timesheet/` 中的所有图片
2. 将每张图片发送给 OpenRouter 上的视觉 LLM，以提取结构化 JSON
3. 交叉核对：标记客户记录了工时但供应商显示打卡缺失的日期（反之亦然）
4. 计算每周项目比率（必须 ≥ 60%）和每月总计比率（必须 ≥ 60%）
5. 打印表格并以 0（满足要求）或 1（不满足要求）退出

在 `.env` 或环境变量中设置 `OPENROUTER_API_KEY` 以运行。默认模型是 `google/gemini-2.5-flash`。
