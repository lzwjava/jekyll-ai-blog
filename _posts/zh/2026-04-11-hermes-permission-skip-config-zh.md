---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 爱马仕权限跳过配置
translated: true
type: note
---

问：Hermes Agent 是否有类似 Claude 那样的 `--dangerously-skip-permissions` 功能？

答：

是的 —— **Hermes Agent 有等效功能**，但它是**基于配置的，而非命令行参数**。

Claude：

```
claude --dangerously-skip-permissions
```

Hermes 等效配置：

```
approvals.mode: off
```

这将**禁用所有危险命令的提示确认**，本质上实现了相同行为。

---

## Hermes 权限系统

Hermes 通常**会阻止危险命令**并要求确认，例如：

* `rm -rf`
* `chmod 777`
* `DROP TABLE`
* `kill -9`
* `curl | sh`
* systemctl stop
* 破坏性文件系统操作

这些操作在命令行中需要显式确认。([Hermes Agent][1])

---

## Hermes 的“跳过权限”模式

你可以在配置中禁用确认提示：

```yaml
approvals:
  mode: off
```

可选模式：

* `manual` → 总是询问（默认）
* `smart` → 自动批准安全命令，询问危险命令
* `off` → **跳过所有确认提示（YOLO 模式）**

这在文档中被明确记录为**跳过所有提示**。([Mintlify][2])

---

## 类 Claude 的命令行风格等效方式

你可以模拟实现：

```bash
hermes --yolo
```

或通过配置：

```yaml
approvals:
  mode: off
```

这将使 Hermes：

* 自动运行 shell 命令
* 自动编辑文件
* 自动安装软件包
* 自动访问网络
* 无确认提示

其精神完全等同于：

```
--dangerously-skip-permissions
```

---

## 与 Claude 的重要区别

Claude：

* 全局跳过
* 无安全层

Hermes：

* 仍具有沙盒选项
* 容器隔离
* 允许列表模式
* Docker 后端安全性

Hermes 可以**跳过确认但仍在沙盒中执行**，这更为安全。([Hermes Agent][1])

---

## 更危险的模式（Hermes）

你还可以配置：

```yaml
toolsets:
  - all
approvals:
  mode: off
```

这将授予权限：

* 终端
* 浏览器
* 文件系统
* SSH
* Docker
* API 调用
* 消息机器人

实现完全自主的智能体。

---

## 总结

是的。

Claude：

```
--dangerously-skip-permissions
```

Hermes：

```
approvals.mode: off
```

相同效果：

* 无权限提示
* 完全自主执行

Hermes 还支持**智能自动批准**，这是 Claude 所不具备的。

```
approvals.mode: smart
```

这对于长期运行的智能体实际上更为友好。

参考文献：

* [https://hermes-agent.nousresearch.com/docs/user-guide/security/](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
* [https://www.mintlify.com/NousResearch/hermes-agent/reference/configuration-options](https://www.mintlify.com/NousResearch/hermes-agent/reference/configuration-options)
* [https://docs.bswen.com/blog/2026-02-21-dangerously-skip-permissions-explained/](https://docs.bswen.com/blog/2026-02-21-dangerously-skip-permissions-explained/)

[1]: https://hermes-agent.nousresearch.com/docs/user-guide/security/?utm_source=chatgpt.com "Security | Hermes Agent"
[2]: https://www.mintlify.com/NousResearch/hermes-agent/reference/configuration-options?utm_source=chatgpt.com "Configuration options - Hermes Agent"