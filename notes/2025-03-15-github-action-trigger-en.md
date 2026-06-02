---
audio: false
generated: true
lang: en
layout: post
title: Triggering GitHub Actions
translated: false
type: note
---

Yes, a GitHub Action can trigger another GitHub Action, though not directly. GitHub Actions workflows are typically triggered by specific events like pushes, pull requests, or schedules, but there are several indirect methods to make one workflow trigger another. Below are the primary ways this can be achieved:

---

### 1. Using the `workflow_dispatch` Event
You can trigger a workflow programmatically using the `workflow_dispatch` event via the GitHub API. This allows one workflow to initiate another that is configured to listen for this event.

- **How it works**: The first workflow makes an API call to trigger the second workflow.
- **Example**:
{% raw %}
  ```yaml
  name: Trigger Another Workflow
  on: [push]
  jobs:
    trigger:
      runs-on: ubuntu-latest
      steps:
        - name: Trigger Workflow
          run: |
            curl -X POST \
              -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
              -H "Accept: application/vnd.github.v3+json" \
              https://api.github.com/repos/<owner>/<repo>/actions/workflows/<workflow_id>/dispatches \
              -d '{"ref": "main"}'
  ```
{% endraw %}
  Replace `<owner>`, `<repo>`, and `<workflow_id>` with your repository details and the target workflow's ID. The second workflow must include `on: [workflow_dispatch]` in its configuration.

---

### 2. Using Repository Dispatch Events
A workflow can send a custom event using a repository dispatch, which another workflow can listen for and trigger on.

- **How it works**: The first workflow sends a repository dispatch event via the GitHub API, and the second workflow responds to that event.
- **Example**:
  - First workflow (sends the event):
{% raw %}
    ```yaml
    name: Send Dispatch Event
    on: [push]
    jobs:
      send-dispatch:
        runs-on: ubuntu-latest
        steps:
          - name: Send Dispatch
            run: |
              curl -X POST \
                -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
                -H "Accept: application/vnd.github.v3+json" \
                https://api.github.com/repos/<owner>/<repo>/dispatches \
                -d '{"event_type": "custom_event"}'
    ```
{% endraw %}
  - Second workflow (triggered by the event):
    ```yaml
    name: Triggered by Dispatch
    on:
      repository_dispatch:
        types: [custom_event]
    jobs:
      respond:
        runs-on: ubuntu-latest
        steps:
          - name: Respond to Event
            run: echo "Triggered by custom_event"
    ```

---

### 3. Triggering via Git Events
One workflow can trigger another by generating a Git event, such as creating a commit or opening a pull request, which the second workflow is set to respond to.

- **How it works**: The first workflow modifies the repository (e.g., by pushing a commit), triggering a second workflow configured for that event (e.g., `on: [push]`).
- **Example**:
  ```yaml
  name: Create Commit
  on: [push]
  jobs:
    create-commit:
      runs-on: ubuntu-latest
      steps:
        - name: Checkout
          uses: actions/checkout@v2
        - name: Create File
          run: echo "New file" > newfile.txt
        - name: Commit and Push
          run: |
            git config user.name "GitHub Action"
            git config user.email "action@github.com"
            git add newfile.txt
            git commit -m "Add new file"
            git push
  ```
  This could trigger another workflow set to run on `push` events.

---

### Key Considerations
- **Permissions**: The GitHub token used in API calls must have sufficient permissions to trigger workflows or send dispatch events.
- **Rate Limits**: Be aware of GitHub's API rate limits, especially for frequently running workflows.
- **Avoid Loops**: Prevent infinite loops by adding conditions to stop workflows from endlessly triggering each other.
- **Configuration**: Ensure the target workflow is correctly set up to listen for the intended event.

---

### Conclusion
While GitHub Actions doesn’t offer a direct mechanism for one workflow to call another, you can achieve this indirectly using `workflow_dispatch`, repository dispatch events, or Git events like commits or pull requests. These methods allow you to chain or trigger workflows effectively based on your needs.
