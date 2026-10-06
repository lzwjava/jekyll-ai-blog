---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 持久自主任务循环
translated: true
type: note
---

问题：Pi Agent 中与 Hermes Agent 类似的 `goal` 命令是什么？

答案：

Hermes Agent 中的 `/goal` 本质上是一个**持久的自主任务循环**。它不仅仅是一个提示快捷方式，而是将代理的行为从：

```
用户提示
    ↓
代理执行一次回复
    ↓
停止
```

转变为：

```
用户设定目标
    ↓
代理工作
    ↓
判断模型检查“是否真的完成？”
    ↓
如果未完成：
    代理自动继续
    ↓
重复直到完成/暂停/预算耗尽
```

Hermes 将 `/goal` 实现为一种 Ralph 循环机制：在每个轮次后，一个独立的判断模型评估完成情况，如果目标未满足，代理会继续执行。（[GitHub][1]）

示例：

```
/goal 修复此仓库中所有失败的测试并让 CI 通过
```

代理将持续执行：

```
检查代码
→ 编辑文件
→ 运行测试
→ 分析失败
→ 修复
→ 重新运行
```

无需你手动输入“继续”。（[Ryder Freeman Logos][2]）

有用的命令：

```text
/goal status     # 查看当前目标
/goal pause      # 暂时停止
/goal resume     # 继续执行
/goal clear      # 移除目标
```

Hermes 还支持添加额外条件：

```text
/subgoal 为新的 API 添加单元测试
```

这样代理必须同时满足原始目标和添加的条件。（[Hermes Agent][3]）

对于 **Pi Agent**，具体取决于你指的是哪种 Pi 实现。如果你指的是 Pi Agent / `pi` 编程代理生态系统，那么它历史上更侧重于交互式代理会话、工具和扩展，而非 Hermes 风格的持久目标。根据现有信息，我没有在 Pi 中看到内置的 `/goal` 命令等价物。

你可以通过扩展在 Pi 中实现相同的思路：

```python
goal = """
构建一个 REST API。
要求：
- 实现端点
- 编写测试
- 运行 pytest
- 修复失败
"""

while True:
    response = agent.run(goal)

    verdict = judge_model(
        goal=goal,
        output=response
    )

    if verdict == "done":
        break
```

关键思路是：

* **普通代理** = “回答这个任务”
* **目标代理** = “持续持有该目标直到完成”

这是迈向代理式软件工程的重要转变之一：人类指定**终点线**，代理负责迭代循环。

参考资料：

* Hermes Agent 持久目标：([GitHub][1])
* Hermes 斜杠命令：([Hermes Agent][3])

[1]: https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/goals.md?utm_source=chatgpt.com "hermes-agent/website/docs/user-guide/features/goals.md at main · NousResearch/hermes-agent · GitHub"
[2]: https://ryderfreeman4logos.github.io/hermes-agent-docs-i18n/en/website/docs/user-guide/features/goals?utm_source=chatgpt.com "Persistent Goals (/goal) - Hermes Agent Docs i18n"
[3]: https://hermes-agent.nousresearch.com/docs/reference/slash-commands?utm_source=chatgpt.com "Slash Commands Reference | Hermes Agent"
