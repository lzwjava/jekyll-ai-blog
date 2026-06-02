---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 卡宴主题中的谷歌字体导入
translated: true
type: note
---

是的——这很可能就是原因。

当你写下：

```scss
@import "jekyll-theme-cayman";
```

你引入的不仅是局部SCSS文件——而是导入了**整个主题的样式表**，其中本身就包含（或链接了）Google字体的导入。Cayman主题默认使用**Open Sans**字体，并通过`https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap`获取该字体。

所以整个流程是这样的：

1. 你的SCSS代码声明`@import "jekyll-theme-cayman";`
2. Jekyll将该语句解析为主题内的`_sass`文件
3. 在Cayman的SCSS文件中存在这样的导入语句：

   ```scss
   @import url("https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap");
   ```
4. 这就是你在开发者工具中看到的网络请求

---

### 如何移除或覆盖

* **覆盖字体导入**：将主题的主SCSS文件复制到你的项目中（例如`assets/css/style.scss`），删除Google字体导入语句，并配置Jekyll不再导入该字体

* **仅覆盖字体系列**：保留Cayman主题的其他样式，但在自定义CSS中强制使用系统字体栈：

  ```css
  html, body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu,
                 "Helvetica Neue", Arial, "Noto Sans", sans-serif;
  }
  ```

  即使Google字体请求仍在发生，浏览器也不会实际使用该字体

* **自托管Open Sans字体**：如果你喜欢Open Sans字体但不想发起外部调用，可下载字体文件并通过`@font-face`在自定义CSS中定义，然后移除Cayman中的`@import url(...)`语句

---

👉 如果需要，我可以为你精准定位Cayman主题中包含Google字体导入的SCSS文件，并演示如何在Jekyll配置中彻底覆盖它。需要我逐步演示具体操作步骤吗？
