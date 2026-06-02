---
audio: false
generated: false
image: true
lang: en
layout: post
title: Hetzner Cloud
translated: false
type: post
---

I am very excited to try this cloud platform recently.

{: .centered }
![](assets/images/hertzner/h.jpg)
*Source: Hetzner*{: .caption }

A server in Helsinki with a configuration of 2 AMD VCPUs, 2GB RAM, 40GB SSD, and 20TB of traffic costs 4.49 USD per month.

An IPv4 address costs an additional 0.60 USD per month, bringing the total to 5.09 USD per month.

They provide services in six locations:

- Nuremberg, Germany
- Falkenstein, Germany
- Helsinki, Finland
- Singapore, Singapore
- Hillsboro, OR, USA
- Ashburn, VA, USA

It's interesting that they don't follow trends to select popular locations. Their locations are different from those of Vultr or Digital Ocean.

The firewall settings are easy to use. Although this was my first time using it, I quickly set up the correct configuration for my proxy server.

> sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh)"

The speed of the Hetzner server in Helsinki is very fast. Using the Speedtest iOS app, the download speed is 423 Mbps, and the upload speed is 56.1 Mbps.

The ping in Shadowrocket is 1175 ms, but this is not a significant issue.

A simple Python script to get server instance details.

```python
from hcloud import Client
import os

# Get the API token from the environment variable
api_token = os.environ.get('HERTZNER_API_KEY')

if not api_token:
    print("Error: HERTZNER_API_KEY environment variable not set.")
    exit(1)

# Create a client instance
client = Client(token=api_token)

# List all servers
servers = client.servers.get_all()

# Print server details
for server in servers:
    print(f"Server ID: {server.id}")
    print(f"Server Name: {server.name}")
    print(f"Server Status: {server.status}")
    print(f"Server IPv4: {server.public_net.ipv4.ip}")
    print(f"Server IPv6: {server.public_net.ipv6.ip}")
    print(f"Server Type: {server.server_type.name}")
    print(f"Server Location: {server.datacenter.location.name}")
    print("----------------------------------")

# If you want to get a specific server by ID
server_id = '59402674'
server = client.servers.get_by_id(server_id)

print(f"Specific Server ID: {server.id}")
print(f"Specific Server Name: {server.name}")
print(f"Specific Server Status: {server.status}")
print(f"Specific Server IPv4: {server.public_net.ipv4.ip}")
print(f"Specific Server IPv6: {server.public_net.ipv6.ip}")
print(f"Specific Server Type: {server.server_type.name}")
print(f"Specific Server Location: {server.datacenter.location.name}")

```
