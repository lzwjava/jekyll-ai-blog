---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python Datetime Module Overview
translated: false
type: note
---

### Overview of Python's datetime Module

Python's `datetime` module provides classes for manipulating dates, times, and timestamps. It's in the standard library, so no installation is needed. Key classes include:
- `date`: Handles dates (year, month, day).
- `time`: Handles times (hour, minute, second, microsecond).
- `datetime`: Combines date and time.
- `timedelta`: Represents a duration (e.g., for date arithmetic).

It's useful for tasks like logging timestamps, calculating durations, or formatting dates for display/output.

### Importing the Module

Import the entire module or specific classes as needed:

```python
import datetime  # Full module

# Or import specific classes
from datetime import datetime, date, time, timedelta
```

### Getting Current Date and Time

Use `datetime.now()` to get the current local date and time as a `datetime` object.

```python
import datetime

now = datetime.datetime.now()
print(now)  # Output: e.g., 2023-10-05 14:30:45.123456
print(type(now))  # <class 'datetime.datetime'>
```

For UTC time, use `datetime.utcnow()` (though preferably use `datetime.now(timezone.utc)` with imports from `datetime.timezone` for timezone awareness).

### Creating Date and Time Objects

Construct objects manually with their constructors.

```python
# Date: year, month, day
d = datetime.date(2023, 10, 5)
print(d)  # 2023-10-05

# Time: hour, minute, second, microsecond (optional)
t = datetime.time(14, 30, 45)
print(t)  # 14:30:45

# Datetime: combines date and time
dt = datetime.datetime(2023, 10, 5, 14, 30, 45)
print(dt)  # 2023-10-05 14:30:45
```

Omit parts that aren't needed (e.g., `datetime.datetime(2023, 10, 5)` creates a datetime at midnight).

### Formatting Dates (strftime)

Convert dates to strings using `strftime` with format codes (e.g., `%Y` for year, `%m` for month).

```python
now = datetime.datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)  # e.g., 2023-10-05 14:30:45

# Common formats:
# %A: Full weekday (e.g., Thursday)
# %B: Full month (e.g., October)
# %Y-%m-%d: ISO date
```

### Parsing Dates from Strings (strptime)

Convert strings to `datetime` objects using `strptime` with matching formats.

```python
date_str = "2023-10-05 14:30:45"
parsed = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(parsed)  # 2023-10-05 14:30:45
print(type(parsed))  # <class 'datetime.datetime'>
```

Match the format exactly, or it will raise a `ValueError`.

### Date Arithmetic with timedelta

Add or subtract time intervals using `timedelta`.

```python
now = datetime.datetime.now()
one_day = datetime.timedelta(days=1)
tomorrow = now + one_day
print(tomorrow)  # Current date + 1 day

# Subtract
yesterday = now - one_day

# Parts: days, seconds, microseconds, milliseconds, minutes, hours, weeks
one_week = datetime.timedelta(weeks=1)
```

For differences between dates:

```python
date1 = datetime.datetime(2023, 10, 5)
date2 = datetime.datetime(2023, 10, 10)
delta = date2 - date1
print(delta.days)  # 5
```

### Timezones (Advanced Usage)

For timezone-aware operations, use `timezone` (Python 3.3+). The module doesn't handle timezone conversions natively; pair with `pytz` library for robust handling.

```python
from datetime import datetime, timezone

# Naive datetime (no timezone)
naive = datetime.now()

# UTC aware
utc = datetime.now(timezone.utc)

# Custom timezone (requires tzinfo)
import pytz  # Might need pip install pytz
eastern = pytz.timezone("US/Eastern")
eastern_time = naive.astimezone(eastern)
```

### Common Tips and Pitfalls
- **Immutable objects**: `datetime` objects can't be modified directly; arithmetics create new ones.
- **Month days**: Use 29 for February in leap years; the module handles this with `calendar` or `dateutil` for leap checks.
- **Performance**: Avoid frequent `now()` calls in loops; store the value.
- **Errors**: Watch for invalid dates (e.g., `date(2023, 2, 30)` raises `ValueError`).
- **Library extensions**: For advanced parsing, consider `dateutil` or `arrow` packages.

For full documentation, check Python's official docs at [docs.python.org](https://docs.python.org/3/library/datetime.html). Practice with these examples in a Python interpreter.
