---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 监控路由器网络流量
translated: true
type: note
---

### 监控360 Wi-Fi 6路由器T7的HTTP请求与TCP连接

360 T7运行定制化基于Linux的固件（非原生完整OpenWrt），因此在原厂配置下的监控能力相比完整Linux系统有所限制。通过管理员权限（网页界面访问）可查看基础日志。若需实现实时HTTP请求记录或TCP连接追踪等深度"破解"功能，最合规的方式是刷入官方支持的OpenWrt系统，开启SSH后使用标准Linux工具。**警告：刷入第三方固件会导致保修失效并可能造成设备变砖——请务必提前备份并严格遵循教程操作，仅对自有设备进行修改。**

#### 1. **获取原厂固件管理员权限**
   - 通过Wi-Fi或以太网连接路由器
   - 浏览器访问 `http://ihome.360.cn` 或 `http://192.168.0.1`（默认IP）
   - 登录：用户名为`admin`，密码见路由器标签（通常为`admin`或特定字符串如`360XXXXXX`——请查看底部贴纸）
   - 进入后访问**系统 > 日志**或**安全 > 日志**查看基础系统与流量日志。这里会显示防火墙拦截记录、连接信息及部分HTTP活动（如被屏蔽网站或入侵尝试），但不包含完整HTTP请求详情

   **网页界面基础监控功能：**
   - **系统日志**：查看近期事件，包括TCP连接尝试与错误记录。支持日志导出（解密可能需要标签密码）
   - **流量统计**：通过**状态 > 网络**或**高级 > 流量监控**查看各设备/IP的带宽使用情况，但无法获取细粒度HTTP/TCP数据
   - 局限性：无法实时查看HTTP载荷；日志均为高层级摘要，未经认证无法导出

#### 2. **高级监控：刷入OpenWrt获取Shell访问权限**
   360 T7（MT7981B芯片组）已获OpenWrt 23.05+快照版支持。刷机后可通过SSH获得完整root shell权限，运行`tcpdump`等工具进行抓包，使用`logread`查看日志

   **刷入OpenWrt步骤（概要说明，请遵循官方指南）：**
   1. 从OpenWrt下载站获取出厂镜像（搜索"Qihoo 360T7 sysupgrade.bin"或出厂镜像）
   2. 备份原厂固件：通过网页界面进入**系统 > 备份**下载配置/固件
   3. 网页界面刷入：通过**系统 > 固件升级**选择.bin文件并应用（路由器将重启进入OpenWrt）
   4. 刷机后：通过`http://192.168.1.1`访问网页界面（LuCI界面），用户名为`root`，初始无密码——请立即通过SSH或网页界面设置密码
   5. 启用SSH：默认开启22端口。从PC连接：`ssh root@192.168.1.1`（Windows系统使用PuTTY）

   **风险应对**：若出现故障，可使用TFTP恢复（启动时按住复位键）或串口控制台（需UART适配器）

#### 3. **OpenWrt系统监控（通过SSH Shell）**
   以root身份SSH登录后，路由器即作为迷你Linux系统运行。如需安装软件包可通过`opkg update && opkg install tcpdump`（内置存储128MB，请保持轻量）

   - **列出所有当前TCP连接（静态视图）：**
     ```
     ss -tunap
     ```
     - 显示已建立/监听中的TCP套接字、端口及进程（示例：`tcp ESTAB 0 0 192.168.1.1:80 192.168.1.100:54321 users:(("uhttpd",pid=1234,fd=3))`）
     - 实时查看：`watch -n 1 'ss -tunap'`

   - **实时TCP流量捕获：**
     按需安装：`opkg update && opkg install tcpdump`
     ```
     tcpdump -i any tcp -n -v
     ```
     - `-i any`：所有接口（br-lan对应LAN，eth0.2对应WAN）
     - HTTP过滤：`tcpdump -i any tcp port 80 -n -v -A`（`-A`参数以ASCII显示HTTP头/请求载荷）
     - 保存文件：`tcpdump -i any tcp -w /tmp/capture.pcap`（通过SCP下载：`scp root@192.168.1.1:/tmp/capture.pcap .`）
     - 对于HTTPS（443端口），注意载荷已加密——建议使用Wireshark离线分析

   - **监控HTTP请求日志：**
     - 系统日志（包含uhttpd网络服务器记录）：`logread | grep uhttpd` 或实时查看 `logread -f`
     - 启用详细HTTP日志：编辑`/etc/config/uhttpd`（网络服务器配置），添加`option log_file '/var/log/uhttpd.log'`，执行`/etc/init.d/uhttpd restart`。追踪日志：`tail -f /var/log/uhttpd.log`（显示GET/POST请求、IP地址及URL）
     - 全网络HTTP监控：使用上述`tcpdump`方法，或安装`ngrep`（`opkg install ngrep`）：`ngrep -d any 'GET|POST|HTTP' -O /tmp/http.pcap`

   - **防火墙/连接日志：**
     - 启用规则日志：`uci set firewall.@rule[0].log='1'; uci commit; /etc/init.d/firewall restart`
     - 查看：`logread | grep fw`（显示丢弃/接受的TCP连接）

#### 合规"破解"技巧
- **安全加固**：配置完成后立即修改root密码（`passwd`），在`/etc/ssh/sshd_config`中禁用密码认证仅保留密钥登录，防火墙限制SSH仅限LAN访问
- **性能注意**：T7配备256MB内存——避免长期重度抓包导致内存溢出
- **恢复原厂**：从360官网下载官方固件，通过OpenWrt的sysupgrade上传（必要时使用`--force`参数）
- 建议在安全环境中测试；若需图形化分析，可通过SCP将.pcap文件传输至PC并用Wireshark打开

以上方案可提供全面监控视野。若原厂界面已满足基础需求，建议保持现状以避免刷机风险

[OpenWrt技术数据：Qihoo 360T7](https://openwrt.org/toh/hwdata/qihoohardware/qihoohardware_360t7)
[360 T7U手册（日志章节）](https://ipc-pr-cdn.jia.360.cn/ipc-pr/luyouqiT7U.pdf)
[OpenWrt日志指南](https://openwrt.org/docs/guide-user/base-system/log.essentials)
[360论坛：日志导出](https://bbs.360.cn/forum-7007-1.html)
