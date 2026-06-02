---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 实用Jenkins持续集成与持续交付指南
translated: true
type: note
---

太棒了——这就为你打造一份**简洁、端到端的 Jenkins 指南**，你可以立即在工作中使用。我会保持内容易于浏览，避免使用过宽的表格。

# Jenkins 是什么（以及何时使用它）

Jenkins 是一个自托管的 CI/CD 自动化服务器：你将它连接到源码仓库，在 `Jenkinsfile` 中定义流水线，它就会在一台或多台机器（“代理节点”）上运行构建、测试和部署。流水线有两种风格——**声明式**（首选）和**脚本式**——两者均由项目提供文档支持。([Jenkins][1])

---

# 核心架构（通俗解释）

* **控制器**：Web 界面、队列和编排核心。
* **代理/节点**：实际运行任务的机器（虚拟机、容器、物理机）。你可以添加多个代理节点，并按能力为其打标签（例如 `java8`、`docker`）。([Jenkins][2])
* **任务/流水线**：工作的定义（理想情况下以代码形式存储在仓库中）。
* **插件**：用于增加功能（凭据管理、认证策略、云代理、JCasC 等）。

---

# 安装与首次运行加固（快速检查清单）

1.  **安装**在 Linux 或容器镜像上。
2.  **反向代理 + TLS**（Nginx/Apache、企业级负载均衡器）。
3.  **Manage Jenkins → Configure Global Security**
    *   设置实际的**安全域**（LDAP/OIDC/SAML 等）。
    *   选择一种**授权**模式（见下文）。([Jenkins][3])
4.  **创建一个管理员**用户（非共享账户）。
5.  **限制注册**，禁用匿名写入权限。
6.  **仅使用凭据插件**——切勿在任务中硬编码密钥。([Jenkins][4])

---

# 访问控制（RBAC 与项目作用域）

Jenkins 自带**基于矩阵的安全**机制，用于细粒度权限控制（构建、配置、删除等）。适用于中小型实例或作为基础配置。([Jenkins][3], [Jenkins Plugins][5])

对于大型组织和需要清晰团队隔离的场景，请安装**基于角色的授权策略**（"role-strategy" 插件）：

*   定义**全局角色**（例如 `admin`、`reader`）。
*   定义按项目/文件夹正则表达式限定作用域的**项目角色**（例如 `team-alpha.*`）。
*   将用户/组分配给角色——这样团队只能查看/构建他们拥有的内容。([Jenkins Plugins][6])

> 提示：将每个团队的流水线放入一个**文件夹**中，然后在文件夹级别应用项目角色。如果需要超细粒度的调整，可与**矩阵**授权结合使用。([Jenkins Plugins][5])

---

# 凭据与密钥（安全模式）

*   在 **Manage Jenkins → Credentials** 中添加密钥（全局或文件夹作用域）。
*   在声明式流水线中，在 `environment` 中使用 `credentials()` 引用，或按需使用 `withCredentials { … }` 绑定。
*   优先使用来自密钥库或提供商插件的短期令牌；定期轮换。([Jenkins][4])

**示例（声明式）：**

```groovy
pipeline {
  agent any
  environment {
    // 从 Username/Password 类型的凭据注入 USER 和 PASS 环境变量
    CREDS = credentials('dockerhub-creds-id')
  }
  stages {
    stage('Login') {
      steps {
        sh 'echo $CREDS_USR | docker login -u $CREDS_USR --password-stdin'
      }
    }
  }
}
```

```groovy
pipeline {
  agent any
  stages {
    stage('Use Secret Text') {
      steps {
        withCredentials([string(credentialsId: 'slack-token', variable: 'SLACK_TOKEN')]) {
          sh 'curl -H "Authorization: Bearer $SLACK_TOKEN" https://slack.example/api'
        }
      }
    }
  }
}
```

用法和绑定的文档在此处。([Jenkins][7])

---

# 大规模使用代理节点

*   添加**永久**或**临时**代理节点；按能力打标签；设置启动方式（SSH、JNLP、云）。
*   Jenkins 会监控磁盘、交换空间、临时目录、时钟漂移，并能自动将不健康的节点设为离线。保持标签清晰，并在流水线阶段中使用 `agent { label 'docker' }` 进行路由。([Jenkins][2])

---

# 可靠的流水线（现代 Jenkinsfile）

**声明式 vs 脚本式**：优先选择**声明式**——结构更清晰，有防护机制（`post`、`options`、`when`、`environment`、`input`、`parallel`）。([Jenkins][1])

**最简 CI 示例：**

```groovy
pipeline {
  agent { label 'docker' }
  options { timestamps(); durabilityHint('PERFORMANCE_OPTIMIZED') }
  triggers { pollSCM('@daily') } // 或者在 SCM 中使用 webhooks
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build')    { steps { sh './gradlew build -x test' } }
    stage('Test')     { steps { sh './gradlew test' } }
    stage('Package')  { when { branch 'main' } steps { sh './gradlew assemble' } }
  }
  post {
    always { junit 'build/test-results/test/*.xml'; archiveArtifacts 'build/libs/*.jar' }
    failure { mail to: 'team@example.com', subject: "Build failed ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
  }
}
```

**关键参考：** Pipeline 手册、语法参考和步骤文档。([Jenkins][1])

---

# 多分支、GitHub/GitLab 与 PR

使用**多分支流水线**或 GitHub/Bitbucket 组织任务，这样每个带有 `Jenkinsfile` 的仓库分支/PR 都会自动构建（通过 webhook）。将分支行为保持在代码中，避免点击操作。

---

# 大规模复用：共享库

当你在多个仓库中重复步骤时，创建一个 **Jenkins 共享库**（变量函数、流水线步骤），并在 `Jenkinsfile` 中使用 `@Library('your-lib') _` 导入。这可以防止复制粘贴流水线，并集中修复问题。

---

# 配置即代码 (JCasC)

将控制器的配置视为代码：将其检入 Git，通过 PR 审查，并可重复地引导新的控制器。

*   安装 **Configuration as Code** 插件。
*   编写 YAML 文件，捕获全局安全设置、代理启动器、工具安装器、文件夹、凭据绑定等。
*   在启动时（通过环境变量 `CASC_JENKINS_CONFIG`）或从 UI 加载它。([Jenkins Plugins][8], [Jenkins][9])

**JCasC 浅尝：**

```yaml
jenkins:
  systemMessage: "Jenkins managed by JCasC"
  authorizationStrategy:
    roleBased:
      roles:
        global:
          - name: "viewer"
            permissions:
              - "Overall/Read"
            assignments:
              - "devs"
  securityRealm:
    local:
      allowsSignup: false
      users:
        - id: "admin"
          password: "${ADMIN_PW}"
unclassified:
  location:
    url: "https://ci.example.com/"
```

官方文档和插件页面见上文。([Jenkins][9], [Jenkins Plugins][8])

---

# 插件（明智地使用）

*   **必知插件**：Credentials, Matrix/Role-Strategy, Pipeline, Git, SSH, Email, Artifact Manager (例如 S3/GCS), Cloud agents (Kubernetes), JCasC。
*   保持插件**最少化并及时更新**，固定关键插件版本，并在预演控制器中测试更新。实用的插件文档位于 jenkins.io 和各插件页面。([Jenkins][10])

---

# 可观测性与维护

*   **日志**：使用控制器日志记录器 + 将日志发送到 ELK/CloudWatch。
*   **制品**：仅归档所需内容。
*   **JUnit**：始终发布测试报告；在测试失败时中断构建。
*   **队列健康度**：监控构建队列和代理节点利用率；相应扩展代理节点。
*   **备份**：备份 `$JENKINS_HOME` 或使用 JCasC + 临时控制器。

---

# 快速安全加固

*   在不需要的地方禁用 CLI；优先使用 API 令牌。
*   将**服务**账户与个人账户分开。
*   仅使用文件夹作用域的密钥；绝不回显密钥。
*   锁定脚本批准；限制在声明式流水线中使用 `script` 步骤。
*   定期审计角色。指导参见 Jenkins 安全文档。([Jenkins][3])

---

# 典型的“Day-2”改进

*   **并行**测试分片以缩短构建时间。
*   **缓存**（例如，代理节点上的 Gradle/Maven 缓存）。
*   **Docker-in-Docker** 或 **Kubernetes 代理节点**，用于干净、可重复的构建环境。
*   在早期阶段加入**质量门禁**（代码检查、SAST/DAST）。
*   **晋级**任务或多环境部署阶段，使用 `when` 条件和手动 `input`。

---

# 故障排查速查

*   构建卡住？检查代理节点日志、工作空间磁盘和节点时钟偏差。Jenkins 会自动将超出健康阈值的节点设为离线。([Jenkins][2])
*   找不到凭据？确保作用域正确（文件夹 vs 全局）且 `credentialsId` 正确。([Jenkins][4])
*   认证异常？重新验证安全域 ↔ 授权策略的配对（Matrix/Role-strategy）。([Jenkins][3], [Jenkins Plugins][6])
*   流水线语法错误？使用**声明式**验证器步骤 / 在线编辑器进行验证。([Jenkins][11])

---

# 可复用的“黄金”起点

```groovy
pipeline {
  agent { label 'k8s || docker || linux' }
  options { timestamps(); buildDiscarder(logRotator(numToKeepStr: '50')); ansiColor('xterm') }
  environment { JAVA_TOOL_OPTIONS = '-XX:+UseContainerSupport' }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Setup')    { steps { sh 'python -V || true' } }
    stage('Build')    { steps { sh './gradlew build -x test' } }
    stage('Test')     { steps { junit 'build/test-results/test/*.xml' } }
    stage('Package')  { when { branch 'main' } steps { sh './gradlew assemble' } }
    stage('Deploy')   { when { branch 'main' } steps { input 'Ship to staging?'; sh './scripts/deploy_staging.sh' } }
  }
  post {
    failure { echo "Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
    always  { archiveArtifacts artifacts: 'build/libs/*.jar', fingerprint: true }
  }
}
```

---

# 延伸阅读（高价值文档）

*   **Pipeline：概述与语法**（声明式 vs 脚本式，所有指令和步骤）。([Jenkins][1])
*   **安全与授权**（Matrix），以及用于 RBAC 的 **Role-Strategy 插件**。([Jenkins][3], [Jenkins Plugins][5])
*   **代理与节点**（添加、健康状态、标签）。([Jenkins][2])
*   **凭据使用**（UI 与流水线助手/绑定）。([Jenkins][4])
*   **配置即代码 (JCasC)**（概念 + 插件）。([Jenkins][9], [Jenkins Plugins][8])

---

如果你需要，我可以根据**你的具体设置**（GitHub vs GitLab、本地部署 vs k8s 代理节点，以及你的 RBAC 模型）来定制这份指南，并草拟：

*   一份 **JCasC** YAML 种子配置，
*   一份针对你团队的 **role-strategy** 映射，以及
*   一个用于标准化阶段的 **Shared Library** 骨架。

[1]: https://www.jenkins.io/doc/book/pipeline/?utm_source=chatgpt.com "Pipeline"
[2]: https://www.jenkins.io/doc/book/managing/nodes/?utm_source=chatgpt.com "Managing Nodes"
[3]: https://www.jenkins.io/doc/book/security/managing-security/?utm_source=chatgpt.com "Managing Security"
[4]: https://www.jenkins.io/doc/book/using/using-credentials/?utm_source=chatgpt.com "Using credentials"
[5]: https://plugins.jenkins.io/matrix-auth/?utm_source=chatgpt.com "Matrix Authorization Strategy"
[6]: https://plugins.jenkins.io/role-strategy/?utm_source=chatgpt.com "Role-based Authorization Strategy"
[7]: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/?utm_source=chatgpt.com "Using a Jenkinsfile"
[8]: https://plugins.jenkins.io/configuration-as-code/?utm_source=chatgpt.com "Configuration as Code | Jenkins plugin"
[9]: https://www.jenkins.io/doc/book/managing/casc/?utm_source=chatgpt.com "Configuration as Code"
[10]: https://www.jenkins.io/doc/developer/publishing/documentation/?utm_source=chatgpt.com "Plugin Documentation"
[11]: https://www.jenkins.io/doc/pipeline/steps/pipeline-model-definition/?utm_source=chatgpt.com "Pipeline: Declarative"
