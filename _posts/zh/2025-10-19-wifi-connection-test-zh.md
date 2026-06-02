---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 自动化WiFi连接测试脚本
translated: true
type: note
---

```python
import subprocess
import time
import os

def get_wifi_interfaces():
    """辅助函数：查找WiFi接口"""
    try:
        result = subprocess.run("nmcli dev status | grep wifi | awk '{print $1}'", shell=True, capture_output=True, text=True)
        interfaces = [iface.strip() for iface in result.stdout.split('\n') if iface.strip()]
        return interfaces
    except:
        return []

def test_wifi_connection(ssid, password="88888888", timeout=30):
    """非交互式测试WiFi连接。返回元组（成功状态：布尔值，错误信息：字符串）"""
    interfaces = get_wifi_interfaces()
    if not interfaces:
        return False, "无可用WiFi接口"
    interface = interfaces[0]  # 使用第一个可用接口
    con_name = f"test-{ssid}"  # 测试配置文件的唯一名称

    # 命令定义
    delete_cmd = f"nmcli connection delete '{con_name}'"
    add_cmd = (
        f"nmcli connection add type wifi con-name '{con_name}' "
        f"ifname {interface} ssid '{ssid}' "
        f"wifi-sec.key-mgmt wpa-psk wifi-sec.psk '{password}' "
        f"-- autoconnect no"
    )
    up_cmd = f"nmcli connection up '{con_name}'"
    disconnect_cmd = f"nmcli device disconnect {interface}"

    try:
        # 删除现有配置文件（如果不存在则忽略错误）
        subprocess.run(delete_cmd, shell=True, capture_output=True, timeout=5)
        time.sleep(1)

        # 创建包含嵌入式密码的新配置文件（非交互式）
        add_result = subprocess.run(add_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if add_result.returncode != 0:
            error = add_result.stderr.strip() or add_result.stdout.strip() or "创建连接配置文件失败"
            return False, f"配置文件创建错误: {error}"

        # 激活配置文件（非交互式）
        up_result = subprocess.run(up_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if up_result.returncode != 0:
            error = up_result.stderr.strip() or up_result.stdout.strip() or "激活失败"
            if "secrets were required" in error.lower():
                error = "密码错误或认证失败"
            elif "activation failed" in error.lower():
                error = f"连接激活失败: {error}"
            return False, f"nmcli错误: {error}"

        # 等待连接稳定
        time.sleep(2)

        # 通过ping测试互联网连接
        ping_test = subprocess.run("ping -c 1 -W 3 8.8.8.8", shell=True, capture_output=True, text=True, timeout=5)
        if ping_test.returncode == 0:
            return True, None
        else:
            error = ping_test.stderr.strip() or "Ping测试失败"
            return False, f"已连接但无法访问互联网: {error}"

    except subprocess.TimeoutExpired:
        return False, f"操作超时（{timeout}秒）"
    except subprocess.SubprocessError as e:
        return False, f"命令执行错误: {str(e)}"
    finally:
        # 清理：关闭连接并删除配置文件
        try:
            subprocess.run(f"nmcli connection down '{con_name}'", shell=True, capture_output=True, timeout=5)
            subprocess.run(delete_cmd, shell=True, capture_output=True, timeout=5)
            subprocess.run(disconnect_cmd, shell=True, capture_output=True, timeout=5)
        except subprocess.SubprocessError:
            pass  # 忽略清理过程中的问题
```
