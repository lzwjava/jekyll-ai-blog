---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 代理工具：Squid 与 Danted
translated: true
type: post
---

## Danted

命令行指令：

```bash
sudo apt-get install dante-server
sudo apt install net-tools
ifconfig
danted
tail -f danted.log
```

`/etc/danted.conf` 配置：

```bash
logoutput: /home/lzwjava/danted.log

internal: 0.0.0.0 port = 1080  # 监听所有接口
external: ens4
# 认证（允许无凭证访问）
method: none

# 规则
client pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    method: none  # 明确允许无认证
}

socks pass {  # 使用 "socks pass" 替代已弃用的 "pass"
    from: 0.0.0.0/0 to: 0.0.0.0/0
    protocol: tcp udp
    method: none  # 无认证必需
}
```

## Squid 配置

```bash
acl all src all
http_access allow all
http_access deny all
http_port 1128
```

尝试失败。需要先清理 `squid.conf`。

```
1737725543.236   1822 14.31.165.22 TCP_TUNNEL/200 1232 CONNECT 91.108.56.121:443 - HIER_DIRECT/91.108.56.121 -
```

## Google Cloud 命令行

```bash
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

gcloud compute ssh --zone "asia-east1-a" "i25" --project "graphite-ally-445108-k3"
```
