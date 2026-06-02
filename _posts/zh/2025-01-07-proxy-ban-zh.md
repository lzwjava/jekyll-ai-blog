---
audio: false
generated: false
image: true
lang: zh
layout: post
title: 防火墙、代理API与VPN检测
translated: true
type: post
---

### 目录

1. [代理服务器中的API能否规避GFW封锁？](#代理服务器中的api能否规避gfw封锁)
   - 混合代理与API流量可避免GFW封锁
   - GFW能区分代理流量与常规HTTP/HTTPS流量
   - GFW可能基于纯代理流量实施封锁
   - GFW采用时间窗口进行流量分析
   - 定期访问API或可防止检测

2. [防火墙（GFW）工作原理](#防火墙gfw工作原理)
   - GFW记录含源地址与目标数据的请求
   - 封禁涉及非法活动的IP地址
   - 使用规则检测特定协议
   - 可根据非法请求比例实施封禁
   - 运用AI进行智能流量模式检测

3. [ChatGPT iOS版VPN检测分析](#chatgpt-ios版vpn检测分析)
   - ChatGPT iOS现可配合部分VPN使用
   - 访问权限取决于VPN服务器地理位置
   - 检测基于特定IP地址
   - 部分云服务商IP遭封禁

## 代理服务器中的API能否规避GFW封锁？

我在Shadowsocks实例上运行了一个简易服务器，代码如下：

```python
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # 为所有路由启用CORS

@app.route('/bandwidth', methods=['GET'])
def get_bandwidth():
    # 运行vnstat命令获取eth0网卡5分钟间隔流量统计
    result = subprocess.run(['vnstat', '-i', 'eth0', '-5', '--json'], capture_output=True, text=True)
    data = result.stdout

    # 将捕获的数据作为JSON响应返回
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

并使用nginx配置443端口服务如下：

```bash
server {
    listen 443 ssl;
    server_name www.some-domain.xyz;

    ssl_certificate /etc/letsencrypt/live/www.some-domain.xyz/fullchain.pem; # 由Certbot管理
    # ...
    location / {

        proxy_pass http://127.0.0.1:5000/;
        # ...
    }
}
```

该服务器程序提供网络数据，我将该服务器兼作代理服务器，从而能在博客上通过网络数据展示在线状态。

有趣的是，该服务器至今数日未被防火墙（GFW）或其他网络控制系统封禁。通常我搭建的代理服务器一两天内就会遭封禁。此服务器在51939等端口运行Shadowsocks程序，因此其流量混合了Shadowsocks代理与常规API流量。这种混合流量似乎让GFW判定该服务器并非专用代理而是常规服务器，从而避免IP被封。

这一现象值得深思。GFW显然采用特定逻辑区分代理流量与常规流量。虽然Twitter和YouTube等网站在中国被屏蔽，但大量国外网站（如国际高校与企业网站）仍可访问。

这表明GFW很可能基于规则区分常规HTTP/HTTPS流量与代理相关流量。同时处理两类流量的服务器似乎能避免封禁，而仅处理代理流量的服务器更易被封锁。

关键问题在于GFW采用多长时间窗口累积数据实施封禁——是一天还是一小时？在此时间窗口内，系统检测流量是否纯属代理性质。若是，则封禁服务器IP。

我常访问博客查看所写内容，但接下来几周我的重心将转向其他任务而非博客写作。这将减少我通过443端口访问`bandwidth` API的频率。若发现再次遭封禁，我应编写程序定期访问该API以迷惑GFW。

以下是结构优化、表述更清晰的文本版本：

## 防火墙（GFW）工作原理

### 步骤1：记录请求

```python
import time

# 存储请求数据的数据库
request_log = []

# 请求记录函数
def log_request(source_ip, target_ip, target_port, body):
    request_log.append({
        'source_ip': source_ip,
        'target_ip': target_ip,
        'target_port': target_port,
        'body': body,
        'timestamp': time.time()
    })
```

`log_request`函数记录传入请求的关键信息，包括源IP、目标IP、目标端口、请求体和时间戳。

### 步骤2：检查并封禁IP

```python
# 检查请求并封禁IP的函数
def check_and_ban_ips():
    banned_ips = set()

    # 遍历所有已记录请求
    for request in request_log:
        if is_illegal(request):
            banned_ips.add(request['target_ip'])
        else:
            banned_ips.discard(request['target_ip'])

    # 对所有识别出的IP实施封禁
    ban_ips(banned_ips)
```

`check_and_ban_ips`函数遍历所有已记录请求，识别并封禁与非法活动关联的IP。

### 步骤3：定义非法请求判定标准

```python
# 模拟检查请求是否非法的函数
def is_illegal(request):
    # 实际非法请求检查逻辑的占位符
    # 例如检查请求体或目标特征
    return "illegal" in request['body']
```

此处`is_illegal`检查请求体是否包含"illegal"一词。此逻辑可扩展为更复杂的判定机制。

### 步骤4：封禁已识别IP

```python
# 封禁IP列表的函数
def ban_ips(ip_set):
    for ip in ip_set:
        print(f"封禁IP: {ip}")
```

识别非法IP后，`ban_ips`函数通过打印IP地址实施封禁（真实系统中可能执行阻塞操作）。

### 步骤5：基于80%非法请求比例的替代封禁方案

```python
# 根据80%非法请求比例检查并封禁IP的函数
def check_and_ban_ips():
    banned_ips = set()
    illegal_count = 0
    total_requests = 0

    # 遍历所有已记录请求
    for request in request_log:
        total_requests += 1
        if is_illegal(request):
            illegal_count += 1

    # 若80%及以上请求为非法，则封禁相关IP
    if total_requests > 0 and (illegal_count / total_requests) >= 0.8:
        for request in request_log:
            if is_illegal(request):
                banned_ips.add(request['target_ip'])

    # 对所有识别出的IP实施封禁
    ban_ips(banned_ips)
```

此替代方案根据非法请求比例判定IP是否应被封禁。若某IP的非法请求占比达80%或更高，则予以封禁。

### 步骤6：增强型非法请求检查（如Shadowsocks与Trojan协议检测）

```python
def is_illegal(request):
    # 检查是否使用Shadowsocks协议（请求体含类二进制数据）
    if request['target_port'] == 443:
        if is_trojan(request):
            return True
    elif is_shadowsocks(request):
        return True
    return False
```

现`is_illegal`函数还检查特定协议如Shadowsocks和Trojan：

- **Shadowsocks**：可检测请求体中是否含加密或类二进制数据
- **Trojan**：若请求经443端口（HTTPS）且符合特定模式（如Trojan流量特征），则标记为非法

### 步骤7：合法请求示例

例如`GET https://some-domain.xyz/bandwidth`类请求显然合法，不会触发封禁机制。

### 步骤8：代理服务器流量特征

代理服务器的流量特征与常规Web或API服务器截然不同。GFW需区分正常Web服务器流量与代理服务器流量，二者呈现完全不同的模式。

### 步骤9：用于智能检测的机器学习与AI模型

鉴于通过网络传输的请求与响应类型繁多，GFW可能采用AI与机器学习模型分析流量模式，智能检测非法行为。通过训练系统识别多种流量类型并运用先进技术，可基于观测模式更有效地封禁或过滤流量。

## 更新

尽管多方尝试，我的代理服务器持续遭封禁。为缓解此问题，我采用Digital Ocean的浮动IP功能实现应对方案——每当遭遇封禁时可快速分配新IP地址。

---

## ChatGPT iOS版VPN检测分析

*2024.12.26*

今日发现ChatGPT iOS应用现可在中国通过VPN登录。此前它会显示如下阻断提示。

但截至今日，配合VPN使用一切正常。

我记得ChatGPT iOS应用初发布时，通过VPN使用并无障碍。后来VPN检测趋于严格，导致登录困难。值得庆幸的是，近期该限制似乎已放宽。

经进一步测试发现：使用DigitalOcean新加坡区域VPN时无法访问应用，但使用台湾或英国VPN（由zhs.cloud提供）时运行完美。

ChatGPT iOS的VPN检测似乎基于特定IP地址。部分云服务商或特定IP地址遭封禁，这或许解释了不同VPN服务器地理位置导致的差异行为。

![](assets/images/chatgpt/block.jpg){: .responsive }

![](assets/images/chatgpt/c1.png){: .responsive }
