---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Smart Filters for Change Requests
translated: false
type: note
---

Good thinking! Here are other effective filters to limit your Change Request search results:

**Time-Based Filters:**
- `Updated` (last modified) - catches recent activity even on older changes
- `Planned start date` or `Planned end date` - future/upcoming changes
- `Actual start/end date` - recently executed changes
- `Closed` date - recently completed changes

**Status/State Filters:**
- `State` → `IN` → [New, Assess, Authorize, Scheduled, Implement] - active changes only
- `State` → `NOT IN` → [Closed, Cancelled] - exclude completed
- `Approval` status - pending, approved, rejected

**Impact/Priority Filters:**
- `Priority` → `is` → [1-Critical, 2-High] - focus on urgent items
- `Impact` → `is` → [1-High, 2-Medium] - significant changes only
- `Risk` assessment level

**Type/Category Filters:**
- `Type` → [Standard, Normal, Emergency] - narrow by change type
- `Category` - specific technology area (Hardware, Software, Network, etc.)
- `Subcategory` - even more specific

**Requester/Involvement Filters:**
- `Requested by` - specific departments or users
- `Configuration item` (CI) - changes affecting specific systems/apps you care about
- `Service` - if your org uses service catalog integration

**Combination Strategy:**
Most effective approach: **Created in last 30 days** + **State is not Closed/Cancelled** + **Assignment group includes parent group**

This gives you recent, active changes with broader scope without overwhelming results. What type of changes are you typically looking for?