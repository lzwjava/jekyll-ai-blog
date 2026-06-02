---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QuickTransfer 无线网络缺少网关地址
translated: true
type: note
---

**问题**：为什么在 iPhone 上，DJI Mini 3 的 QuickTransfer Wi-Fi 只显示 IP 地址和子网掩码，没有网关？

**回答**：
DJI Mini 3 的 **QuickTransfer** 模式会在无人机与 iPhone 之间建立直连的点对点 Wi-Fi 连接。这是一个私有的、隔离的网络，专为从无人机存储向手机（通过 DJI Fly app）进行高速文件传输（最高可达 25 MB/s）而设计。它 **不是** 一个可连接互联网的完整网络，这解释了为何没有显示网关（路由器地址）。

### 为何不显示网关
- 在标准家庭或公共 Wi-Fi 中，手机会连接到路由器，路由器充当连接互联网的 **网关**。iPhone Wi-Fi 详情中的网关字段指向该路由器（例如 192.168.1.1）。
- 在 QuickTransfer 模式下，无人机本身充当 Wi-Fi 接入点（类似于简单的 ad-hoc 或直连 Wi-Fi 服务器），**不涉及路由器或互联网接入**。
- 连接仅限于本地——iPhone 会获得一个 IP 地址（通常类似 192.168.x.x）和一个子网掩码（通常为 255.255.255.0），但 **没有网关**，因为不存在将流量路由到无人机和手机之外的路由设备。
- 这完全是 iOS 设备上 DJI QuickTransfer 的正常预期行为。DJI Fly app 通过此直连链路处理所有通信，其中蓝牙用于初始配对/握手，Wi-Fi 用于实际的数据传输。

### DJI Mini 3 QuickTransfer 工作原理
1.  开启无人机电源，**快速按电源按钮三次** 进入 QuickTransfer 模式（状态指示灯闪烁蓝色）。
2.  打开 DJI Fly app（确保蓝牙和 Wi-Fi 已开启，并授予“本地网络”权限）。
3.  app 会提示连接至无人机的 Wi-Fi 网络（名称类似 "DJI_Mini3_XXXXXX"）。
4.  iPhone 会自动或手动加入该网络。您可能会在 Wi-Fi 设置中看到有限的详情（仅 IP 地址和子网掩码）。
5.  连接成功后，app 中将显示无人机的相册以供快速下载。

**注意**：在 iOS 上，无人机的 Wi-Fi 网络在设置中通常不会显示可见的密码——app 会管理连接。

### 传输失败时的常见问题与解决方法
-   关闭 **蜂窝数据**（或先开启飞行模式，然后重新启用 Wi-Fi 和蓝牙）——iPhone 有时会尝试使用移动数据，而非无人机的 Wi-Fi。
-   进入 iPhone **设置 > 隐私与安全性 > 本地网络**，确保允许 DJI Fly 访问。
-   重启无人机和 iPhone，并关闭后重新打开 DJI Fly app。
-   在 iPhone 设置中忘记无人机的 Wi-Fi 网络，然后重试（这会清除旧的缓存连接）。
-   更新 DJI Fly app 和无人机固件。
-   确保两台设备均有足够的存储空间，且无人机中的 microSD 卡已正确插入。

这种直连设计使传输快速简单，无需互联网或遥控器。这并非故障——不显示网关是设计使然。

**参考资料**：
- https://support.dji.com/help/content?customId=01700011149&spaceId=17&re=US&lang=en (DJI 官方 QuickTransfer 指南)
- https://www.heliguy.com/blogs/knowledge-base/how-do-i-use-dji-mini-3-s-quicktransfer/
- DJI Mini 3 用户手册及多位用户报告确认的直连 Wi-Fi 行为。
