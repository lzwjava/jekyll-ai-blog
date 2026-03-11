---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 企业网络搜索变通方案
translated: true
type: note
---

问题：在银行企业环境中，无法使用外部 API（如 Tavily），但允许使用浏览器（Google/Edge/Chrome），并且 Python requests 可以通过企业代理访问互联网，如何实现简单的网络搜索系统？

回答：

在许多**银行或高度监管的企业环境**中，由于**安全、合规和数据泄露风险**，通常会阻止直接使用外部搜索 API（如 Tavily、SerpAPI 或其他 AI 搜索工具）。然而，这些环境通常仍允许：

* 通过**企业代理**进行正常网页浏览
* 访问 Google 或 Bing 等搜索引擎
* 通过批准的代理服务器进行程序化 HTTP 请求

因此，可以使用**三种实用方法**来实现简单的网络搜索系统。

---

## 1. 浏览器自动化（最类似于 Copilot 行为）

这种方法使用**由代码控制的真实浏览器**来执行搜索，就像人类用户一样。

### 架构

```
用户查询
    ↓
Python 服务
    ↓
Playwright / Selenium
    ↓
企业代理
    ↓
Google / Bing
    ↓
解析结果页面
    ↓
返回标题 + 链接 + 片段
```

### 为什么在企业环境中有效

* 使用**正常浏览器流量**
* 看起来与员工浏览相同
* 即使许多 API 被阻止也能工作

### 使用 Playwright（Python）的示例

```python
from playwright.sync_api import sync_playwright

def search_google(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"https://www.google.com/search?q={query}")

        results = page.query_selector_all("h3")

        output = []
        for r in results[:5]:
            output.append(r.inner_text())

        browser.close()
        return output

print(search_google("latest fed interest rate"))
```

### 优点

* 支持企业代理
* 搜索引擎更难阻止
* 非常可靠

### 缺点

* 需要安装浏览器自动化工具
* 比 API 调用稍慢

---

# 2. 直接 HTTP 搜索（轻量级 Python Requests）

如果代理允许 HTTP 请求，您可以**直接查询搜索引擎 HTML**并解析结果。

### 架构

```
查询
 ↓
Python requests
 ↓
企业代理
 ↓
搜索引擎 HTML
 ↓
HTML 解析器 (BeautifulSoup)
 ↓
结果
```

### 示例

```python
import requests
from bs4 import BeautifulSoup

proxy = {
    "http": "http://proxy.company.com:8080",
    "https": "http://proxy.company.com:8080"
}

def search_bing(query):
    url = f"https://www.bing.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, proxies=proxy)

    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for item in soup.select("li.b_algo h2 a"):
        results.append({
            "title": item.text,
            "url": item["href"]
        })

    return results[:5]

print(search_bing("US inflation rate 2026"))
```

### 优点

* 非常简单
* 快速
* 易于与 LLM 工具集成

### 缺点

* 搜索引擎可能进行速率限制
* HTML 结构可能发生变化

---

# 3. 内部搜索代理服务（最佳企业架构）

大型公司通常会创建一个**中央内部网络搜索网关**。

不是每个工具都直接访问互联网，而是调用**内部服务**。

### 架构

```
LLM / Copilot
      ↓
内部搜索 API
      ↓
企业代理
      ↓
Google / Bing
      ↓
内容解析器
      ↓
干净的 JSON 结果
```

示例 API 响应：

```json
{
  "query": "Fed interest rate",
  "results": [
    {
      "title": "Federal Reserve Interest Rate Decision",
      "url": "https://www.federalreserve.gov",
      "snippet": "The Federal Reserve maintained..."
    }
  ]
}
```

### 好处

* 安全团队可以审计请求
* 防止数据泄露
* 缓存结果
* 可以过滤被禁网站

这**非常类似于企业 Copilot 工具的工作方式**。

---

# 4. 与 LLM 检索管道结合

获取搜索结果后，系统可以获取内容。

管道示例：

```
用户问题
   ↓
搜索引擎查询
   ↓
前 5 个 URL
   ↓
获取 HTML
   ↓
提取文本
   ↓
分块内容
   ↓
发送到 LLM
   ↓
最终答案
```

用于获取文章文本的 Python 示例：

```python
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    paragraphs = soup.find_all("p")

    text = "\n".join(p.text for p in paragraphs)

    return text[:5000]
```

---

# 5. 为什么 Microsoft Copilot 在企业环境中有效

企业 Copilot 系统通常使用：

1. **Bing 内部 API**
2. **企业代理路由**
3. **内容过滤**
4. **企业安全层**

因此，架构大致为：

```
Copilot
  ↓
Microsoft Bing API
  ↓
安全搜索过滤器
  ↓
企业安全网关
  ↓
互联网
```

您的内部系统可以使用以下方式复制**80% 的此功能**：

* 搜索抓取
* 代理使用
* 内容提取
* LLM 摘要

---

# 6. 最佳最小企业设置

对于**银行环境**，简单的架构将是：

```
Python 搜索服务
    │
    ├── requests + proxy
    │
    ├── Bing/Google HTML 解析
    │
    ├── 获取前 3 个页面
    │
    └── 返回文本到 LLM
```

技术栈：

* Python
* requests
* BeautifulSoup
* 企业代理
* 可选 Playwright

这可以用**约 200 行代码**构建。

---

# 7. 关键企业考虑因素

### 安全

* 防止敏感数据查询日志记录
* 清理用户输入

### 合规

* 白名单域
* 阻止风险站点

### 性能

* 缓存搜索结果
* 限制页面获取大小

### 稳定性

* 使用多个搜索引擎 (Bing + DuckDuckGo)

---

# 8. 简单企业搜索管道示例

```
用户问题
     ↓
搜索引擎查询
     ↓
前 5 个结果
     ↓
下载页面
     ↓
提取文本
     ↓
LLM 摘要
     ↓
答案 + 引用
```

这本质上**就是现代 AI 搜索代理的工作方式**。

---

如果有帮助，我还可以展示：

* **完整的 150 行 Python 企业搜索代理**
* **如何构建类似于 Copilot 的网络搜索工具**
* **OpenAI / Perplexity 风格搜索管道的内部工作原理**

参考资料：

* [https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)
* [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/)
* [https://requests.readthedocs.io/en/latest/](https://requests.readthedocs.io/en/latest/)
* [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)