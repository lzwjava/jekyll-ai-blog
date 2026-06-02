---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Jenkins任务配置指南
translated: true
type: note
---

### 配置 Jenkins 中的任务

Jenkins 支持不同类型的任务（也称为项目），最常见的是**自由风格项目**（适用于简单构建）和**流水线项目**（适用于使用 Jenkinsfile 的更复杂脚本化工作流）。下面我将概述这两种类型的配置步骤。假设您已安装并运行 Jenkins（例如通过 Docker 或在服务器上）。访问 Jenkins 仪表板（地址为 `http://localhost:8080` 或您的服务器 URL）并登录。

#### 创建和配置自由风格项目的步骤

自由风格项目操作简单，使用图形界面配置步骤，非常适合初学者或简单的代码构建和测试任务。

1. **新建任务**：
   - 在 Jenkins 仪表板左侧菜单栏点击**新建任务**。
   - 输入任务名称（例如 "MyFirstBuild"）。
   - 选择**自由风格项目**并点击**确定**。

2. **通用设置**：
   - 为任务添加描述信息。
   - 可选启用功能如"丢弃旧的构建"（例如仅保留最近10次构建）或添加参数（例如在构建时接收用户输入的字符串参数或选项参数）。

3. **源码管理**：
   - 选择版本控制工具，如 Git。
   - 输入代码仓库地址（例如 GitHub 仓库）。
   - 按需添加凭据（例如用户名/密码或 SSH 密钥）。
   - 指定构建分支（例如 `*/main`）。

4. **构建触发器**：
   - 选择任务启动方式，例如：
     - **定期构建**（例如使用 cron 语法 `H/5 * * * *` 表示每5分钟执行）
     - **轮询 SCM** 检查代码变更
     - **GitHub 钩子触发器** 接收 GitHub 的 Webhook
     - **在其他项目构建后构建** 实现任务链

5. **构建环境**：
   - 勾选选项如**构建前清空工作区**确保环境清洁
   - 为控制台输出添加时间戳或设置环境变量

6. **构建步骤**：
   - 点击**增加构建步骤**并选择操作如：
     - **执行 shell**（Linux/Mac 系统：例如 `echo "Hello World"` 或运行脚本）
     - **调用顶层 Maven 目标**（Java 项目构建）
     - **执行 Windows 批处理命令**（Windows 系统）
   - 可依次添加多个步骤

7. **构建后操作**：
   - 添加操作如：
     - **归档成品**（例如保存 JAR 文件）
     - **发布 JUnit 测试结果报告**
     - **发送邮件通知**（根据构建成功/失败状态）
     - **触发其他项目**

8. **保存并运行**：
   - 点击**保存**
   - 返回任务页面点击**立即构建**进行测试
   - 查看控制台输出获取详细信息

#### 创建和配置流水线项目的步骤

流水线通过代码定义（声明式或脚本式），为 CI/CD 工作流提供更灵活的配置方式。

1. **新建任务**：
   - 在仪表板点击**新建任务**
   - 输入名称并选择**流水线**，点击**确定**

2. **通用设置**：
   - 类似自由风格项目：添加描述、参数等

3. **构建触发器**：
   - 与自由风格项目相同的选项（如 Webhook、定时构建）

4. **流水线定义**：
   - 选择**Pipeline script**直接编写代码，或选择**Pipeline script from SCM**从代码仓库获取（例如 Git 中的 `Jenkinsfile`）
   - 声明式流水线脚本示例：

     ```
     pipeline {
         agent any
         stages {
             stage('Build') {
                 steps {
                     echo 'Building...'
                     sh 'mvn clean install'  // Maven 构建示例
                 }
             }
             stage('Test') {
                 steps {
                     echo 'Testing...'
                     sh 'mvn test'
                 }
             }
             stage('Deploy') {
                 steps {
                     echo 'Deploying...'
                 }
             }
         }
         post {
             always {
                 echo '此步骤始终执行'
             }
         }
     }
     ```

   - 此示例定义了包含构建、测试、部署阶段的流水线

5. **保存并运行**：
   - 保存任务
   - 执行构建并通过流水线视图监控各阶段进度

Jenkins 在每个配置区域都提供了丰富选项，请根据需求进行探索（例如安全方面可添加凭据，并行处理可使用代理/节点）。新手建议从自由风格项目入门，后续为扩展性需求转向流水线。

### Jenkins 的软件集成与协作

Jenkins 通过**插件**（超过2000个可用）具有高度可扩展性，可与 DevOps 生态中的几乎所有工具集成。这些集成支持构建触发、部署、测试、通知等功能。插件可通过**管理 Jenkins > 管理插件**安装。

#### 按类别划分的常见集成

- **版本控制**：Git、GitHub、GitLab、Bitbucket、SVN – 用于拉取代码并通过 Webhook 在提交/推送事件时触发构建
- **容器化与编排**：Docker（构建/推送镜像）、Kubernetes（部署到集群）、Helm – 用于基于容器的工作流
- **云服务商**：AWS（通过插件使用 EC2、S3、Lambda）、Azure、Google Cloud – 用于部署到云基础设施
- **测试与质量**：SonarQube（代码质量扫描）、Selenium（UI测试）、JUnit（单元测试）、Cucumber（BDD）– 集成到构建步骤实现自动化测试
- **部署与监控**：Ansible、Terraform（基础设施即代码）、Prometheus、Grafana – 用于构建后的编排和监控
- **通知与协作**：Slack、Microsoft Teams、邮件、Jira、Trello – 发送构建状态提醒或更新工单
- **构建工具**：Maven、Gradle（Java）、npm（Node.js）、pip（Python）– 执行各语言构建
- **安全**：OWASP Dependency-Check、Trivy（漏洞扫描）– 在持续集成过程中进行安全扫描
- **其他**：Artifactory/Nexus（制品仓库）、Zapier（无代码集成）、Octopus Deploy（高级部署）

例如集成 GitHub 时，安装 GitHub 插件即可启用 Webhook 触发。使用 Docker 时，通过 Docker Pipeline 插件在流水线中构建镜像。甚至可以为特定工具创建自定义插件。

如需了解更多，请查阅官方插件索引。请定期更新插件以确保安全。

#### 参考资料

- [使用项目 - Jenkins](https://www.jenkins.io/doc/book/using/working-with-projects/)
- [Jenkins - 设置构建任务 - Tutorials Point](https://www.tutorialspoint.com/jenkins/jenkins_setup_build_jobs.htm)
- [如何在 Jenkins 中创建和配置构建任务 | BrowserStack](https://www.browserstack.com/guide/build-jobs-in-jenkins)
- [Jenkins 构建：在 Jenkins 中设置自由风格项目（分步指南）](https://phoenixnap.com/kb/jenkins-build-freestyle-project)
- [管理插件 - Jenkins](https://www.jenkins.io/doc/book/managing/plugins/)
- [如何将 Jenkins 与不同工具和技术集成？](https://www.addwebsolution.com/blog/integrating-jenkins-with-other-tools-and-technologies)
- [Jenkins 插件库](https://plugins.jenkins.io/)
- [Jenkins 官网](https://www.jenkins.io/)
- [十大精选 Jenkins 插件 | Octopus 博客](https://octopus.com/blog/jenkins-ten-plugins)
