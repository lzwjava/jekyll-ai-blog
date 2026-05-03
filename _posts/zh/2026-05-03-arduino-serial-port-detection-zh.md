---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino串口检测报告
translated: true
type: note
---

## Arduino 连接报告

### 检测方法

1. **`ls /dev/cu.* /dev/tty.*`** — 列出 macOS 上所有串行/字符设备，并筛选出 `usb`/`arduino`/`serial` 相关模式。这是主要的检测方式。
2. **`ioreg -c IOSerialBSDClient`** — 查询 macOS I/O 注册表，获取串行设备的内核级驱动信息。
3. **`stat`** + **`lsof`** — 检查设备文件元数据以及是否有进程正在使用该端口。

---

### 检测结果

| 属性 | 值 |
|---|---|
| **呼叫设备** | `/dev/cu.usbserial-1110` |
| **拨入设备** | `/dev/tty.usbserial-1110` |
| **TTY 后缀** | `1110`（USB 序列号后 4 位） |
| **连接时间** | 2026-05-03 23:30:19 |
| **权限** | `crw-rw-rw-`（所有用户均可读写） |
| **驱动程序** | `IOSerialBSDClient`（苹果串行系列） |
| **端口状态** | **未使用**（无进程打开） |
| **芯片类型** | 可能为 **CH340**（克隆版 Uno）或 **FTDI** — 后缀 `usbserial` 表示 USB 转 UART 桥接芯片 |

### 备注

- 使用 `/dev/cu.usbserial-1110` 上传程序或读取串行输出
- 默认 Arduino 波特率为 `9600`
- `tty.*` 用于传入连接；`cu.*`（call-up）用于传出/Arduino 通信
- `system_profiler SPUSBDataType` 返回为空 — 这可能是 M 系列 Mac 在 USB 子系统报告方面的限制