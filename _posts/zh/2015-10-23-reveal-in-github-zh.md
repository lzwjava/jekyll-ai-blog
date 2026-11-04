---
audio: false
generated: false
image: false
lang: zh
layout: post
title: Xcode插件：Reveal-In-GitHub
translated: true
type: post
---

这是来自 GitHub 项目 [https://github.com/lzwjava/Reveal-In-GitHub](https://github.com/lzwjava/Reveal-In-GitHub) 的 README.md。

---

# Reveal-In-GitHub

一款 Xcode 插件，旨在无缝导航到当前仓库中关键的 GitHub 功能。只需点击一下，即可轻松访问 GitHub 上的历史记录、指责、拉取请求、问题和通知，一切都在几秒钟内完成。

![plugin](https://cloud.githubusercontent.com/assets/5022872/10867703/96e980be-80ab-11e5-9aaa-a06ef476b7f7.gif)

我的公司在 GitHub 上工作。我经常打开 GitHub。有时我在 Xcode 上编辑代码并看不懂某段代码，于是我会到 GitHub 上查看指责（blame）信息。有时我查找某个文件最近的提交记录，以帮助理解代码的演变过程。所以我想知道是否有工具可以帮助我从 Xcode 快速打开 GitHub。因此我编写了这个插件。当你在 Xcode 中编辑某个源文件时，很容易知道你当前在哪个 GitHub 仓库工作，也知道你在编辑哪个文件。因此，快速跳转到 GitHub 上的该文件、快速跳转到当前编辑行的指责页面、快速跳转到当前仓库的 issues 或 PRs，都是很有意义的。

## 菜单项

<img width="700" alt="2015-11-01 12 56 35" src="https://cloud.githubusercontent.com/assets/5022872/10864813/5df3f05e-8034-11e5-9f3e-03ae3fbc3cfc.png">

共有六个菜单项：

菜单标题       | 快捷键                | GitHub URL 模式（当我编辑 LZAlbumManager.m 第 40 行时）
----------------|-----------------------|----------------------------------
设置            |⌃⇧⌘S |
仓库            |⌃⇧⌘R | <https://github.com/lzwjava/LZAlbum>
问题            |⌃⇧⌘I | <https://github.com/lzwjava/LZAlbum/issues>
拉取请求        |⌃⇧⌘P | <https://github.com/lzwjava/LZAlbum/pulls>
快速文件        |⌃⇧⌘Q | <https://github.com/lzwjava/LZAlbum/blob/fd7224/LZAlbum/manager/LZAlbumManager.m#L40>
历史列表        |⌃⇧⌘L | <https://github.com/lzwjava/LZAlbum/commits/fd7224/LZAlbum/manager/LZAlbumManager.m>
指责            |⌃⇧⌘B | <https://github.com/lzwjava/LZAlbum/blame/fd7224/LZAlbum/manager/LZAlbumManager.m#L40>
通知            |⌃⇧⌘N | <https://github.com/leancloud/LZAlbum/notifications?all=1>

这些快捷键经过精心设计，不会与 Xcode 的默认快捷键冲突。快捷键模式为 ⌃⇧⌘（Ctrl+Shift+Command），再加上菜单标题的首字母。

## 自定义

有时你希望快速跳转到 Wiki。操作如下，打开设置：

<img width="500" alt="2015-11-01 12 56 35" src="https://cloud.githubusercontent.com/assets/5022872/10864939/fa83f286-8037-11e5-97d7-e9549485b11d.png">

例如，快速文件的模式与实际 URL：

```
           {git_remote_url}       /blob/{commit}/          {file_path}         #{selection}
https://github.com/lzwjava/LZAlbum/blob/fd7224/LZAlbum/manager/LZAlbumManager.m#L40-L43
```

`{commit}` 是当前分支的最新提交哈希。使用它比使用分支更好，因为分支的 HEAD 可能会变化，导致 #L40-L43 的代码也可能发生改变。

因此，如果你想为当前仓库的 Wiki 添加一个快捷方式，只需添加一个菜单项，并将模式设置为 `{git_remote_url}/wiki`。

在设置中，`Clear Default Repos` 表示如果你有多个 Git 远程仓库，首次触发时会询问你选择其中一个：

<img width="400" src="https://cloud.githubusercontent.com/assets/5022872/10865120/5794994a-803c-11e5-9527-965f7e617e8f.png">

之后插件会记住你的选择，再次触发菜单时会默认打开该远程仓库。点击 `Clear Default Repos` 按钮会清除这一设置，再次询问你选择。

## 安装

推荐使用 [Alcatraz](http://alcatraz.io/) 安装，

![qq20151101-1 2x](https://cloud.githubusercontent.com/assets/5022872/10867743/0ce351c6-80ae-11e5-82e2-f740887153f7.jpg)

或者

1. 克隆此仓库。
2. 打开 `Reveal-In-GitHub.xcodeproj`，然后构建它。
3. `Reveal-In-GitHub.xcplugin` 应位于 `~/Library/Application Support/Developer/Shared/Xcode/Plug-ins`。
4. 重启 Xcode。
5. 打开任意一个 GitHub 项目，按下 ⌃⇧⌘B (Ctrl+Shift+Command+B) 查看代码的指责（blame）。

## 安装

推荐使用 [Alcatraz](http://alcatraz.io/)，可参考巧神的一遍[博客](http://blog.devtang.com/blog/2014/03/05/use-alcatraz-to-manage-xcode-plugins/)。安装好后，按照上图搜索 `Reveal In GitHub`，点击 `Install` 即可。

如果不使用这个工具的话，那么也只需三步：

* 克隆该项目到本地。
* 打开 xcodeproj，点击 Build 构建。这会在目录`~/Library/Application Support/Developer/Shared/Xcode/Plug-ins` 生成 Reveal-In-GitHub.xcplugin 文件。
* 重启 Xcode，打开任意一个放在 GitHub 上的项目。按下 `Ctrl+Shift+Command+B` 即可。

## 致谢

在开发过程中，发现另一个插件 [ShowInGitHub](https://github.com/larsxschneider/ShowInGitHub) 也做了类似的事情。我从中学到了一些技术。特此感谢。

## 许可证

MIT