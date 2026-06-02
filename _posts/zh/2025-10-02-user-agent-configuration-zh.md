---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter用户代理配置数组
translated: true
type: note
---

### 概述
这段 PHP 代码片段是 CodeIgniter 框架（一个 PHP Web 框架）中用户代理类配置文件的一部分。它定义了四个数组（`$platforms`、`$browsers`、`$mobiles` 和 `$robots`），用于将用户代理字符串片段映射到浏览器、操作系统、移动设备和网络爬虫/机器人的人类可读名称。该代码用于根据客户端发送的 HTTP User-Agent 头来解析和识别访问网站的设备类型、浏览器或机器人。

这些数组是关联数组（键值对），其中键是用户代理字符串中的部分字符串（不区分大小写匹配），值是对应的显示名称。CodeIgniter 的用户代理库使用这些数组进行检测，例如判断访问者是否使用 Android 系统、Chrome 浏览器或是搜索引擎机器人。

### $platforms 数组
该数组用于识别操作系统或平台。键是可能出现在 User-Agent 头中的子字符串，值是用于显示的清晰名称。

- **示例条目**：
  - `'windows nt 10.0'` → `'Windows 10'`
  - `'android'` → `'Android'`
  - `'os x'` → `'Mac OS X'`
- **用途**：帮助检测客户端的操作系统（例如 Windows、iOS、Linux），用于分析、内容定制或功能调整。
- **注意**：顺序对准确性很重要，因为某些子字符串可能重叠（例如，`'windows'` 是最后的通用匹配项）。

### $browsers 数组
识别 Web 浏览器。浏览器通常报告多个标识符，因此顺序会优先考虑子类型（如注释所述）。

- **示例条目**：
  - `'Chrome'` → `'Chrome'`
  - `'MSIE'` → `'Internet Explorer'`
  - `'Firefox'` → `'Firefox'`
  - 特殊情况：`'Opera.*?Version'`（类似正则表达式的匹配）用于现代 Opera 浏览器，其报告为 "Opera/9.80" 并带有版本号。
- **用途**：确定浏览器（例如 Chrome、Safari），以提供浏览器特定功能或重定向。
- **正则表达式说明**：某些键使用基本的正则表达式模式（例如 `.*?` 用于通配符匹配），在库中处理。

### $mobiles 数组
映射移动设备、手机及相关设备/浏览器的用户代理标志。它更大，包括手机、平板电脑、游戏机和回退类别。

- **结构部分**：
  - 手机/制造商：`'iphone'` → `'Apple iPhone'`，`'samsung'` → `'Samsung'`。
  - 操作系统：`'android'` → `'Android'`，`'symbian'` → `'Symbian'`。
  - 浏览器：`'opera mini'` → `'Opera Mini'`，`'fennec'` → `'Firefox Mobile'`。
  - 其他/回退：`'mobile'` → `'Generic Mobile'` 用于未匹配的移动指示符。
- **用途**：标记移动设备，用于响应式设计、仅限移动设备的功能或应用重定向。包括旧条目（一些已注释掉，因为过时）。

### $robots 数组
列出常见的网络爬虫和机器人。键是机器人用户代理中的子字符串。

- **示例条目**：
  - `'googlebot'` → `'Googlebot'`
  - `'bingbot'` → `'Bing'`
  - `'yandex'` → `'YandexBot'`
- **用途**：识别爬虫以进行 SEO 处理，例如向机器人提供不同内容（例如无广告）或记录机器人流量。

### 在 CodeIgniter 中的使用
- 用户代理类加载此文件，并使用诸如 `is_browser()`、`is_mobile()`、`is_robot()` 和 `platform()` 等方法解析 User-Agent 字符串。
- 它通过这些数组执行不区分大小写的搜索，以匹配字符串中的键。
- 对于差异（例如未列出的新设备/浏览器），您需要手动或通过社区扩展更新这些数组。

### 附加说明
- **安全性**：这纯粹用于数据收集；它不执行有害代码。User-Agent 字符串可能被伪造，因此不要依赖此进行关键安全检查。
- **更新**：CodeIgniter 版本可能已添加/修改条目；这看起来像是较旧的快照（例如，Edge 作为 'Spartan' 已过时）。
- **如何测试**：在 PHP 脚本中，您可以加载此文件并使用 `strpos` 或正则表达式来匹配示例 User-Agent 字符串。

如果您提供特定部分或有关于实现的问题，请告诉我！
