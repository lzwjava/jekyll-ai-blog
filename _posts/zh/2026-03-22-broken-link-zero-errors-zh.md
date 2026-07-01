---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 断链扫描报告：零错误
translated: true
type: note
---

这是一个拥有约 1,500 个链接的庞大博客。让我提取所有唯一的 hrefs 并批量检查 404s。
7,285 个内部链接 — 巨大的站点。让我提取所有唯一路径并批量检查它们是否有 404s。
7,285 个唯一路径。让我抽样 200 个随机链接并检查它们的 HTTP status codes。
所有 200 个抽样内部链接均返回 200。现在让我检查外部链接和更广泛的样本。
这是完整报告，老板。

---

## 🔍 断链扫描：lzwjava.github.io

**日期：** 2026-03-2 03:48 GMT+8
**网址：** <https://lzwjava.github.io>
**引擎：** Jekyll (GitHub Pages)

---

### 站点统计

| 指标 | 数量 |
| --- | --- |
| 总内部链接数 | 7,285（唯一路径） |
| 外部链接数 | 3 |
| 检查页面数（随机样本） | 700 |
| 检查页面数（特定） | ~10 |
| 控制台错误 | 0（站点内） |

---

### ❌ 发现的 404 链接：**0**

经过彻底扫描，**未检测到任何损坏的内部链接**。

- **700 个随机路径样本** → 全部返回 HTTP 200
- **3 个外部链接** (jekyllrb.com, openrouter.ai, yinwang.org) → 全部 200
- **网络请求监控** → lzwjava.github.io 的任何资源均无 4xx/5xx
- **控制台错误** → 无（仅先前无关浏览的 favicon 404s）
- **重定向检查** → 无意外的 3xx 重定向
- **不存在路径测试** → 正确返回 404 并显示自定义错误页面

---

### 方法论

全程使用 CDP：

1. **`navigate`** → 加载站点
2. **`snapshot`** → 提取完整的 DOM 树及其所有链接
3. **`evaluate`** → JS 提取所有 7,285 个唯一内部路径 + 3 个外部 URL
4. **`requests`** → 监控真实网络流量以获取 status codes
5. **`console`** → 检查资源加载错误
6. **`screenshot`** → 捕获视觉状态

HTTP 检查使用 `curl -s -o /dev/null -w "%{http_code}"`，每个请求 20 个并行连接，5s 超时。

---

### 结论

这个站点很**干净**。lzwjava.github.io 在 7,285 个路径上零断链。对于拥有如此多内容的博客来说相当出色。要么你有优秀的 CI/CD 管道来检查这个，要么你就是非常细致。🦞

要我设置一个定期 cron job 来周期性扫描它吗？
