---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows专属软件类别
translated: true
type: note
---

**问题：哪些软件仅存在于 Windows 上（或强烈偏向 Windows 独占）？**

Windows 仍有大量软件要么在 macOS/Linux 上不存在，要么仅在 Windows 上表现最佳。最大的类别包括：

## 1. 专业企业软件

### 微软生态系统

* Microsoft Access — 数据库桌面应用（无原生 Mac/Linux 版本）
* Visual Basic 6 遗留应用 — 许多老式企业系统仍依赖 Windows
* Power BI Desktop — 仅限 Windows 的桌面应用（虽有 Web 版本，但完整创作功能集中于 Windows）
* SQL Server Management Studio (SSMS) — 仅限 Windows

### 企业 / 政府

许多公司运行：

* ERP 客户端
* 银行软件
* 工业控制软件
* 内部 .NET 应用程序

因为这些系统围绕以下技术构建：

* .NET Framework
* COM
* Active Directory
* Windows 身份验证

---

## 2. 游戏

Windows 主导 PC 游戏领域。

示例：

* 大多数 DirectX 游戏
* 受反作弊保护的游戏

一些历史上需要 Windows 的游戏：

* 《Valorant》（Vanguard 反作弊）
* 许多电竞游戏
* 许多 AAA 大作首发版本

原因：

```
游戏引擎
    |
DirectX 12
    |
Windows GPU 驱动栈
    |
反作弊内核驱动
```

Linux/macOS 往往无法支持完整链路。

---

## 3. 工程 / CAD / 3D

大量工业软件以 Windows 为首选：

* Autodesk AutoCAD（Windows 支持最全面）
* Dassault Systèmes CATIA
* SolidWorks
* Siemens NX
* 许多工厂仿真工具

机械工程公司通常统一采用 Windows 平台。

---

## 4. 硬件厂商工具

一个巨大的 Windows 独占领域：

### 主板 / GPU 调优

* MSI Afterburner
* ASUS Armoury Crate
* Gigabyte Control Center

### 设备固件

* 打印机/扫描仪工具
* BIOS 更新工具
* RGB 控制器

Linux/macOS 往往缺乏官方工具。

---

## 5. 企业 Windows 管理

Windows 拥有独特的管理工具：

* Active Directory
* 组策略编辑器
* Windows Server 管理
* SCCM / Intune 桌面管理
* PowerShell + Windows API

大型组织通常依赖这些工具。

---

## 6. .NET Framework 遗留软件

现代 .NET 已跨平台，但老式企业应用：

```
C#
 |
.NET Framework 4.x
 |
WPF / WinForms
 |
Windows API
```

仅限 Windows。

示例：

* 会计软件
* 医院系统
* 政府应用程序

---

## 7. Adobe / 创意领域差异

大多数 Adobe 应用现已支持 macOS，但 Windows 仍具优势：

* 更好的 GPU 兼容性
* 更多插件
* 更广泛的硬件支持

尤其在以下领域：

* 视频制作
* 3D 渲染
* AI 图像工具

---

## 8. AI / ML 工具（部分 Windows 优势）

大多数严肃的机器学习在 Linux 上进行，但 Windows 拥有一些独特工具：

* 通过 WSL2 进行 CUDA 开发
* NVIDIA Studio 驱动
* 游戏级 GPU 生态系统
* 部分图形化 AI 工具

然而：

```
研究型机器学习：
Linux > Windows

企业桌面端 AI：
Windows > Linux
```

---

## 9. Windows 为何拥有这些优势

历史原因：

```
1980年代
IBM PC
    |
DOS
    |
Windows
    |
企业采用
    |
庞大生态锁定
```

Windows 成为以下领域的默认平台：

* 办公环境
* 工厂
* 游戏
* 工程
* 企业 IT

---

对于像您这样的开发者 / AI 工程师：

```
机器学习：
Linux Ubuntu > Windows

软件开发：
Linux/macOS > Windows（通常）

游戏：
Windows > 其他一切

企业兼容性：
Windows > 其他一切
```

当前常见的配置：

```
MacBook
    |
编码 / SSH
    |
Linux GPU 服务器
    |
训练

Windows PC
    |
游戏 + 专有软件
```

这就是为什么即使主开发环境是 Linux，许多 AI 工程师仍会保留一台 Windows 机器。
