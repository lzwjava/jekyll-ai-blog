---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI从代码中解码表单需求
translated: true
type: note
---

**问题：** 将前端源码复制给AI是否是理解表单需求（包括隐藏规则）的有效技巧？

**答案：**

是的，这是一种非常有效的技术，尤其适用于政府/企业级表单。用户可见的网页通常只是**表示层**，实际的验证逻辑可能存在于JavaScript、HTML属性、API请求或隐藏配置中。

典型工作流程：

```
浏览器
  |
  |-- HTML
  |     ├── 字段名称
  |     ├── 必填属性
  |     ├── 输入类型
  |     └── 隐藏字段
  |
  |-- JavaScript
  |     ├── 验证规则
  |     ├── 文件大小限制
  |     ├── 可接受格式
  |     ├── 条件字段
  |     └── 错误提示信息
  |
  |-- 网络API
        ├── 后端验证
        ├── 允许的值
        └── 提交数据模型
```

将前端代码提供给AI可以揭示以下内容：

### 1. 隐藏的必填字段

示例：

```html
<input
  name="passportNumber"
  required
/>
```

页面可能没有直观显示红色的`*`符号，但浏览器会拒绝空值提交。

---

### 2. 文件上传规则

你可能会发现：

```html
<input
 type="file"
 accept=".pdf,.jpg,.png"
>
```

或者：

```javascript
if (file.size > 5 * 1024 * 1024) {
   alert("文件过大");
}
```

这告诉你：

* 允许的格式
* 最大文件大小
* 是否优先使用PDF
* 是否接受图片

---

### 3. 条件逻辑

示例：

```javascript
if (nationality === "China") {
   show("mainlandResidencePermit")
}
```

网页可能不会解释某个字段为何出现，但代码直接显示了规则。

---

### 4. 后端API数据模型

最有价值的部分往往不是HTML，而是网络请求。

打开：

```
Chrome 开发者工具
 -> Network（网络）
 -> 提交按钮
 -> Payload（请求负载）
```

你可能会看到：

```json
{
 "educationLevel": "MASTER",
 "documents": [
   {
     "type": "TRANSCRIPT",
     "fileId": "xxxx"
   }
 ]
}
```

这揭示了真实的数据模型。

---

对于像香港优才计划（QMAS）这样的表单，我会执行以下操作：

```
1. 打开页面
2. 开发者工具 → Sources（源代码）
3. 搜索关键词：
      required（必填）
      upload（上传）
      file（文件）
      pdf
      jpg
      size（大小）
      validation（验证）
      error（错误）
4. Network（网络）选项卡
5. 提交一份测试草稿
6. 将JS/API请求负载复制给AI
7. 询问AI：
      "提取所有验证规则和所需文件"
```

重要的注意事项：

前端规则**并非最终真相**。后端可能有额外的检查机制。

可以这样理解：

```
前端 = 客户端提示 + 用户体验
后端 = 实际权限
```

因此最强大的方法是：

```
页面文本
   +
HTML
   +
JavaScript
   +
网络API
   +
AI分析
```

这本质上是对表单数据模型进行逆向工程。对于复杂的移民、银行、税务或企业级表单，这种方法比手动阅读说明要快得多。