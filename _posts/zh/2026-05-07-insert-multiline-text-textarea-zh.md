---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在文本区域中插入多行文本
translated: true
type: note
---

问题：当复制困难时，如何用 JavaScript 轻松向 textarea 插入多行文本？

答案：

可以。最简单的方法是使用 JavaScript **模板字符串**（反引号 `` ` ``），这样可以直接保留多行内容。

示例：

```javascript id="kj6ojg"
const text = `
第1行
第2行
第3行

这里是另一个段落。
`;

const textarea = document.getElementById("q12");

textarea.value = text;

textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

---

# 更好的方法：使用提示弹窗

这样可以避免手动转义引号。

运行：

```javascript id="nwwc6x"
const text = prompt("在此粘贴你的内容：");

const textarea = document.getElementById("q12");

textarea.value = text;

textarea.dispatchEvent(new Event("input", { bubbles: true }));
```

然后：

1. 浏览器弹窗出现
2. 粘贴大量内容到弹窗中
3. 内容自动插入到 textarea

这通常是最便捷的方式。

---

# 超级便捷的书签小工具

创建一个浏览器书签，将以下内容作为 URL：

```javascript id="g3cixv"
javascript:(()=>{const t=prompt("粘贴文本");const e=document.getElementById("q12");e.value=t;e.dispatchEvent(new Event("input",{bubbles:true}))})()
```

然后：

* 打开面试页面
* 点击书签
* 粘贴内容
* 完成

---

# 更优方案：自动从剪贴板读取

现代浏览器支持：

```javascript id="4kt81j"
(async () => {
  const text = await navigator.clipboard.readText();

  const textarea = document.getElementById("q12");

  textarea.value = text;

  textarea.dispatchEvent(new Event("input", { bubbles: true }));
})();
```

这将直接插入你的剪贴板内容。

你可能需要：

* HTTPS 页面
* 剪贴板权限
* 先进行用户交互

---

# 处理大量文本

如果内容非常大，模拟打字更安全：

```javascript id="9gq31o"
(async () => {
  const text = await navigator.clipboard.readText();

  const el = document.getElementById("q12");

  el.focus();

  for (const ch of text) {
    el.value += ch;

    el.dispatchEvent(
      new Event("input", { bubbles: true })
    );

    await new Promise(r => setTimeout(r, 1));
  }
})();
```

某些系统认为这更像真实的打字输入。