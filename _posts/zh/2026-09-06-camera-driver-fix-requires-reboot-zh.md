---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 摄像头驱动修复需要重启
translated: true
type: note
---

## 摘要

**问题所在：** 你的“GL USB2.0 UVC Camera Device”（GenesysLogic 芯片，`VID_A16F&PID_0304`）在此电脑上有两个相互冲突的驱动程序绑定：

| 节点 | 驱动程序 | 结果 |
|------|--------|--------|
| `…\7&2f50fd3d&0&0000` | **`glavcam.sys`**（`oem153.inf`） | ❌ 问题 39 — 驱动程序加载失败 |
| `…\6&349b1f0b&0&0000` | **Microsoft `usbvideo.sys`**（收件箱内置） | ✅ 可用 |

厂商的 `glavcam.sys` 是 **未签名的 Vista 时代“Longhorn DDK”驱动程序**，而你的系统启用了 **内存完整性（HVCI）**。代码完整性（事件 3111，状态 `0xC0000220`）拒绝加载该驱动，表现为 `0xC000026C`（STATUS_DRIVER_UNABLE_TO_LOAD）→“驱动程序无法在此设备上加载。”Windows 正确阻止了它——该驱动本来就不应在 Win10 24H2 上使用。

**我所执行的操作：**
1. `pnputil /delete-driver oem153.inf /uninstall /force` — 从驱动程序存储中移除了有问题的驱动包，并卸载了其设备 ✅
2. 删除了残留的 `glavcam` 内核服务（`sc delete glavcam`） ✅
3. 移除了失效的设备节点并重新扫描 ✅

**当前状态：** 不再有设备存在问题，`glavcam` 已完全移除，内存完整性保持开启（安全性未削弱）。摄像头的 USB 复合设备已连接，但 Windows 报告**需要重启**以完成摄像头接口的重新枚举——重启后它将自动绑定到已签名的收件箱内置 **`usbvideo.sys`**（即“USB2.0 UVC PC Camera”驱动程序，该驱动在同一摄像头型号上已正常工作）。

**下一步：** 重启电脑。需要我现在触发 `shutdown /r /t 0`，还是你方便时再重启？启动后，通过以下命令验证：
```
pnputil /enum-devices /deviceid "USB\VID_A16F&PID_0304"
```
——你应该会看到一个 `Camera` 类别的“USB2.0 UVC PC Camera”节点，`Driver Name: usbvideo.inf`，状态为 `Started`，并且摄像头会在应用程序（相机、Teams 等）中出现。