---
audio: false
generated: false
image: false
lang: zh
layout: post
title: Eclipse 转换为 Emacs
translated: true
type: post
---

作为一个使用了半年Emacs的用户，我简直无法想象自己以前是怎么编码的，移动手离开标准位置去点击鼠标或按箭头键，感觉那么笨拙和难以忍受。现在，当我告诉朋友们我设置了Alt+P和Alt+N快捷键来快速在XML文件和图形布局之间切换时，他们的回应只是“okay”，暗示着使用鼠标切换也可以。
对我来说，这简直是噩梦；刚好不够快！如果你是Emacs用户，你会理解的。

这篇文章描述了构建快速的Eclipse“编辑”环境的简单技巧。基本上，你的手可以保持在标准位置，使你可以以最大效率编码！

最重要的事情是安装Emacs+插件。请参阅“Emacs+: Eclipse中的Emacs体验”。

为了充分利用代码助手，你需要使其能够由任何字符触发，并防止在按空格或=时自动完成。我推荐从CSDN下载这个jar文件。有了它，再加上快速的Google搜索，你可以在瞬间导入包。

接下来，让我们自定义一些快捷键：

1）将Alt+P绑定到“Previous Sub-Tab”，Alt+N绑定到“Next Sub-Tab”。

子选项卡是编辑器下方的选项卡栏，例如在编辑XML文件时的“图形布局”和“XML”选项卡。这使你可以立即查看布局。

2）将Ctrl+C, Ctrl+C绑定到“Run”。

这是从sbcl的配置中复制的。默认是Ctrl+F11，对于一个频繁使用的快捷键来说，这实在是太远了，让Emacs用户感到不适！我愚蠢地按了Ctrl+F11几天才改变它。

3）将Ctrl+X, Ctrl+O绑定到“Next View”。在Windows和编辑文本中。

这使你可以在编写Java代码时从编辑器瞬间跳转到控制台。

4）将Ctrl+X, O绑定到“Next Editor”。在Windows和编辑文本中。

这使你可以快速在Java文件之间切换。

5）将Ctrl+Q绑定到“Quick Fix”。

这样，当你输入`@string/xx`，光标在`xx`上时，按Ctrl+Q然后Enter将立即跳转到`string.xml`，光标位于`<string name="xx">TODO</string>`中的`TODO`。

6）将Ctrl+Shift+W绑定到“Close”（在Windows中）并删除原始绑定（关闭所有）。
原始的关闭快捷键是Ctrl+W，这与我们在浏览器、聊天框和文件资源管理器中的习惯一致。但是，它与Emacs的剪切命令冲突。实际上，按Ctrl+Shift+W一秒钟就可以关闭许多文件。所以，将Ctrl+Shift+W从“关闭所有”改为“关闭”并不会失去任何东西。

有一个问题：安装Emacs+后，在编辑代码时，当代码助手出现时，按上下箭头键不会选择代码助手的候选项列表中的项，而是在编辑的代码上下移动。默认情况下，它是通过F2激活的。激活代码助手会将焦点放在代码助手上，然后你只能使用上下箭头键进行选择。如果我们能使用Ctrl+P和Ctrl+N就太好了！编辑代码将会像闪电一样快！但是问题在于，安装Emacs+插件后，虽然Eclipse变得更像Emacs，但这个功能丢失了。在干净的Eclipse中，选择Emacs（而不是Emacs+Scheme）键盘布局，当代码助手出现时，你可以使用Ctrl+N和Ctrl+P选择补全项。有人在Stack Overflow上问过这个问题，但还没有答案。

如果我们能够使用Ctrl+P和Ctrl+N选择补全项，那将是真正的奇迹！
