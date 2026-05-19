---
audio: false
generated: true
image: false
lang: en
layout: post
title: Trigger GitHub Actions via API
translated: false
type: note
---

**Question:** How to trigger a GitHub Actions workflow by API?

**Answer:**

There are two main ways to trigger a GitHub Actions workflow via the GitHub REST API:

1. **Using `workflow_dispatch`** — Recommended for manually triggering a specific workflow (most common use case).  
   The workflow must include `on: workflow_dispatch:` (optionally with `inputs`).

2. **Using `repository_dispatch`** — For triggering workflows from external systems with a custom event type (useful for cross-repo or third-party integrations).

### 1. Trigger via `workflow_dispatch` (preferred method)

**Workflow file requirement** (.github/workflows/my-workflow.yml):

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

- `{workflow_id}` can be:  
  - Workflow file name (e.g. `deploy.yml`)  
  - Workflow ID number (get it via GET /repos/{owner}/{repo}/actions/workflows)

**Example using curl** (2022-11-28 API version — current as of 2026):

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

- Response: `204 No Content` on success  
- `ref`: branch, tag, or commit SHA (required)  
- `inputs`: optional, must match workflow inputs

**Using GitHub CLI** (simpler):

```bash
gh workflow run deploy.yml \
  --ref main \
  -f environment=production \
  -f version=v1.5.0
```

### 2. Trigger via `repository_dispatch` (custom events)

**Workflow file requirement**:

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

In the workflow you can access:  
`github.event.client_payload.environment`

### Authentication & Permissions

- Use a **Personal Access Token (classic)** with `repo` scope (or `workflow` scope for workflow_dispatch)  
- For GitHub Apps: `actions:write` permission  
- Never commit tokens — use secrets or secure vaults

### Quick Tips

- Always include `-H "X-GitHub-Api-Version: 2022-11-28"` (or newer stable version)  
- Check workflow runs in the Actions tab after triggering  
- Rate limits apply — 180–5000 requests/hour depending on token type  
- To find workflow_id: `GET /repos/{owner}/{repo}/actions/workflows`

**References:**

- [Create a workflow dispatch event - GitHub Docs](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
- [Events that trigger workflows (workflow_dispatch) - GitHub Docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch)
- [Manually running a workflow - GitHub Docs](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow)
- [Create a repository dispatch event - GitHub Docs](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)