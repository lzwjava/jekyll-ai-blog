---
audio: false
generated: true
lang: zh
layout: post
title: 触发GitHub Actions
translated: true
type: note
---

是的，GitHub Action 可以触发另一个 GitHub Action，尽管不是直接触发。GitHub Actions 工作流通常由特定事件触发，例如推送、拉取请求或定时任务，但有几种间接方法可以实现一个工作流触发另一个工作流。以下是主要的实现方式：

---

### 1. 使用 `workflow_dispatch` 事件
您可以通过 GitHub API 使用 `workflow_dispatch` 事件以编程方式触发工作流。这允许一个工作流启动另一个配置为监听此事件的工作流。

- **工作原理**：第一个工作流通过 API 调用触发第二个工作流。
- **示例**：
{% raw %}
  ```yaml
  name: 触发其他工作流
  on: [push]
  jobs:
    trigger:
      runs-on: ubuntu-latest
      steps:
        - name: 触发工作流
          run: |
            curl -X POST \
              -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
              -H "Accept: application/vnd.github.v3+json" \
              https://api.github.com/repos/<owner>/<repo>/actions/workflows/<workflow_id>/dispatches \
              -d '{"ref": "main"}'
  ```
{% endraw %}
  将 `<owner>`、`<repo>` 和 `<workflow_id>` 替换为您的仓库详情和目标工作流的 ID。第二个工作流的配置中必须包含 `on: [workflow_dispatch]`。

---

### 2. 使用仓库分发事件
一个工作流可以通过 GitHub API 发送自定义的仓库分发事件，另一个工作流可以监听并响应此事件。

- **工作原理**：第一个工作流通过 GitHub API 发送仓库分发事件，第二个工作流响应该事件。
- **示例**：
  - 第一个工作流（发送事件）：
{% raw %}
    ```yaml
    name: 发送分发事件
    on: [push]
    jobs:
      send-dispatch:
        runs-on: ubuntu-latest
        steps:
          - name: 发送分发
            run: |
              curl -X POST \
                -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
                -H "Accept: application/vnd.github.v3+json" \
                https://api.github.com/repos/<owner>/<repo>/dispatches \
                -d '{"event_type": "custom_event"}'
    ```
{% endraw %}
  - 第二个工作流（由事件触发）：
    ```yaml
    name: 由分发触发
    on:
      repository_dispatch:
        types: [custom_event]
    jobs:
      respond:
        runs-on: ubuntu-latest
        steps:
          - name: 响应事件
            run: echo "由 custom_event 触发"
    ```

---

### 3. 通过 Git 事件触发
一个工作流可以通过生成 Git 事件（例如创建提交或打开拉取请求）来触发另一个工作流，第二个工作流配置为响应该事件。

- **工作原理**：第一个工作流修改仓库（例如通过推送提交），触发第二个配置为响应该事件（例如 `on: [push]`）的工作流。
- **示例**：
  ```yaml
  name: 创建提交
  on: [push]
  jobs:
    create-commit:
      runs-on: ubuntu-latest
      steps:
        - name: 检出代码
          uses: actions/checkout@v2
        - name: 创建文件
          run: echo "新文件" > newfile.txt
        - name: 提交并推送
          run: |
            git config user.name "GitHub Action"
            git config user.email "action@github.com"
            git add newfile.txt
            git commit -m "添加新文件"
            git push
  ```
  这可能会触发另一个设置为在 `push` 事件上运行的工作流。

---

### 关键注意事项
- **权限**：API 调用中使用的 GitHub token 必须具有足够的权限来触发工作流或发送分发事件。
- **速率限制**：请注意 GitHub 的 API 速率限制，特别是对于频繁运行的工作流。
- **避免循环**：通过添加条件来防止工作流无限循环触发。
- **配置**：确保目标工作流正确设置为监听预期事件。

---

### 结论
虽然 GitHub Actions 没有提供直接调用另一个工作流的机制，但您可以通过 `workflow_dispatch`、仓库分发事件或 Git 事件（如提交或拉取请求）间接实现此功能。这些方法允许您根据需要有效链接或触发工作流。
