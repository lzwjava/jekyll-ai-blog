---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 定制USB盘并添加背景和图标
translated: true
type: post
---

这篇文章最初用中文撰写并发布在QQ空间。

---

**I. 定制USB驱动器图标:**

1. 首先，选择你喜欢的图标。图标文件的扩展名应为`.ico`。
2. 将图标文件复制到你的USB驱动器并在USB驱动器上创建一个新的文本文档。
3. 在文本文档中写入以下内容：

   ```
   [autorun]
   ICON=\xxx.ico,0
   ```

   其中`xxx.ico`是你的图标文件的名称（包括扩展名）。
4. 将文本文件保存为`autorun.inf`。
   **注意：** 确保将扩展名更改为`.inf`，而不是`.txt`。如果文件图标变为带有黄色齿轮的图标，则说明你做对了。
   拔下USB驱动器并重新插入。你会看到USB驱动器的图标已更改为你选择的图标。
   这种方法也可以用于外接硬盘或CD/DVD刻录。

**II. 定制背景:**

1. 首先，选择你喜欢的背景图像并将其复制到你的USB驱动器。
2. 创建一个新的文本文件并将以下内容复制进去：

   ```
   [ExtShellFolderViews]
   {BE098140-A513-11D0-A3A4-00C04FD706EC}={BE098140-A513-11D0-A3A4-00C04FD706EC}
   [{BE098140-A513-11D0-A3A4-00C04FD706EC}]
   Attributes=1
   IconArea_Image=aaa.jpg
   IconArea_Text=0x00FFFFFF
   [.ShellClassInfo]
   ConfirmFileOp=0
   ```

   这段代码的意思是：

   其中`aaa.jpg`是你选择的图像文件的名称（包括扩展名）。

   `IconArea_Text= 0x00FFFFFF`  这行代码改变了USB驱动器上的文本颜色。

   颜色代码是：

   * 红色: `0x000000FF`
   * 黄色: `0x0000FFFF`
   * 蓝色: `0x00FF0000`
   * 灰色: `0x00808080`
   * 橄榄绿: `0x006BDEC7`
   * 黑色: `0x00000000`
   * Excel背景颜色: `0x00848284`
   * 白色: `0x00FFFFFF`
   * 绿色: `0x00008000`
   * 紫色: `0x00C000C0`

   选择你喜欢的颜色（与你的背景相配）并替换现有的颜色代码。

   你可以在`IconArea_Text=`后面更改颜色以适应你的喜好。

3. 将文本文件保存为`Desktop.ini`。修改完成。
   刷新USB驱动器，你应该会看到更改。
   上述四个文件都可以隐藏以防止误删。
   改变图标后，需要拔下并重新插入USB驱动器才能看到效果。
   改变背景后，刷新USB驱动器以查看更改。
