---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC EDGAR API 访问
translated: true
type: note
---

让我检查一下这个页面。这是**SEC搜索文件**页面——通往**EDGAR**（电子数据收集、分析与检索系统）的门户，EDGAR是美国证券交易委员会用于公开访问公司文件的系统。

它提供的内容：

- **公司搜索** — 按公司名称、股票代码、CIK或文件编号查找文件（10-K年度报告、10-Q季度报告、8-K重大事件、S-1 IPO注册、Form 3/4/5内部交易等）
- **全文搜索** — 跨20年以上文件的关键词搜索
- **最新文件** — 文件提交时的实时信息流
- **EDGAR API** — 用于程序化访问的RESTful端点（按文件提交者查询历史记录、XBRL财务报表数据）

对于你构建优先的兴趣，API是实用的部分。它们免费，无需密钥，只需一个`User-Agent`头：

```bash
# 按CIK查询某公司的所有文件元数据（苹果 = 0000320193）
curl -s -H "User-Agent: <EMAIL>" \
  https://data.sec.gov/submissions/CIK0000320193.json | jq '.filings.recent.form[:5]'

# XBRL公司事实（结构化财务数据——收入、每股收益等）
curl -s -H "User-Agent: <EMAIL>" \
  https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json | jq '.facts.["us-gaap"].Revenues.units' | head
```

```python
import requests

H = {"User-Agent": "<EMAIL>"}  # SEC要求提供UA，否则返回403

def latest_filings(cik: int, n=10):
    cik = f"{cik:010d}"
    r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=H).json()
    recent = r["filings"]["recent"]
    return list(zip(recent["form"], recent["filingDate"], recent["accessionNumber"]))[:n]

print(latest_filings(320193))  # 苹果公司
```

速率限制为10请求/秒。XBRL的`companyfacts` / `companyconcept`端点是金矿——如果你希望将结构化基本面数据拉入数据集，这是用于LLM金融智能体或评估集的干净真实数据。

参考资料：

- [SEC搜索文件](https://www.sec.gov/search-filings)
- [EDGAR API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
