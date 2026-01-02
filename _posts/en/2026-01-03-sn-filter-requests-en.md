---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Filtering Change Requests in ServiceNow
translated: false
type: note
---

Question: How to use filters to search for change requests in ServiceNow?

Answer: 

In ServiceNow, change requests are stored in the **change_request** table. To search and filter them effectively, follow these steps:

### Accessing the Change Requests List
1. Log in to your ServiceNow instance.
2. In the left-hand navigation pane (Application Navigator), type "Change" in the filter navigator search bar.
3. Under the **Change** module, select one of the predefined lists, such as:
   - **All** (shows all change requests)
   - **My Changes** (your assigned or created changes)
   - **My Group Changes** (changes for groups you manage)
   - **Open** or other categorized views.
   
   Alternatively, go directly to **Change > All** or search for "change_request.list" in the navigator to open the full list view.

### Using Filters in the List View
Once in the list view:
- At the top of the list, you'll see a **breadcrumb** (e.g., "All") and a filter builder.
- Click the **funnel icon** or the area next to the breadcrumb to open the condition builder.
- Build your filter:
  1. Select a field (e.g., Number, Short description, State, Type, Assignment group, Created, etc.).
  2. Choose an operator (e.g., is, contains, starts with, is one of, greater than).
  3. Enter or select a value.
  4. Add more conditions with **AND** or **OR**.
  5. Use grouping with parentheses for complex queries.
- Click **Run** to apply the filter and refresh the list.

### Quick Search Tips
- Use the global search bar at the top: Type "CHG*" for change numbers or keywords.
- In the list, use the search box above columns for quick text search.

### Saving and Reusing Filters
- After building a filter, click the dropdown next to the breadcrumb and select **Save** to name and save it for future use.
- Saved filters appear in the breadcrumb menu for quick access.

### Common Filter Examples
- **My open changes**: Assignment group > is one of > My groups (dynamic) **AND** State > is one of > New, Assess, Authorize.
- **Emergency changes this month**: Type > is > Emergency **AND** Created > on > This month.
- **Approved changes**: Approval > is > Approved.

Filters can be combined with sorting (click column headers) and column personalization (right-click headers > Configure > List Layout).

References:  

- [https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/change-management/task/t_CreateAChange.html](https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/change-management/task/t_CreateAChange.html)  
- [https://community.servicenow.com/community?id=community_question&sys_id=720b7d861bfcccd0ada243f6fe4bcb24](https://community.servicenow.com/community?id=community_question&sys_id=720b7d861bfcccd0ada243f6fe4bcb24)  
- [https://docs.servicenow.com/en-US/bundle/tokyo-platform-user-interface/page/use/using-lists/task/t_SavingFilters.html](https://docs.servicenow.com/en-US/bundle/tokyo-platform-user-interface/page/use/using-lists/task/t_SavingFilters.html)