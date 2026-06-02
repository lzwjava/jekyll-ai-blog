---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 配置 Azure DevOps 分支触发器
translated: true
type: note
---

Azure DevOps Pipelines 允许您配置触发构建和部署的分支。这主要通过 **CI 触发器**（用于代码推送时的构建）和 **PR 触发器**（用于拉取请求）实现。YAML 管道（推荐用于版本控制）和经典管道的配置略有不同。以下我将首先重点介绍 YAML，因为这是现代方法，然后简要介绍经典管道。所有示例均假设使用 Git 仓库。

## YAML 管道：配置分支触发器

YAML 管道直接在您的 `azure-pipelines.yml` 文件中定义触发器。默认情况下，管道会在推送到 **所有分支** 时触发（相当于 `trigger: branches: include: - '*'`）。您可以自定义此设置以实现更精细的控制。

### 步骤 1：基本设置
1. 在您的 Azure DevOps 项目中，转到 **Pipelines > Builds**（对于 CD，则为 **Releases**）。
2. 创建或编辑管道，并选择 **YAML** 作为模板。
3. 在 YAML 编辑器中，在顶层添加一个 `trigger` 部分。

### 步骤 2：简单分支包含
使用简单列表来触发特定分支或模式：
```yaml
trigger:
- main          # 在推送到 'main' 时触发
- develop       # 同时也在 'develop' 上触发
- releases/*    # 任何以 'releases/' 开头的分支（例如，releases/v1.0）
```
- 将 YAML 文件保存并提交到您的仓库。管道现在将仅在这些分支上运行。
- 支持通配符，如 `*`（零个或多个字符）和 `?`（单个字符）。对于以 `*` 开头的模式请使用引号（例如，`"*-hotfix"`）。

### 步骤 3：高级包含/排除
用于排除或更高精度控制：
```yaml
trigger:
  branches:
    include:
    - main
    - releases/*
    - feature/*
    exclude:
    - releases/old-*     # 排除 'releases/old-v1' 等
    - feature/*-draft    # 排除草稿功能分支
```
- **Include**：*可以* 触发构建的分支（如果省略，则默认为所有分支）。
- **Exclude**：从包含列表中过滤掉的分支（在包含规则之后应用）。
- 如果您指定了任何 `branches` 子句，它将覆盖默认设置（所有分支）——只有显式包含的分支才会触发。
- 对于标签：在包含中使用 `refs/tags/v1.*`。

### 步骤 4：路径过滤器（可选）
结合文件路径进行更精细的控制：
```yaml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - src/*.cs          # 仅当 'src' 文件夹中有更改时触发
    exclude:
    - docs/*.md         # 忽略文档更改
```
- 路径相对于仓库根目录，并且区分大小写。

### 步骤 5：批处理和选择退出
- **批处理运行**：将多次推送排队到一个构建中（减少干扰）：
  ```yaml
  trigger:
    batch: true
    branches:
      include:
      - main
  ```
- **禁用触发器**：设置 `trigger: none` 以禁用 CI。
- **按提交跳过**：在提交消息中添加 `[skip ci]` 或 `***NO_CI***`。

### PR 触发器
对于拉取请求，添加一个 `pr` 部分：
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
- 这将验证针对这些分支的 PR。

### 测试
- 推送到匹配的分支：管道会自动运行。
- 在 **Pipelines > Runs** 中查看运行情况并检查触发器详细信息。

## 经典管道：配置分支触发器
对于旧版/经典管道（基于 UI）：
1. 在 **Pipelines > Builds** 中编辑您的管道。
2. 转到 **Triggers > Continuous integration**。
3. 勾选 **Enable continuous integration**。
4. 在 **Branch filters** 下，添加包含（例如，`main`）或排除（例如，`develop`）。
5. 对于路径：在同一选项卡中使用 **Path filters**。
6. 对于 PR：转到 **Triggers > Pull request validation** 并设置分支过滤器。

建议切换到 YAML 以获得更好的可维护性。

## 最佳实践
- 从简单开始：仅触发 `main` 和 `develop` 分支。
- 对嘈杂的分支（如 `*-hotfix`）使用排除规则。
- 使用分支策略（Repos > Branches > Policies）进行安全加固，例如设置必需的审阅者。
- 监控：使用管道分析来了解触发频率。

有关最新详细信息，请参阅官方文档。

[构建 Azure Repos Git 仓库](https://learn.microsoft.com/en-us/azure/devops/pipelines/repos/azure-repos-git?view=azure-devops&tabs=yaml)
[Azure Pipelines 中的触发器](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops&tabs=yaml)
