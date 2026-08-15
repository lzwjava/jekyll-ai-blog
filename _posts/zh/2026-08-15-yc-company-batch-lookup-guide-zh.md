---
audio: false
generated: true
image: false
lang: zh
layout: post
title: YC公司批次查询指南
translated: true
type: note
---

## 问题：如何了解一家 YC 公司、它属于哪一期批次，以及每个批次包含哪些公司？

## 答案

最简单的方法是使用 **YC 官方公司目录**：

[Y Combinator 公司目录](https://www.ycombinator.com/companies?utm_source=chatgpt.com)

该目录收录了 YC 投资的全部公司，包含：

* 公司名称
* YC 批次
* 创始人姓名
* 行业
* 地点
* 网站
* 状态（活跃/被收购/已上市）
  ([YC 创始人列表][1])

---

### 1. 理解 YC 批次命名规则

YC 批次采用以下格式：

```
<W/S/F/P><年份>
```

示例：

| 批次 | 含义       |
| ---- | ---------- |
| W24  | 2024 年冬季 |
| S24  | 2024 年夏季 |
| W25  | 2025 年冬季 |
| S25  | 2025 年夏季 |
| F25  | 2025 年秋季 |

历史上 YC 主要有：

```
冬季 (W)
夏季 (S)
```

后来增加了更多季度。（[Extruct AI][2]）

---

### 2. 搜索某家公司

示例：

搜索：

```
Cursor YC
```

你会得到：

```
Cursor
批次: W24
行业: 人工智能
```

或：

```
Perplexity
批次: W19
```

---

### 3. 浏览同一批次的所有公司

示例：

“显示 YC S25 批次的所有 AI 初创公司”

前往：

```
YC 目录
↓
筛选
↓
批次 = S25
↓
行业 = 人工智能
```

即可看到该批次的全部公司。

近期示例：

* W24 批次约有 248 家公司。（[Seedtable][3]）
* S25 批次约有 160 多家公司。（[Seedtable][4]）

---

### 4. 通过编程方式访问 YC 数据

如果你想像分析数据集一样分析 YC：

```bash
git clone https://github.com/yc-oss/api
```

然后：

```python
import requests

companies = requests.get(
    "https://yc-oss.github.io/api/companies/all.json"
).json()

for c in companies:
    if c["batch"] == "W24":
        print(c["name"], c["one_liner"])
```

YC 社区 API 数据集包含数千家公司及批次元数据。（[GitHub][5]）

---

### 5. 对于 AI 初创公司研究，可按如下方式筛选

一个实用的工作流程：

```
YC 目录
    |
    +-- 批次: W24/S24/W25/S25
    |
    +-- 行业:
          - 人工智能
          - 开发者工具
          - B2B SaaS
          - 机器人
    |
    +-- 状态:
          活跃
          正在招聘
```

这能帮你找到“当前的 YC 前沿”。

---

### 6. 按批次划分的著名 YC 公司

| 公司       | 批次 |
| ---------- | ---- |
| Airbnb     | W09  |
| Dropbox    | S07  |
| Stripe     | S09  |
| OpenAI     | S12  |
| Coinbase   | S12  |
| Scale AI   | W16  |

---

在研究 AI 初创公司时，我主要关注以下批次：

```
W23
S23
W24
S24
W25
S25
W26
```

因为这些批次包含了当前浪潮中的：

* AI agents
* coding agents
* AI 基础设施
* 模型工具
* 机器人技术
* 垂直 AI 公司

参考资料：

* [Y Combinator 公司目录](https://www.ycombinator.com/companies?utm_source=chatgpt.com)
* [YC 开源 API](https://github.com/yc-oss/api?utm_source=chatgpt.com)
* ([YC 创始人列表][1])

[1]: https://ycfounderlist.com/blog/how-to-find-yc-companies?utm_source=chatgpt.com "如何找到 YC 公司与创始人——完整目录指南"
[2]: https://www.extruct.ai/data-room/ycombinator-companies/?utm_source=chatgpt.com "Y Combinator 公司 - 完整情报数据库 | Extruct AI"
[3]: https://seedtable.com/investors/y-combinator/batch/w24?utm_source=chatgpt.com "Y Combinator W24 批次——公司列表 | Seedtable"
[4]: https://seedtable.com/investors/y-combinator/batch/s25?utm_source=chatgpt.com "Y Combinator S25 批次——公司列表 | Seedtable"
[5]: https://github.com/yc-oss/api?utm_source=chatgpt.com "GitHub - yc-oss/api: Y Combinator 投资公司的公开 API · GitHub"
