---
audio: false
generated: true
lang: en
layout: post
title: Using Azure DevOps Pipelines
translated: false
type: note
---

Let's break this down into two parts: **using Azure DevOps Pipelines** and **writing YAML for pipelines**. I'll provide a clear, practical explanation for both.

---

### **How to Use Azure DevOps Pipelines**

Azure DevOps Pipelines is a CI/CD (Continuous Integration/Continuous Deployment) tool that automates building, testing, and deploying code. Here’s how to get started:

#### **1. Set Up a Project**

- Log into Azure DevOps (dev.azure.com) with your organization.
- Create a new project (or use an existing one) by clicking "New Project," giving it a name, and setting visibility (public/private).

#### **2. Connect Your Code**

- Go to **Repos** in your project and push your code to a repository (GitHub, Azure Repos, Bitbucket, etc.).
- Alternatively, link an external repo under **Pipelines > New Pipeline > Connect** and select your source.

#### **3. Create a Pipeline**

- Navigate to **Pipelines** > **Builds** > **New Pipeline**.
- Choose your repo and branch.
- Azure offers two options:
  - **Classic Editor**: A GUI-based approach (no YAML needed).
  - **YAML**: A code-based pipeline (recommended for flexibility and version control).
- For YAML, select "Starter pipeline" or configure from an existing file in your repo.

#### **4. Define the Pipeline**

- If using YAML, you'll write a `.yml` file (e.g., `azure-pipelines.yml`) in your repo’s root. (More on this below.)
- Add triggers (e.g., run on every push to `main`), steps (e.g., build, test), and deployment targets.

#### **5. Run and Monitor**

- Save and commit the YAML file (or save in the Classic Editor).
- Click **Run** to trigger the pipeline manually, or let it run automatically based on triggers.
- Check the logs under **Pipelines > Builds** to monitor progress or troubleshoot failures.

#### **6. Deploy (Optional)**

- Add a **release Pipeline** (under **Releases**) or extend your YAML to deploy to environments like Azure App Service, Kubernetes, or VMs.

---

### **How to Write YAML for Azure Pipelines**

YAML (Yet Another Markup Language) is a human-readable format used to define pipeline configurations. Here’s a crash course:

#### **Basic Structure**

```yaml
trigger:
  - main  # Run pipeline when 'main' branch is updated

pool:
  vmImage: 'ubuntu-latest'  # Specify the build agent (e.g., Ubuntu, Windows, macOS)

steps:
  - script: echo Hello, world!  # A simple command to run
    displayName: 'Run a one-line script'
```

- **`trigger`**: Defines when the pipeline runs (e.g., on push to `main`).
- **`pool`**: Specifies the virtual machine image for the build agent.
- **`steps`**: Lists tasks to execute (scripts, built-in tasks, etc.).

#### **Common Elements**

1. **Variables**:

   ```yaml
   variables:
     buildConfiguration: 'Release'
   steps:
     - script: echo $(buildConfiguration)  # Outputs 'Release'
   ```

2. **Jobs** (group steps):

   ```yaml
   jobs:
   - job: Build
     steps:
       - script: echo Building...
   - job: Test
     steps:
       - script: echo Testing...
   ```

3. **Tasks** (pre-built actions):

   ```yaml
   steps:
     - task: DotNetCoreCLI@2  # Example: Build a .NET project
       inputs:
         command: 'build'
         projects: '**/*.csproj'
   ```

4. **Conditions**:

   ```yaml
   steps:
     - script: echo This runs only on main
       condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
   ```

5. **Stages** (for multi-phase pipelines):

   ```yaml
   stages:
   - stage: Build
     jobs:
       - job: BuildJob
         steps:
           - script: echo Building...
   - stage: Deploy
     dependsOn: Build
     jobs:
       - job: DeployJob
         steps:
           - script: echo Deploying...
   ```

#### **Real-World Example**

Here’s a pipeline for a Node.js app:

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0  # Install Node.js
    inputs:
      versionSpec: '16.x'
    displayName: 'Install Node.js'

  - script: |
      npm install
      npm run build
    displayName: 'Install and Build'

  - task: CopyFiles@2  # Copy build artifacts
    inputs:
      contents: 'dist/**'
      targetFolder: '$(Build.ArtifactStagingDirectory)'

  - task: PublishBuildArtifacts@1  # Publish artifacts
    inputs:
      pathToPublish: '$(Build.ArtifactStagingDirectory)'
      artifactName: 'dist'
```

#### **Tips for Writing YAML**

- Use consistent indentation (2 spaces, no tabs).
- Validate syntax with an editor (e.g., VS Code with the "YAML" extension).
- Reference the [Azure Pipelines YAML schema](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema) for options.
- Start simple, then add complexity (e.g., stages, variables) as needed.

---

### **Next Steps**

- **Try it**: Create a repo, add a basic `azure-pipelines.yml` like the one above, and run it in Azure DevOps.
- **Learn more**: Check Microsoft’s [official docs](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started) or search for sample pipelines on GitHub.
- **Ask me**: If you hit a snag or want a specific example (e.g., Python, Java), let me know!

What do you want to dive deeper into? Setting up a pipeline, YAML syntax, or something else?
