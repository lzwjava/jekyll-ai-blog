---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exporting WeChat Work Attendance Data
translated: false
type: note
---

**Question:** How do I export monthly punch card attendance details (月明细) from WeChat Work? The mobile app doesn't expose an export function, and the Mac app seems limited.

**Answer:**

WeChat Work doesn't expose a direct UI export for individual users. Here are your actual options, ranked by feasibility:

### 1. **Admin export (if you have org admin access)**
If your organization admin has enabled data export, they can batch-export attendance via:
- Admin console → Work → Attendance/Punch Card → Data Export
- This exports for the whole org, but at least it's structured data

Ask your admin if this is enabled.

### 2. **API + script (most reliable for engineers)**
If your org has API access enabled:

```python
from wechatwork import WeComAPI

# Get your attendance records via API
client = WeComAPI(corpid, corpsecret)
records = client.attendance.get_monthdata(userid, year=2024, month=5)

# Dump to CSV
import csv
with open('attendance.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'checkin', 'checkout', 'status'])
    writer.writerows(records)
```

You'll need:
- `corpid` and `corpsecret` (ask your admin)
- The official [WeChat Work API docs](https://work.weixin.qq.com/api/doc/90000/90135/90269)

### 3. **Browser DevTools scraping (quick workaround)**
Open WeChat Work web (work.weixin.qq.com):
- Navigate to Attendance → Monthly Details
- Open DevTools (F12) → Network tab
- The page makes API calls to fetch data — copy the response JSON
- Paste into a Python script to convert to CSV/Excel

```python
import json
import csv

# Paste the API response JSON here
data = json.loads(clipboard_data)

with open('attendance.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'status', 'checkin_time', 'checkout_time'])
    for record in data['records']:
        writer.writerow(record)
```

### 4. **Screenshots → OCR (last resort)**
If nothing else works, take screenshots and use Tesseract OCR:
```bash
tesseract screenshot.png output.txt
# Manual cleanup to CSV
```

**My recommendation:** Try option 2 (API) if your org has it enabled — it's the most scalable. If not, option 3 (DevTools + JSON extraction) takes 10 minutes and gets clean data without screenshots.

What's your org's IT setup like? Do you know if API access is already enabled?