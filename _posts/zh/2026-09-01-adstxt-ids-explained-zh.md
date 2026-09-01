---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ads.txt 标识符解析
translated: true
type: note
---

****问题：**为什么发布商需要在 ads.txt 中添加数字/字母数字条目，以及它如何发挥作用？

**回答：**

## 什么是 ads.txt？

`ads.txt`（授权数字卖家）是 IAB 技术实验室制定的一项标准，允许发布商声明**哪些公司有权销售其广告库存**。它是一个纯文本文件，托管在您域名的根目录下（例如 `yourdomain.com/ads.txt`）。

## 这些条目代表什么？

每行的格式如下：

```
<域名>, <卖家ID>, <关系类型>, <认证ID>
```

以您的示例为例：

```
google.com, pub-6168351539440296, DIRECT, f08c47fec0942fa0
```

| 字段 | 值 | 含义 |
| --- | --- | --- |
| 域名 | `google.com` | 获授权销售的广告网络/广告交易平台 |
| 卖家ID | `pub-6168351539440296` | 您在该平台上的唯一发布商账户ID |
| 关系类型 | `DIRECT` 或 `RESELLER` | 广告库存的销售方式 |
| 认证ID | `f08c47fec0942fa0` | 用于验证卖家的可选TAG认证ID |

## DIRECT 与 RESELLER 的区别

- **DIRECT** — 您与该广告系统有直接合同（例如，您直接注册了 Google AdSense）
- **RESELLER** — 第三方获得授权，可通过该平台转售您的库存（例如，一个头部竞价合作伙伴）

## 为什么ID是字母数字/长字符的？

这些ID（如 `pub-6168351539440296` 或 `cacb0ecf-f044-478f-acd5-ce83c2d8937f`）只是每个广告网络分配的**唯一账户标识符**。它们可以是：

- 数字型（`2671`）
- 带前缀的字符串（Google的 `pub-XXXX`）
- UUID格式（Admixer的 `cacb0ecf-...`）

每个网络内部使用**自己的格式**——ID格式没有通用标准，只有行结构是统一的。

## 它如何保护生态系统？

1. **广告商/DSP** 在购买库存前会抓取您的 `ads.txt` 文件
2. 他们会**交叉核对**卖家ID是否存在于广告网络自身的 `sellers.json` 文件中
3. 如果某个ID未列出 → 该出价将被**拒绝**，以防欺诈
4. 这可以有效防止恶意行为者通过**域名欺骗**伪造优质库存

## 关于 `#nativo`、`#Illumin` 这类注释

以 `#nativo` 或 `#Illumin` 结尾的行只是供人阅读的**注释**，用于追踪是哪个合作伙伴/平台添加了该条目——它们没有任何技术作用。

---

**参考来源：**

- [IAB 技术实验室 ads.txt 规范](https://iabtechlab.com/ads-txt/)
- [Google ads.txt 指南](https://support.google.com/admanager/answer/7441288)
- [IAB sellers.json 规范](https://iabtechlab.com/sellers-json/)
