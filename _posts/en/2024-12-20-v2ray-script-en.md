---
audio: true
generated: false
image: false
lang: en
layout: post
title: V2Ray Script
translated: false
type: post
---

This is a V2Ray script I often use.

```bash
#!/bin/bash

# Exit on error
set -e

# Step 1: Download the V2Ray installation script
curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh > in.sh

# Step 2: Make the installation script executable
chmod +x in.sh

# Step 3: Run the installation script
sudo ./in.sh

# Step 4: Start V2Ray service
sudo systemctl start v2ray

# Step 5: Check if V2Ray is running
echo "Checking if V2Ray is running..."
ps aux | grep v2ray

# Step 6: Write the config.json file content
echo "Writing V2Ray configuration..."
cat << EOF | sudo tee /usr/local/etc/v2ray/config.json > /dev/null
{
    "inbounds": [
        {
            "port": 1080,
            "listen": "0.0.0.0",
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": "9f02f6b2-1d7d-4b10-aada-69e050f1be6b",
                        "level": 0,
                        "alterId": 0,
                        "email": "example@v2ray.com",
                        "security": "auto"
                    }
                ]
            },
            "streamSettings": {
                "network": "tcp"
            },
            "sniffing": {
                "enabled": true,
                "destOverride": [
                    "http",
                    "tls"
                ]
            },
            "tag": "vmess-inbound",
            "udp": true
        }
    ],
    "outbounds": [
        {
            "protocol": "freedom",
            "settings": {},
            "tag": "outbound-freedom",
            "udp": true
        }
    ],
    "log": {
        "loglevel": "debug",
        "access": "/var/log/v2ray/access.log",
        "error": "/var/log/v2ray/error.log"
    },
    "stats": {
        "enabled": false
    },
    "environment": {
        "v2ray.vmess.aead.forced": "false"
    }
}
EOF

# Step 7: Restart V2Ray service to apply changes
sudo systemctl restart v2ray

# Step 8: Show V2Ray service status
echo "V2Ray service status:"
sudo systemctl status v2ray
```
