---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JSON存储的手动去重模式
translated: true
type: note
---

**问题：** 在添加记录时是否应该强制唯一性——即`add_record`中的去重逻辑是否是处理JSON存储中"唯一键"问题的正确位置？

**回答：**

是的，你在`add_record`中使用的`_record_key` + `existing_keys`集合方案正是JSON存储的正确模式。你实际上手动实现了数据库`UNIQUE`约束的功能。

但有几个需要注意的改进点：

## 当前逻辑正确但有一个脆弱点

```python
def _record_key(record_type: str, rec: dict) -> str:
    if record_type == "client_timesheet":
        return f"{rec.get('week_start', '')}_{rec.get('week_end', '')}"
    elif record_type == "vendor_punch_card":
        return rec.get("date", "")
    elif record_type == "vendor_timesheet":
        return rec.get("date", "")
    return str(sorted(rec.items()))  # ← 脆弱的回退方案
```

回退方案`str(sorted(rec.items()))`会在新增记录类型时静默失效——它会按完整内容相等性进行"去重"，这几乎从来不是你想要的。建议改为显式处理：

```python
def _record_key(record_type: str, rec: dict) -> str:
    if record_type == "client_timesheet":
        return f"{rec['week_start']}_{rec['week_end']}"
    elif record_type in ("vendor_punch_card", "vendor_timesheet"):
        return rec["date"]
    raise ValueError(f"Unknown record_type: {record_type!r}")
```

失败时抛出异常，而不是静默处理。

## 真正的唯一性漏洞：跨月份问题

你的去重只检查了同一个月桶内的数据：

```python
existing_keys = {_record_key(record_type, r) for r in all_data[month]["records"]}
```

像`2026-05-31`这样的打卡日期，如果调用者传入错误的`month`，理论上可能同时落在`202605`和`202606`两个桶中。对于打卡记录和供应商工时表，自然键是`date`本身——建议验证日期确实属于声明的月份：

```python
def _validate_month(record_type: str, rec: dict, month: str) -> bool:
    date_field = rec.get("date") or f"{rec.get('week_start', '')}"
    return date_field.startswith(f"{month[:4]}-{month[4:]}")
```

## `add_record`的返回值没有在可见的地方被使用

你返回了`(added, skipped)`，但调用方应该记录这个信息：

```python
added, skipped = add_record(data_dir, staff_id, record_type, month, records)
if skipped:
    print(f"  ↩ {skipped} 个重复记录被跳过，{added} 个已添加")
```

否则静默跳过看起来就像静默失败。

## 总结

在这个规模下，你的JSON加手动去重方案是**正确且足够的**。这个模式与SQLite的功能对应关系清晰：

| SQLite | 你的JSON方案 |
|---|---|
| `PRIMARY KEY (date)` | 返回`date`的`_record_key` |
| `INSERT OR IGNORE` | `if key in existing_keys: skip` |
| `UNIQUE (week_start, week_end)` | `f"{week_start}_{week_end}"` 复合键 |

无需数据库——只需加强回退方案并添加跳过记录的日志即可。
