---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 增强验证与详细日志记录
translated: true
type: note
---

好的。以下是 `/Users/lzwjava/projects/tt/tt/repl.py` 中修改的内容：

1. 新增了 `_validate_client_week()` — 对提取的客户时间表数据执行完整性检查：
   - 必须至少包含 1 天
   - `total_hours` 必须大于 0
   - `project_pct` 必须在 0.0–1.0 之间
   - `week_end` 不能早于 `week_start`
   - 所有日期必须落在该周的范围内
   - 提取的月份必须与用户选择的月份一致

2. 提取后，每种记录类型会打印完整的详细信息：
   - `client_timesheet`：周范围、状态、总工时/项目工时、逐日明细
   - `vendor_punch_card`：逐日状态和原始标签
   - `vendor_timesheet`：逐日上午/下午勾选标记和工时

3. 如果验证失败 → 打印“REJECTED”及原因，不会添加到记录列表
4. 如果所有图片都被拒绝 → 显示拒绝摘要并返回（不出现“保存？”提示）
5. 如果部分通过、部分拒绝 → 仅对有效的记录询问“保存？”，并注明拒绝的数量
