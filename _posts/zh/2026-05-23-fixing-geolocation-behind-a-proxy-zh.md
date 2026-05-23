---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在代理后修复地理位置定位
translated: true
type: note
---

**问题：** `ww weather` 使用了 `wttr.in`，该服务通过 IP 自动检测位置。但由于你的流量经过洛杉矶的 hysteria2 代理服务器，它显示的是洛杉矶天气，而非广州天气。

**尝试 1 — macOS CoreLocation（GPS）：**
- 编写了一个使用 `CoreLocation` 框架获取真实 GPS 坐标的 Swift 脚本
- 失败：macOS Sequoia 要求为终端授予定位服务权限，这需要在系统设置中进行 GUI 交互。请求最终超时。

**尝试 2 — WiFi BSSID 地理定位：**
- 尝试通过 CoreWLAN、`system_profiler`、`ioreg` 和旧版 `airport` CLI 获取无线路由器的 BSSID（MAC 地址）
- 全面失败：macOS Sequoia 出于隐私考虑，对 SSID/BSSID 进行了屏蔽。`ioreg` 显示 `<SSID Redacted>`，BSSID 为 `000000000000`。即使是编译后的 Swift 二进制文件也遇到同样问题——操作系统在未获得定位服务授权的情况下，在核心层面阻止了该数据。

**尝试 3 — 路由器管理页面（192.168.1.1）：**
- 你的路由器运行 OpenWrt/LuCI，地址为 192.168.1.1
- 成功访问 LuCI 网页，但 API 接口（`/cgi-bin/luci/api/status`、`/cgi-bin/luci/api/network/wireless`）未注册——无法在没有认证的情况下通过编程方式获取 WAN IP 或 WiFi 信息

**尝试 4 — 绕过代理进行 IP 地理定位（最终方案）：**
- 关键思路：使用 `curl --noproxy '*'` 或 Python 的 `urllib.ProxyHandler({})` 绕过 hysteria2 代理，直接从真实 IP（中国电信骨干网，14.19.30.x）访问互联网
- 测试了三个地理定位服务：
  - `ipinfo.io` → 深圳（22.54, 114.06）——城市错误，偏差约 100 公里
  - `ip-api.com` → **广州**（23.12, 113.25）——正确！接近增城
  - `ipapi.co` → 返回空值（受速率限制）
- 最终方案：采用 `ip-api.com`——对中国运营商 IP 更准确，正确识别为广州

**`--detail` 显示的内容及各数据来源：**
- **城市**：通过你的真实（非代理）WAN IP 从 `ip-api.com` 获取的地理定位
- **运营商**：`ip-api.com` —— "Chinanet (Chinanet GD)" = 中国电信广东骨干网
- **本地 IP**：`ipconfig getifaddr en0` ——你在路由器上的局域网地址
- **网关**：解析 `netstat -rn` 中的默认路由 —— 你的路由器地址 192.168.1.1
- **WiFi 信道/PHY**：`system_profiler SPAirPortDataType` —— 该数据未被屏蔽，仅 SSID/BSSID 被隐藏
- **信号强度**：同一 `system_profiler` 输出 —— RSSI -49 dBm，信号良好

**为什么增城显示为"广州"：** 增城是广州市的一个区。IP 地理定位只能解析到城市级别，而非区级。`ip-api.com` 提供的坐标（23.12, 113.25）实际上非常接近增城中心。就天气而言，两者相同——距离仅 30 公里以内。