---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 筛选父组更改请求
translated: true
type: note
---

在 ServiceNow 中，您可以过滤 Change Requests 以包含当前组之上的 parent group 或 assignment group。以下是几种方法：

**Option 1: 按 Assignment Group 层级过滤**
如果您的组在 ServiceNow 中具有层级结构：
- 添加过滤器：`Assignment group` → `Parent` → `is` → [您的 Parent Group 名称]
- 或者使用 `Assignment group` → `IN` → [您的组, Parent Group] 以同时查看两者

**Option 2: 使用 Group Membership**
- 通过 `Assignment group` → `CONTAINS` → [包含相关组的部分名称] 进行过滤
- 例如，如果组命名为 "IT-Support-L1" 和 "IT-Support-L2"，则过滤包含 "IT-Support" 的组

**Option 3: 创建自定义过滤器**
1. 进入 Change > All
2. 点击过滤器图标
3. 添加条件：`Assignment group` → `is one of`
4. 选择您的组以及您想要的 parent group
5. 将其保存为个人或共享过滤器以便快速访问

**Option 4: 使用 Dot-Walking（如果您的组织结构支持）**
- `Assignment group.parent` → `is` → [特定的 parent group]
- `Assignment group.parent.name` → `CONTAINS` → [关键词]

**Pro tip:** 如果您只想查看 parent group 的 Change 而不包含您自己的组，可以添加类似 `AND Assignment group IS NOT [您当前的组]` 的条件。

您的 ServiceNow 实例是否有特定的 group hierarchy 结构？如果提供更多信息，我可以为您提供更精确的过滤器设置。
