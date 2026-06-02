---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用pytz处理Python时区
translated: true
type: note
---

### 安装 pytz

pytz 是用于处理时区感知日期时间对象的第三方 Python 库。请注意，从 Python 3.9+ 开始，建议新代码使用内置的 `zoneinfo` 模块（它属于标准库且能自动处理更新），但 pytz 仍被广泛使用。

使用 pip 安装 pytz：

```
pip install pytz
```

### pytz 基础用法

pytz 需与 Python 的 `datetime` 模块配合使用。核心概念：

- **时区对象**：使用 `pytz.timezone()` 创建时区感知对象（例如 "UTC" 或 "America/New_York"）
- **本地化**：通过 `.localize()` 为原生 `datetime` 对象附加时区信息
- **时区转换**：使用 `.astimezone()` 进行时区转换
- **注意事项**：为避免夏令时处理错误，请勿直接在 `datetime` 对象上使用 pytz 构造函数，务必先进行本地化

导入所需模块：

```python
import datetime
import pytz
```

### 应用示例

#### 1. 获取指定时区的当前时间

使用 `pytz.utc` 或特定时区。最佳实践是在内部始终使用 UTC 时间。

```python
# 获取当前 UTC 时间
utc_now = datetime.datetime.now(pytz.utc)
print(utc_now)  # 示例：2023-10-15 14:30:00+00:00

# 获取美国东部当前时间
eastern = pytz.timezone('US/Eastern')
eastern_now = datetime.datetime.now(eastern)
print(eastern_now)  # 示例：2023-10-15 10:30:00-04:00（已调整夏令时）
```

#### 2. 本地化原生日期时间

将原生（时区未感知）日期时间转换为时区感知对象。

```python
# 创建原生日期时间（例如 2023年10月15日12:00）
naive_dt = datetime.datetime(2023, 10, 15, 12, 0)
print(naive_dt)  # 2023-10-15 12:00:00

# 本地化为美国东部时间
eastern = pytz.timezone('US/Eastern')
aware_dt = eastern.localize(naive_dt)
print(aware_dt)  # 2023-10-15 12:00:00-04:00
```

#### 3. 时区转换

先本地化日期时间，再进行时区转换。

```python
# 从 UTC 时间开始
utc_dt = pytz.utc.localize(datetime.datetime(2023, 10, 15, 14, 0))
print(utc_dt)  # 2023-10-15 14:00:00+00:00

# 转换为太平洋时间
pacific = pytz.timezone('US/Pacific')
pacific_dt = utc_dt.astimezone(pacific)
print(pacific_dt)  # 2023-10-15 07:00:00-07:00
```

#### 4. 处理时区列表

pytz 支持 Olson 数据库中的常用时区名称。

```python
# 列出可用时区
print(pytz.all_timezones[:10])  # 示例：['Africa/Abidjan', 'Africa/Accra', ...]

# 或按国家筛选
print(pytz.country_timezones['US'])  # ['America/New_York', 'America/Los_Angeles', ...]
```

### 迁移至 zoneinfo（推荐 Python 3.9+ 使用）

新版 Python 建议使用内置 `zoneinfo` 替代 pytz 以简化操作：

```python
from zoneinfo import ZoneInfo
import datetime

# 等效于 pytz 示例
eastern_now = datetime.datetime.now(ZoneInfo('US/Eastern'))
aware_dt = datetime.datetime(2023, 10, 15, 12, 0).replace(tzinfo=ZoneInfo('US/Eastern'))
```

### 常见问题与技巧

- **歧义时间处理**：在夏令时转换期间，使用 `.localize()` 的 `is_dst` 参数（例如 `eastern.localize(naive_dt, is_dst=False)`）
- **UTC 标准化**：进行时间计算前先转换为 UTC 可避免错误
- **更新 pytz**：该库使用 IANA tzdata，需通过 pip 保持更新
- 更多信息请参阅 [pytz 文档](https://pythonhosted.org/pytz/)。若遇错误，可粘贴代码片段获取调试帮助。
