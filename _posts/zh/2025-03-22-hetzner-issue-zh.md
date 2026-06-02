---
audio: false
generated: true
lang: zh
layout: post
title: Hetzner API故障
translated: true
type: note
---

让我们分析您遇到的错误并解释代码中发生的情况：

### 错误信息：
```
为服务器 sg5 创建快照时出错：无法执行操作，因为服务器已锁定（locked, f21b9dc9d1535310）
```

这个错误来自 Hetzner Cloud API（通过 `hcloud` Python SDK），表明为名为 `sg5` 的服务器创建快照的操作失败，因为服务器**已被锁定**。服务器被锁定意味着另一个操作（例如之前的快照、重启或调整配置）当前正在进行中，在该过程完成之前，服务器暂时无法接受新操作。

### 代码解析：
以下是您的脚本说明及错误发生位置：

```python
from hcloud import Client
import os

# 从环境变量获取 API 令牌
api_token = os.environ.get('HERTZNER_API_KEY')

if not api_token:
    print("错误：未设置 HERTZNER_API_KEY 环境变量")
    exit(1)

# 创建客户端实例
client = Client(token=api_token)

def create_snapshot(server):
    try:
        response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
        print(f"已为服务器 {server.name} 创建快照，ID：{response.image.id}")
    except Exception as e:
        print(f"为服务器 {server.name} 创建快照时出错：{e}")

# 列出所有服务器
servers = client.servers.get_all()

# 打印服务器详情并创建快照
for server in servers:
    print(f"服务器 ID：{server.id}")
    print(f"服务器名称：{server.name}")
    print(f"服务器状态：{server.status}")
    print(f"服务器 IPv4：{server.public_net.ipv4.ip}")
    print(f"服务器 IPv6：{server.public_net.ipv6.ip}")
    print(f"服务器类型：{server.server_type.name}")
    print(f"服务器位置：{server.datacenter.location.name}")
    print("----------------------------------")
    create_snapshot(server)
```

1. **API 令牌设置**：
   - 脚本从环境变量（`HERTZNER_API_KEY`）获取 Hetzner API 密钥。如果未设置，则报错退出。

2. **客户端初始化**：
   - 使用 API 令牌创建 `Client` 实例，用于与 Hetzner Cloud API 交互。

3. **`create_snapshot` 函数**：
   - 该函数尝试使用 `client.servers.create_image()` 为指定服务器创建快照。
   - 参数说明：
     - `server`：要创建快照的服务器对象
     - `description`：快照名称（如 `sg5-snapshot`）
     - `type="snapshot"`：指定镜像类型为快照（区别于备份或 ISO）
   - 成功时输出快照 ID，失败时捕获并输出异常（如您遇到的错误）

4. **服务器列表获取**：
   - `client.servers.get_all()` 获取您 Hetzner 账户下的所有服务器列表
   - 脚本遍历服务器，输出详细信息（ID、名称、状态、IP 等），并为每个服务器调用 `create_snapshot()`

5. **错误发生位置**：
   - 在 `create_snapshot()` 函数内部，`client.servers.create_image()` 调用因服务器 `sg5` 被锁定而失败。`hcloud` 库根据 API 响应抛出异常信息（`cannot perform operation because server is locked`）

### 服务器被锁定的原因？
当有操作正在进行时，服务器会进入锁定状态。常见原因包括：
- 正在创建另一个快照
- 服务器正在重启、调整配置或重建
- 之前的操作尚未完成

错误信息中的锁定 ID（`f21b9dc9d1535310`）是锁定服务器的正在执行操作的唯一标识符。

### 解决方案：
以下是解决问题的步骤和脚本改进方案：

#### 1. **在操作前检查锁定状态**
修改脚本，在服务器被锁定时跳过快照创建。您可以通过 `client.actions.get_all()` 检查服务器当前操作。

改进后的 `create_snapshot` 函数：
```python
def create_snapshot(server):
    try:
        # 通过检查服务器操作判断是否被锁定
        actions = client.actions.get_all(server=server)
        for action in actions:
            if action.status == "running":
                print(f"跳过 {server.name} 的快照创建：服务器被操作 {action.id} 锁定")
                return
        # 无运行中操作时执行快照创建
        response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
        print(f"已为服务器 {server.name} 创建快照，ID：{response.image.id}")
    except Exception as e:
        print(f"为服务器 {server.name} 创建快照时出错：{e}")
```

#### 2. **等待锁定解除**
如果您希望等待而非跳过，可以轮询服务器操作直到锁定解除：
```python
import time

def wait_for_unlock(server):
    while True:
        actions = client.actions.get_all(server=server)
        running = any(action.status == "running" for action in actions)
        if not running:
            break
        print(f"等待服务器 {server.name} 解除锁定...")
        time.sleep(5)  # 每次检查间隔 5 秒

def create_snapshot(server):
    try:
        wait_for_unlock(server)
        response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
        print(f"已为服务器 {server.name} 创建快照，ID：{response.image.id}")
    except Exception as e:
        print(f"为服务器 {server.name} 创建快照时出错：{e}")
```

#### 3. **手动检查锁定状态**
- 使用 Hetzner Cloud 控制台或 API 检查 ID 为 `f21b9dc9d1535310` 的操作状态
- Python API 调用示例：
  ```python
  action = client.actions.get_by_id("f21b9dc9d1535310")
  print(f"操作状态：{action.status}，命令：{action.command}")
  ```
- 如果操作卡住，可能需要联系 Hetzner 技术支持

#### 4. **重新运行脚本**
当服务器解除锁定后（操作完成或手动解决），重新运行脚本即可

### 补充说明：
- **速率限制**：循环为多个服务器创建快照可能触发 Hetzner API 的速率限制。建议在请求间添加延迟（如 `time.sleep(1)`）
- **错误处理**：当前脚本在遇到错误时不会中断循环，这是正确的处理方式

如果您需要帮助实施这些修复方案或进行进一步调试，请随时告知！
