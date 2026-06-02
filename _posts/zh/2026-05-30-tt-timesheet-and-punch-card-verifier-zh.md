---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 时间表与打卡记录验证器
translated: true
type: note
---

## 摘要

**项目：** `tt` — 用于承包商出勤合规性的考勤表与打卡记录验证工具。

**工作流程：**
1. 用户注册（`tt register <id> <name>`）并登录（`tt login <id>`）
2. 通过 REPL（`uv run tt` 不带参数）运行 `/add_records`，该命令：
   - 截取考勤表或打卡记录的屏幕截图
   - 将其发送至 OpenRouter 视觉大模型（gemini-2.5-flash）进行结构化提取
   - 将提取的数据保存至 `data/<staff_id>/<record_type>.json`
   - 将图片复制到 `images/` 目录，并用时间戳重命名
3. `tt verify` 交叉核对客户考勤表与供应商打卡记录
4. 针对 60% 项目时间阈值，按周/月报告通过/未通过情况

**当前数据：**
- 1 个注册用户：`45294575`（james.z.w.li）
- 已提取 5 周的客户考勤表记录（2026 年 5 月）
- 项目比率：80%、80%、80%、100%、100% — 全部通过

**本次会话修复的 Bug：**
1. `uv run tt` 运行失败 — `pyproject.toml` 中缺少 `[build-system]`（已添加 hatchling）
2. `tt status` 崩溃 — `.session.json` 被误当作承包商缓存（已添加隐藏文件过滤）
3. 已将 `uv.lock` 从 Git 跟踪中移除
4. GitHub 远程 URL 更新为 `lzwjava/tt`

**架构说明：**
- 存在两套缓存系统：扁平式的 `data/<name>.json`（来自 `tt verify` 的承包商验证缓存）和按用户划分的 `data/<staff_id>/<type>.json`（来自 `/add_records` 的 REPL 记录）
- REPL 具备完整的 Tab 补全、交互提示以及图片提取流水线
- 所有数据均为 Pydantic v2 模型，支持 JSON 序列化
