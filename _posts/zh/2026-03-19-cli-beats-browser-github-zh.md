---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CLI 胜过浏览器：GitHub Actions
translated: true
type: note
---

问题：使用 Claude Code CLI 是否比在浏览器中点击来触发 GitHub Actions 工作流更容易？

回答：

是的，当然。使用 Claude Code（或任何 CLI 方法）来触发 GitHub Actions 工作流，比使用浏览器 UI 要简单得多，而且效率更高。原因如下：

## CLI 与浏览器用于 GitHub Actions

### CLI 优势

**速度与效率**
- 一条命令即可触发：`gh workflow run gh-pages.yml`
- 无需页面加载、导航或点击菜单
- 终端中即时反馈

**可脚本化与自动化**
- 可以与其他命令串联
- 易于循环、重试或调度
- 可以从脚本或其他工具如 Claude Code 中触发

**更好的可见性**
- `gh run list` 提供清晰、结构化的状态视图
- 可以编程方式轮询/监视运行
- 更容易将输出管道传输到其他工具

**上下文切换**
- 保持在终端中——无需打开浏览器
- 保持工作流不间断

---

### Claude Code 在纯 CLI 基础上的额外功能

Claude Code 可以：
- **智能决定*何时*触发** 工作流（例如，在构建成功后）
- **解析运行输出** 并做出反应——如检测 `in_progress` 与 `pending` 或 `success`
- **串联操作**——触发 → 等待 → 检查结果 → 处理失败
- **处理并发逻辑**——如您的示例所示，它自动检测到 `cancel-in-progress` 行为

---

### 来自您的示例

Claude Code 正确执行了：
1. 触发 `gh workflow run gh-pages.yml`
2. 验证新运行显示为 `pending`（`23255811075`）
3. 检测到并发计划运行处于 `in_progress`
4. 推理 `cancel-in-progress` 并发设置
5. 必要时重新运行并确认 `success`

这种 **观察 → 推理 → 行动** 的水平，正是使 Claude Code 比在 GitHub UI 中点击按钮更强大的原因。

---

### 快速参考

| 操作 | 浏览器 | CLI (`gh`) | Claude Code |
|---|---|---|---|
| 触发工作流 | 4–5 次点击 | 1 条命令 | 自动 |
| 检查状态 | 刷新页面 | `gh run list` | 自动 |
| 响应结果 | 手动 | 脚本化 | 智能 |
| 处理并发 | 手动检查 | 手动检查 | 推理 |

**底线：** CLI 在重复性上胜过浏览器；Claude Code 在智能性上胜过纯 CLI。