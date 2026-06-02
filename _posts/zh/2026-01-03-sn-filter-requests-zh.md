---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 ServiceNow 中筛选变更请求
translated: true
type: note
---

Question: 如何在 ServiceNow 中使用 filters 搜索 change requests？

Answer:

在 ServiceNow 中，change requests 存储在 **change_request** 表中。要有效地搜索和过滤它们，请按照以下步骤操作：

### 访问 Change Requests 列表

1. 登录您的 ServiceNow 实例。
2. 在左侧导航栏（Application Navigator）的 filter navigator 搜索框中输入 "Change"。
3. 在 **Change** 模块下，选择一个预定义的列表，例如：
   - **All**（显示所有 change requests）
   - **My Changes**（您分配到的或创建的 changes）
   - **My Group Changes**（您管理的 groups 的 changes）
   - **Open** 或其他分类视图。

   或者，直接进入 **Change > All**，或在 navigator 中搜索 "change_request.list" 以打开完整的 list view。

### 在 List View 中使用 Filters

进入 list view 后：

- 在列表顶部，您会看到一个 **breadcrumb**（例如 "All"）和一个 filter builder。
- 点击 **漏斗图标** 或 breadcrumb 旁边的区域以打开 condition builder。
- 构建您的 filter：
  1. 选择一个 field（例如 Number, Short description, State, Type, Assignment group, Created 等）。
  2. 选择一个 operator（例如 is, contains, starts with, is one of, greater than）。
  3. 输入或选择一个 value。
  4. 使用 **AND** 或 **OR** 添加更多条件。
  5. 对于复杂的查询，可以使用括号进行分组。
- 点击 **Run** 应用 filter 并刷新列表。

### 快速搜索技巧

- 使用顶部的 global search 栏：输入 "CHG*" 搜索 change 编号或关键词。
- 在列表中，使用列上方的 search box 进行快速文本搜索。

### 保存和重复使用 Filters

- 构建 filter 后，点击 breadcrumb 旁边的下拉菜单并选择 **Save**，为其命名并保存以便将来使用。
- 保存的 filters 会出现在 breadcrumb 菜单中，方便快速访问。

### 常用 Filter 示例

- **My open changes**: Assignment group > is one of > My groups (dynamic) **AND** State > is one of > New, Assess, Authorize。
- **Emergency changes this month**: Type > is > Emergency **AND** Created > on > This month。
- **Approved changes**: Approval > is > Approved。

Filters 可以与排序（点击列标题）和列个性化（右键点击标题 > Configure > List Layout）结合使用。

References:

- [https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/change-management/task/t_CreateAChange.html](https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/change-management/task/t_CreateAChange.html)
- [https://community.servicenow.com/community?id=community_question&sys_id=720b7d861bfcccd0ada243f6fe4bcb24](https://community.servicenow.com/community?id=community_question&sys_id=720b7d861bfcccd0ada243f6fe4bcb24)
- [https://docs.servicenow.com/en-US/bundle/tokyo-platform-user-interface/page/use/using-lists/task/t_SavingFilters.html](https://docs.servicenow.com/en-US/bundle/tokyo-platform-user-interface/page/use/using-lists/task/t_SavingFilters.html)
