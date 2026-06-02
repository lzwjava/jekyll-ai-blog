---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 学位实践考试爬虫与AI分类器
translated: true
type: note
---

该命令已实现端到端运行。以下是新增内容以及对真实网站执行 `ww degree practical --pages 2` 的实际结果：

**新增内容：**
- `ww/degree/degree.py` — 爬虫 + AI 分析器
- 在 `ww/main.py` 中注册了 `degree` 命令，并附有帮助文本

**使用方法：**
- `ww degree` — AI 分类概览（最新页面，约 20 条记录）
- `ww degree practical` — 筛选实践考核/成绩相关文章
- `ww degree list` — 原始抓取列表，无 AI 处理
- `--pages N` — 最多抓取 11 页（共 203 条记录）
- `--model <name>` — 覆盖 OpenRouter 模型

**你应关注的实践考核文章（来自 `ww degree practical --pages 2`）：**

- [2026-04-20] [关于查询2026年4月25-26日自考实践考核考场座位号的通知](https://jxjy.gdufs.edu.cn/info/1178/19297.htm) — 2026年4月实践考核考场座位查询。
- [2025-12-19] [广东外语外贸大学2026年上半年实践考核报考通知-面向社会考生](https://jxjy.gdufs.edu.cn/info/1178/18914.htm) — 2026年上半年实践考核报考通知。
- [2025-12-10] [关于推迟2026年上半年实践考核报考时间的通知](https://jxjy.gdufs.edu.cn/info/1178/18899.htm) — 2026年上半年报考时间推迟。
- [2025-12-02] [关于发布自学考试实践考核课程考试大纲的通知](https://jxjy.gdufs.edu.cn/info/1178/18890.htm) — 实践考核课程考试大纲。
- [2025-11-21] [关于公布2025年11月自学考试实践考核成绩的通知](https://jxjy.gdufs.edu.cn/info/1178/18879.htm) — 2025年11月实践考核成绩发布。
- [2025-10-24] [关于查询2025年11月1-2日自考实践考核考场座位号的通知](https://jxjy.gdufs.edu.cn/info/1178/18846.htm) — 2025年11月考场座位查询。
- [2025-05-19] [关于公布2025年4月自学考试实践考核成绩的通知](https://jxjy.gdufs.edu.cn/info/1178/18678.htm) — 2025年4月实践考核成绩。
- [2025-04-08] [关于公布2025年4月19-20日自考实践考核考场座位号的通知](https://jxjy.gdufs.edu.cn/info/1178/18617.htm) — 2025年4月考场座位号。

重复出现的类别为：**报考**、**座位号**、**成绩**和**大纲**——AI 正是依据这四个关键词进行识别，因此任何包含这些关键词的新通知都会自动被筛选出来。
