---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 高级 Outlook 邮件搜索技巧
translated: true
type: note
---

Question: 如何在 Outlook 邮件中使用 "AND"、"OR" 或其他高级技巧进行搜索？

Answer: 

Microsoft Outlook 在桌面客户端和网页版 (Outlook on the web) 中均支持高级搜索技术，帮助您更精准地查找邮件。搜索框通常位于窗口或页面的顶部。

### 基本原则
- 默认情况下，不带操作符的多个单词会被视为 **AND** 逻辑（例如，“project budget” 会查找同时包含这两个单词的邮件）。
- 使用**引号**搜索精确短语：`"project budget"`。
- **AND**、**OR**、**NOT** 等操作符必须大写。
- 使用括号 **()** 对复杂查询进行分组。

### 在 Outlook 桌面端 (Windows)
Outlook 使用带有 Keyword Query Language (KQL) 的 **Instant Search**。

#### 常用关键词 (字段操作符)
- **from:** 发件人 (例如，`from:john@example.com`)
- **to:** 收件人
- **subject:** 包含在主题行中
- **body:** 包含在正文中
- **hasattachment:yes** 或 **hasattachment:no**
- **received:** 日期 (例如，`received:2025` 或 `received:>01/01/2025`)
- **category:** 颜色分类

#### 使用 AND 和 OR
- **AND** (默认或显式)：`project AND budget` (两个词出现在任何地方)
- **OR**：`project OR budget` (包含其中任何一个词)
- 组合字段：`(subject:project OR body:project) AND from:john`

#### 示例
- 来自 John 且主题包含 "report" 的邮件：`subject:report from:john`
- 包含附件且内容涉及 "invoice" 或 "bill" 的邮件：`hasattachment:yes (invoice OR bill)`
- 上周收到且包含 "meeting" 的邮件：`received:lastweek meeting`
- 复杂查询：`(from:alice OR from:bob) AND (subject:urgent OR category:red)`

#### 其他技巧
- 点击搜索框打开功能区上的 **Search** 选项卡，然后使用 **Refine** 选项（如 From、Subject、Has Attachments）——这些会自动添加操作符。
- 对于非常复杂的搜索：转到 **Search Tools > Advanced Find** (Ctrl+Shift+F)。使用 Advanced 选项卡添加多个条件，或通过注册表启用 Query Builder 以实现完整的 AND/OR 控制。
- 搜索范围：选择 Current Folder、All Subfolders、Current Mailbox 或 All Mailboxes。

### 在 Outlook 网页版 (浏览器版)
使用 **Advanced Query Search (AQS)**，与桌面版类似但略有不同。

#### 常用关键词
- **from:**
- **to:**
- **subject:**
- **body:** (可能有所不同)
- 其他如 **attachments:**、**received:**

#### 使用 AND 和 OR
- 多个词之间隐含 AND 关系。
- 支持显式的 **AND**、**OR**、**NOT**。
- 示例通常使用冒号语法。

#### 示例
- `subject:report`
- `from:john subject:(project OR budget)`
- `hasattachments:yes invoice`

#### 其他技巧
- 点击搜索框旁边的 **Filters** 图标，可选择 From、To、Date、Attachments 等选项。
- 更多操作：直接输入关键词（例如 `subject:keyword`）。

注意：网页版的某些高级字段可能比桌面版少，但基本的 AND/OR 逻辑工作方式类似。对于大型邮箱，网页版的搜索速度通常更快。

这些技术适用于大多数最新版本（Outlook for Microsoft 365、2021 等）。如果搜索结果不完整，请确保 Indexing 已完成（桌面端：File > Options > Search > Indexing Options）。

References:  

- [How to search in Outlook - Microsoft Support](https://support.microsoft.com/en-us/office/how-to-search-in-outlook-d824d1e9-a255-4c8a-8553-276fb895a8da)  
- [Search Mail and People in Outlook on the web - Microsoft Support](https://support.microsoft.com/en-us/office/search-mail-and-people-in-outlook-on-the-web-b27e5eb7-3255-4c61-bf16-1c6a16bc2e6b)  
- [Instant Search query commands reference](https://www.howto-outlook.com/howto/searchcommands.htm)