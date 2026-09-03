---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB显微镜AMCap和gloptics.net
translated: true
type: note
---

**问题：** 对于像 **星微光学 高倍电子显微镜 USB 高清工业维修测量鉴定数码放大镜** 这样的 USB 数字工业显微镜，是否使用 **AMCap**，并且 `gloptics.net` 是获取它的地方吗？

**回答：** 是的——**如果该显微镜在 Windows 系统中以标准 USB UVC 摄像头形式呈现**，AMCap 是一个非常常见的选择。

典型连接链路如下：

```text
USB 显微镜
      │
      ▼
Windows USB/UVC 驱动程序
      │
      ▼
"USB2.0 UVC PC Camera"
或
"GL USB2.0 UVC Camera Device"
      │
      ▼
     AMCap
      │
      ├── 显示显微镜实时图像
      ├── 快照
      ├── 视频捕获
      └── 有时支持显微镜的 ZOOM/SNAP 按钮
```

而且 **`gloptics.net` 确实与这些通用 USB 显微镜相关联**。我找到了一份实际的显微镜说明书，其中明确说明要去 `www.gloptics.net` 下载 **“USB Microscope Driver amcap software”**。([ncsciencefestival.org][1])

因此，对于您提到的这类显微镜，我建议尝试以下步骤：

1. 将 USB 显微镜插入 Windows 系统。
2. 打开 **设备管理器 → 摄像头 / 图像设备**。
3. 查看它是否显示为类似以下名称：

   ```text
   USB2.0 UVC PC Camera
   GL USB2.0 UVC Camera Device
   ```
4. 打开 **AMCap**。
5. `Devices` → 选择该显微镜。
6. 您应该就能看到显微镜的实时画面。

AMCap 本身基本上是一个 **USB 摄像头/UVC 查看器**，并非特殊的显微镜技术。其他 UVC 软件也可以使用。([Arducam][2])

### 一个重要的区别

如果您正在进行 **GPU/PCB 维修**，实际上有两个不同的层级：

```text
AMCap
  ↓
仅提供摄像头图像
```

与

```text
S-EYE / 测量软件
  ↓
图像
+ 测量
+ 校准
+ 距离/角度/直径测量
```

例如，显微镜供应商会将 AMCap 与测量软件区分开来：AMCap 处理摄像头源和捕获，而 S-EYE 提供测量功能。([jiusion.com][3])

所以，**对于检查 GPU 焊点、VRAM、MOSFET、线圈、PCB 走线等，AMCap 作为基本查看器完全够用**。您不一定需要供应商的花哨软件。

另外，是的：**`gloptics.net` → USB Microscope Driver / AMCap** 正是您记忆中的那个生态系统。([the-colliers.net][4])

[AMCap / USB 显微镜驱动程序信息](https://gloptics.net/?utm_source=chatgpt.com)

**参考资料：**

* [Jiusion USB 显微镜驱动程序指南](https://jiusion.com/pages/driver-microscope?utm_source=chatgpt.com)
* [数字显微镜连接说明](https://ncsciencefestival.org/sites/default/files/documents/Digital%20Microscope%20Connection%20Instructions.pdf?utm_source=chatgpt.com)
* [引用 gloptics.net + AMCap 的 USB 显微镜用户手册](https://www.the-colliers.net/docs/public/guides%20%26%20manuals/WiFi%20Box%20Digital%20Microscope%20User%20Manual.pdf?utm_source=chatgpt.com)

[1]: https://ncsciencefestival.org/sites/default/files/documents/Digital%20Microscope%20Connection%20Instructions.pdf?utm_source=chatgpt.com "数字显微镜连接说明"
[2]: https://docs.arducam.com/UVC-Camera/USB2-UVC-Camera-Kit/Quick-Start-Guide/Windows/?utm_source=chatgpt.com "Windows 上的 UVC 摄像头 - Arducam Wiki"
[3]: https://jiusion.com/pages/driver-microscope?utm_source=chatgpt.com "USB 显微镜驱动程序下载"
[4]: https://www.the-colliers.net/docs/public/guides%20%26%20manuals/WiFi%20Box%20Digital%20Microscope%20User%20Manual.pdf?utm_source=chatgpt.com "3. 如何在 PC / Windows 7/8/10 系统中安装 Amcap 软件（只有使用此软件，ZOOM 和 SNAP 按钮才能正常工作，并且使用此方法无需运行光盘）"