---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安全弹出Mac宗卷
translated: true
type: note
---

问题：在 Mac 上，如果 Finder 正在使用某个宗卷，我能否将光标移动到其他文件夹，然后弹出该磁盘？

答案：

不完全如此。在 macOS 上，如果一个宗卷（如外置驱动器）正在“使用中”，Finder 或其他应用可能会阻止其弹出。仅仅将 Finder 光标移动到其他文件夹**并不会自动释放该宗卷**。关键因素在于**是否有任何进程或应用正在主动访问该宗卷上的文件**。

以下是安全弹出它的方法：

1. **关闭该宗卷上的所有打开文件或窗口**。
2. **退出可能正在使用该驱动器文件的应用**（包括显示该驱动器的 Finder 窗口）。
3. 一旦没有任何内容在访问该宗卷，你可以：

   * 在桌面或 Finder 中右键单击该驱动器 → *弹出*。
   * 将驱动器图标拖到废纸篓（它会变为弹出符号）。
4. 如果系统仍然显示磁盘在使用中，你可以检查哪个进程正在使用它：

   * 打开**终端**并运行：

     ```bash
     lsof | grep /Volumes/YourDriveName
     ```

     这会显示访问该驱动器的文件或进程。然后你可以退出或强制关闭这些进程。

仅靠移动光标或在 Finder 中切换文件夹，如果仍有后台进程在使用该宗卷，则无法释放它。

参考：

* [Apple 支持 – 弹出外置驱动器](https://support.apple.com/guide/mac-help/eject-an-external-drive-mchlp2591/mac)
* [Macworld – 如何强制弹出卡住的驱动器](https://www.macworld.com/article/671749/how-to-force-eject-an-external-drive-mac.html)
