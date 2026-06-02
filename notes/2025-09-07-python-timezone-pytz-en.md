---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python Timezone Handling with pytz
translated: false
type: note
---

### Installing pytz
pytz is a third-party Python library for handling timezone-aware datetime objects. Note that as of Python 3.9+, the built-in `zoneinfo` module is preferred for new code (it's in the standard library and handles updates automatically), but pytz remains widely used.

To install pytz, use pip:
```
pip install pytz
```

### Basic Usage with pytz
pytz works with Python's `datetime` module. Key concepts:
- **Timezone objects**: Use `pytz.timezone()` to create timezone-aware objects (e.g., for "UTC" or "America/New_York").
- **Localization**: Attach a timezone to a naive `datetime` object using `.localize()`.
- **Conversion**: Use `.astimezone()` to convert between timezones.
- **Pitfalls**: Avoid using `pytz` constructors directly on `datetime` objects; always localize first to handle daylight saving time (DST) correctly.

Import required modules:
```python
import datetime
import pytz
```

### Examples

#### 1. Get Current Time in a Specific Timezone
Use `pytz.utc` or specific timezones. Always work with UTC internally for best practices.

```python
# Get current UTC time
utc_now = datetime.datetime.now(pytz.utc)
print(utc_now)  # e.g., 2023-10-15 14:30:00+00:00

# Get current time in US Eastern time
eastern = pytz.timezone('US/Eastern')
eastern_now = datetime.datetime.now(eastern)
print(eastern_now)  # e.g., 2023-10-15 10:30:00-04:00 (adjusts for DST)
```

#### 2. Localizing a Naive Datetime
Convert a naive (timezone-unaware) datetime to a timezone-aware one.

```python
# Create a naive datetime (e.g., October 15, 2023, 12:00)
naive_dt = datetime.datetime(2023, 10, 15, 12, 0)
print(naive_dt)  # 2023-10-15 12:00:00

# Localize to US Eastern time
eastern = pytz.timezone('US/Eastern')
aware_dt = eastern.localize(naive_dt)
print(aware_dt)  # 2023-10-15 12:00:00-04:00
```

#### 3. Converting Between Timezones
First localize a datetime, then convert.

```python
# Start with UTC time
utc_dt = pytz.utc.localize(datetime.datetime(2023, 10, 15, 14, 0))
print(utc_dt)  # 2023-10-15 14:00:00+00:00

# Convert to Pacific time
pacific = pytz.timezone('US/Pacific')
pacific_dt = utc_dt.astimezone(pacific)
print(pacific_dt)  # 2023-10-15 07:00:00-07:00
```

#### 4. Handling Lists of Timezones
pytz supports common timezone names from the Olson database.

```python
# List available timezones
print(pytz.all_timezones[:10])  # Sample: ['Africa/Abidjan', 'Africa/Accra', ...]

# Or country-specific
print(pytz.country_timezones['US'])  # ['America/New_York', 'America/Los_Angeles', ...]
```

### Migration to zoneinfo (Recommended for Python 3.9+)
For newer Python versions, use the built-in `zoneinfo` instead of pytz for simplicity:
```python
from zoneinfo import ZoneInfo
import datetime

# Equivalent to pytz examples
eastern_now = datetime.datetime.now(ZoneInfo('US/Eastern'))
aware_dt = datetime.datetime(2023, 10, 15, 12, 0).replace(tzinfo=ZoneInfo('US/Eastern'))
```

### Common Issues and Tips
- **Ambiguous times**: During DST transitions, use `is_dst` in `.localize()` (e.g., `eastern.localize(naive_dt, is_dst=False)`).
- **UTC normalization**: Convert to UTC before arithmetic to avoid errors.
- **Update pytz**: It uses IANA tzdata; keep it updated via pip.
- For more, check the [pytz documentation](https://pythonhosted.org/pytz/). If you encounter errors, paste code snippets for debugging help.
