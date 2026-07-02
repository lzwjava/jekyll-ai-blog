---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计划重复笔记修复
translated: true
type: note
---

工作流按计划运行（每2小时一次），而非推送触发——因此下一次运行将自动应用修复。完整说明如下：

---

## 根因

`test_no_duplicate_notes` 检测到 **重复的笔记对** ：

| 文件 | 路径 | 行数 |
|------|------|------|
| `2025-10-06-finacle-vs-avaloq-1-en.md` | notes/ + _posts/en/ +_posts/zh/ | 66 |
| `2025-10-06-finacle-vs-avaloq-en.md` | notes/ + _posts/en/ +_posts/zh/ | 45 |

相同日期（`2025-10-06`）、相同标题 *"Finacle vs Avaloq Banking Platforms"* 、相同内容。`-1` 变体是基于表格原版的散文格式重新生成版本。相似性检查（前200字符匹配度90%以上）将其标记为重复。

## 已应用的修复

已移除所有3个带 `-1` 后缀的重复文件：

- `notes/2025-10-06-finacle-vs-avaloq-1-en.md`
- `_posts/en/2025-10-06-finacle-vs-avaloq-1-en.md`
- `_posts/zh/2025-10-06-finacle-vs-avaloq-1-zh.md`

## 验证

- `test_no_duplicate_notes` 本地通过：`✓ 在10953个文件中未发现重复`
- Pre-commit 钩子通过：`Duplicate notes check....Passed`
- 已推送到 `main` 分支（提交 `0f12685ab`）
- 工作流按计划运行（`0 */2 * * *`），因此下一次部署（约2小时后）将应用修复

第二次失败（运行编号28501676010）根因相同——同样因该重复对而失败。