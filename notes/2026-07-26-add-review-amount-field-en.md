---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add Review Amount Field
translated: false
type: note
---

Now I have a complete understanding. Here's the analysis for **Requirement #4 — 新增"评审金额"**:

---

## Analysis of Current Code

### Navigation Path

```
结算送审 (Settlement Review)
  └── 已送审 (Already Submitted)  →  projectjiesuaninfojszlist.html  (title: "已送审")
        └── 查看 (Detail)          →  projectjiesuandetail.html
        └── 修改 (Edit)            →  projectjiesuanedit.html
        └── (Workflow)             →  projectjiesuanworkflow.html / workflowdetail.html
```

### Pages Currently Displaying Settlement Basic Info (01结算基本信息)

| Page | Mode | Fields currently shown |
| ------ | ------ | ---------------------- |
| `projectjiesuandetail.html` (lines 60-120) | Read-only view | 结算编号, 申请日期, 申请人名, 所属单位, 合同编号, 合同名称, 审定前支付, 审定时间, 财局受理委托书时间, 审定报告号, 财局受理委托书编号, **材料调差价**, **评审费用** |
| `projectjiesuanedit.html` (lines 55-110) | Editable form | Same fields |
| `projectjiesuanworkflow.html` (lines 65-115) | Workflow edit | Same fields |
| `projectjiesuanworkflowdetail.html` (lines 55-105) | Workflow view | Same fields |

### Current `ProjectJiesuan.java` Entity

The last fields in the entity are:

```java
// 材料调差价 (String)
public String getMaterial(){ return super.get("material"); }

// 评审费用 (String)
public String getReview(){ return super.get("review"); }
```

No `reviewAmount` or `reviewamount` field exists yet.

---

## Changes Required

### 1️⃣ Database — Add column

```sql
ALTER TABLE PROJECT_JIESUAN ADD reviewamount NUMBER(18,2) DEFAULT 0;
```

The amount should be numeric (Double), not String like `material`/`review`.

### 2️⃣ Domain — Add field to `ProjectJiesuan.java`

```java
/**
 * 评审金额
 */
public Double getReviewamount() {
    return super.getDouble("reviewamount");
}
public void setReviewamount(Double reviewamount) {
    super.set("reviewamount", reviewamount);
}
```

### 3️⃣ UI Pages — Add "评审金额" field to 结算基本信息 section

In each of the 4 pages, add the new field in the last row of the basic info form, alongside the existing "评审费用" field.

**Example for edit pages** (`projectjiesuanedit.html`):

```html
<div role="row">
    <div role="control" label="评审费用">
        <input id="review" class="mini-textbox" bind="jiesuan.review" />
    </div>
    <div role="control" label="评审金额">
        <input id="reviewamount" class="mini-textbox" bind="jiesuan.reviewamount" />
    </div>
</div>
```

**Example for detail/view pages** (`projectjiesuandetail.html`):

```html
<div role="row">
    <div role="control" label="评审费用">
        <input id="review" class="mini-outputtext" bind="jiesuan.review" />
    </div>
    <div role="control" label="评审金额">
        <input id="reviewamount" class="mini-outputtext" bind="jiesuan.reviewamount" />
    </div>
</div>
```

### 4️⃣ Files to Modify

| # | File | Change |
| --- | ------ | -------- |
| 1 | `domain/jiesuan/ProjectJiesuan.java` | Add `reviewamount` (Double) getter/setter |
| 2 | Database | `ALTER TABLE PROJECT_JIESUAN ADD reviewamount NUMBER(18,2)` |
| 3 | `projectjiesuandetail.html` | Add read-only field in 结算基本信息 section |
| 4 | `projectjiesuanedit.html` | Add editable field in 结算基本信息 section |
| 5 | `projectjiesuanworkflow.html` | Add editable field in 结算基本信息 section |
| 6 | `projectjiesuanworkflowdetail.html` | Add read-only field in 结算基本信息 section |

---

Let me know if you'd like me to proceed with implementing Requirement #4, or would you like me to analyze the remaining requirements first?
