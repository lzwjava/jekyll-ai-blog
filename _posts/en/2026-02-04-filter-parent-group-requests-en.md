---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Filter Parent Group Change Requests
translated: false
type: note
---

In ServiceNow, you can filter Change Requests to include your parent/assignment group above your current group. Here are a few approaches:

**Option 1: Filter by Assignment Group Hierarchy**
If your groups have a hierarchical structure in ServiceNow:
- Add a filter for `Assignment group` → `Parent` → `is` → [Your Parent Group Name]
- Or use `Assignment group` → `IN` → [Your Group, Parent Group] to see both

**Option 2: Use Group Membership**
- Filter by `Assignment group` → `CONTAINS` → partial name that captures related groups
- For example, if groups are named like "IT-Support-L1" and "IT-Support-L2", filter by groups containing "IT-Support"

**Option 3: Create a Custom Filter**
1. Go to Change > All
2. Click the filter icon
3. Add condition: `Assignment group` → `is one of`
4. Select your group and the parent group(s) you want
5. Save this as a personal or shared filter for quick access

**Option 4: Use Dot-Walking (if your org structure supports it)**
- `Assignment group.parent` → `is` → [specific parent group]
- `Assignment group.parent.name` → `CONTAINS` → [keyword]

**Pro tip:** You can also add a condition like `AND Assignment group IS NOT [Your Current Group]` if you only want to see the parent group's changes without your own.

Does your ServiceNow instance have a specific group hierarchy structure I should know about to give you a more precise filter?
