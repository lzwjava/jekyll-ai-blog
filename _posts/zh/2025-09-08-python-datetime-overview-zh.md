---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python日期时间模块概览
translated: true
type: note
---

### Python datetime 模块概述

Python 的 `datetime` 模块提供了处理日期、时间和时间戳的类。它属于标准库，无需安装。主要类包括：
- `date`：处理日期（年、月、日）
- `time`：处理时间（时、分、秒、微秒）
- `datetime`：组合日期和时间
- `timedelta`：表示时间间隔（例如用于日期运算）

该模块适用于记录时间戳、计算持续时间或格式化日期显示/输出等任务。

### 模块导入

根据需要导入整个模块或特定类：

```python
import datetime  # 完整模块

# 或导入特定类
from datetime import datetime, date, time, timedelta
```

### 获取当前日期和时间

使用 `datetime.now()` 获取当前本地日期和时间作为 `datetime` 对象。

```python
import datetime

now = datetime.datetime.now()
print(now)  # 输出示例：2023-10-05 14:30:45.123456
print(type(now))  # <class 'datetime.datetime'>
```

对于 UTC 时间，可使用 `datetime.utcnow()`（但更推荐使用带时区感知的 `datetime.now(timezone.utc)`，需从 `datetime.timezone` 导入）。

### 创建日期和时间对象

通过构造函数手动创建对象。

```python
# 日期：年、月、日
d = datetime.date(2023, 10, 5)
print(d)  # 2023-10-05

# 时间：时、分、秒、微秒（可选）
t = datetime.time(14, 30, 45)
print(t)  # 14:30:45

# 日期时间：组合日期和时间
dt = datetime.datetime(2023, 10, 5, 14, 30, 45)
print(dt)  # 2023-10-05 14:30:45
```

可省略不需要的部分（例如 `datetime.datetime(2023, 10, 5)` 会创建午夜时分的 datetime 对象）。

### 日期格式化（strftime）

使用带格式代码的 `strftime` 将日期转换为字符串（例如 `%Y` 表示年，`%m` 表示月）。

```python
now = datetime.datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)  # 示例：2023-10-05 14:30:45

# 常用格式：
# %A：完整星期名（如 Thursday）
# %B：完整月份名（如 October）
# %Y-%m-%d：ISO 日期格式
```

### 字符串解析为日期（strptime）

使用匹配格式的 `strptime` 将字符串转换为 `datetime` 对象。

```python
date_str = "2023-10-05 14:30:45"
parsed = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(parsed)  # 2023-10-05 14:30:45
print(type(parsed))  # <class 'datetime.datetime'>
```

格式必须完全匹配，否则会引发 `ValueError`。

### 使用 timedelta 进行日期运算

使用 `timedelta` 加减时间间隔。

```python
now = datetime.datetime.now()
one_day = datetime.timedelta(days=1)
tomorrow = now + one_day
print(tomorrow)  # 当前日期 + 1天

# 减法运算
yesterday = now - one_day

# 时间单位：天、秒、微秒、毫秒、分钟、小时、周
one_week = datetime.timedelta(weeks=1)
```

计算日期差值：

```python
date1 = datetime.datetime(2023, 10, 5)
date2 = datetime.datetime(2023, 10, 10)
delta = date2 - date1
print(delta.days)  # 5
```

### 时区处理（高级用法）

对于时区感知操作，可使用 `timezone`（Python 3.3+）。该模块不原生处理时区转换，建议搭配 `pytz` 库进行健壮处理。

```python
from datetime import datetime, timezone

# 朴素 datetime（无时区信息）
naive = datetime.now()

# UTC 时区感知
utc = datetime.now(timezone.utc)

# 自定义时区（需要 tzinfo 对象）
import pytz  # 可能需要 pip install pytz
eastern = pytz.timezone("US/Eastern")
eastern_time = naive.astimezone(eastern)
```

### 常见技巧与注意事项
- **不可变对象**：`datetime` 对象不能直接修改，算术运算会创建新对象
- **月份天数**：闰年二月可使用 29 天，模块会通过 `calendar` 或 `dateutil` 处理闰年检查
- **性能优化**：避免在循环中频繁调用 `now()`，建议存储该值
- **错误处理**：注意非法日期（如 `date(2023, 2, 30)` 会引发 `ValueError`）
- **扩展库**：高级解析可考虑 `dateutil` 或 `arrow` 包

完整文档请参阅 Python 官方文档 [docs.python.org](https://docs.python.org/3/library/datetime.html)。建议在 Python 解释器中练习这些示例。
