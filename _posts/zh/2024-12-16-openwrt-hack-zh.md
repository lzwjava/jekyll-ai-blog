---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 使用 OpenClash 和 Shadowsocks 增强 OpenWRT
translated: true
type: post
---

### 更新软件包列表

```bash
root@OpenWrt:~# opkg update
Downloading https://downloads.openwrt.org/releases/22.03.3/targets/ramips/mt7621/packages/Packages.gz
Updated list of available packages in /var/opkg-lists/openwrt_core
Downloading https://downloads.openwrt.org/releases/22.03.3/targets/ramips/mt7621/packages/Packages.sig
Signature check passed.
Downloading https://downloads.openwrt.org/releases/22.03.3/packages/mipsel_24kc/base/Packages.gz
Updated list of available packages in /var/opkg-lists/openwrt_base
Downloading https://downloads.openwrt.org/releases/22.03.3/packages/mipsel_24kc/base/Packages.sig
Signature check passed.
Downloading https://downloads.openwrt.org/releases/22.03.3/packages/mipsel_24kc/luci/Packages.gz
Updated list of available packages in /var/opkg-lists/openwrt_luci
Downloading https://downloads.openwrt.org/releases/22.03.3/packages/mipsel_24kc/luci/Packages.sig
Signature check passed.
root@OpenWrt:~#
```

### 安装 Shadowsocks 插件

要安装 `luci-app-shadowsocks-libev` 插件：

```bash
root@OpenWrt:~# opkg install luci-app-shadowsocks-libev
Installing luci-app-shadowsocks-libev (git-22.066.30464-cea4277) to root...
Downloading https://downloads.openwrt.org/releases/22.03.3/packages/mipsel_24kc/luci/luci-app-shadowsocks-libev_git-22.066.30464-cea4277_all.ipk
Configuring luci-app-shadowsocks-libev.
```

### 安装 OpenClash

有关详细信息，请参阅 OpenClash 的 [GitHub 仓库](https://github.com/vernesong/OpenClash?tab=readme-ov-file)。以下是安装必要组件的步骤。

1. 安装 OpenSSH SFTP 服务器：

   ```bash
   opkg install openssh-sftp-server
   ```

2. 使用 `scp` 将 OpenClash 包复制到路由器：

   ```bash
   scp luci-app-openclash_0.46.050-beta_all.ipk root@192.168.1.1:~/
   ```

### OpenClash 配置示例

以下是一个 OpenClash 的配置示例：

```yaml
port: 7890
socks-port: 7891
mixed-port: 7892
allow-lan: true
mode: Rule
log-level: info
external-controller: 0.0.0.0:9090
experimental:
  ignore-resolve-fail: true

dns:
  enable: true
  # ipv6: false
  listen: 0.0.0.0:53
  fake-ip-range: 198.18.0.1/16
  default-nameserver:
    - 119.29.29.29
    - 223.5.5.5
    #- 223.6.6.6
  nameserver:
    - https://223.5.5.5/dns-query
    - https://1.12.12.12/dns-query
    #- https://doh.pub/dns-query
    #- https://dns.alidns.com/dns-query
  fake-ip-filter:
    - "*.lan"
    - "*.localdomain"
    - "*.example"
    - "*.invalid"
    - "*.localhost"
    - "*.test"
    - "*.local"

proxies:
  - name: "My SS Proxy"
    type: ss
    server: 209.97.0.0
    port: 57500
    cipher: chacha20-ietf-poly1305
    password: "jHLE54zNC000000"
    udp: true
    plugin: ""
    plugin-opts: {}

proxy-groups:
  - name: "Proxy"
    type: select
    proxies:
      - "My SS Proxy"

rules:
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

通过这些步骤，您可以增强您的 OpenWRT 设备以支持高级网络配置和代理功能。请始终参考官方文档以获取更新和最佳实践。
