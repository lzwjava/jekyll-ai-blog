---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SECEDGAR API申报指南
translated: true
type: note
---

问题：这是什么？（指SEC EDGAR提及的内容）

回答：

你的消息中没有图片或文件——只有文本“SEC EDGAR filings (10-K, 10-Q, 8-K, etc.)”。因此我将解释该字符串所指的内容。

**EDGAR**（电子数据收集、分析与检索系统）是美国证券交易委员会（SEC）的公开系统，美国上市公司在此提交强制性披露文件。该系统免费、支持全文搜索，并提供简洁的JSON/REST API——使其成为AI/智能体管道的优质数据源。

文件类型：

- **10-K** —— 年度报告。包含经审计的财务报表、风险因素、管理层讨论与分析（MD&A）。这是最重要的文件。
- **10-Q** —— 季度报告。未经审计，内容比10-K精简。
- **8-K** —— 定期报告之间的重大事件（收购、高管变动、破产等）。按需提交。

对你而言，最有价值的部分是API。所有文件均通过CIK（中央索引键）进行标识：

```bash
# 将股票代码解析为CIK
curl -s 'https://www.sec.gov/files/company_tickers.json' \
  -H 'User-Agent: <​EMAIL>' | jq '.[] | select(.ticker=="AAPL")'

# 获取某个CIK的所有文件元数据（CIK需补零至10位）
curl -s 'https://data.sec.gov/submissions/CIK0000320193.json' \
  -H 'User-Agent: <​EMAIL>' | jq '.filings.recent.form'

# XBRL财务数据（结构化数据，无需解析HTML）
curl -s 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json' \
  -H 'User-Agent: <​EMAIL>'
```

`companyconcept`/`companyfacts` XBRL端点可直接返回结构化的财务数据（收入、每股收益等）JSON格式——完全无需处理杂乱的HTML文件解析。SEC要求`User-Agent`头中包含联系信息，否则会返回403错误。速率限制为10次/秒。

AI原生应用角度：将10-K中的MD&A和风险因素部分输入大语言模型（LLM），用于逐年对比差异；或基于全文搜索端点（`https://efts.sec.gov/LATEST/search-index?q=...`）构建检索智能体。

参考资料：

- [SEC EDGAR API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [EDGAR全文搜索](https://efts.sec.gov/LATEST/search-index)
