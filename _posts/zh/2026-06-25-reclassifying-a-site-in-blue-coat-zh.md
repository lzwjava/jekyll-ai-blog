---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Blue Coat中重新分类站点
translated: true
type: note
---

**问题：** 如何在 Symantec Blue Coat 的系统中更改网站类别，使其被解除封锁？

**答案：**

直接在 `sitereview.bluecoat.com` 上操作：

---

## 步骤

### 1. 查找网站
访问：
```
https://sitereview.bluecoat.com/#/lookup-result/huggingface.co
```

### 2. 查看当前类别
页面会显示 Blue Coat 当前分配的类别——例如 `Technology/Internet`、`File Storage`、`Malicious Sources` 等。

### 3. 提交重新分类
在同一页面有一个 **"Submit for Review"** 或 **"Suggest a Category Change"** 按钮。

填写：
- **你建议的类别** → 选择像 `Technology/Internet` 或 `Research/Reference` 这类无害的选项
- **理由** → 写 1–2 句话

理由示例：
```
HuggingFace 是一个合法的 AI/ML 研究平台，供全球工程师和
研究人员访问开源模型和文档。它应归类为
Technology/Internet 或 Research/Reference。
```

### 4. 提交 —— 无需账户
Symantec 接受匿名提交。他们会审核并更新其全球数据库。

---

## 提交后会发生什么

```
你的提交
      ↓
Symantec 审核（1–2 周）
      ↓
全球 Blue Coat 数据库更新
      ↓
所有使用 Blue Coat 的企业代理
自动拉取新类别
      ↓
你银行的代理自动解除封锁
```

---

## 实际结果

| 当前类别 | 成功几率 |
|-----------------|-------------------|
| `Malicious Sources` | 低 — 难以重新分类 |
| `File Storage` | 中等 |
| `Technology/Internet`（已正确） | 类别已正确，是 IT 策略在阻止 —— 不同问题 |
| `Uncategorized` | 高 — 容易解决 |

如果类别已经正确但银行策略封锁了该类别，那么重新分类也无济于事。此时需要转为内部 IT 白名单申请。