---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在深信服OSM中设置屏幕尺寸
translated: true
type: note
---

**问：如何在深信服运维安全管理系统远程桌面会话中设置屏幕分辨率（例如 1600×1200）？**

在**深信服运维安全管理系统（Sangfor OSM）**中，分辨率通常由**Web 门户内的 RDP 客户端设置**控制，而非 Windows 显示设置。

请尝试以下方法：

### 方法一：连接前设置分辨率（RDP Web）

1. 登录深信服运维安全管理系统 Web 门户。
2. 进入：

```
运维中心 / 资产管理
    ↓
选择服务器
    ↓
RDP / 远程桌面
```

3. 在点击**连接**前，查找：

```
连接设置
高级设置
显示设置
分辨率
```

4. 选择：

```
1600 × 1200
```

或：

```
自定义分辨率
宽度: 1600
高度: 1200
```

然后点击连接。

---

### 方法二：如果使用 Windows 远程桌面客户端（mstsc）

若深信服提供 RDP 文件：

1. 下载/打开 `.rdp` 文件。
2. 用记事本编辑。

添加：

```
desktopwidth:i:1600
desktopheight:i:1200
session bpp:i:32
```

示例：

```
screen mode id:i:2
desktopwidth:i:1600
desktopheight:i:1200
session bpp:i:32
```

保存后重新打开。

---

### 方法三：如果深信服使用自有的 EasyConnect 隧道

流程通常为：

```
您的电脑
   |
EasyConnect VPN
   |
深信服 OSM
   |
RDP 网关
   |
目标 Windows 服务器
```

分辨率由最后一步的 RDP 客户端协商决定。

因此：

* EasyConnect **不**设置屏幕尺寸。
* 深信服 OSM 的 RDP 模块负责设置。
* Windows mstsc 设置可覆盖此项。

---

### 检查 RDP Web 客户端是否支持

部分深信服版本使用 HTML5 RDP。此时：

连接后查找工具栏：

```
☰
 └── 显示
       ├── 适应窗口
       ├── 实际大小
       └── 分辨率
```

设置：

```
1600x1200
```

---

如果您能提供深信服版本（例如 **M7.6.7**）以及连接方式是使用 **RDP Web** 还是**下载 .rdp 文件 + mstsc**，我可提供精确的菜单路径。