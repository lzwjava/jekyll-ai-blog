---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 动态技能加载实时生效
translated: true
type: note
---

**问题：** Claude Code 能否在一次会话中动态生成一个新技能，并让它立即加载，而无需重启？

**回答：**

是的——这可以工作，并且在最近的 Claude Code 版本中得到了官方支持。Claude Code 会监控技能目录的文件变化。在 `~/.claude/skills/`、项目中的 `.claude/skills/` 或 `--add-dir` 目录内的 `.claude/skills/` 中添加、编辑或删除技能，都会在当前会话中生效，无需重启。

因此，你想象中的“自修改代理”循环——Claude 在任务中途自己编写 `SKILL.md`，然后使用它——是可行的：

```bash
# 在 Claude Code 会话中，Claude 可以自行完成此操作：
mkdir -p .claude/skills/changelog-gen
cat > .claude/skills/changelog-gen/SKILL.md << 'EOF'
---
name: changelog-gen
description: 根据 git diff 生成更新日志条目。当用户要求总结最近的更改或撰写发布说明时使用。
---

# 更新日志生成

1. 运行 `git log --oneline -20` 和 `git diff HEAD~5 --stat`
2. 将更改分组：feat / fix / refactor / docs
3. 按照 Keep a Changelog 格式输出，最新的在前
EOF
# 技能现已生效——下一个相关提示即可触发它。无需重启。
```

从机制上讲，它之所以能在不撑爆上下文的情况下工作，是因为技能使用了渐进式披露。Claude 在启动时加载元数据并将其包含在系统提示中——这是一种轻量级方法，意味着你可以安装许多技能而不会造成上下文负担；Claude 只知道每个技能的存在以及何时使用它。元数据每个技能约 100 个 token；完整指令（少于 5k token）仅在 Claude 确定技能适用时才加载；捆绑资源则按需加载。文件监控器仅实时刷新该元数据索引。

可能会给你带来麻烦的注意事项：

1. **顶级技能目录必须已经存在。** 创建一个在会话启动时尚不存在的顶级技能目录，需要重启 Claude Code 以便新目录能被监控。因此，在启动前执行 `mkdir -p .claude/skills`，或者在那里保留一个空的 `.gitkeep` 文件。在已有目录内部，新的技能文件夹可以热加载。

2. **只有 SKILL.md 文本可以热重载。** 实时变化检测只覆盖 SKILL.md 文本。对于一个同时也是插件的技能文件夹，对 hooks/、.mcp.json、agents/ 和 output-styles/ 的更改需要执行 `/reload-plugins` 才能生效。纯 markdown 技能是即时的；插件级别的则需要 `/reload-plugins`。

3. **触发完全依赖于 `description` 前置元数据**——Claude 会将你的提示与描述进行匹配，因此一个描述含糊的动态生成技能永远不会被触发。如果你想在同一会话中确定性地调用它，只需明确告诉 Claude：“使用 changelog-gen 技能。”

对于你的 `ww`/`iclaw`/`zz` 代理工具，一个有趣的模式是**引导技能**：一个元技能，其任务是“当用户描述一个重复的工作流程时，将其提炼成 `.claude/skills/` 下的一个新技能。”这本质上就是运行时自我扩展——代理将自己短暂的体验编译成持久的、低 token 成本的能力。Anthropic 正好提供了一个 `skill-creator` 技能来实现这一点；动态加载行为使其可以在单次会话中使用，而不是陷入编写-重启-测试的循环。

有一点需要凭经验验证（在一个测试仓库中花 5 分钟测试）：一个在对话中途创建的技能是否会在下一次交互时*自动*触发，或者元数据刷新会延迟一个回合。文档说“在当前会话中生效”，但对于刚创建的技能的自动触发敏感性值得测试——通过名称显式调用是可靠的路径。

**参考：**

- [使用技能扩展 Claude — Claude Code 文档](https://code.claude.com/docs/en/skills)
- [代理技能概述 — Claude API 文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)