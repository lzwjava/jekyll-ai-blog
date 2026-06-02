---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用JavaScript设置文本区域的值
translated: true
type: note
---

问题：什么 JavaScript 代码可以设置此 `<textarea>` 的值？

答案：

对于你的 textarea：

```html
<textarea autocomplete="off" rows="3" style="max-height:100px;" id="q12" name="q12"></textarea>
```

使用此 JavaScript：

```javascript
document.getElementById("q12").value = "your text here";
```

如果页面使用了 React/Vue/Angular，普通的 `.value` 无法正确更新内部状态，请使用：

```javascript
const textarea = document.getElementById("q12");

textarea.value = "your text here";

textarea.dispatchEvent(new Event("input", { bubbles: true }));
textarea.dispatchEvent(new Event("change", { bubbles: true }));
```

你可以在以下位置运行它：

* 浏览器开发者工具控制台
* 书签小工具
* Tampermonkey 用户脚本
* 注入脚本

示例：

```javascript
const textarea = document.getElementById("q12");

textarea.value = `
你好，面试官，

这是通过编程方式插入的内容。
`;

textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

如果 textarea 位于 iframe 内：

```javascript
const iframe = document.querySelector("iframe");

const textarea =
  iframe.contentDocument.getElementById("q12");

textarea.value = "hello";
textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

如果有多个 textarea：

```javascript
document.querySelectorAll("textarea")[0].value = "hello";
```

或者具体指定：

```javascript
document.querySelector('textarea[name="q12"]').value = "hello";
```
