---
audio: false
generated: false
image: false
lang: en
layout: post
title: Enhancing OpenWRT with OpenClash and Shadowsocks
translated: false
type: post
---

### Updating Package Lists

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

### Installing Shadowsocks Plugin

To install the `luci-app-shadowsocks-libev` plugin:

```bash
root@OpenWrt:~# opkg install luci-app-shadowsocks-libev
Installing luci-app-shadowsocks-libev (git-22.066.30464-cea4277) to root...
Downloading https://downloads.openwrt.org/releases/22.03.3/packages/mipsel_24kc/luci/luci-app-shadowsocks-libev_git-22.066.30464-cea4277_all.ipk
Configuring luci-app-shadowsocks-libev.
```

### OpenClash Installation

Refer to the OpenClash [GitHub repository](https://github.com/vernesong/OpenClash?tab=readme-ov-file) for more details. Below are the steps to install the necessary components.

1. Install the OpenSSH SFTP server:

   ```bash
   opkg install openssh-sftp-server
   ```

2. Use `scp` to copy the OpenClash package to the router:

   ```bash
   scp luci-app-openclash_0.46.050-beta_all.ipk root@192.168.1.1:~/
   ```

### Sample OpenClash Configuration

Below is a sample configuration for OpenClash:

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

With these steps, you can enhance your OpenWRT device to support advanced networking configurations and proxy functionalities. Always refer to the official documentation for updates and best practices.
