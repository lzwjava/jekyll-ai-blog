---
audio: false
generated: false
image: true
lang: zh
layout: post
title: Hetzner 云
translated: true
type: post
---

我最近非常期待试用这个云平台。

{: .centered }
![](assets/images/hertzner/h.jpg)
*来源: Hetzner*{: .caption }

在赫尔辛基的一台服务器，配置为2个AMD VCPU，2GB内存，40GB SSD，并带有20TB的流量，每月只需4.49美元。

一个IPv4地址每月额外需0.60美元，总共每月5.09美元。

他们提供服务于以下六个地点：

- 德国纽伦堡
- 德国法尔凯恩斯坦
- 芬兰赫尔辛基
- 新加坡新加坡
- 美国俄勒冈州希尔斯堡
- 美国弗吉尼亚州阿什本

有趣的是，他们没有遵循流行趋势选择热门地点。他们的服务地点与Vultr或Digital Ocean的地点有所不同。

防火墙设置非常易于使用。虽然这是我第一次使用它，但我很快就为我的代理服务器设置了正确的配置。

> sudo bash -c "$(wget -qO- <https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh>)"

赫尔辛基的Hetzner服务器速度非常快。使用iOS上的Speedtest应用程序，下载速度为423 Mbps，上传速度为56.1 Mbps。

在Shadowrocket中，ping为1175 ms，但这并不是一个重要的问题。

一个简单的Python脚本来获取服务器实例详细信息。

```python
from hcloud import Client
import os

# 从环境变量获取API令牌
api_token = os.environ.get('HERTZNER_API_KEY')

if not api_token:
    print("Error: HERTZNER_API_KEY环境变量未设置.")
    exit(1)

# 创建客户端实例
client = Client(token=api_token)

# 列出所有服务器
servers = client.servers.get_all()

# 打印服务器详细信息
for server in servers:
    print(f"服务器ID: {server.id}")
    print(f"服务器名称: {server.name}")
    print(f"服务器状态: {server.status}")
    print(f"服务器IPv4: {server.public_net.ipv4.ip}")
    print(f"服务器IPv6: {server.public_net.ipv6.ip}")
    print(f"服务器类型: {server.server_type.name}")
    print(f"服务器位置: {server.datacenter.location.name}")
    print("----------------------------------")

# 如果要获取特定服务器的详细信息
server_id = '59402674'
server = client.servers.get_by_id(server_id)

print(f"特定服务器ID: {server.id}")
print(f"特定服务器名称: {server.name}")
print(f"特定服务器状态: {server.status}")
print(f"特定服务器IPv4: {server.public_net.ipv4.ip}")
print(f"特定服务器IPv6: {server.public_net.ipv6.ip}")
print(f"特定服务器类型: {server.server_type.name}")
print(f"特定服务器位置: {server.datacenter.location.name}")
```
