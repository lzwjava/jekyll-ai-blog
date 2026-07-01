---
audio: false
generated: false
image: false
lang: zh
layout: post
title: Xcode 插件：在 GitHub 中显示
translated: true
type: post
---

这是来自GitHub项目的README.md文件 [https://github.com/lzwjava/Reveal-In-GitHub](https://github.com/lzwjava/Reveal-In-GitHub)。

---

# Reveal-In-GitHub

这是一个为在Xcode中无缝导航到当前仓库的关键GitHub功能而设计的Xcode插件。只需点击一下，就可以轻松访问GitHub历史记录、指责、拉取请求、问题和通知，只需几秒钟。

![插件](https://cloud.githubusercontent.com/assets/5022872/10867703/96e980be-80ab-11e5-9aaa-a06ef476b7f7.gif)

我的公司在GitHub上工作。我经常打开GitHub。有时，我在Xcode上编辑，不理解某些代码，所以我去GitHub责备它们。有时，找到文件的最新提交以帮助我弄清楚代码是如何演变的。所以我想知道是否有一个工具可以帮助我从Xcode快速打开GitHub。所以我写了这个插件。当你在Xcode上编辑某个源文件时，很容易知道你正在哪个GitHub仓库工作，并且知道你正在编辑哪个文件。因此，它有意义的快速跳转到GitHub上的文件，快速跳转到GitHub上的当前编辑行的责任，快速跳转到Xcode正在工作的当前仓库的问题或PR。

## 菜单项

<img width="700" alt="2015-11-01 12 56 35" src="https://cloud.githubusercontent.com/assets/5022872/10864813/5df3f05e-8034-11e5-9f3e-03ae3fbc3cfc.png">

它有六个菜单项：

菜单标题 | 快捷方式 | GitHub URL模式（当我在LZAlbumManager.m 第40行编辑时）
----------- | ---------- | ----------------------------------
设置 | ⌃⇧⌘S |
仓库 | ⌃⇧⌘R | <https://github.com/lzwjava/LZAlbum>
问题 | ⌃⇧⌘I | <https://github.com/lzwjava/LZAlbum/issues>
拉取请求 | ⌃⇧⌘P | <https://github.com/lzwjava/LZAlbum/pulls>
快速文件 | ⌃⇧⌘Q | <https://github.com/lzwjava/LZAlbum/blob/fd7224/LZAlbum/manager/LZAlbumManager.m#L40>
历史记录 | ⌃⇧⌘L | <https://github.com/lzwjava/LZAlbum/commits/fd7224/LZAlbum/manager/LZAlbumManager.m>
责任 | ⌃⇧⌘B | <https://github.com/lzwjava/LZAlbum/blame/fd7224/LZAlbum/manager/LZAlbumManager.m#L40>
通知 | ⌃⇧⌘N | <https://github.com/leancloud/LZAlbum/notifications?all=1>

快捷方式是精心设计的。它们不会与Xcode默认快捷方式冲突。快捷方式模式是 ⌃⇧⌘（Ctrl+Shift+Command），加上菜单标题的第一个字符。

## 自定义

有时，你可能想快速跳转到维基。这是方法，打开设置：

<img width="500" alt="2015-11-01 12 56 35" src="https://cloud.githubusercontent.com/assets/5022872/10864939/fa83f286-8037-11e5-97d7-e9549485b11d.png">

例如，

快速文件，模式和实际URL：

```
           {git_remote_url}       /blob/{commit}/          {file_path}         #{selection}
https://github.com/lzwjava/LZAlbum/blob/fd7224/LZAlbum/manager/LZAlbumManager.m#L40-L43
```

{commit} 是当前分支的最新提交哈希。这比使用分支好。因为分支的HEAD可能会改变。所以代码在第40行-43行中的代码可能也会改变。

所以如果你想添加一个快捷方式到当前仓库的维基，只需添加一个菜单项并将模式设置为 `{git_remote_url}/wiki`。

在设置中，`Clear Default Repos` 说如果你有多个git远程，当第一次触发时，它会要求你选择其中一个：

<img width="400" src="https://cloud.githubusercontent.com/assets/5022872/10865120/5794994a-803c-11e5-9527-965f7e617e8f.png">

然后插件会记住你选择的内容。因此，当你再次触发菜单时，将打开该远程仓库作为默认值。按钮 `Clear Default Repos` 将清除此设置，将要求你再次选择。

## 安装

推荐使用 [Alcatraz](http://alcatraz.io/)，可参考巧神的一遍[博客](http://blog.devtang.com/blog/2014/03/05/use-alcatraz-to-manage-xcode-plugins/)。安装好后，按照上图搜索 `Reveal In GitHub`，点击 `Install` 即可。

如果不使用这个工具的话，那么也只需三步：

* 克隆该项目到本地。
* 打开 xcodeproj，点击 Build 构建。这会在目录`~/Library/Application Support/Developer/Shared/Xcode/Plug-ins` 生成 Reveal-In-GitHub.xcplugin 文件。
* 重启 Xcode，打开任意一个放在 GitHub 上的项目。按下 `Ctrl+Shift+Command+B` 即可。

## 致谢

在开发过程中，发现另一个插件 [ShowInGitHub](https://github.com/larsxschneider/ShowInGitHub) 做了类似的事情。我从中学到了一些技术。感谢这个。

## 许可证

MIT
