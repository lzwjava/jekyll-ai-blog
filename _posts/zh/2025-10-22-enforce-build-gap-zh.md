---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 强制实施30分钟构建间隔
translated: true
type: note
---

### 修改工作流程以强制构建间隔30分钟

为确保您的Jekyll部署工作流程不会运行过于频繁（即连续运行之间至少间隔30分钟），您可以在`build`作业的早期添加条件步骤。该步骤将通过查询GitHub API获取此工作流程最近一次成功运行的时间戳。如果当前触发时间距离上次运行完成时间不足30分钟，作业将提前退出并显示消息（跳过构建）。

此方案特点：
- 使用GitHub REST API（无需外部工具）
- 仅检查**成功**的先前运行（状态："completed"，结果："success"）
- 计算时间差（秒）并与1800（30分钟）比较
- 兼容现有的推送和`workflow_dispatch`触发器
- 不影响并发设置（该设置处理重叠运行）

#### 更新后的YAML代码片段
将此新步骤插入到`build`作业的"检出代码库"步骤之后。工作流程其余部分保持不变。

{% raw %}
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      TELEGRAM_BOT_API_KEY: ${{ secrets.TELEGRAM_BOT_API_KEY }}
      OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: Enforce 30-Minute Build Gap
        id: cooldown
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # 获取此工作流程最近一次成功运行记录
          RUNS_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/${{ github.repository }}/actions/workflows/${{ github.workflow_ref }}/runs?status=completed&conclusion=success&per_page=1&sort=timestamp&direction=desc")

          # 提取最近成功运行的completed_at时间戳（ISO 8601格式）
          LAST_COMPLETED_AT=$(echo "$RUNS_RESPONSE" | jq -r '.[0].completed_at // empty')
          
          if [ -z "$LAST_COMPLETED_AT" ] || [ "$LAST_COMPLETED_AT" = "null" ]; then
            echo "未找到先前成功运行记录。继续执行构建。"
            echo "skip_build=false" >> $GITHUB_OUTPUT
            exit 0
          fi

          # 将时间戳转换为Unix秒数用于比较
          CURRENT_TIME=$(date -u +%s)
          LAST_TIME=$(date -d "$LAST_COMPLETED_AT" +%s)
          TIME_DIFF=$((CURRENT_TIME - LAST_TIME))

          echo "最近成功运行完成时间: $LAST_COMPLETED_AT (时间差: ${TIME_DIFF}秒)"

          if [ $TIME_DIFF -lt 1800 ]; then  # 1800秒 = 30分钟
            echo "构建已跳过：距离上次成功运行不足30分钟。"
            echo "skip_build=true" >> $GITHUB_OUTPUT
            exit 0
          else
            echo "时间间隔符合要求。继续执行构建。"
            echo "skip_build=false" >> $GITHUB_OUTPUT
            exit 0
          fi

      # 若冷却检查未通过则跳过整个构建（为后续步骤添加此条件或将构建步骤包裹在if中）
      - name: Set up Python 3.13.2
        if: steps.cooldown.outputs.skip_build != 'true'
        uses: actions/setup-python@v4
        with:
          python-version: "3.13.2"

      # ...（在此之后的所有剩余步骤重复添加'if: steps.cooldown.outputs.skip_build != 'true''条件）
```
{% endraw %}

#### 关键变更说明
1. **API查询**：
   - 使用`curl`调用GitHub Actions API的工作流运行端点
   - 筛选`status=completed`和`conclusion=success`仅获取已完成的成功运行
   - 限制`per_page=1`并按`timestamp desc`排序获取最近记录
   - 提取`completed_at`（上次运行的确切结束时间）

2. **时间计算**：
   - 使用`date`将当前时间和上次完成时间转换为Unix时间戳
   - 计算秒级时间差
   - 若小于1800秒，设置`skip_build=true`并提前退出步骤

3. **条件执行**：
   - 为**每个后续步骤**添加`if: steps.cooldown.outputs.skip_build != 'true'`（例如Python设置、安装依赖直至同步构建站点）
   - 确保冷却触发时作业在GitHub界面显示"skipped"，同时记录原因

4. **处理的边缘情况**：
   - 无历史运行记录：继续执行（首次构建）
   - 失败/进行中的历史运行：忽略并继续执行
   - API错误：默认继续执行（安全回退）
   - `jq`已预装在`ubuntu-latest`环境中，无需额外设置

#### 测试变更
- 将此配置提交到`main`分支（将触发工作流程）
- 快速多次触发推送/手动调度：30分钟内的第二次运行应被跳过
- 在作业日志中查看"构建已跳过"消息
- 如需调整间隔（如1小时），将`1800`改为`3600`

#### 替代方案
- **计划触发器**：若需*定期*每30分钟构建（无论推送），在`on:`部分添加：
  ```yaml
  schedule:
    - cron: '*/30 * * * *'  # 每30分钟
  ```
  但此设置不对推送触发强制间隔——如需可配合冷却步骤使用
- **自定义操作**：为提升可复用性，可将冷却逻辑封装为可复用工作流或复合操作
- **局限性**：此方案检查运行完成时间而非开始时间。若前次运行超过30分钟仍在执行，并发设置会自动取消

若此方案与您的具体需求不符（例如您希望实现*至少*每30分钟调度），请提供更多细节！