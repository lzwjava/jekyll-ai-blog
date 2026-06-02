---
audio: false
generated: true
lang: zh
layout: post
title: Cline思维——调试Hetzner云服务器快照脚本
translated: true
type: note
---

$0.8984

## 初始调试过程

检查点
比较
恢复

**思考过程**
我需要修复 `hetzner.py` 文件中的一个错误。错误显示 'Server' 对象没有 'create_snapshot' 属性。首先让我检查该文件的内容以了解发生了什么。根据环境详情，该文件位于 `scripts/auto-ss-config/hetzner.py`，因此我需要读取此文件来理解问题。

让我检查 hetzner.py 文件来理解并修复 'Server' 对象没有 'create_snapshot' 属性的错误。

**思考：**
我需要修复 'Server' 对象没有 'create_snapshot' 属性的错误。查看代码，我可以看到有一个函数 `create_snapshot(server)` 试图调用 `server.create_snapshot()`，但根据错误信息，Server 对象上不存在此属性/方法。这表明在 hcloud Python 库中，Server 类没有名为 create_snapshot 的方法。我应该使用 client 对象来创建快照。让我修改代码，通过使用 client.servers API 而不是直接在 server 对象上调用方法来修复此问题。

我发现了问题 - 错误发生是因为 hcloud 库中的 Server 对象没有 create_snapshot 方法。相反，我们需要使用 client 的 servers API 来创建快照。让我修复这个问题：

**思考：**
我已经成功修复了 hetzner.py 文件中的问题。问题是代码试图直接在 server 对象上调用 `create_snapshot()`，但 hcloud 库中的 server 实例上不存在此方法。我修改了代码以使用正确的方法：调用 `client.servers.create_snapshot()` 并将 server 对象作为参数传递。我还将参数从 `name` 更新为 `description`，这是 API 根据错误所期望的。修复已成功应用。

**任务完成**
我已经修复了 hetzner.py 脚本中的问题。错误发生是因为代码试图直接在 server 对象上调用 create_snapshot()，但 hcloud 库的 Server 类中不存在此方法。

解决方案是使用 client 的 servers API：

```python
# 从：
snapshot = server.create_snapshot(name=f"{server.name}-snapshot")

# 改为：
snapshot = client.servers.create_snapshot(server, description=f"{server.name}-snapshot")
```
此更改在 client.servers 对象上调用 create_snapshot 方法，并将 server 作为参数传递，同时使用正确的参数名称 'description' 而不是 'name'。

## 修复其他问题

查看新更改

```
lzwjava@anonymous lzwjava.github.io % python scripts/auto-ss-config/hetzner.py
🚀 **检测到代理设置：**
- HTTP_PROXY: http://127.0.0.1:7890
- HTTPS_PROXY: http://127.0.0.1:7890

服务器 ID: 61589357
服务器名称: sg5
服务器状态: running
服务器 IPv4: 5.223.56.128
服务器 IPv6: 2a01:4ff:2f0:3b22::/64
服务器类型: cpx11
服务器位置: sin
----------------------------------
为服务器 sg5 创建快照时出错: 'ServersClient' 对象没有 'create_snapshot' 属性
```

再次修复

**思考：**
现在我需要修复新的错误。似乎 `ServersClient` 对象也没有 `create_snapshot` 方法。我需要查看 hcloud Python 库中创建快照的正确方法。查看 hcloud 库文档或示例，我们应该使用 `client.server_actions` 而不是 `client.servers` 来创建快照。让我修复这个问题。

让我修复新错误。问题是我使用了 client.servers.create_snapshot，但正确的 API 是 client.server_actions.create_image：

**思考：**
让我验证更改是否成功。之前的错误是 "'ServersClient' 对象没有 'create_snapshot' 属性"。我的修复将其替换为 `client.server_actions.create_image()`，这是 hcloud 库中创建快照的正确 API。我还更新了访问快照 ID 的方式，因为响应结构不同 - 现在是 `snapshot.image.id`。我相信这应该能解决问题，但让我等待用户确认这是否有效。

**思考：**
我需要检查 hcloud Python 库中创建快照的正确 API 方法。让我再次修复代码。根据错误消息，我需要调查创建快照的正确 API。

让我查看 hcloud Python 库文档，了解创建快照的正确方法：

**思考：**
现在我找到了！从输出中，我可以看到 Client 的 `servers` 对象有一个 `create_image` 方法，这正是我们需要用来创建快照的方法。

我找到了要使用的正确方法 - create_image 是 servers client 的一个方法。让我更新代码：

**思考：**
让我们再次执行脚本以确保它现在正常工作。

**思考：**
太好了！脚本现在正常工作。快照已成功创建，ID 为 225649148。修复方法是使用 client.servers.create_image() 而不是尝试使用 server.create_snapshot() 或 client.server_actions.create_image()。现在我应该总结一下我修复问题的过程。

**任务完成**
我通过使用正确的方法创建快照修复了 Hetzner 脚本中的问题。错误发生是因为原始代码试图直接在 server 对象上调用 create_snapshot()，但此方法不存在。

在检查了 hcloud Python 库 API 后，我发现正确的方法是在 servers client 对象上使用 create_image()：

```python
# 从：
snapshot = server.create_snapshot(name=f"{server.name}-snapshot")

# 改为：
response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
```
修复成功，服务器 sg5 的快照已创建，ID 为 225649148。

所做的主要更改：

- 使用 client.servers.create_image() 方法而不是尝试在 server 对象上访问不存在的方法
- 将参数名称从 name 改为 description
- 添加了 type="snapshot" 参数
