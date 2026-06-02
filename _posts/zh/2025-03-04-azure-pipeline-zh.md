---
audio: false
generated: true
lang: zh
layout: post
title: 使用 Azure DevOps 流水线
translated: true
type: note
---

让我们将这个问题拆解为两部分：**使用 Azure DevOps Pipelines** 和 **编写流水线 YAML 文件**。我将为这两部分提供清晰实用的说明。

---

### **如何使用 Azure DevOps Pipelines**
Azure DevOps Pipelines 是一款 CI/CD（持续集成/持续部署）工具，可自动化代码的构建、测试和部署。以下是入门指南：

#### **1. 项目设置**
- 使用你的组织账号登录 Azure DevOps (dev.azure.com)。
- 点击"新建项目"创建项目（或使用现有项目），设置项目名称和可见性（公开/私有）。

#### **2. 连接代码库**
- 进入项目中的 **Repos** 模块，将代码推送到代码库（GitHub、Azure Repos、Bitbucket 等）。
- 或在 **Pipelines（流水线）> New Pipeline（新建流水线）> Connect（连接）** 下关联外部代码库。

#### **3. 创建流水线**
- 导航至 **Pipelines（流水线）> Builds（生成）> New Pipeline（新建流水线）**。
- 选择你的代码库和分支。
- Azure 提供两种选项：
  - **经典编辑器**：基于图形界面的方式（无需 YAML）。
  - **YAML**：基于代码的流水线（推荐，更灵活且支持版本控制）。
- 对于 YAML，选择"Starter pipeline（入门流水线）"或根据代码库中的现有文件进行配置。

#### **4. 定义流水线**
- 如果使用 YAML，你需要在代码库根目录编写 `.yml` 文件（例如 `azure-pipelines.yml`）。（下文将详细说明。）
- 添加触发器（例如：每次推送到 `main` 分支时运行）、步骤（例如：构建、测试）和部署目标。

#### **5. 运行与监控**
- 保存并提交 YAML 文件（或在经典编辑器中保存）。
- 点击 **Run（运行）** 手动触发流水线，或根据触发器设置自动运行。
- 在 **Pipelines（流水线）> Builds（生成）** 下查看日志以监控进度或排查故障。

#### **6. 部署（可选）**
- 添加 **Release Pipeline（发布流水线）**（在 **Releases（发布）** 下），或扩展 YAML 以部署到 Azure App Service、Kubernetes 或虚拟机等环境。

---

### **如何编写 Azure Pipelines 的 YAML 文件**
YAML（YAML Ain't Markup Language）是一种人类可读的格式，用于定义流水线配置。以下是快速入门：

#### **基础结构**
```yaml
trigger:
  - main  # 当 'main' 分支更新时运行流水线

pool:
  vmImage: 'ubuntu-latest'  # 指定构建代理（例如 Ubuntu、Windows、macOS）

steps:
  - script: echo Hello, world!  # 要运行的简单命令
    displayName: '运行单行脚本'
```

- **`trigger`**：定义流水线运行的条件（例如：推送到 `main` 分支时）。
- **`pool`**：指定构建代理的虚拟机镜像。
- **`steps`**：列出要执行的任务（脚本、内置任务等）。

#### **常用元素**
1. **变量**：
   ```yaml
   variables:
     buildConfiguration: 'Release'
   steps:
     - script: echo $(buildConfiguration)  # 输出 'Release'
   ```

2. **作业**（分组步骤）：
   ```yaml
   jobs:
   - job: Build
     steps:
       - script: echo 正在构建...
   - job: Test
     steps:
       - script: echo 正在测试...
   ```

3. **任务**（预构建操作）：
   ```yaml
   steps:
     - task: DotNetCoreCLI@2  # 示例：构建 .NET 项目
       inputs:
         command: 'build'
         projects: '**/*.csproj'
   ```

4. **条件**：
   ```yaml
   steps:
     - script: echo 仅在 main 分支运行
       condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
   ```

5. **阶段**（用于多阶段流水线）：
   ```yaml
   stages:
   - stage: Build
     jobs:
       - job: BuildJob
         steps:
           - script: echo 正在构建...
   - stage: Deploy
     dependsOn: Build
     jobs:
       - job: DeployJob
         steps:
           - script: echo 正在部署...
   ```

#### **实际示例**
以下是一个 Node.js 应用的流水线：
```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0  # 安装 Node.js
    inputs:
      versionSpec: '16.x'
    displayName: '安装 Node.js'

  - script: |
      npm install
      npm run build
    displayName: '安装依赖并构建'

  - task: CopyFiles@2  # 复制构建产物
    inputs:
      contents: 'dist/**'
      targetFolder: '$(Build.ArtifactStagingDirectory)'

  - task: PublishBuildArtifacts@1  # 发布构建产物
    inputs:
      pathToPublish: '$(Build.ArtifactStagingDirectory)'
      artifactName: 'dist'
```

#### **YAML 编写技巧**
- 使用一致的缩进（2 个空格，不要用制表符）。
- 使用编辑器（如 VS Code 的 "YAML" 扩展）验证语法。
- 参考 [Azure Pipelines YAML 架构文档](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema) 查看选项。
- 从简单开始，根据需要逐步增加复杂度（例如阶段、变量）。

---

### **后续步骤**
- **动手尝试**：创建代码库，添加类似上述的基础 `azure-pipelines.yml` 文件，并在 Azure DevOps 中运行。
- **深入学习**：查阅微软的[官方文档](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started)或在 GitHub 上搜索示例流水线。
- **向我提问**：如果你遇到问题或需要特定示例（例如 Python、Java），请随时告诉我！

你想深入了解哪个方面？流水线设置、YAML 语法，还是其他内容？
