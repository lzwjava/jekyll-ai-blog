---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 API 触发 GitHub Actions
translated: true
type: note
---

**Question:** 如何通过 API 触发 GitHub Actions workflow？

**Answer:**

通过 GitHub REST API 触发 GitHub Actions workflow 主要有两种方式：

1. **使用 `workflow_dispatch`** — 推荐用于手动触发特定的 workflow（最常见的使用场景）。
   workflow 必须包含 `on: workflow_dispatch:`（可选择性配置 `inputs`）。

2. **使用 `repository_dispatch`** — 用于从外部系统通过自定义事件类型触发 workflow（适用于跨仓库或第三方集成）。

### 1. 通过 `workflow_dispatch` 触发（首选方法）

**Workflow 文件要求** (.github/workflows/my-workflow.yml):

{% raw %}
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
      version:
        description: 'Version tag'
        required: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.environment }} version ${{ inputs.version || 'latest' }}"
```
{% endraw %}

**API Endpoint**

`POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches`

- `{workflow_id}` 可以是：
  - Workflow 文件名（例如 `deploy.yml`）
  - Workflow ID 数字（通过 GET /repos/{owner}/{repo}/actions/workflows 获取）

**Example using curl** (2022-11-28 API 版本 — 截至 2026 年的当前版本):

```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/deploy.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "environment": "production",
      "version": "v1.5.0"
    }
  }'
```

- 响应：成功时返回 `204 No Content`
- `ref`：branch、tag 或 commit SHA（必填）
- `inputs`：可选，必须与 workflow 中的 inputs 匹配

**Using GitHub CLI**（更简单）：

```bash
gh workflow run deploy.yml \
  --ref main \
  -f environment=production \
  -f version=v1.5.0
```

### 2. 通过 `repository_dispatch` 触发（自定义事件）

**Workflow 文件要求**：

```yaml
on:
  repository_dispatch:
    types: [deploy, build, test]
```

**API Endpoint**

`POST /repos/{owner}/{repo}/dispatches`

**Example curl**:

```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "deploy",
    "client_payload": {
      "environment": "prod",
      "service": "api"
    }
  }'
```

在 workflow 中你可以通过以下方式访问：

`github.event.client_payload.environment`

### Authentication & Permissions

- 使用带有 `repo` 作用域（如果是 workflow_dispatch 则需要 `workflow` 作用域）的 **Personal Access Token (classic)**
- 对于 GitHub Apps：需要 `actions:write` 权限
- 切勿提交 token —— 请使用 secrets 或安全库（secure vaults）

### Quick Tips

- 始终包含 `-H "X-GitHub-Api-Version: 2022-11-28"`（或更新的稳定版本）
- 触发后，在 Actions 选项卡中查看 workflow 运行状态
- 存在速率限制（Rate limits） —— 取决于 token 类型，每小时 180–5000 次请求
- 查找 workflow_id：`GET /repos/{owner}/{repo}/actions/workflows`

**References:**

- [Create a workflow dispatch event - GitHub Docs](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
- [Events that trigger workflows (workflow_dispatch) - GitHub Docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch)
- [Manually running a workflow - GitHub Docs](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow)
- [Create a repository dispatch event - GitHub Docs](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
