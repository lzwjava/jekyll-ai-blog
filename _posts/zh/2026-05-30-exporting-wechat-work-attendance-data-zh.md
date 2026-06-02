---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 导出企业微信考勤数据
translated: true
type: note
---

**问题：** 如何从企业微信导出每月打卡考勤明细（月明细）？手机应用未提供导出功能，Mac 端似乎也受限。

**回答：**

企业微信未为个人用户提供直接 UI 导出功能。以下是按可行性排序的实际方案：

### 1. **管理员导出（如果你有组织管理员权限）**

如果你的组织管理员已启用数据导出，可通过以下方式批量导出考勤数据：

- 管理后台 → 工作台 → 考勤/打卡 → 数据导出
- 导出范围为整个组织，但至少数据是结构化的

请询问你的管理员是否已开启此功能。

### 2. **API + 脚本（对工程师来说最可靠）**

如果你的组织已启用 API 访问：

```python
from wechatwork import WeComAPI

# 通过 API 获取考勤记录
client = WeComAPI(corpid, corpsecret)
records = client.attendance.get_monthdata(userid, year=2024, month=5)

# 导出为 CSV
import csv
with open('attendance.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'checkin', 'checkout', 'status'])
    writer.writerows(records)
```

你需要：

- `corpid` 和 `corpsecret`（询问你的管理员）
- 官方[企业微信 API 文档](https://work.weixin.qq.com/api/doc/90000/90135/90269)

### 3. **浏览器开发者工具抓取（快速临时方案）**

打开企业微信网页版（work.weixin.qq.com）：

- 进入 考勤 → 月明细
- 打开开发者工具（F12）→ Network 标签页
- 页面会通过 API 请求数据——复制返回的 JSON
- 粘贴到 Python 脚本中转换为 CSV/Excel

```python
import json
import csv

# 在此粘贴 API 响应的 JSON 数据
data = json.loads(clipboard_data)

with open('attendance.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'status', 'checkin_time', 'checkout_time'])
    for record in data['records']:
        writer.writerow(record)
```

### 4. **截图 → OCR（最后手段）**

如果其他方法均无效，可截屏后使用 Tesseract OCR：

```bash
tesseract screenshot.png output.txt
# 手动清理为 CSV
```

**我的建议：** 如果组织已启用 API，优先尝试方案 2（API）——它最具扩展性。若未启用，方案 3（开发者工具 + JSON 提取）只需 10 分钟即可获得干净数据，无需截图。

你的组织 IT 环境如何？是否知道 API 访问已启用？
