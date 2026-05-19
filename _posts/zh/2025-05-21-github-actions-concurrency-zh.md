---
audio: false
generated: true
lang: zh
layout: post
title: GitHub Actions并发配置
translated: true
type: note
---

您当前的 GitHub Actions 工作流配置已设置 `cancel-in-progress: false`，这意味着它*不应*取消 `gh-pages` 并发组中正在进行的作业。如果作业仍被取消，可能是其他问题或配置错误导致此行为。以下是验证和修复问题的步骤：

### 1. **确认并发设置**
您的配置在防止作业取消方面看起来是正确的：

```yaml
concurrency:
  group: 'gh-pages'
  cancel-in-progress: false
```

- **作用说明**：带有 `cancel-in-progress: false` 的 `concurrency` 键可确保同一 `gh-pages` 组的多个工作流运行能够同时进行而不会相互取消。
- **放置位置**：确保此 `concurrency` 块定义在**工作流级别**（YAML 文件的顶层，不在作业或步骤内部）。例如：

```yaml
name: 部署到 GitHub Pages
on:
  push:
    branches: [ main ]
concurrency:
  group: 'gh-pages'
  cancel-in-progress: false
jobs:
  构建和部署:
    runs-on: ubuntu-latest
    steps:
      # 您的步骤在此处
```

如果 `concurrency` 块位置错误（例如在作业内部），它将无法按预期工作。如需调整，请将其移至顶层。

### 2. **检查冲突的并发设置**
- **多个工作流**：如果您有多个与 `gh-pages` 分支交互的工作流（例如独立的 YAML 文件），请确保*所有*相关的工作流都设置了 `cancel-in-progress: false`。只要有一个工作流设置了 `cancel-in-progress: true`（或缺少 `concurrency` 配置），就可能会取消其他工作流的作业。
- **仓库设置**：检查是否有仓库级设置或第三方 GitHub Actions 强制执行取消操作。例如，某些 CI/CD 集成或自定义操作可能会覆盖并发行为。

### 3. **验证工作流触发器**
如果触发器配置错误或存在竞态条件，作业可能看似被“取消”。请检查工作流的 `on` 部分：
- 确保工作流仅在预期时触发（例如 `on: push: branches: [ main ]` 或 `on: pull_request`）。
- 如果定义了多个触发器（例如 `push` 和 `pull_request`），它们可能会创建重叠的运行。如需不同触发器使用独立的 `concurrency.group` 名称，可参考：

{% raw %}
```yaml
concurrency:
  group: 'gh-pages-${{ github.event_name }}'
  cancel-in-progress: false
```
{% endraw %}

这会为 `push` 和 `pull_request` 事件创建独立的并发组，防止相互干扰。

### 4. **检查 GitHub Actions 日志**
- 前往 GitHub 仓库的 **Actions** 标签页，查看被取消作业的日志。
- 查找指示作业取消原因的消息（例如“因并发被取消”，或其他原因如超时、手动取消或失败）。
- 如果日志提及并发问题，请仔细检查所有涉及 `gh-pages` 分支的工作流是否都设置了 `cancel-in-progress: false`。

### 5. **处理手动取消操作**
如果有人通过 GitHub 界面手动取消工作流运行，无论 `cancel-in-progress: false` 如何设置，都会停止该次运行中的所有作业。请确保团队成员了解除非必要，不要手动取消运行。

### 6. **考虑工作流依赖关系**
如果作业因早期步骤的依赖关系或失败而被取消：
- 检查工作流中的 `needs` 关键字。如果某个作业失败，依赖它的作业可能会被跳过或取消。
- 使用 `if: always()` 确保即使早期作业失败，后续作业仍能运行：

```yaml
jobs:
  构建:
    runs-on: ubuntu-latest
    steps:
      # 构建步骤
  部署:
    needs: 构建
    if: always()
    runs-on: ubuntu-latest
    steps:
      # 部署步骤
```

### 7. **使用最小化工作流测试**
如果问题仍然存在，可创建一个最小化测试工作流来隔离问题：

```yaml
name: 测试并发
on:
  push:
    branches: [ main ]
concurrency:
  group: 'gh-pages'
  cancel-in-progress: false
jobs:
  测试作业:
    runs-on: ubuntu-latest
    steps:
      - name: 睡眠模拟长时作业
        run: sleep 60
      - name: 输出信息
        run: echo "作业完成！"
```

推送多次提交以触发并发运行，并验证作业是否能在无取消的情况下完成。

### 8. **检查 GitHub Actions 状态**
在极少数情况下，GitHub Actions 可能出现平台级问题。请查看 [GitHub 状态页面](https://www.githubstatus.com/)或 X 上关于 GitHub Actions 中断的最新消息。

### 9. **调试技巧**
- 添加步骤记录工作流运行 ID 和并发组以便调试：

{% raw %}
```yaml
steps:
  - name: 记录运行详情
    run: echo "运行 ID: ${{ github.run_id }}, 并发组: ${{ github.workflow }}-${{ github.event_name }}"
```
{% endraw %}

- 如需编程方式检查运行中的工作流，可使用 GitHub Actions API（需要高级设置）。

### 如果问题仍未解决
如果作业仍被取消：
- 请分享完整的工作流 YAML 文件，以及 GitHub Actions 日志中取消消息的截图或描述。
- 告知是否使用了特定操作（例如 `actions/checkout`、`peaceiris/actions-gh-pages`），或者是否有多个工作流与 `gh-pages` 交互。

这将有助于精确定位问题。请告知如何进一步协助！