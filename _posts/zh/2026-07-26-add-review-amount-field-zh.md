---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加评论数量字段
translated: true
type: note
---

现在我完全理解了。以下是针对**需求 #4 — 新增"评审金额"**的分析：

---

## 当前代码分析

### 导航路径

```
结算送审
  └── 已送审  →  projectjiesuaninfojszlist.html  (标题："已送审")
        └── 查看          →  projectjiesuandetail.html
        └── 修改          →  projectjiesuanedit.html
        └── (工作流)      →  projectjiesuanworkflow.html / workflowdetail.html
```

### 当前显示结算基本信息的页面（01结算基本信息）

| 页面 | 模式 | 当前显示的字段 |
| ------ | ------ | ---------------- |
| `projectjiesuandetail.html`（第60-120行） | 只读视图 | 结算编号、申请日期、申请人名、所属单位、合同编号、合同名称、审定前支付、审定时间、财局受理委托书时间、审定报告号、财局受理委托书编号、**材料调差价**、**评审费用** |
| `projectjiesuanedit.html`（第55-110行） | 可编辑表单 | 相同字段 |
| `projectjiesuanworkflow.html`（第65-115行） | 工作流编辑 | 相同字段 |
| `projectjiesuanworkflowdetail.html`（第55-105行） | 工作流查看 | 相同字段 |

### 当前 `ProjectJiesuan.java` 实体

实体中的最后字段为：

```java
// 材料调差价 (String)
public String getMaterial(){ return super.get("material"); }

// 评审费用 (String)
public String getReview(){ return super.get("review"); }
```

目前尚不存在 `reviewAmount` 或 `reviewamount` 字段。

---

## 需要进行的修改

### 1️⃣ 数据库 — 添加列

```sql
ALTER TABLE PROJECT_JIESUAN ADD reviewamount NUMBER(18,2) DEFAULT 0;
```

该金额应为数字类型（Double），而非像 `material`/`review` 那样的字符串类型。

### 2️⃣ 领域层 —
