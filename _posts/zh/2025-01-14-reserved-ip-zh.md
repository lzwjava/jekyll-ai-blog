---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 管理DigitalOcean保留IP
translated: true
type: post
---

服务器IP地址容易被防火墙（GFW）屏蔽是一个常见的挑战，尤其是云服务器。为了缓解这一问题，一种策略是使用DigitalOcean的保留IP，并在当前IP被屏蔽时将其重新分配给您的Droplet。本文将介绍一个自动化此过程的Python脚本。该脚本已在[GitHub](https://github.com/lzwjava/auto-ss-config)上开源。

该脚本允许您：

*   检查保留IP是否分配给特定Droplet。
*   如果当前IP被屏蔽，将新的保留IP重新分配给Droplet。
*   检查保留IP的80端口是否开放（一种简单的检查IP是否可用的方法）。

以下是Python脚本：

```python
import socket
import os
import argparse
import json
import requests
import time

# 获取DigitalOcean API头信息的函数
def get_digitalocean_headers():
    api_key = os.environ.get("DO_API_KEY")
    if not api_key:
        print("错误：环境变量中未找到DO_API_KEY。")
        return None
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

# 从DigitalOcean获取所有保留IP的函数
def fetch_reserved_ips():
    headers = get_digitalocean_headers()
    if not headers:
        return None
    try:
        url = "https://api.digitalocean.com/v2/reserved_ips"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        reserved_ips_data = resp.json().get("reserved_ips", [])
        with open('response.json', 'w') as f:
            json.dump(reserved_ips_data, f, indent=4) # 将响应保存到文件以便调试
        return reserved_ips_data
    except requests.exceptions.RequestException as e:
        print(f"获取保留IP地址时出错：{e}")
        return None

# 从Droplet取消分配保留IP的函数
def unassign_ip_from_droplet(ip_address, droplet_id, droplet_name):
    headers = get_digitalocean_headers()
    if not headers:
        return False

    try:
        url = f"https://api.digitalocean.com/v2/reserved_ips/{ip_address}"
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        print(f"成功从Droplet {droplet_name} 删除IP {ip_address}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"从Droplet {droplet_name} 删除IP {ip_address} 时出错：{e}")
        return False

# 将保留IP分配给Droplet的函数
def assign_ip_to_droplet(ip_address, droplet_id, droplet_name):
    headers = get_digitalocean_headers()
    if not headers:
        return False

    try:
        url = f"https://api.digitalocean.com/v2/reserved_ips/{ip_address}/actions"
        req = {
            "type": "assign",
            "droplet_id": droplet_id
        }
        resp = requests.post(url, headers=headers, json=req)
        resp.raise_for_status()
        print(f"成功将IP {ip_address} 分配给Droplet {droplet_name}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"将IP {ip_address} 分配给Droplet {droplet_name} 时出错：{e}")
        return False

# 处理保留IP、检查分配并在需要时重新分配的函数
def process_reserved_ips(reserved_ips, droplet_name, only_check=False):
    if not reserved_ips:
        print("您的账户中没有找到保留IP。")
        return None

    for reserved_ip in reserved_ips:
        ip_address = reserved_ip.get("ip")
        if not ip_address:
            print("未找到保留IP的IP地址。")
            continue

        droplet = reserved_ip.get("droplet", None)
        if droplet_name:
            if droplet and droplet.get("name") == droplet_name:
                print(f"保留IP {ip_address} 已分配给Droplet：{droplet_name}")
                if only_check:
                    if check_port_80(ip_address):
                        print(f"Droplet {droplet_name} 的IP {ip_address} 的80端口已开放")
                    else:
                        print(f"Droplet {droplet_name} 的IP {ip_address} 的80端口已关闭")
                    return ip_address
                droplet_id = droplet.get("id")
                if droplet_id:
                    if unassign_ip_from_droplet(ip_address, droplet_id, droplet_name):
                        # 取消分配后尝试分配新IP

                        new_ip = create_new_reserved_ip(droplet_id)
                        if new_ip:
                            print("分配新IP前等待10秒...")
                            time.sleep(10)
                            if assign_ip_to_droplet(new_ip, droplet_id, droplet_name):
                                print(f"成功将新IP {new_ip} 分配给Droplet {droplet_name}")
                            else:
                                print(f"未能将新IP {new_ip} 重新分配给Droplet {droplet_name}")
                        else:
                            print("没有可分配的IP")

                else:
                    print(f"无法取消分配IP {ip_address}，因为未找到Droplet ID。")
                return None
            elif droplet:
                print(f"保留IP {ip_address} 未分配给Droplet：{droplet_name}")
            else:
                print(f"没有Droplet分配给保留IP：{ip_address}")
        else:
            return ip_address
    return None

# 创建新保留IP的函数
def create_new_reserved_ip(droplet_id):
    headers = get_digitalocean_headers()
    if not headers:
        print("获取DigitalOcean头信息失败。")
        return False
    try:
        url = "https://api.digitalocean.com/v2/reserved_ips"
        req = {
            "region": "sgp1", # 如果需要可以更改区域
        }
        print(f"尝试为Droplet ID {droplet_id} 创建新的保留IP")
        resp = requests.post(url, headers=headers, json=req)
        resp.raise_for_status()
        new_ip = resp.json().get("reserved_ip", {}).get("ip")
        print(f"成功创建新的保留IP：{new_ip}")
        return new_ip
    except requests.exceptions.RequestException as e:
        print(f"创建新保留IP时出错：{e}")
        return False

# 检查IP地址的80端口是否开放的函数
def check_port_80(ip_address):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip_address, 80))
            return True
    except Exception:
        return False

# 获取保留IP的主函数
def get_reserved_ip(droplet_name=None, only_check=False):
    reserved_ips = fetch_reserved_ips()
    if reserved_ips is None:
        return None
    return process_reserved_ips(reserved_ips, droplet_name, only_check)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="获取DigitalOcean保留IP地址。")
    parser.add_argument("--droplet-name", required=True, help="要检查保留IP是否分配给的Droplet名称。")
    parser.add_argument("--only-check", action="store_true", help="仅检查IP是否分配给Droplet，不重新分配。")
    args = parser.parse_args()

    reserved_ip = get_reserved_ip(args.droplet_name, args.only_check)
    if reserved_ip:
        print(f"保留IP地址为：{reserved_ip}")
```

**解释：**

1.  **导入库：** 导入网络操作、环境变量、参数解析、JSON处理、HTTP请求和时间延迟所需的库。
2.  **`get_digitalocean_headers()`：** 从环境变量中获取DigitalOcean API密钥，并构建API请求所需的头信息。
3.  **`fetch_reserved_ips()`：** 使用API获取与您的DigitalOcean账户关联的所有保留IP。它还将原始响应保存到`response.json`以便调试。
4.  **`unassign_ip_from_droplet()`：** 从指定的Droplet取消分配给定的保留IP。
5.  **`assign_ip_to_droplet()`：** 将给定的保留IP分配给指定的Droplet。
6.  **`process_reserved_ips()`：** 这是核心逻辑：
    *   它遍历所有保留IP。
    *   如果提供了`droplet_name`，它会检查IP是否分配给该Droplet。
    *   如果`only_check`为真，它会检查80端口是否开放并返回IP。
    *   如果不是`only_check`，它会取消分配当前IP，创建一个新IP，并将新IP分配给Droplet。
7.  **`create_new_reserved_ip()`：** 在`sgp1`区域创建一个新的保留IP（您可以更改此区域）。
8.  **`check_port_80()`：** 检查给定IP地址的80端口是否开放。这是验证IP是否可用的简单方法。
9.  **`get_reserved_ip()`：** 协调获取和处理保留IP的过程。
10. **`if __name__ == '__main__':`：** 解析命令行参数（`--droplet-name`和`--only-check`）并调用`get_reserved_ip`以执行脚本。

**使用方法：**

1.  **设置DigitalOcean API密钥：** 使用您的DigitalOcean API密钥设置`DO_API_KEY`环境变量。
2.  **运行脚本：**
    *   要检查IP是否分配给Droplet以及80端口是否开放：
        ```bash
        python 脚本名称.py --droplet-name 您的Droplet名称 --only-check
        ```
    *   要将新IP重新分配给Droplet：
        ```bash
        python 脚本名称.py --droplet-name 您的Droplet名称
        ```

该脚本提供了一个管理保留IP的基本框架。您可以根据具体需求进一步扩展它。
