---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS与Linux中的网络服务
translated: true
type: note
---

### macOS 与 Linux 中的网络服务及相关术语

这些术语主要指向网络服务名称，通常定义在 macOS 和 Linux 系统的 `/etc/services` 文件中。该文件将标准网络服务的服务名称映射到端口号和协议。其中部分为官方 IANA 注册服务，其他则是系统配置中常用的别名或协议名称。以下基于 macOS（采用类 BSD 基础）和 Linux 发行版中的标准用法对各术语进行解释。

- **service**：这是 macOS（通过 launchd）和 Linux（通过 systemd 或 init 系统）中系统守护进程或进程的通用术语。它并非 `/etc/services` 中的特定网络服务，但可能指代 Linux 中用于管理传统 SysV 初始化脚本的 "service" 命令，或泛指任何后台服务。

- **ircu**：指代 IRCU（Internet Relay Chat Undernet）服务，一种 IRC 服务器软件的变体。使用端口 6667/tcp（有时也使用 udp）。在 Linux 中，可能与 ircu 或 undernet-ircu 等 IRC 守护进程相关联。现代 macOS 或 Linux 系统通常不预装，但可通过 ports 或软件包安装用于聊天服务器。

- **complex-link**：可能是 "commplex-link" 的拼写错误或变体，这是注册在端口 5001/tcp 的网络服务。用于通信多路复用链路（例如某些网络工具或协议中）。在 macOS 中，该端口与 AirPort/Time Capsule 配置或路由器管理工具（如 Netgear 或 Apple 设备）相关联。在 Linux 中，可能出现在防火墙规则或 netstat 输出中用于类似用途。

- **dhcpc**：DHCP 客户端服务的别名，使用端口 68/udp（也称为 bootpc）。这是 DHCP 的客户端端，用于动态获取 IP 地址。在 Linux 中由 dhclient 或 dhcpcd 等进程处理；在 macOS 中由 configd 或 bootpd（客户端模式）处理。

- **zeroconf**：指代零配置网络（Zeroconf），一种无需手动配置即可自动发现服务的协议。在 macOS 中实现为 Bonjour（使用端口 5353/udp 的 mDNS）。在 Linux 中通常为 Avahi（同样使用端口 5353/udp）。用于发现打印机、共享资源及其他本地网络服务。

- **ntp**：网络时间协议服务，用于通过网络同步系统时钟。使用端口 123/udp（有时也使用 tcp）。在 Linux 中由 ntpd 或 chronyd 处理；在 macOS 中由 ntpd 或内置时间同步守护进程处理。

- **http**：超文本传输协议，网络通信的基础。使用端口 80/tcp（有时使用 udp）。在 macOS 和 Linux 中均与 Apache（httpd）或 Nginx 等 Web 服务器相关联。

- **ssh**：安全外壳协议，用于安全远程访问和文件传输。使用端口 22/tcp（及 udp/sctp）。在 Linux 和 macOS 中，守护进程为 sshd，可通过系统偏好设置或 sshd_config 启用。

- **hgvirtgrp**：这似乎是与虚拟化相关的用户组引用，可能是 Linux 中 "libvirt group" 的变体或拼写错误（例如 libvirt 或 libvirt-qemu 组）。在 Linux 中，将用户加入 libvirt 组可授予其通过 libvirt 管理虚拟机（用于 KVM/QEMU）的权限。在 macOS 中，虚拟化使用 Hypervisor 框架，但不存在标准的 "hgvirtgrp" 组——可能指代用于 hypervisor/虚拟化工具（如 QEMU 或 Virt-Manager）的自定义组。若为特定组，请检查系统中的 `/etc/group` 文件。

这些术语常见于 `netstat`、`lsof` 或防火墙配置（如 macOS 的 pf、Linux 的 iptables/ufw）等工具中。如需准确定义，请查阅系统的 `/etc/services` 文件或 IANA 端口注册表。

**参考资料**
[服务名称与传输协议端口号注册表](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
[什么是带有 commplex-link 的开放端口？ - Apple 社区](https://discussions.apple.com/thread/7747034)
[在 macOS 上运行 virt-manager 和 libvirt](https://www.arthurkoziel.com/running-virt-manager-and-libvirt-on-macos/)
