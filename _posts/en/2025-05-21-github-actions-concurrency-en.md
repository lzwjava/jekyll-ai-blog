---
audio: false
generated: true
lang: en
layout: post
title: GitHub Actions Concurrency Settings
translated: false
type: note
---

Your current GitHub Actions workflow configuration already has `cancel-in-progress: false`, which means it *should not* cancel in-progress jobs for the `gh-pages` concurrency group. If jobs are still being canceled, there might be another issue or misconfiguration causing this behavior. Below are steps to verify and fix the issue:

### 1. **Confirm Concurrency Settings**

Your configuration looks correct for preventing job cancellations:

```yaml
concurrency:
  group: 'gh-pages'
  cancel-in-progress: false
```

- **What this does**: The `concurrency` key with `cancel-in-progress: false` ensures that multiple workflow runs for the same `gh-pages` group can run simultaneously without canceling each other.
- **Where to place it**: Ensure this `concurrency` block is defined at the **workflow level** (top level of the YAML file, not inside a job or step). For example:

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
concurrency:
  group: 'gh-pages'
  cancel-in-progress: false
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      # Your steps here
```

If the `concurrency` block is misplaced (e.g., inside a job), it won't work as expected. Move it to the top level if needed.

### 2. **Check for Conflicting Concurrency Settings**

- **Multiple workflows**: If you have multiple workflows (e.g., separate YAML files) that interact with the `gh-pages` branch, ensure *all* relevant workflows have `cancel-in-progress: false`. A single workflow with `cancel-in-progress: true` (or missing `concurrency`) could cancel jobs from other workflows.
- **Repository settings**: Check if any repository-level settings or third-party GitHub Actions are enforcing cancellations. For example, some CI/CD integrations or custom actions might override concurrency behavior.

### 3. **Verify Workflow Triggers**

Jobs might appear to be "canceled" if triggers are misconfigured or if there are race conditions. Check the `on` section of your workflow:

- Ensure the workflow is triggered only when intended (e.g., `on: push: branches: [ main ]` or `on: pull_request`).
- If multiple triggers (e.g., `push` and `pull_request`) are defined, they might create overlapping runs. Use unique `concurrency.group` names for different triggers if needed, like:

{% raw %}

```yaml
concurrency:
  group: 'gh-pages-${{ github.event_name }}'
  cancel-in-progress: false
```

{% endraw %}

This creates separate concurrency groups for `push` and `pull_request` events, preventing them from interfering.

### 4. **Check GitHub Actions Logs**

- Go to the **Actions** tab in your GitHub repository and review the logs of canceled jobs.
- Look for messages indicating why the job was canceled (e.g., "Canceled due to concurrency" or other reasons like timeouts, manual cancellation, or failures).
- If the logs mention concurrency, double-check that *all* workflows touching the `gh-pages` branch have `cancel-in-progress: false`.

### 5. **Handle Manual Cancellations**

If someone manually cancels a workflow run via the GitHub UI, it will stop all jobs in that run, regardless of `cancel-in-progress: false`. Ensure your team knows not to manually cancel runs unless necessary.

### 6. **Consider Workflow Dependencies**

If jobs are being canceled due to dependencies or failures in earlier steps:

- Check for `needs` keywords in your workflow. If one job fails, dependent jobs may be skipped or canceled.
- Use `if: always()` to ensure subsequent jobs run even if earlier ones fail:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Build steps
  deploy:
    needs: build
    if: always()
    runs-on: ubuntu-latest
    steps:
      # Deploy steps
```

### 7. **Test with a Minimal Workflow**

If the issue persists, create a minimal test workflow to isolate the problem:

```yaml
name: Test Concurrency
on:
  push:
    branches: [ main ]
concurrency:
  group: 'gh-pages'
  cancel-in-progress: false
jobs:
  test-job:
    runs-on: ubuntu-latest
    steps:
      - name: Sleep to simulate long job
        run: sleep 60
      - name: Print message
        run: echo "Job completed!"
```

Push multiple commits to trigger concurrent runs and verify if jobs complete without cancellation.

### 8. **Check GitHub Actions Status**

Rarely, GitHub Actions may have platform-wide issues. Check the [GitHub Status page](https://www.githubstatus.com/) or recent posts on X about GitHub Actions outages.

### 9. **Debugging Tips**

- Add a step to log the workflow run ID and concurrency group for debugging:

{% raw %}

```yaml
steps:
  - name: Log run details
    run: echo "Run ID: ${{ github.run_id }}, Concurrency Group: ${{ github.workflow }}-${{ github.event_name }}"
```

{% endraw %}

- Use the GitHub Actions API to inspect running workflows programmatically if needed (requires advanced setup).

### If It’s Still Not Working

If jobs are still being canceled:

- Share the full workflow YAML file and a screenshot or description of the cancellation message from the GitHub Actions logs.
- Let me know if you’re using specific actions (e.g., `actions/checkout`, `peaceiris/actions-gh-pages`) or if you have multiple workflows interacting with `gh-pages`.

This will help pinpoint the exact issue. Let me know how I can assist further!
