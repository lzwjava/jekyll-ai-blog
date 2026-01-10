---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 网页设计与制作知识点
translated: true
type: note
---

## Chapter 1: Web Design Fundamentals (1-15)

1. **Web design definition**: 规划、构思和实施网站设计方案的过程，旨在确保网站的功能性和用户友好性
2. **Website components**: Domain name、Web hosting、网页、导航结构和 Content management system
3. **Client-server architecture**: 理解浏览器如何发送请求以及服务器如何响应 Web content
4. **HTTP/HTTPS protocols**: World Wide Web 数据通信的基础
5. **URL structure**: 网络地址中的 Protocol、Domain name、路径和参数
6. **Static vs dynamic websites**: 内容生成和数据库集成方面的差异
7. **Web standards**: W3C 关于 HTML、CSS 和 Accessibility 合规性的指南
8. **Browser compatibility**: 确保在不同浏览器（Chrome、Firefox, Safari、Edge）中显示一致
9. **Responsive web design**: 使布局适应不同的屏幕尺寸和设备
10. **Web design principles**: 平衡、对比、强调、统一和留白 (White space)
11. **User experience (UX)**: 专注于用户满意度和易用性
12. **User interface (UI)**: 用户在网页上交互的视觉元素
13. **Information architecture**: 逻辑性地组织和构建网站内容
14. **Wireframing**: 在详细设计之前创建基础布局蓝图
15. **Website planning process**: 需求分析、设计、开发、测试和部署

## Chapter 2: HTML Basics (16-30)

16. **HTML definition**: 用于构建 Web content 的 HyperText Markup Language
17. **HTML document structure**: `<!DOCTYPE>`、`<html>`、`<head>` 和 `<body>` 标签
18. **HTML tags and elements**: 开始标签、结束标签和自闭合标签
19. **HTML attributes**: 标签内提供的附加信息（id、class、src、href）
20. **Headings**: 用于层级内容结构的 `<h1>` 到 `<h6>`
21. **Paragraphs and line breaks**: 用于文本格式化的 `<p>` 和 `<br>` 标签
22. **Text formatting tags**: `<strong>`、`<em>`、`<u>`、`<mark>`、`<small>`
23. **Lists**: 有序列表 `<ol>`、无序列表 `<ul>` 和列表项 `<li>`
24. **Hyperlinks**: 带有 href 属性、用于导航的 `<a>` 标签
25. **Images**: 带有 src 和 alt 属性的 `<img>` 标签
26. **Tables**: 用于表格数据的 `<table>`、`<tr>`、`<td>`、`<th>`
27. **Forms**: 用于用户输入的 `<form>`、`<input>`、`<textarea>`、`<select>`
28. **Semantic HTML5 elements**: `<header>`、`<nav>`、`<main>`、`<article>`、`<section>`、`<footer>`
29. **Meta tags**: 关于网页的信息（charset、viewport、description）
30. **HTML comments**: 用于代码文档化的 `<!-- -->`

## Chapter 3: CSS Fundamentals (31-45)

31. **CSS definition**: 用于为 HTML 元素设置样式的 Cascading Style Sheets
32. **CSS syntax**: Selector、Property 和 Value
33. **Three ways to add CSS**: Inline (行内)、Internal (内部/嵌入式) 和 External (外部) 样式表
34. **CSS selectors**: Element、Class、ID、Attribute 和 Pseudo-class 选择器
35. **Selector specificity**: 当多条规则适用时计算优先级
36. **Color properties**: 使用 Hex、RGB、RGBA、HSL 设置 color 和 background-color
37. **Text properties**: font-family、font-size、font-weight、text-align、line-height
38. **Box model**: Content (内容)、Padding (内边距)、Border (边框) 和 Margin (外边距)
39. **Display properties**: block、inline、inline-block、none
40. **Position properties**: static、relative、absolute、fixed、sticky
41. **Float and clear**: 用于元素定位的布局技术
42. **Flexbox**: 用于灵活盒子排列的现代布局系统
43. **CSS Grid**: 用于复杂设计的二维布局系统
44. **Pseudo-classes**: :hover、:active、:focus、:nth-child()
45. **Pseudo-elements**: ::before、::after、::first-letter、::first-line

## Chapter 4: Advanced CSS (46-55)

46. **CSS transitions**: 属性变化时的平滑动画
47. **CSS transforms**: rotate、scale、translate、skew 函数
48. **CSS animations**: 用于复杂动画的 @keyframes
49. **Media queries**: 针对不同屏幕尺寸的 Responsive design
50. **CSS variables**: 用于可复用值的自定义属性
51. **Gradients**: linear-gradient 和 radial-gradient 背景
52. **Shadows**: box-shadow 和 text-shadow 效果
53. **Border-radius**: 创建圆角
54. **Opacity and transparency**: 控制元素可见度
55. **CSS frameworks**: Bootstrap、Tailwind CSS、Foundation 等概念

## Chapter 5: JavaScript Basics (56-70)

56. **JavaScript definition**: 用于实现交互式 Web 功能的编程语言
57. **Variables**: var、let、const 声明及其作用域 (Scope)
58. **Data types**: String、Number、Boolean、Array、Object、Null、Undefined
59. **Operators**: 算术、比较、逻辑和赋值运算符
60. **Conditional statements**: if、else if、else、switch
61. **Loops**: 用于迭代的 for、while、do-while 循环
62. **Functions**: 函数声明、表达式和 Arrow functions (箭头函数)
63. **Arrays**: 创建、访问和操作数组元素
64. **Array methods**: push、pop、shift、unshift、slice、splice
65. **Objects**: 键值对和对象属性
66. **DOM manipulation**: 选择和修改 HTML 元素
67. **Event handling**: onclick、onload、onchange 等事件监听器
68. **Form validation**: 在提交前检查用户输入
69. **JSON**: 用于数据交换的 JavaScript Object Notation
70. **AJAX basics**: 无需刷新页面即可实现异步数据加载

## Chapter 6: Web Graphics and Multimedia (71-80)

71. **Image formats**: JPEG、PNG、GIF、SVG 的特性和用途
72. **Image optimization**: 用于快速加载的压缩技术
73. **Vector vs raster graphics**: 缩放性和使用场景
74. **Favicon**: 浏览器标签页中显示的小图标
75. **Audio elements**: 带有 controls 和 source 文件的 `<audio>` 标签
76. **Video elements**: `<video>` 标签及支持的格式（MP4、WebM）
77. **Canvas API**: 使用 JavaScript 绘制图形
78. **SVG (Scalable Vector Graphics)**: 基于 XML 的矢量图像
79. **Icon fonts**: Font Awesome、Material Icons 集成
80. **Background images**: CSS 背景属性和定位

## Chapter 7: Website Optimization and Testing (81-90)

81. **Page load speed**: 网站快速加载的重要性
82. **Minification**: 减小 CSS 和 JavaScript 文件大小
83. **Caching**: 用于提高性能的浏览器缓存 (Browser caching)
84. **CDN (Content Delivery Network)**: 全球内容分发网络
85. **SEO basics**: Search Engine Optimization 基础
86. **Title tags and meta descriptions**: 提高搜索可见性
87. **Alt text for images**: Accessibility (无障碍) 和 SEO 优势
88. **Cross-browser testing**: 确保跨平台兼容性
89. **Mobile-first design**: 优先考虑移动端用户体验
90. **Accessibility standards**: 用于包容性设计的 WCAG 指南

## Chapter 8: Web Publishing and Maintenance (91-100)

91. **Domain registration**: 选择并注册域名
92. **Web hosting types**: Shared (共享)、VPS、Dedicated (专用) 和 Cloud hosting (云托管)
93. **FTP (File Transfer Protocol)**: 上传文件到 Web 服务器
94. **Website deployment**: 将网站发布到生产环境
95. **Version control basics**: 用于追踪代码更改的 Git
96. **Website backup**: 用于数据保护的定期备份策略
97. **Security considerations**: HTTPS、SQL injection 防护、XSS 防护
98. **Analytics**: 用于追踪访问者行为的 Google Analytics
99. **Website maintenance**: 定期更新、内容翻新、Bug 修复
100. **Legal requirements**: 隐私政策、版权、GDPR 合规性

---

**Note**: 本知识点列表涵盖了广东自学考试《13167 网页设计与制作》课程中通常考核的基础概念。在备考时，应重点理解理论概念及其在实践中的应用。