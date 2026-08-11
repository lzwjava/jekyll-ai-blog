---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CLI作为代理的键入函数
translated: true
type: note
---

问题：CLI本质上是否是函数调用？在为人类和智能体设计CLI时，什么才是重要的？

回答：是的。在智能体时代，CLI非常接近于**带类型的函数接口**。区别在于调用方是进程（shell、人类或智能体），而返回通道是stdout/stderr + 退出码 + 文件/状态变更。

一个很好的思维模型：

```python
result = deploy(
    app="my-api",
    env="prod",
    replicas=3
)
```

等价于：

```bash
mycli deploy \
  --app my-api \
  --env prod \
  --replicas 3
```

CLI本质上是一个序列化层：

```
人类/智能体
      |
      v
  CLI解析器
      |
      v
 带类型的函数
      |
      v
 业务逻辑
      |
      v
 结构化结果
```

对于AI智能体，设计原则会发生变化。

## 1. 流式进度至关重要

传统CLI：

```
$ deploy

（等待5分钟）

完成
```

对智能体不友好，因为模型没有观察结果。

改进版：

```
$ deploy

[1/5] 验证配置...
[2/5] 构建镜像...
[3/5] 推送注册表...
[4/5] 滚动部署...
[5/5] 健康检查...

状态=成功
耗时=312秒
```

智能体通过以下循环运作：

```
观察 -> 推理 -> 行动 -> 观察
```

没有观察意味着智能体如同盲人。

这就是为什么以下工具：

* `git`
* `kubectl`
* `docker`
* 云CLI

功能强大：它们暴露了中间状态。

---

## 2. 日志不再仅服务于人类

传统思维：

```
日志 -> 开发者调试
```

智能体原生思维：

```
日志 -> 智能体感知输入
```

示例：

糟糕的：

```
错误：失败
```

好的：

```json
{
  "status": "failed",
  "step": "database_migration",
  "error_type": "connection_timeout",
  "database": "postgres",
  "retryable": true,
  "suggestion": "check network policy"
}
```

智能体无法可靠推断隐藏状态。

需提供：

* 当前步骤
* 输入
* 输出
* 错误
* 可能的恢复操作

---

## 3. 人类CLI与智能体CLI应有所区别

人类喜欢：

```bash
git rm file.txt
```

简洁。

智能体偏好：

```bash
git remove-file \
  --path=file.txt \
  --confirm=true \
  --reason="cleanup unused file"
```

因为语言模型不是在输入快捷方式。它们是在生成结构化操作。

对于智能体：

清晰度 > 简洁度。

---

## 4. 退出码被低估了

许多CLI仅返回：

```
0 成功
1 错误
```

对智能体友好的：

```
0  成功

10 无效参数
20 权限拒绝
30 网络故障
40 资源缺失
50 可重试失败
```

这样智能体可以决定：

```python
if exit_code == 30:
    retry()

if exit_code == 40:
    ask_user()

if exit_code == 50:
    exponential_backoff()
```

---

## 5. 使输出可机器解析

现代CLI应具备：

```bash
mycli deploy --json
```

输出：

```json
{
  "deployment_id": "abc123",
  "status": "running",
  "progress": 0.7
}
```

人类：

```bash
mycli deploy
```

输出：

```
Deploying api-server...
70% complete
```

同一引擎，不同渲染器。

---

## 6. 像设计API一样设计CLI

良好的架构：

```
              REST API
                 |
人类CLI ---- 核心引擎 ---- 智能体工具
                 |
              Python SDK
```

CLI不应包含业务逻辑。

示例：

```
cli.py
   |
   v
services/deploy.py
   |
   v
云提供商
```

之后：

```python
agent.call(
    "deploy",
    {
      "app": "api",
      "environment": "prod"
    }
)
```

自然就能工作。

---

这就是为什么MCP/工具调用感觉与CLI设计相似。MCP工具本质上就是：

```
CLI命令
      +
JSON模式
      +
结构化输出
```

未来的模式可能是：

```
旧：
人类 -> CLI -> 程序

新：
人类 -> CLI -> 程序
智能体 -> 工具 -> 程序
智能体 -> CLI -> 程序
```

如今最好的CLI不仅仅是一个命令行界面。它是一个**人类可读、机器可调用且执行过程可观察的API**。