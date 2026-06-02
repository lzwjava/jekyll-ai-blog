---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 变更请求的智能过滤器
translated: true
type: note
---

好主意！以下是其他有效的过滤器，可以用来限制你的 Change Request 搜索结果：

**Time-Based 过滤器：**

- `Updated`（最后修改时间）- 即使是较旧的变更，也能捕捉到最近的活动
- `Planned start date` 或 `Planned end date` - 未来/即将进行的变更
- `Actual start/end date` - 最近执行的变更
- `Closed` 日期 - 最近完成的变更

**Status/State 过滤器：**

- `State` → `IN` → [New, Assess, Authorize, Scheduled, Implement] - 仅限活动中的变更
- `State` → `NOT IN` → [Closed, Cancelled] - 排除已完成的变更
- `Approval` 状态 - pending, approved, rejected

**Impact/Priority 过滤器：**

- `Priority` → `is` → [1-Critical, 2-High] - 关注紧急项目
- `Impact` → `is` → [1-High, 2-Medium] - 仅限重大变更
- `Risk` 评估等级

**Type/Category 过滤器：**

- `Type` → [Standard, Normal, Emergency] - 按变更类型缩小范围
- `Category` - 特定技术领域（Hardware, Software, Network 等）
- `Subcategory` - 更具体的分类

**Requester/Involvement 过滤器：**

- `Requested by` - 特定部门或用户
- `Configuration item` (CI) - 影响你关注的特定系统/应用的变更
- `Service` - 如果你的组织使用了 service catalog 集成

**组合策略：**

最有效的方法：**Created in last 30 days** + **State is not Closed/Cancelled** + **Assignment group includes parent group**

这可以让你在不获得冗余结果的情况下，获取更大范围内的近期活动变更。你通常在寻找哪种类型的变更？
