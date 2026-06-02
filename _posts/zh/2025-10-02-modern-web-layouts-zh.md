---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 现代网页样式与布局
translated: true
type: note
---

### 概述
这段代码采用 SCSS (Sass) 语法编写，包含嵌套结构、伪类选择符（&）和 @extend 指令。它定义了基础网页布局、表单、按钮及工具类的样式，呈现简洁现代的美学风格（如圆角、柔和阴影、悬停过渡效果）。无单位数值属性（如 `font-size 16px`）是 SCSS 的简写形式。下面按模块解析选择器及其作用效果。

### 全局样式（html, body）
```css
html, body
  font-family Verdana
  font-size 16px
  height 100%
  background-color #D2D2D2
```
- 应用简易字体栈（Verdana 备用字体）和 16px 字号
- 设置 100% 高度实现全屏布局，常用于居中或覆盖视口
- 背景采用浅灰色 (#D2D2D2) 作为中性基色

### 列表与链接样式（ul, a）
```css
ul
  list-style-type none
  padding 0
  margin 0

a
  color #000
  cursor pointer
  text-decoration none
```
- 清除无序列表默认项目符号、内边距和外边距，便于自定义样式
- 链接设为黑色 (#000)，悬停时显示指针光标，无下划线，呈现按钮化效果

### 色彩与文本工具类 (.a-blue)
```css
.a-blue
  color #00BDEF
```
- 蓝色文字工具类 (#00BDEF 浅蓝)，常用于强调元素

### 按钮样式 (.btn, .btn-blue, .btn-gray, .btn-gray-2)
```css
.btn
  border-radius 3px
  padding 10px

.btn-blue
  background #00BDEF
  color #fff
  -webkit-box-shadow 0px 1px 0px rgba(255,255,255,0.15) inset,0px 1px 2px rgba(0,0,0,0.15)
  box-shadow 0px 1px 0px rgba(255,255,255,0.15) inset,0px 1px 2px rgba(0,0,0,0.15)
  &:hover
    background #00ABD8
    transition .5s

.btn-gray
  background #eee
  color #333
  border 1px solid #d5d5d5
  border-radius 3px
  -webkit-box-shadow 0px 1px 0px rgba(255,255,255,0.15) inset,0px 1px 2px rgba(0,0,0,0.15)
  box-shadow 0px 1px 0px rgba(255,255,255,0.15) inset,0px 1px 2px rgba(0,0,0,0.15)
  &:hover
    background #ddd
    transition 0.5s

.btn-gray-2
  background #eee
  color #333
  border 1px solid #d5d5d5
  border-radius 3px
  &:hover
    background #ddd
    transition 0.5s
```
- `.btn` 为基础按钮类，设置 3px 圆角和 10px 内边距
- `.btn-blue`：蓝色按钮 (#00BDEF 背景，白色文字)，含内嵌高光和投影增强层次感。悬停时蓝色加深并伴随 0.5 秒平滑过渡
- `.btn-gray` 与 `.btn-gray-2`：灰色按钮（浅背景 #eee，深色文字 #333，细微边框 #d5d5d5），具有相似阴影效果。`.btn-gray-2` 无显式投影但具备相同悬停效果（变亮至 #ddd），适用于次要操作

### 定位工具类 (.absolute-center, .full-space)
```css
.absolute-center
    margin auto
    position absolute
    top 0
    left 0
    bottom 0
    right 0

.full-space
    position absolute
    top 0
    left 0
    bottom 0
    right 0
```
- `.absolute-center`：在父容器内绝对居中（四边距为 0 且自动外边距）
- `.full-space`：使元素绝对定位填满父容器全部空间

### 表单样式 (.base-form, input/textarea/select, button)
```css
.base-form
  @extend .absolute-center
  max-width 350px
  height 400px
  background #fff
  border-radius 20px
  text-align center
  padding 20px 10px

input, textarea, select
  box-sizing border-box
  border none
  outline none
  &:focus
    border none
    outline none
    box-shadow 0px 1px 4px 0px rgba(0,0,0,.06)
    -webkit-box-shadow 0px 1px 4px 0px rgba(0,0,0,.06)

button
  border-style none
  outline none
```
- `.base-form`：继承 `.absolute-center` 实现模态框式表单居中（最大宽度 350px，高度 400px，白色背景，20px 圆角，居中对齐，内边距）。适合登录/注册表单
- 输入框、文本域、下拉框：无边框且盒模型包含内边距；聚焦时无轮廓线，但添加浅灰阴影提升用户体验
- 按钮：移除默认边框和轮廓，需配合 `.btn` 类实现美观样式

此代码构建了具有样式化按钮和输入框的响应式居中表单页面。若使用 SCSS 需编译为标准 CSS。自定义时可根据需求调整色彩或尺寸参数。
