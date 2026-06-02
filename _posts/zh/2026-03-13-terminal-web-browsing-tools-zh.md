---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终端网页浏览工具指南
translated: true
type: note
---

我会搜索有关允许通过终端界面浏览网页的工具的信息。问题：是否有任何工具允许人们将终端视为浏览器，从而浏览网页并跟随重定向？

答案：

是的，有几个优秀的工具允许您直接从终端浏览网页。这些是基于文本的网页浏览器，可以渲染 HTML，跟随链接，并像传统图形浏览器一样导航重定向。

## 流行的基于终端的网页浏览器

### 1. **Lynx**
Lynx 是一个基于文本的网页浏览器，允许用户在终端环境中浏览网页，开发于 1992 年，支持 HTML、HTTPS 和 FTP 协议。它是最古老且最成熟的命令行浏览器之一。使用方法：
- 安装：`sudo apt install lynx`
- 使用：`lynx [URL]`
- 导航：使用箭头键移动，Enter 跟随链接，向左箭头返回

### 2. **w3m**
w3m 是一个流行的开源基于文本的终端网页浏览器，支持 SSL 连接、颜色和内联图像。它积极维护且功能强大：
- 安装：`sudo apt install w3m`
- 使用：`w3m [URL]`
- 导航：箭头键导航，Shift+B 返回，Shift+T 新标签页，Shift+U 打开新 URL

### 3. **Links/ELinks**
ELinks 以其按 ESC 键访问的菜单系统脱颖而出，允许您输入和保存 URL、添加书签并设置浏览器。这种浏览器提供更交互式的体验：
- 安装：`sudo apt install links` 或 `sudo apt install elinks`
- 使用：`links [URL]` 或 `elinks [URL]`
- 导航：右箭头跟随链接，向左箭头返回，ESC 打开菜单

### 4. **Browsh**
Browsh 是一个现代基于文本的浏览器，可以显示 HTML5、CSS3、JS、视频甚至 WebGL，设计用于通过 SSH 或 Mosh 在远程服务器上运行，并以文本形式从终端浏览网页，从而显著降低带宽并提高浏览速度。
- 使用：`ssh brow.sh`（使用 SSH 连接）
- 按 Ctrl+L 聚焦 URL 栏

## 主要特性

这些工具支持：
- 跟随超链接和重定向
- 多标签页（某些浏览器中）
- Cookie 处理
- 鼠标支持（某些实现中）
- 通过外部程序查看图像
- 搜索功能
- 键盘导航

## 使用场景

终端浏览器在没有图形界面的远程服务器场景中非常有用，用于检查状态页面、阅读文档，或通过命令行直接浏览相关网页资源进行故障排除。它们在低带宽环境和无干扰浏览中也很有益。

参考资料：

- https://itsfoss.com/terminal-web-browsers/
- https://opensource.com/article/16/12/web-browsers-linux-command-line
- https://www.tecmint.com/command-line-web-browser-download-file-in-linux/
- https://www.tutorialspoint.com/a-command-line-web-browsing-with-lynx-and-links-tools
- https://www.fosslinux.com/18554/how-to-access-website-using-command-line-from-the-terminal.htm
