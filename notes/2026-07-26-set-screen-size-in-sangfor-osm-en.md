---
audio: false
generated: true
image: false
lang: en
layout: post
title: Set Screen Size in Sangfor OSM
translated: false
type: note
---

**Question: How to set screen size (e.g. 1600×1200) in 深信服运维安全管理系统 remote desktop session?**

In **深信服运维安全管理系统 (Sangfor OSM)**, the resolution is usually controlled by the **RDP client settings inside the web portal**, not by Windows display settings.

Try these:

### Method 1: Set resolution before connecting (RDP Web)

1. Login to 深信服运维安全管理系统 web portal.
2. Go to:

```
运维中心 / 资产管理
    ↓
选择服务器
    ↓
RDP / Remote Desktop
```

3. Before clicking **连接**, look for:

```
连接设置
高级设置
显示设置
分辨率
```

4. Select:

```
1600 × 1200
```

or:

```
自定义分辨率
宽度: 1600
高度: 1200
```

Then connect.

---

### Method 2: If using Windows Remote Desktop Client (mstsc)

If Sangfor gives you an RDP file:

1. Download/open the `.rdp` file.
2. Edit it with Notepad.

Add:

```
desktopwidth:i:1600
desktopheight:i:1200
session bpp:i:32
```

Example:

```
screen mode id:i:2
desktopwidth:i:1600
desktopheight:i:1200
session bpp:i:32
```

Save and open again.

---

### Method 3: If Sangfor uses its own EasyConnect tunnel

The flow is usually:

```
Your PC
   |
EasyConnect VPN
   |
Sangfor OSM
   |
RDP gateway
   |
Target Windows Server
```

The resolution is negotiated by the RDP client at the last step.

So:

* EasyConnect does **not** set the screen size.
* Sangfor OSM RDP module sets it.
* Windows mstsc settings can override it.

---

### Check if the RDP Web client supports it

Some Sangfor versions use HTML5 RDP. In that case:

Look for the toolbar after connecting:

```
☰
 └── Display
       ├── Fit to window
       ├── Actual size
       └── Resolution
```

Set:

```
1600x1200
```

---

If you tell me your Sangfor version (for example **M7.6.7**) and whether you connect using **RDP Web** or **download .rdp + mstsc**, I can give the exact menu path.
