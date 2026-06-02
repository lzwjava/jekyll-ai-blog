---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 正确创建WebSphere应用服务器
translated: true
type: note
---

不，命令 `nodeName -name serverName admin create applciation server`（注意"applciation"的拼写错误）在 IBM WebSphere Application Server (WAS) 中使用 wsadmin 脚本创建应用服务器是不正确的。

### 正确语法
正确的命令应使用 Jython（wsadmin 推荐脚本语言）中的 `AdminTask.createApplicationServer` 方法。它需要：
- 将**节点名称**作为第一个参数（字符串）
- 将**选项列表**作为第二个参数，包括用于指定服务器名称的 `-name` 参数

**基础示例：**
```jython
AdminTask.createApplicationServer('YourNodeName', ['-name', 'YourServerName'])
```

- 将 `'YourNodeName'` 替换为实际节点名（如 `ndnode1`）
- 将 `'YourServerName'` 替换为期望的服务器名称（如 `appServer1`）
- 可在列表中添加可选参数，例如使用默认服务器模板的 `'-templateName', 'default'`

### 执行步骤
1. 以 Jython 模式启动 wsadmin：`./wsadmin.sh -lang jython -user admin -password pass`
2. 执行上述命令
3. 保存配置：`AdminConfig.save()`
4. 退出：`quit`

这将在指定节点上创建一个基础应用服务器。如需更多选项（如端口、JVM 设置），请参阅完整的 AdminTask 文档。

[AdminTask 对象的 ServerManagement 命令组](https://www.ibm.com/docs/en/was-nd/9.0.5?topic=scripting-servermanagement-command-group-admintask-object)
[使用脚本创建服务器](https://www.ibm.com/docs/en/was/9.0.5?topic=scripting-creating-server-using)
