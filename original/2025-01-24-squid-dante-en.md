---
audio: true
generated: false
image: false
lang: en
layout: post
title: 'Proxy Tool: Squid and Danted'
type: post
---

## Danted

Command line instructions:

```bash
sudo apt-get install dante-server
sudo apt install net-tools
ifconfig
danted
tail -f danted.log
```

`/etc/danted.conf` configuration:

```bash
logoutput: /home/lzwjava/danted.log

internal: 0.0.0.0 port = 1080  # Listen on all interfaces
external: ens4
# Authentication (allow all without credentials)
method: none

# Rules
client pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    method: none  # Explicitly allow no-auth
}

socks pass {  # Use "socks pass" instead of deprecated "pass"
    from: 0.0.0.0/0 to: 0.0.0.0/0
    protocol: tcp udp
    method: none  # Required for no-auth
}
```

## Squid Configuration

```bash
acl all src all
http_access allow all
http_access deny all
http_port 1128
```

Failed to try. Need to clean up `squid.conf` first.

```
1737725543.236   1822 14.31.165.22 TCP_TUNNEL/200 1232 CONNECT 91.108.56.121:443 - HIER_DIRECT/91.108.56.121 -
```

## Google Cloud Command Lines

```bash
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

gcloud compute ssh --zone "asia-east1-a" "i25" --project "graphite-ally-445108-k3"
```
