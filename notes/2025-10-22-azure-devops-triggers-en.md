---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring Azure DevOps Branch Triggers
translated: false
type: note
---

Azure DevOps Pipelines allow you to configure which branches trigger builds and deployments. This is primarily done through **CI triggers** (for builds on code pushes) and **PR triggers** (for pull requests). The configuration differs slightly between YAML pipelines (recommended for version control) and classic pipelines. Below, I'll focus on YAML first, as it's the modern approach, then cover classic briefly. All examples assume a Git repository.

## YAML Pipelines: Configuring Branch Triggers

YAML pipelines define triggers directly in your `azure-pipelines.yml` file. By default, pipelines trigger on pushes to **all branches** (equivalent to `trigger: branches: include: - '*'`). You can customize this for finer control.

### Step 1: Basic Setup

1. In your Azure DevOps project, go to **Pipelines > Builds** (or **Releases** for CD).
2. Create or edit a pipeline and select **YAML** as the template.
3. In the YAML editor, add a `trigger` section at the top level.

### Step 2: Simple Branch Includes

Use a simple list to trigger on specific branches or patterns:

```yaml
trigger:
- main          # Triggers on pushes to 'main'
- develop       # Also 'develop'
- releases/*    # Any branch starting with 'releases/' (e.g., releases/v1.0)
```

- Save and commit the YAML file to your repo. The pipeline will now only run for these branches.
- Wildcards like `*` (zero or more characters) and `?` (single character) are supported. Quote patterns starting with `*` (e.g., `*-hotfix`).

### Step 3: Advanced Includes/Excludes

For exclusions or more precision:

```yaml
trigger:
  branches:
    include:
    - main
    - releases/*
    - feature/*
    exclude:
    - releases/old-*     # Excludes 'releases/old-v1', etc.
    - feature/*-draft    # Excludes draft features
```

- **Include**: Branches that *can* trigger (starts with all if omitted).
- **Exclude**: Filters out from the include list (applied after includes).
- If you specify any `branches` clause, it overrides the default (all branches)—only explicit includes will trigger.
- For tags: Use `refs/tags/v1.*` in includes.

### Step 4: Path Filters (Optional)

Combine with file paths for granular control:

```yaml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - src/*.cs          # Only if changes in 'src' folder
    exclude:
    - docs/*.md         # Ignore doc changes
```

- Paths are relative to the repo root and case-sensitive.

### Step 5: Batching and Opting Out

- **Batch runs**: To queue multiple pushes into one build (reduces noise):

  ```yaml
  trigger:
    batch: true
    branches:
      include:
      - main
  ```

- **Disable triggers**: Set `trigger: none` for no CI.
- **Skip per commit**: Add `[skip ci]` or `***NO_CI***` to commit messages.

### PR Triggers

For pull requests, add a `pr` section:

```yaml
pr:
  branches:
    include:
    - main
    - develop
  paths:
    include:
    - src/*
```

- This validates PRs targeting these branches.

### Testing

- Push to a matching branch: Pipeline runs automatically.
- View runs in **Pipelines > Runs** and check the trigger details.

## Classic Pipelines: Configuring Branch Triggers

For legacy/classic pipelines (UI-based):

1. Edit your pipeline in **Pipelines > Builds**.
2. Go to **Triggers > Continuous integration**.
3. Check **Enable continuous integration**.
4. Under **Branch filters**, add includes (e.g., `main`) or excludes (e.g., `develop`).
5. For paths: Use **Path filters** in the same tab.
6. For PRs: Go to **Triggers > Pull request validation** and set branch filters.

Switch to YAML for better maintainability.

## Best Practices

- Start simple: Trigger on `main` and `develop` only.
- Use excludes for noisy branches like `*-hotfix`.
- Secure with branch policies (Repos > Branches > Policies) for required reviewers.
- Monitor: Use pipeline analytics for trigger frequency.

For the latest details, refer to official docs.

[Build Azure Repos Git repositories](https://learn.microsoft.com/en-us/azure/devops/pipelines/repos/azure-repos-git?view=azure-devops&tabs=yaml)
[Triggers in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops&tabs=yaml)
