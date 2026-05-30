---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SQLite数据库包含八个表
translated: true
type: note
---

该项目使用 **SQLite** — 有一个专门的 `db.py` 模块。数据库位于 `data/tt.db`（而不是项目根目录下的空 `tt.db` 文件）。

以下是数据库中的 **8 个表**：

```
users                — 员工注册表（staff_id, staff_name, registered_at）
session              — 当前登录用户（单行，id=1）
client_timesheets    — 客户周工时记录（staff_id, month, week, hours）
client_timesheet_days— 每个工时的每日明细（外键 → client_timesheets）
vendor_punch_cards   — 供应商打卡记录（50+ 列用于考勤数据）
vendor_timesheets    — 供应商日工时记录（am/pm/hours）
references           — 记录类型参考（essential_keys, raw_example）
contractor_cache     — 缓存的外包人员数据（name, extracted_at, data 为 JSON blob）
images               — 上传图片注册表（filename, md5, added_at）
```

`data/tt.db` 数据库是真实的数据库。根目录下的 `tt.db` 是空的/未使用的 — 可能是早期版本遗留的过期文件。