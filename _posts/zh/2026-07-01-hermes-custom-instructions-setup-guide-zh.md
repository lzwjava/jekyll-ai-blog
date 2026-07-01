---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 爱马仕自定义指令设置指南
translated: true
type: note
---

问题：如何为 Hermes Agent（Nous Research）设置自定义指令？

回答：

Hermes 有三个层次的"自定义指令"，每个层次的范围不同。针对你的使用场景（多个项目、AI 原生工具链、你已经运行 `ww`/`iclaw`/`zz`），你可能需要全部三个层次。

**1. `SOUL.md` — 全局人格 / 始终开启的指令**

这是顶层系统提示槽——跨所有会话、所有项目持久存在，直到你切换配置文件。

```bash
$HERMES_HOME/SOUL.md   # 默认路径：~/.hermes/SOUL.md
```

SOUL.md 位于系统提示的顶层，成为智能体本身的身份标识。直接编辑它：

```bash
cat ~/.hermes/SOUL.md
# 然后用你喜欢的编辑器编辑
$EDITOR ~/.hermes/SOUL.md
```

一个最小模板（参考文档）："你是一位务实且品味出色的资深工程师。你优先追求真相、清晰度和实用性，而非礼貌性的客套。"——请根据你自己的语气改写（例如："优先进行第一性原理的解释，先展示代码再写文字，默认隐藏密钥/IP/令牌"）。

修改后启动新会话以使更改生效——系统提示在会话启动时一次性组装，不会在对话中途改变，以保证提示缓存稳定性。

**2. `AGENTS.md` — 项目级规则**

将其放在仓库根目录下，用于指定仓库特定的指令（编码规范、隐藏规则、部署流程等）。将 AGENTS.md 放置在你正在工作的项目根目录，并描述项目特定的规则。当 Hermes 在该目录中运行时，它会与 SOUL.md 一起加载——相当于 CLAUDE.md 的等价物。

**3. 配置文件（Profiles）——完全隔离的智能体，带有独立指令**

鉴于你希望实现设计师/程序员/研究员的角色分离（你的 `ww`/`iclaw`/`zz` 设置已经暗示了这一点），配置文件允许每个都有自己的 `SOUL.md`、技能、记忆和 API 密钥：

```bash
hermes profile create work --clone        # 仅复制配置/SOUL.md/.env
hermes profile create backup --clone-all  # + 记忆 + 技能 + 会话
```

命令别名会自动生成——名为 'work' 的配置文件会直接提供 `work chat`、`work setup`、`work gateway start`、`work skills list` 命令。

**配置级指令（`config.yaml`）**

模型路由、终端后端、自学习开关——虽然不是严格意义上的"指令"，但会影响行为：

```bash
hermes config edit
```

**推荐顺序**（来自官方自定义指南）：1. 编辑 SOUL.md 并启动新会话。2. 配置 config.yaml（模型、终端后端、自学习）。3. 为每个项目创建 AGENTS.md。4. 将角色拆分为不同的配置文件，每个配有独立的 SOUL.md。5. 积累技能——在完成复杂任务后指示智能体"将此流程记录为技能"。6. 定期检查 MEMORY.md/USER.md 中过时的信息。

**一个值得注意的陷阱**：另外两个记忆文件会自动填充并注入到每个会话的系统提示中——MEMORY.md（最多 2200 字符）用于环境/项目约定，USER.md（最多 1375 字符）用于你的个人资料——姓名、沟通偏好、技能水平、要避免的事项。这些由智能体自行维护（它自己写入），但你也可以手动编辑——它们的行为类似于优先级较低但自动更新的 SOUL.md。

如果你希望将隐藏行为（密码、IP、团队 ID）作为一项始终有效的规则，而不是在每次提示中重复，请将其放入 `SOUL.md`——这是唯一保证在每个会话中（无论项目或配置文件）都会加载的层次。

参考：

- [Hermes Agent 完整自定义指南](https://note.com/zephel01/n/n95cb081e42de?hl=en)
- [Hermes Agent 大师班——记忆层次](https://www.dailydoseofds.com/p/hermes-agent-masterclass/)
- [Hermes Agent 文档——快速入门](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)